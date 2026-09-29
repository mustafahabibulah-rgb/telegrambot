# services/user_service.py
from database.connection import Session
from database.models import UserBase

def save_user_to_db(telegram_id: int, name: str):
    """Сохраняет пользователя в базу данных"""
    with Session() as session:
        existing_user = session.query(UserBase).filter_by(id=telegram_id).first()

        if not existing_user:
            new_user = UserBase(id=telegram_id, name=name)
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
        existing_contact = session.query(UserBase).filter_by(id=contact_id).first()

        if not existing_contact and contact_id:
            new_contact = UserBase(id=contact_id, name=contact_name, phone=contact_phone)
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
        return session.query(UserBase).all()
