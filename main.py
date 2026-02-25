from functools import wraps
from aiogram.filters import CommandStart, Command
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ChatInviteLink, FSInputFile

from dotenv import load_dotenv
import os

from sqlalchemy import select

from db import Group, User, async_session_maker, create_or_update, get_or_create, init_models
import texts

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
load_dotenv()
TOKEN = os.getenv('TOKEN')
DEV_CHAT_ID = os.getenv('DEV_CHAT_ID')
bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_name_from_vcard(vcard: str) -> str | None:
    """Extract name from vCard string. Returns None if not found."""
    if not vcard:
        return None
    for line in vcard.split('\n'):
        if line.startswith('FN:'):
            return line[3:].strip()
    return None


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
            defaults={"full_name": message.chat.full_name, "username": message.chat.username},
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
    await message.answer(f"Ваш ID: {message.chat.id}")


@dp.message(F.contact)
@notify_on_exception
async def handle_new_contact(message: types.Message) -> None:
    async with async_session_maker() as session:
        await get_or_create(
            session,
            User,
            defaults={"full_name": get_name_from_vcard(message.contact.vcard)},
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

    group_link: ChatInviteLink = await bot.create_chat_invite_link(chat_id=-1001619680490, member_limit=1)
    await message.reply(text.format(invite_link=group_link.invite_link))


async def main():
    logger.info("Initializing models...")
    await init_models()
    logger.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
