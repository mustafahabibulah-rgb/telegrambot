from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base  # Добавили импорт Base

engine = create_engine("sqlite:///db/database.db")

Session = sessionmaker(bind=engine)

def init_database():
    # Эта строка автоматически создаст нужные таблицы в файле database.db
    Base.metadata.create_all(bind=engine)










