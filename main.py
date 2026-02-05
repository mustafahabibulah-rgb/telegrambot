from functools import wraps
from aiogram.filters import CommandStart, Command
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile

from dotenv import load_dotenv
import os

from db import User, async_session_maker, get_or_create, init_models
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


@notify_on_exception
@dp.message(CommandStart())
async def start_command_handler(message: types.Message):
    if message.chat.type != "private":
        await message.answer("Этот бот работает только в приватных чатах.")
        return

    async with async_session_maker() as session:
        await get_or_create(
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


@notify_on_exception
@dp.message(Command("id"))
async def id_command_handler(message: types.Message):
    await message.answer(f"Ваш ID: {message.chat.id}")


async def main():
    logger.info("Initializing models...")
    await init_models()
    logger.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
