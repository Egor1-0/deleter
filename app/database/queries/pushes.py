import datetime
from sqlalchemy import select

from app.database.models import Scheduler, User, Settings
from app.database.session import async_session

from app.database.queries.requests import get_user 

async def add_user(user_id: int, username: str) -> None:
    async with async_session() as session:
        if not await get_user(user_id=user_id):
            user = User(tg_id=user_id, username=username)
            session.add(user)
            await session.commit()


async def add_scheduler(expire: datetime.datetime, 
                        message_id: int, 
                        username: str | None,  
                        message_text: str | None) -> None:
    async with async_session() as session:
        scheduler = Scheduler(expire=expire, message_id=message_id, 
                              username=username, message_text=message_text)
        session.add(scheduler)
        await session.commit()

async def push_settings() -> None:
    async with async_session() as session:
        settings = await session.scalar(select(Settings))
        if not settings:
            settings = Settings(
                greeting_text = 'Спасибо за запуск бота. Теперь вы будете получать уведомления,' 
                                'когда ваша обьява самоудалится на канале'
                                '\nОбьявы💯% Знакомства❤️МОРЕ' 
                                '\nhttps://t.me/+Tzquzyo_mCw5YmJi!',
                notification_text = 'Ваша обьява была удалена',
            )
            session.add(settings)
            await session.commit()