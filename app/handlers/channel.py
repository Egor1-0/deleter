from aiogram import Router
from aiogram.types import Message

from app.database.queries import get_settings, add_scheduler
from app.services.scheduler import start_scheduler

channel_router = Router()

@channel_router.channel_post()
async def create_timer(message: Message):
    settings = await get_settings()

    await start_scheduler(delta=settings.time_delta, # запуск шедулера 
                          message=message)