from openai import OpenAI
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatMemberStatus
from aiogram.enums.parse_mode import ParseMode
from functools import wraps
from aiogram.filters import CommandStart, Command
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ChatInviteLink, Contact, ContentType, FSInputFile, ResultChatMemberUnion
import tempfile
from pathlib import Path
import subprocess

from dotenv import load_dotenv
import os

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import Group, User, async_session_maker, create_or_update, get_or_create, init_models
from keyboards import LanguageCallback, language_keyboard
import texts

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
load_dotenv()
TOKEN = os.getenv('TOKEN')
DEV_CHAT_ID = os.getenv('DEV_CHAT_ID')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Per (sender_group_id, recipient_group_id) lock: 
# same pair runs one-by-one, different pairs run in parallel.
_translate_locks: dict[tuple[int, ...], asyncio.Lock] = {}
_translate_locks_guard = asyncio.Lock()


def get_name_from_contact(contact: Contact) -> str | None:
    """Extract name from vCard string. Returns None if not found."""
    if hasattr(contact, 'first_name'):
        return f"{contact.first_name} {contact.last_name or ''}"

    if hasattr(contact, 'vcard') and contact.vcard:
        for line in contact.vcard.split('\n'):
            if line.startswith('FN:'):
                return line[3:].strip()

    return None


async def translate_text(
    sender_group: Group,
    recipient_group: Group,
    text: str,
    key: tuple[int, int],
) -> None:
    recipient_language = recipient_group.language
    instructions = f"Translate the text to {recipient_language} language"
    response = client.responses.create(
        model="gpt-5",
        input=text,
        instructions=instructions,
        previous_response_id=sender_group.previous_response_id,
        store=True,
    )

    async with async_session_maker() as session:
        query = select(Group).filter(
            Group.id.in_(key)
        )
        result = await session.execute(query)
        groups = result.scalars().all()
        for group in groups:
            group.previous_response_id = response.id
        await session.commit()

    await bot.send_message(
        chat_id=recipient_group.id, 
        text=response.output_text,
    )


async def translate_voice(
    sender_group: Group,
    recipient_group: Group,
    voice_file_id: str,
    key: tuple[int, int],
) -> None:
    # 1. Download voice file from Telegram to a temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        safe_id = voice_file_id.replace("/", "_")
        input_path = Path(tmpdir) / f"{safe_id}.oga"
        converted_path = Path(tmpdir) / f"{safe_id}.wav"

        # aiogram v3 provides a unified download method
        await bot.download(voice_file_id, input_path)

        # 2. Convert .oga (OGG/Opus) to a format supported by OpenAI (e.g. WAV) using ffmpeg
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",  # overwrite output file if exists
                "-i",
                str(input_path),
                str(converted_path),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0 or not converted_path.exists():
            raise RuntimeError("Failed to convert voice message with ffmpeg")

        # 3. Transcribe original voice (now in WAV)
        with converted_path.open("rb") as f:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=f,
            )

        original_text = getattr(transcription, "text", None)
        if not original_text:
            raise ValueError("Failed to transcribe voice message")

        # 4. Translate text to recipient language using the same conversation thread
        await translate_text(sender_group, recipient_group, original_text, key)


def notify_on_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            # Try to report to dev chat, then re-raise
            try:
                error_text = (
                    f"Handler {func.__name__} failed: {type(exc).__name__}: {exc}\n"
                )
                await bot.send_message(chat_id=int(DEV_CHAT_ID), text=error_text)
            except Exception:  # noqa: BLE001
                pass
            raise

    return wrapper


@dp.message(CommandStart())
@notify_on_exception
async def start_command_handler(message: types.Message):
    if message.chat.type != "private":
        await message.answer(texts.group_msg.get(message.from_user.language_code, "en"))
        return

    async with async_session_maker() as session:
        await create_or_update(
            session,
            User,
            defaults={
                "full_name": message.chat.full_name, 
                "username": message.chat.username, 
                "language_code": message.from_user.language_code
            },
            id=message.chat.id,
        )

    text = texts.send_contact.get(
        message.from_user.language_code, "en"
    )
    animation = FSInputFile("output.gif")

    await message.answer_animation(animation, caption=text)


