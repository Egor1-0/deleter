from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Изменить текст приветствия'),
        KeyboardButton(text='Изменить текст уведомления')],
        [KeyboardButton(text='Изменить время удаления поста'),
        KeyboardButton(text='Добавить админа')],
    ], resize_keyboard=True
) # главная клавиатура админа