import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram import F

logging.basicConfig(level=logging.INFO)

load_dotenv()

TOKEN = os.getenv("TOKEN")

GROUP_1_ID = -5242993488
GROUP_2_ID = -5146230560

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.text == "/start")
async def start_handler(message: types.Message):

    if message.chat.type == "private":

        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="руски"),
                    types.KeyboardButton(text="арабски")
                ]
            ],
            resize_keyboard=True
        )

        await message.answer(
            "📋 Выберите язык",
            reply_markup=keyboard
        )

    else:
        await message.answer("бот переводчик")


@dp.message(F.text.in_(["руски", "арабски"]))
async def language_handler(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text="📱 Отправить контакт"
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Отправь контакт собеседника через меню Telegram:\n"
        "📎 → Контакт",
        reply_markup=keyboard
    )


@dp.message(F.contact)
async def contact_handler(message: types.Message):

    contact = message.contact

    text = (
        "✅ Контакт получен\n\n"
        f"Имя: {contact.first_name}\n"
        f"Фамилия: {contact.last_name or '-'}\n"
        f"Телефон: {contact.phone_number}\n"
        f"User ID: {contact.user_id or '-'}"
    )

    await message.answer(text)


@dp.message(F.text == "/id")
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