@dp.message(Command("id"))
@notify_on_exception
async def id_command_handler(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else None
    thread_id = message.message_thread_id

    text = f"📌 Chat ID: {chat_id}\n"

    if user_id:
        text += f"👤 Your ID: {user_id}\n"

    if thread_id is not None:
        text += f"🧵 Thread ID: {thread_id}\n"

    await message.answer(text)


@dp.message(Command("empty"))
@notify_on_exception
async def empty_command_handler(message: types.Message):
    if message.chat.type == "private":
        return

    if message.from_user.id != int(DEV_CHAT_ID):
        return

    bot_member: ResultChatMemberUnion = await bot.get_chat_member(message.chat.id, bot.id)
    if bot_member.status not in ["administrator", "creator"]:
        await message.answer("Please add bot to the group as admin")
        return

    async with async_session_maker() as session:
        group, created = await get_or_create(
            session,
            Group,
            defaults={"recipient_id": None, "sender_id": None},
            id=message.chat.id,
        )
    
    await message.answer(f"Group ID: {group.id}, created: {created}")


@dp.message(Command("language"), F.chat.type.in_({"group", "supergroup"}))
@notify_on_exception
async def language_command_handler(message: types.Message):
    await message.answer(
        text=texts.choose_language.get(message.from_user.language_code, "en"),
        reply_markup=await language_keyboard(),
    )

    await message.delete()


@dp.message(F.new_chat_members)
@notify_on_exception
async def handle_new_chat_members(message: types.Message) -> None:
    async with async_session_maker() as session:
        query = select(User).filter(User.groups_as_recipient.any(Group.id == message.chat.id))
        result = await session.execute(query)
        recipient = result.scalars().one_or_none()

    await bot.set_chat_title(message.chat.id, recipient.full_name)

    async with async_session_maker() as session:
        query = select(Group).filter_by(
            recipient_id=message.from_user.id, sender_id=recipient.id
        )
        result = await session.execute(query)
        recipient_group = result.scalars().first()

    text = texts.user_joined_group.get(message.from_user.language_code, "en")
    group_link: ChatInviteLink = await bot.create_chat_invite_link(chat_id=recipient_group.id, member_limit=1)
    await bot.send_message(
        chat_id=recipient.id, 
        text=text.format(
            user_id=message.from_user.id, 
            user_name=message.from_user.full_name, 
            group_link=group_link.invite_link
        )
    )


@dp.message(F.contact, F.chat.type.in_({"private"}))
@notify_on_exception
async def handle_new_contact(message: types.Message) -> None:
    async with async_session_maker() as session:
        await get_or_create(
            session,
            User,
            defaults={"full_name": get_name_from_contact(message.contact)},
            id=message.contact.user_id,
        )

    async with async_session_maker() as session:
        query = select(Group).filter_by(
            recipient_id=message.contact.user_id, sender_id=message.from_user.id
        )
        result = await session.execute(query)
        group = result.scalars().one_or_none()

    text = texts.group_link.get(message.from_user.language_code, "en")
    if group:
        group_link: ChatInviteLink = await bot.create_chat_invite_link(chat_id=group.id, member_limit=1)
        await message.reply(text.format(invite_link=group_link.invite_link))
        return

    async with async_session_maker() as session:
        query = select(Group).filter_by(
            recipient_id=None, sender_id=None
        )
        result = await session.execute(query)
        group = result.scalars().first()

        if not group:
            await message.answer(texts.no_group_found.get(message.from_user.language_code, "en"))
            raise ValueError(
                f"No group found, please manually add 2 empty groups, "
                f"user link = <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
            )

        group.recipient_id = message.contact.user_id
        group.sender_id = message.from_user.id
        await session.commit()

    group_link: ChatInviteLink = await bot.create_chat_invite_link(chat_id=group.id, member_limit=1)
    await message.reply(text.format(invite_link=group_link.invite_link))

    async with async_session_maker() as session:
        query = select(Group).filter_by(
            recipient_id=None, sender_id=None
        )
        result = await session.execute(query)
        group = result.scalars().first()

        if not group:
            await message.answer(texts.no_group_found.get(message.from_user.language_code, "en"))
            raise ValueError(
                f"No group found, please manually add 1 empty group, "
                f"user link = <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
            )

        group.recipient_id = message.from_user.id
        group.sender_id = message.contact.user_id
        await session.commit()


@dp.callback_query(LanguageCallback.filter())
@notify_on_exception
async def handle_language_callback(callback_query: types.CallbackQuery, callback_data: LanguageCallback):
    async with async_session_maker() as session:
        query = select(Group).filter_by(id=callback_query.message.chat.id)
        result = await session.execute(query)
        group = result.scalars().one_or_none()

        if group.sender_id != callback_query.from_user.id:
            await callback_query.answer(
                text=texts.not_group_sender.get(callback_query.from_user.language_code, "en"),
            )
            return

        group.language = callback_data.language.name
        await session.commit()

    text = texts.language_changed.get(callback_query.from_user.language_code, "en")
    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    await callback_query.answer(
        text=text.format(language=callback_data.language.value),
    )


@dp.message(F.chat.type.in_({"group", "supergroup"}))
@notify_on_exception
async def handle_group_new_message(message: types.Message) -> None:
    bot_member: ResultChatMemberUnion = await bot.get_chat_member(message.chat.id, bot.id)
    if bot_member.status != ChatMemberStatus.ADMINISTRATOR:
        await message.answer("Please add bot to the group as admin")
        return

    async with async_session_maker() as session:
        query = select(Group).options(joinedload(Group.recipient)).filter_by(
            id=message.chat.id
        )
        result = await session.execute(query)
        sender_group = result.scalars().one_or_none()

    if not sender_group:
        await message.answer(texts.not_authorized_group.get(message.from_user.language_code, "en"))
        raise ValueError(
            f"Group not authorized, "
            f"user link = <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
        )

    if not sender_group.language:
        await message.answer(
            text=texts.choose_language.get(message.from_user.language_code, "en"),
            reply_markup=await language_keyboard(),
        )
        return

    async with async_session_maker() as session:
        query = select(Group).filter_by(
            sender_id=sender_group.recipient_id, 
            recipient_id=message.from_user.id,
        )
        result = await session.execute(query)
        recipient_group = result.scalars().one_or_none()

    if not recipient_group.language:
        text=texts.recipient_not_set_language.get(message.from_user.language_code, "en")
        await message.answer(
            text=text.format(user_id=sender_group.recipient.id, full_name=sender_group.recipient.full_name),
        )
        return

    key = tuple(sorted([sender_group.id, recipient_group.id]))

    async with _translate_locks_guard:
        if key not in _translate_locks:
            _translate_locks[key] = asyncio.Lock()
        lock = _translate_locks[key]

    async with lock:
        assert sender_group.previous_response_id == recipient_group.previous_response_id

        if message.content_type == ContentType.TEXT:
            await translate_text(sender_group, recipient_group, message.text, key)

        elif message.content_type == ContentType.VOICE:
            await translate_voice(sender_group, recipient_group, message.voice.file_id, key)

        else:
            await bot.forward_message(
                chat_id=recipient_group.id,
                from_chat_id=message.chat.id,
               message_id=message.message_id,
            )


async def main():
    logger.info("Initializing models...")
    await init_models()
    logger.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
