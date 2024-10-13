from sqlalchemy import update

from app.database.models import Scheduler, Settings, User
from app.database.session import async_session


async def update_scheduler(message_id: int) -> None:
    """помечает, что пост удален"""
    async with async_session() as session:
        await session.execute(update(Scheduler)
                              .where(Scheduler.message_id == message_id)
                              .values(deleted=True))
        await session.commit()


async def update_greeting_text(text: str) -> None:
    async with async_session() as session:
        await session.execute(update(Settings)
                              .where(Settings.id == 1)
                              .values(greeting_text=text))
        await session.commit()


async def update_notification_text(text: str) -> None:
    async with async_session() as session:
        await session.execute(update(Settings)
                              .where(Settings.id == 1)
                              .values(notification_text=text))
        await session.commit()


async def update_delete_time(time: int) -> None:
    async with async_session() as session:
        await session.execute(update(Settings)
                              .where(Settings.id == 1)
                              .values(time_delta=time))
        await session.commit()


async def update_user_to_admin(username: str) -> None:
    async with async_session() as session:
        await session.execute(update(User)
                              .where(User.username == username)
                              .values(is_admin=True))
        await session.commit()