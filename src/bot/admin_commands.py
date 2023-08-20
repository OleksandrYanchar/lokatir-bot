import os
import random
from aiogram import Bot, Dispatcher, types
from settings import bot, dp, chupa_id, chupa_ID, admins_ID,photos_directory
@dp.message_handler(commands=['restartTracking'])
# Handle 'restartTracking' command to restart tracking
async def start_tracking(message: types.Message):
    global chupa_id
    if message.from_user.id in admins_ID:
        chupa_id = chupa_ID
        await bot.send_message(message.chat.id, 'tracking started')

@dp.message_handler(commands=['stopTracking'])
# Handle 'stopTracking' command to stop Tracking

async def stop_tracking(message: types.Message):
    global chupa_id
    if message.from_user.id in admins_ID:
        chupa_id +=1
        await bot.send_message(message.chat.id,   'tracking stopped')


@dp.message_handler(commands=['changeTrackID'])
# Handle 'changeTrackID' command to change tracked users ID defined in chupa_id

async def change_track_id(message: types.Message):
    global chupa_id
    command_parts = message.text.split()
    if message.from_user.id in admins_ID:
        if len(command_parts) > 1:
            new_chupa_id = int(command_parts[-1])
            chupa_id = new_chupa_id
            await message.reply(f"Ви змінили ID для відстеження повідомлень на {chupa_id}")
            for IDs in admins_ID:
                bot.send_message(IDs, f'тепер трекає {chupa_id}')
        else:
            await message.reply("Введіть команду у форматі /changeTrackID ID")


@dp.message_handler()
#monitor spesific users messages and reply to them by sending random picture, ID is defined in chupa_id
async def chupa(message: types.Message):
    photo_files = [file for file in os.listdir(photos_directory) if file.endswith('.jpg')]
    if message.from_user.id == chupa_id:
        random_photo = random.choice(photo_files)
        with open(os.path.join(photos_directory, random_photo), 'rb') as photo:
            await message.reply_photo(photo)
