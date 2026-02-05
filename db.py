from sqlalchemy.exc import NoResultFound
from typing import Any, List, Optional, Type
from sqlalchemy import BigInteger, ForeignKey, String, insert, select
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

Base = declarative_base()
engine = create_async_engine("sqlite+aiosqlite:///translator.sqlite")
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(length=256))
    username: Mapped[Optional[str]] = mapped_column(String(length=128))
    groups_as_sender: Mapped[List["Group"]] = relationship(
        back_populates="sender",
        foreign_keys="Group.sender_id",
    )
    groups_as_recipient: Mapped[List["Group"]] = relationship(
        back_populates="recipient",
        foreign_keys="Group.recipient_id",
    )


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    sender: Mapped["User"] = relationship(
        back_populates="groups_as_sender",
        foreign_keys=[sender_id],
    )
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    recipient: Mapped["User"] = relationship(
        back_populates="groups_as_recipient",
        foreign_keys=[recipient_id],
    )
    language_code: Mapped[str] = mapped_column(String(length=5))


async def get_or_create(session: AsyncSession, model: Type[Base], defaults: Optional[dict] = None, **kwargs: Any) -> tuple[Any, bool]:
    if defaults is None:
        defaults = {}

    try:
        query = select(model).filter_by(**kwargs)
        result = await session.execute(query)
        instance = result.scalars().one()
        return instance, False

    except NoResultFound:
        params = {**kwargs, **defaults}
        query = insert(model).values(**params).returning(model)
        result = await session.execute(query)
        await session.commit()
        instance = result.scalars().one()
        return instance, True


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
