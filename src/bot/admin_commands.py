import os
import random
from aiogram import Bot, Dispatcher, types
from settings import bot, dp, chupa_id, chupa_ID, admins_ID,photos_directory
from users_database import  UsersDatabase

users_db = UsersDatabase()

@dp.message_handler(commands=['admin'])
async def admin_menu(message: types.Message):
    if message.from_user.id in admins_ID:
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_markup.add('/restartTracking', '/stopTracking', '/changeTrackID').add('/users','/sendAlert','/stats').add('/addUser','/back')
        await message.reply("Адмін меню", reply_markup=user_markup)
@dp.message_handler(commands=['back'])
async def default_menu(message: types.Message):
    if message.from_user.id in admins_ID:
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_markup.add('/quiz', '/creators').add('/HowRomanAreYou', '/top')
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
# Handle 'restartTracking' command to restart tracking
async def start_tracking(message: types.Message):
    global chupa_id
    if message.from_user.id in admins_ID:
        chupa_id = chupa_ID
        for IDs in admins_ID:
            await bot.send_message(IDs, 'tracking started')

@dp.message_handler(commands=['stopTracking'])
# Handle 'stopTracking' command to stop Tracking

async def stop_tracking(message: types.Message):
    global chupa_id
    if message.from_user.id in admins_ID:
        chupa_id +=1
        for IDs in admins_ID:
            await bot.send_message(IDs,   'tracking stopped')


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
                await bot.send_message(IDs, f'тепер ,бот трекає {chupa_id}')
        else:
            await message.reply("Введіть команду у форматі /changeTrackID ID")
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



@dp.message_handler()
#monitor spesific users messages and reply to them by sending random picture, ID is defined in chupa_id
async def chupa(message: types.Message):
    photo_files = [file for file in os.listdir(photos_directory) if file.endswith('.jpg')]
    if message.from_user.id == chupa_id:
        random_photo = random.choice(photo_files)
        with open(os.path.join(photos_directory, random_photo), 'rb') as photo:
            await message.reply_photo(photo)
