from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    change_greeting_text = State()
    change_notification_text = State()
    change_delete_time = State()
    add_admin = State()