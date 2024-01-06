import os

from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsGroup
from handlers.groups.meme import process_response
from loader import dp


@dp.message_handler(IsGroup(), commands=['meme'])
async def meme(message: types.Message):
    arguments = message.get_args()
    if len(arguments) == 0:
        await message.reply("You have to put prompt after /meme")
    else:
        file_name = await process_response(arguments)
        if len(file_name) > 0:
            photo = open(file_name, "rb")
            await message.reply_photo(photo)
            os.remove(file_name)
        else:
            await message.reply("Please try again in a minute")
