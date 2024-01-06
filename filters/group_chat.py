from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import config


class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return str(message.chat.id) in config.ALLOWED_GROUPS
