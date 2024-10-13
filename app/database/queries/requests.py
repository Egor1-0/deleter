from typing import Optional
from sqlalchemy import select

from app.database.models import Scheduler, User, Settings
from app.database.session import async_session


async def get_all_admins() -> list[User]:
    async with async_session() as session:
        result = await session.scalars(select(User)
                                       .where(User.is_admin == True))
        return result


async def get_user(user_id: int) -> Optional[User]:
    async with async_session() as session:
        return await session.scalar(select(User)
                                    .where(User.tg_id == user_id))


async def get_user_by_username(username: str) -> Optional[User]:
    async with async_session() as session:
        result = await session.scalar(select(User)
                                      .where(User.username == username.replace('@', '')))
        return result

async def get_scheduler(message_id: int) -> Scheduler:
    async with async_session() as session:
        result = await session.scalar(select(Scheduler)
                                      .where(Scheduler.message_id == message_id))
        return result


async def get_all_schedulers() -> list[Scheduler]:
    async with async_session() as session:
        result = await session.scalars(select(Scheduler)
                                       .where(Scheduler.deleted == False))
        return result
    
async def get_settings() -> Settings:
    async with async_session() as session:
        return await session.scalar(select(Settings))