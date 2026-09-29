import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram import F
# Импортируем только то, что нужно для работы с БД и сервисами
from database.connection import init_database, Session
from database.models import UserBase  # Теперь импортируем из нашей новой папки database.models, а не из db!
from services.user_service import save_user_to_db, save_contact_to_db, get_all_users



logging.basicConfig(level=logging.INFO)

load_dotenv()

TOKEN = os.getenv("TOKEN")

GROUP_1_ID = -5242993488
GROUP_2_ID = -5146230560

bot = Bot(token=TOKEN)
dp = Dispatcher()



@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    # Сохраняем пользователя в БД
    user_name = message.from_user.first_name or message.from_user.username or "Unknown"
    save_user_to_db(message.from_user.id, user_name)

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
    # Сохраняем язык в БД
    with Session() as session:
        user = session.query(UserBase).filter_by(id=message.from_user.id).first()
        if user:
            user.name = f"{message.text} - {user.name}"
            session.commit()
            print(f"🌐 Язык {message.text} сохранён для пользователя {message.from_user.id}")

    await message.answer(
        "Отправь контакт собеседника через меню Telegram:\n"
        "📎 → Контакт"
    )


@dp.message(F.contact)
async def contact_handler(message: types.Message):
    contact = message.contact

    sender_id = message.from_user.id
    sender_name = message.from_user.first_name or message.from_user.username or "Unknown"

    contact_id = contact.user_id
    contact_phone = contact.phone_number
    contact_first_name = contact.first_name
    contact_last_name = contact.last_name or ""
    contact_full_name = f"{contact_first_name} {contact_last_name}".strip()

    save_user_to_db(sender_id, sender_name)

    if contact_id:
        save_contact_to_db(sender_id, contact_id, contact_full_name, contact_phone)

    text = (
        "✅ Контакт получен и сохранён в базу данных!\n\n"
        f"👤 Отправитель: {sender_name}\n"
        f"📱 Контакт: {contact_full_name}\n"
        f"📞 Телефон: {contact_phone}\n"
        f"🆔 ID контакта: {contact_id or 'Не указан'}"
    )

    await message.reply(text)


@dp.message(F.text == "/id")
async def get_chat_id(message: types.Message):
    await message.answer(f"Ваш ID: {message.chat.id}")



async def main():
    init_database()  # Создаёт таблицы при запуске бота
    await bot.delete_webhook(drop_pending_updates=True)  # сброс вебхука
    await dp.start_polling(bot)





@dp.message(F.text == "/db")
async def show_db_handler(message: types.Message):
    """Показывает содержимое базы данных"""
    users = get_all_users()

    if not users:
        await message.answer("📭 База данных пуста")
        return

    text = "📊 Пользователи в БД:\n\n"
    for user in users:
        text += f"🆔 ID: {user.id}, 👤 Имя: {user.name}"
        if user.phone:
            text += f", 📞 {user.phone}"
        text += "\n"

    await message.answer(text)


@dp.message()
async def forward_messages(message: types.Message):
    if message.chat.id == GROUP_1_ID:
        await message.copy_to(GROUP_2_ID)
    elif message.chat.id == GROUP_2_ID:
        await message.copy_to(GROUP_1_ID)


# ============ ЗАПУСК ============

async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # сброс вебхука
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())