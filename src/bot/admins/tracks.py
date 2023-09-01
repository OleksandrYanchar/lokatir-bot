import os
import random
from configs.settings import bot, dp, chupa_id, admins_ID, photos_directory
from aiogram import types

tracking_enabled = True
@dp.message_handler(commands=['restartTracking'])
async def start_tracking(message: types.Message):
    global tracking_enabled
    if message.from_user.id in admins_ID and not tracking_enabled:
        tracking_enabled = True
        for IDs in admins_ID:
            await bot.send_message(IDs, 'tracking started')
@dp.message_handler(commands=['stopTracking'])
async def stop_tracking(message: types.Message):
    global tracking_enabled
    if message.from_user.id in admins_ID and tracking_enabled:
        tracking_enabled = False
        for IDs in admins_ID:
            await bot.send_message(IDs, 'tracking stopped')

@dp.message_handler(commands=['addTrackID'])
async def add_track_id(message: types.Message):
        global chupa_id
        if message.from_user.id in admins_ID:
            if len(message.text.split()) > 1:
                user_ids = [id.strip() for id in message.text.split()[1:] if id.strip().isdigit()]
                added_users = 0
                for user_id in user_ids:
                    if user_id not in chupa_id:
                        chupa_id.append(user_id)
                        added_users += 1
                if added_users > 0:
                    await message.reply(f'Додано {added_users} треків')
                else:
                    await message.reply('Всі користувачі вже трекаються')
            else:
                await message.reply('Введи айді')

@dp.message_handler(commands=['removeTrackID'])
async def remove_track_id(message: types.Message):
    global chupa_id
    if message.from_user.id in admins_ID:
        if len(message.text.split()) > 1:
            user_ids = [id.strip() for id in message.text.split()[1:] if id.strip().isdigit()]
            removed_ids = []
            for user_id in user_ids:
                if user_id in chupa_id:
                    chupa_id.remove(user_id)
                    removed_ids.append(user_id)
            if removed_ids:
                await message.reply(f"Видалено айді: {removed_ids}")
            else:
                await message.reply('Не знайдено айді для видалення')
        else:
            await message.reply('Введи айді')


@dp.message_handler(commands=['addTrackID'])
async def add_track_id(message: types.Message):
    global chupa_id
    if message.from_user.id in admins_ID:
        if len(message.text.split()) > 1:
            user_ids = [id.strip() for id in message.text.split()[1:] if id.strip().isdigit()]
            added_users = 0
            for user_id in user_ids:
                if user_id not in chupa_id:
                    chupa_id.append(user_id)
                    added_users += 1
            if added_users > 0:
                await message.reply(f'Додано {added_users} треків')
            else:
                await message.reply('Всі користувачі вже трекаються')
        else:
            await message.reply('Введи айді')


@dp.message_handler(commands=['tracks'])
async def send_tracks(message: types.Message):
    if message.from_user.id in admins_ID:
        await message.answer(chupa_id)