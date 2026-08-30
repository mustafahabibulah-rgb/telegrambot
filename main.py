import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram import F
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from typing import Optional

logging.basicConfig(level=logging.INFO)

load_dotenv()

TOKEN = os.getenv("TOKEN")

GROUP_1_ID = -5242993488
GROUP_2_ID = -5146230560

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ============ МОДЕЛИ БАЗЫ ДАННЫХ ============

class Base(DeclarativeBase):
    pass


class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)


class Human(Base):
    __tablename__ = "humans"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    owner_id: Mapped[int] = mapped_column(ForeignKey("humans.id"))


class BomBom(Base):
    __tablename__ = "bomboms"

    id: Mapped[int] = mapped_column(primary_key=True)
    bom_bom: Mapped[Optional[str]] = mapped_column(String(30))


# ============ ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ ============

DB_URL = 'sqlite:///db/database.db'
engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(engine)


def init_database():
    """Создаёт таблицы при запуске бота"""
    Base.metadata.create_all(engine)
    print("✅ База данных инициализирована")


# Инициализируем базу данных при запуске
init_database()


# ============ ФУНКЦИИ ДЛЯ РАБОТЫ С БАЗОЙ ============

def save_user_to_db(telegram_id: int, name: str):
    """Сохраняет пользователя в базу данных"""
    with Session() as session:
        existing_user = session.query(UserBase).filter_by(id=telegram_id).first()

        if not existing_user:
            new_user = UserBase(
                id=telegram_id,
                name=name
            )
            session.add(new_user)
            session.commit()
            print(f"✅ Пользователь {telegram_id} добавлен в БД")
            return new_user
        else:
            print(f"ℹ️ Пользователь {telegram_id} уже существует в БД")
            return existing_user


def save_contact_to_db(sender_id: int, contact_id: int, contact_name: str, contact_phone: str):
    """Сохраняет контакт в базу данных"""
    with Session() as session:
        # Проверяем, есть ли контакт в БД
        existing_contact = session.query(UserBase).filter_by(id=contact_id).first()

        if not existing_contact and contact_id:
            # Если контакта нет в БД, создаём
            new_contact = UserBase(
                id=contact_id,
                name=contact_name,
                phone=contact_phone
            )
            session.add(new_contact)
            session.commit()
            print(f"✅ Контакт {contact_id} добавлен в БД")
            return new_contact
        else:
            print(f"ℹ️ Контакт {contact_id} уже существует в БД")
            return existing_contact


def get_all_users():
    """Получает всех пользователей из базы"""
    with Session() as session:
        users = session.query(UserBase).all()
        return users


# ============ ХЕНДЛЕРЫ ============

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
    # Получаем данные контакта
    contact = message.contact

    # Информация о том, кто отправил контакт
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name or message.from_user.username or "Unknown"

    # Информация о контакте
    contact_id = contact.user_id
    contact_phone = contact.phone_number
    contact_first_name = contact.first_name
    contact_last_name = contact.last_name or ""
    contact_full_name = f"{contact_first_name} {contact_last_name}".strip()

    # Сохраняем отправителя в БД (если его нет)
    save_user_to_db(sender_id, sender_name)

    # Сохраняем контакт в БД (если есть ID и его нет в БД)
    if contact_id:
        save_contact_to_db(sender_id, contact_id, contact_full_name, contact_phone)

    # Текст для ответа
    text = (
        "✅ Контакт получен и сохранён в базу данных!\n\n"
        f"👤 Отправитель: {sender_name}\n"
        f"📱 Контакт: {contact_full_name}\n"
        f"📞 Телефон: {contact_phone}\n"
        f"🆔 ID контакта: {contact_id or 'Не указан'}"
    )

    # Отвечаем на сообщение с контактом (reply)
    await message.reply(text)


@dp.message(F.text == "/id")
async def get_chat_id(message: types.Message):
    await message.answer(f"Ваш ID: {message.chat.id}")


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