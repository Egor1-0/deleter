from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.database.queries import *

basic_router = Router()


@basic_router.message(CommandStart())
async def start(message: Message):
    await add_user(user_id=message.from_user.id, # добавляет юзера в бд
                   username=message.from_user.username)
    
    settings = await get_settings()

    await message.answer(
            settings.greeting_text # отправляет текст приветствия
        )
