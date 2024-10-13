from datetime import datetime

from sqlalchemy import DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Scheduler(Base):
    """шедулер для удаления постов"""
    __tablename__ = "scheduler"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column()
    expire: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    deleted: Mapped[bool] = mapped_column(default=False)
    username: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    message_text: Mapped[str | None] = mapped_column(default=None)

class User(Base):
    """юзер в боте"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(default=None)
    is_admin: Mapped[bool] = mapped_column(default=False)


class Settings(Base):
    """базовые настройки бота, которые может менять админ"""
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    greeting_text: Mapped[str] = mapped_column()
    notification_text: Mapped[str] = mapped_column()
    time_delta: Mapped[int] = mapped_column(default=1)