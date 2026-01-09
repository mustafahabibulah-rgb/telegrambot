import asyncio
from aiogram import Bot, Dispatcher, types

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(lambda m: "start" in m.text.lower() or "/start" in m.text.lower())
async def menu_handler(message: types.Message):
    kb = [
        [types.KeyboardButton(text="руски"), types.KeyboardButton(text="арабски")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        "📋 выберите язык",
        reply_markup=keyboard
    )


@dp.message()
async def hello(message: types.Message):
    await message.send_copy(message.from_user.id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
