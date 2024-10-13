from aiogram.types import Message
from aiogram.filters import BaseFilter

from app.database.queries import get_user

class CheckAdminFilter(BaseFilter):
    """проверка на админа. получает юзера из бд и смотрит, является ли юзер админом"""
    async def __call__(self, message: Message) -> bool:
        user = await get_user(user_id=message.from_user.id)
        if user:
            return user.is_admin
        return False