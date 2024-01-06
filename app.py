from aiogram import executor

import filters
from loader import dp
import handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    filters.setup(dp)
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
