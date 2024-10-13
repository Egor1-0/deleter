from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.queries import (update_greeting_text, update_notification_text, 
                                  update_delete_time, update_user_to_admin, get_user_by_username)
from app.filters.check_admin import CheckAdminFilter
from app.keyboards.admin_kb import main_admin_kb
from app.handlers.admin_handers.states import AdminStates

main_admin_router = Router()

main_admin_router.message.filter(CheckAdminFilter()) # проверка на админа для всего роутера

@main_admin_router.message(F.text.lower() == "отмена")
@main_admin_router.message(CommandStart())
async def admin_start(message: Message, state: FSMContext):
    await message.answer("Панель админа. Выберите функции:", reply_markup=main_admin_kb)
    await state.clear()


@main_admin_router.message(F.text == "Изменить текст приветствия")
async def change_greeting_text(message: Message, state: FSMContext):
    await message.answer('Отправьте текст приветствия для бота. Отправьте "отмена" для отмены')
    await state.set_state(AdminStates.change_greeting_text)


@main_admin_router.message(AdminStates.change_greeting_text)
async def change_greeting_text(message: Message, state: FSMContext):
    await update_greeting_text(message.text)
    await message.answer("Текст приветствия изменен")
    await state.clear()


@main_admin_router.message(F.text == "Изменить текст уведомления")
async def change_notification_text(message: Message, state: FSMContext):
    await message.answer('Отправьте текст уведомления для бота. Отправьте "отмена" для отмены')
    await state.set_state(AdminStates.change_notification_text)


@main_admin_router.message(AdminStates.change_notification_text)
async def change_greeting_text(message: Message, state: FSMContext):
    await update_notification_text(message.text)
    await message.answer("Текст приветствия изменен")
    await state.clear()


@main_admin_router.message(F.text == "Изменить время удаления")
async def change_delete_time(message: Message, state: FSMContext):
    await message.answer('Отправьте время в часах. Отправьте "отмена" для отмены')
    await state.set_state(AdminStates.change_delete_time)


@main_admin_router.message(AdminStates.change_delete_time)
async def change_greeting_text(message: Message, state: FSMContext):
    if message.text.isdigit():
        await update_delete_time(int(message.text))
        await message.answer("Время удаления изменено")
        await state.clear()
    else:
        await message.answer("Время должно быть целым числом, ведите еще раз")


@main_admin_router.message(F.text == "Добавить админа")
async def add_admin(message: Message, state: FSMContext):
    await message.answer('Отправьте username пользователя. Отправьте "отмена" для отмены')
    await state.set_state(AdminStates.add_admin)


@main_admin_router.message(AdminStates.add_admin)
async def add_admin(message: Message, state: FSMContext):
    username = message.text.replace('@', '')
    if await get_user_by_username(username=username):
        await update_user_to_admin(username)
        await message.answer("Админ добавлен")
        await state.clear()
    else:
        await message.answer("Пользователь не найден. Проверьте правильность ввода, либо зарегистрируйте пользователя (чтобы он /start в боте написал)")