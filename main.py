from functools import wraps
from aiogram.filters import CommandStart, Command
import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv('TOKEN')
DEV_CHAT_ID = os.getenv('DEV_CHAT_ID')
GROUP_1_ID='-5004537976'
GROUP_2_ID='-5018213536'

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


@dp.message()
async def hello(message: types.Message):
    if message.chat.id == GROUP_1_ID:
        await message.copy_to(GROUP_2_ID)

    elif message.chat.id == GROUP_2_ID:
        await message.copy_to(GROUP_1_ID)


@dp.message(CommandStart())
async def menu_handler(message: types.Message):
    kb = [
        [types.KeyboardButton(text="руски"), types.KeyboardButton(text="арабски")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        "📋 выберите язык",
        reply_markup=keyboard
    )


@dp.message(Command("id"))
async def get_chat_id(message: types.Message):
    await message.answer(f"Ваш ID: {message.chat.id}")


# @dp.message()
# async def hello(message: types.Message):
#     await message.send_copy(message.from_user.id)


async def main():
    logger.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
