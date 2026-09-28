from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///translator.sqlite")

Base = declarative_base()

class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    reply_to = Column(Integer, nullable=False)

Base.metadata.create_all(engine)


class Base(DeclarativeBase):
    pass


class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)


DB_URL = 'sqlite:///db/database.db'
engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(engine)


def init_database():
    """Создаёт таблицы при запуске бота"""
    Base.metadata.create_all(engine)
    print("✅ База данных инициализирована")


# Инициализируем базу данных при запуске
init_database()




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

