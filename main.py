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

    await message.answer(
        "Отправь контакт собеседника через меню Telegram:\n"
        "📎 → Контакт"
    )




from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
	pass






from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
	pass

class UserBase(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(30))


from sqlalchemy import ForeignKey

# предыдущие импорты
...


class Human(Base):
    __tablename__ = "humans"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[id] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    owner_id: Mapped[int] = mapped_column(ForeignKey("Human.id"))


joe = Human(name="Joe")
vaz_1111 = Car(name="Ока", owner_id=1)

from typing import Optional

...


class BomBom(Base):
    __tablename__ = "bomboms"

    id: Mapped[int] = mapped_column(primary_key=True)
    bom_bom: Mapped[Optional[str]] = mapped_column(String())


bom_one = BomBom()
bom_two = BomBom(bom_bom="Бом-Бом")





from sqlalchemy import create_engine
engine = create_engine("sqlite:///(путь к БД)", echo=True)





from sqlalchemy import create_engine
from models import Base

DB_URL = 'sqlite:///db/database.db'
engine = create_engine(DB_URL, echo=True)

def create_db_and_tables() -> None:
	Base.metadata.create_all(engine)





from sqlalchemy.orm import sessionmaker
from database import engine

Session = sessionmaker(engine)

with Session() as session:
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm import Mapped
    from sqlalchemy.orm import mapped_column
    from sqlalchemy import String

    from database import engine

    Session = sessionmaker(engine)


    # перенесём сюда модель для наглядности
    class UserBase(Base):
        __tablename__ = "users"

        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(30))
        email: Mapped[str] = mapped_column(String(100))


    joe = UserBase(name="Joe", email="joe@example.com")


    def create_user(user: UserBase, session) -> None:
        session.add(user)


    with Session() as session:
        try:
            create_user(joe, session)
        except:
            session.rollback()
            raise
        else:
            session.commit()




from sqlalchemy import select

# какой-то код, например тот, который писали выше

def get_by_name(name: str, session) -> list[UserBase]:
	statement = select(UserBase).where(UserBase.name == name)
	db_object = session.scalars(statement).one()
	return db_object


with Session() as session:
    print(get_by_name("Joe", session))




class UserBase(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(30))
	email: Mapped[str] = mapped_column(String(100))

	def __repr__(self) -> str:
		return f"UserBase(id={self.id}, name={self.name}, email={self.email})"




[UserBase(id=1, name=SQLAlchemyJoe, email=joe@examle.com)]




def update(new_object: UserBase, session) -> None:
	session.merge(new_object)

with Session() as session:
    try:
        joe = get_by_name("Joe", session)
        joe.name = "Bob"
        update(joe, session)
    except:
        session.rollback()
        raise
    else:
        session.commit()




def delete(name: str, session) -> UserBase:
	statement = select(UserBase).where(UserBase.name == name)
	db_object = session.scalars(statement).one()

	session.delete(db_object)
	return db_object

with Session() as session:
    try:
        delete("Joe", session)
    except:
        session.rollback()
        raise
    else:
        session.commit()




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
