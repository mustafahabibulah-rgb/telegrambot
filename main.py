import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

logging.basicConfig(level=logging.INFO)

load_dotenv()

TOKEN = os.getenv("TOKEN")

GROUP_1_ID = -5242993488
GROUP_2_ID = -5146230560

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(lambda m: m.text and "/start" in m.text.lower())
async def menu_handler(message: types.Message):

    if message.chat.type == "private":

        kb = [
            [types.KeyboardButton(text="руски"),
             types.KeyboardButton(text="арабски")]
        ]

        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )

        await message.answer(
            "📋 выберите язык",
            reply_markup=keyboard
        )

    else:
        await message.answer("бот переводчик")


@dp.message(lambda m: m.text and "/id" in m.text.lower())
async def get_chat_id(message: types.Message):
    await message.answer(f"Ваш ID: {message.chat.id}")


@dp.message()
async def forward_messages(message: types.Message):

    if message.chat.id == GROUP_1_ID:
        await message.copy_to(GROUP_2_ID)

    elif message.chat.id == GROUP_2_ID:
        await message.copy_to(GROUP_1_ID)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

