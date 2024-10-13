import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers.basic import basic_router
from app.handlers.channel import channel_router
from app.handlers.admin_handers.main_admin_handlers import main_admin_router
from app.database.queries import push_settings
from app.services.scheduler import on_start
from config import TOKEN

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    await bot.delete_webhook()

    await push_settings() # добавление настроек в бд, если их нет

    dp.include_router(channel_router)
    dp.include_router(main_admin_router)
    dp.include_router(basic_router)

    await on_start(bot) # просмотрите аннотацию

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
