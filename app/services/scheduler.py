from datetime import datetime, timedelta, timezone

import pytz
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database.queries import (get_user_by_username, get_all_admins, update_scheduler, 
                                  get_all_schedulers, add_scheduler, get_settings)
from config import GROUP_ID

async def delete_post(message_text: Message, username: str, bot: Bot, message_id: int):
    """функция удаления поста. срабатывает отложенно. шедулер создается в start_scheduler-функции. 
    если пользователь зареган, ему отправляется уведомление. если пользователь не зареган, уведомление не отправляется, 
    а бот удаляет пост и уведомляет о нем всем админам."""
    try:
        await bot.delete_message(chat_id=GROUP_ID, message_id=message_id)
    except TelegramBadRequest:
        return

    await update_scheduler(message_id=message_id) # помечает, что удаление завершено в бд (нужно для on_start)

    settings = await get_settings()

    if message_text:
        if username != 'Неизвестный пользователь': # в функцию передается такое имя, если в тексте не указан юзернейм
            user = await get_user_by_username(username) # проверяет наличие юзера в бд, чтобы по айди отправить уведомление
            if user:
                await bot.send_message(chat_id=user.tg_id,
                                        text=settings.notification_text) # текст уведомления из настроек
                
                for admin in (await get_all_admins()): # отправляет уведомление всем админам
                    await bot.send_message(chat_id=admin.tg_id, text=f"Пост {username} удален. Отправлено автору")

        else:
            for admin in (await get_all_admins()): # отправляет уведомление всем админам
                await bot.send_message(chat_id=admin.tg_id,
                                    text=f"Пост {username} удален. Уведомление НЕ отправлено. Автор не зарегистрирован.")


async def on_start(bot: Bot):
    """функция, добавляющая в шедулер неудаленные посты. срабатывает при запуске бота. 
    нужна на случай непредвиденных остановок сервера или сбоев в его работе"""
    schedulers = await get_all_schedulers()
    for scheduler in schedulers:
        scheduler_expire_utc = scheduler.expire.astimezone(pytz.timezone('Europe/Moscow'))
        if datetime.now(pytz.timezone('Europe/Moscow')) > scheduler_expire_utc: # если пост должен был быть удален раньше настоящего момента, бот его удаляет
            
            try:
                await bot.delete_message(
                    message_id=scheduler.message_id,
                    chat_id=GROUP_ID)
                
                for admin in (await get_all_admins()): # отправляет уведомление всем админам
                    await bot.send_message(
                        chat_id=admin.tg_id,
                        text=f"Пост {scheduler.username} удален. Бот был в отключке.",
                    )

                await update_scheduler(message_id=scheduler.message_id) # помечает, что удаление завершено в бд (нужно для on_start)
            except TelegramBadRequest:
                continue
            continue

        shed = AsyncIOScheduler()
        shed.add_job(delete_post, "date", # добавляет в шедулер неудаленные посты, которые не должны быть удалены. срабатывает при запуске бота
                     run_date=scheduler_expire_utc,
                     kwargs={
                                'bot': bot, 
                                'message_text': scheduler.message_text,
                                'username': scheduler.username,
                                'message_id': scheduler.message_id,
                              })
        shed.start()


async def start_scheduler(delta: int, message: Message):
    """функция создания шедулера. срабатывает при создании поста. добавляет в шедулер пост, 
    который должен быть удален, а также в бд. это нужно для on_start"""
    scheduler = AsyncIOScheduler()
    moscow_tz = pytz.timezone('Europe/Moscow')
    expire_time = datetime.now(moscow_tz) + timedelta(minutes=delta) # время удаления поста
    username = ''  

    if (message.caption and message.video) or (message.caption and message.photo): 
        username = ''
        for word in message.caption.split(): # проверяет есть ли в посте юзернейм. если есть, то сохраняет его
            if "@" in word:
                username = word
                break

        for admin in (await get_all_admins()): # отправляет уведомление всем админам
            await message.bot.send_message(
                text=f'Пост пользователя {username} будет удален {expire_time.strftime("%d/%m/%Y, %H:%M:%S")}.',
                chat_id=admin.tg_id
            )

    elif message.text:
        text_content = message.text
        username = ''
        for word in text_content.split(): # проверяет есть ли в посте юзернейм. если есть, то сохраняет его
            if "@" in word:
                username = word
                break

        for admin in (await get_all_admins()): # отправляет уведомление всем админам
            await message.bot.send_message(
                text=f'Пост пользователя {username} будет удален {expire_time.strftime("%d/%m/%Y, %H:%M:%S")}.',
                chat_id=admin.tg_id
            )
    else:
        pass # нужно, чтобы если в посте несколько медиа, отпрвилось только одно сообщение 

    if not username: # если в посте нет юзернейма, записывает в таком виде. нужно для отправления уведомления
        username = "Неизвестный пользователь"

    now_utc = datetime.now(pytz.timezone('Europe/Moscow'))
    expire_time_utc = now_utc + timedelta(minutes=delta)

    message_text = message.text or message.caption # получает текст поста

    await add_scheduler(expire=expire_time_utc, # сохраняет в бд пост. нужно для on_start
                        message_id=message.message_id,
                        username=username,
                        message_text=message_text)

    

    scheduler.add_job(delete_post, "date", # создает шедулер для удаления поста
                      run_date=expire_time,
                      kwargs={
                                'bot': message.bot, 
                                'message_text': message_text,
                                'username': username,
                                'message_id': message.message_id,
                              })
    scheduler.start() # запускает отложенное удаление поста