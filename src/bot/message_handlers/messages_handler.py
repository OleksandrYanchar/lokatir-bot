import os
import asyncio
import random
from aiogram import types
from configs.settings import dp, bot, admins_ID, chupa_id, photos_directory
from admins.notes import get_notes_status, append_notes
@dp.message_handler()
async def process_message(message: types.Message):
    global get_notes_status

    append_notes_task = asyncio.create_task(append_notes(message))
    chupa_task = asyncio.create_task(chupa(message))
    forward_task = asyncio.create_task(forward(message))

    if get_notes_status:
        await append_notes_task
    else:
        await asyncio.gather(chupa_task, forward_task)

@dp.message_handler()
async def chupa(message: types.Message):
    from admins.tracks import tracking_enabled
    if str(message.from_user.id) in str(chupa_id) and tracking_enabled:
        photo_files = [file for file in os.listdir(photos_directory) if file.endswith('.jpg')]
        random_photo = random.choice(photo_files)
        with open(os.path.join(photos_directory, random_photo), 'rb') as photo:
            await message.reply_photo(photo)


async def forward(message: types.Message):
    if get_notes_status:
        return

    for IDs in admins_ID:
        await bot.forward_message(IDs, message.chat.id, message.message_id)
