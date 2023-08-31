import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from settings import bot, dp, chupa_id, admins_ID,photos_directory
from users_database import  UsersDatabase

users_db = UsersDatabase()

tracking_enabled = True
get_notes_status = False
@dp.message_handler(commands=['admin'])
async def admin_menu(message: types.Message):
    if message.from_user.id in admins_ID:
        admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        admin_markup.add('/restartTracking', '/stopTracking', '/tracks').add('/users','/sendAlert','/addUser').add('/addTrackID','removeTrackID','/sendMessage').add('/stats','/back').add('/addNote', '/notes')
        await message.reply("Адмін меню", reply_markup=admin_markup)
@dp.message_handler(commands=['back'])
async def default_menu(message: types.Message):
    if message.from_user.id in admins_ID:
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_markup.add('/quiz', '/creators', '/ban').add('/HowRomanAreYou', '/top', '/rofl')
        if message.from_user.id in admins_ID:
            user_markup.add('/admin')
        await message.reply("Звичайне меню", reply_markup=user_markup)
@dp.message_handler(commands=['users'])
async def get_ids(message: types.Message):
    users = []
    db_entries = users_db.get_all_entries()
    for entry in db_entries:
        users.append(entry[0])
    await bot.send_message(message.chat.id, f"{users} ")


@dp.message_handler(commands=['addUser'])
async def add_user(message: types.Message):
    if message.from_user.id in admins_ID:
        if len(message.text.split()) > 1:
            user_ids = [id.strip() for id in message.text.split()[1:] if id.strip().isdigit()]
            added_users = 0
            for user_id in user_ids:
                if not users_db.user_exists(user_id):
                    users_db.add_user(user_id)
                    added_users += 1
            if added_users > 0:
                await message.reply(f'додано {added_users} користувачів до бд')
            else:
                await message.reply(' всі  користувачі вже існують у бд')
        else:
            await message.reply(' введи айді')


@dp.message_handler(commands=['sendAlert'])
async def send_message(message: types.Message):
    if message.from_user.id in admins_ID:
        if len(message.text.split())> 1:
            alert_text = message.text.replace('/sendAlert', '').strip()
            db_entries = users_db.get_all_entries()
            for entry in db_entries:
                user_id = entry[0]
                try:
                    await bot.send_message(user_id, alert_text)
                except Exception as e:
                    await bot.send_message(message.chat.id, f'{e}:{user_id}')
        else:
            await  message.reply('введи текст')

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


@dp.message_handler(commands=['sendMessage'])
async def send_message(message: types.Message):
    if message.from_user.id in admins_ID:
        if len(message.text.split()) > 1:
            if len(message.text.split()) > 2:
                if not message.text.split()[1].lstrip('-').isdigit():
                    await message.reply('айді повинно бути цифрами')
                else:
                    alert_text = ' '.join(message.text.split()[2:])
                    user_id = int(message.text.split()[1])
                    try:
                        await bot.send_message(user_id, alert_text)
                    except Exception as e:
                        await message.reply(f'Error: {e}')
            else:
                await message.reply('введи текст повідомлення')
        else:
            await message.reply('введи айді і текст')

@dp.message_handler(commands=['addNote'])
async def add_note(message: types.Message):
    global get_notes_status
    if message.from_user.id in admins_ID:
        await message.answer('Enter notes')
        get_notes_status = True

@dp.message_handler(commands=['notes'])
async def get_notes(message: types.message):
    if message.chat.type == 'private':
        if message.from_user.id in admins_ID:
            await bot.send_document(message.chat.id, open('../../notes.txt', 'rb'))
    else:
        await message.answer( "Недостатньо прав")

@dp.message_handler()
async def process_message(message: types.Message):
    global get_notes_status

    append_notes_task = asyncio.create_task(append_notes(message))
    chupa_task =  asyncio.create_task(chupa(message))
    forward_task = asyncio.create_task(forward(message))

    if get_notes_status:
        await append_notes_task
    else:
        await chupa_task
        await forward_task


@dp.message_handler()
async def chupa(message: types.Message):
    if str(message.from_user.id) in str(chupa_id) and tracking_enabled:
        photo_files = [file for file in os.listdir(photos_directory) if file.endswith('.jpg')]
        random_photo = random.choice(photo_files)
        with open(os.path.join(photos_directory, random_photo), 'rb') as photo:
            await message.reply_photo(photo)

async def forward(message: types.Message):
    for IDs in admins_ID:
        await bot.forward_message(IDs, message.chat.id, message.message_id)


@dp.message_handler()
async def append_notes(message: types.Message):
    global get_notes_status
    if message.from_user.id in admins_ID:
        if get_notes_status:
            try:
                with open('../../notes.txt', 'a') as file:
                    file.write(message.text + '\n')
                    await message.answer('Note added')
            except Exception as e:
                await message.answer(e)
            get_notes_status= False
