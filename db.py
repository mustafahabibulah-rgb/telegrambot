from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///translator.sqlite")

Base = declarative_base()

class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    reply_to = Column(Integer, nullable=False)

Base.metadata.create_all(engine)
