from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta
from settings import dp,bot, start_time, admins_ID
from users_database import UsersDatabase
from jokes import jokes
import os
import random
import asyncio

users_db = UsersDatabase()
@dp.message_handler(commands=['start'])
#handle the '/start' command

async def cmd_start(message: types.Message):
    user_id = message.chat.id
    if not users_db.user_exists(user_id):
        users_db.add_user(user_id)
    #makes commands board for users
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.add('/quiz', '/creators','/ban').add('/HowRomanAreYou', '/top', '/rofl')
    # add board switcher for admins

    if message.from_user.id in admins_ID:
        user_markup.add('/admin')
    for IDs in admins_ID:
        await  bot.forward_message(IDs, message.chat.id, message.message_id)
    await message.answer('Привіт, я бот-вікторина Локатира романа.', reply_markup=user_markup)
    await message.answer_sticker('CAACAgIAAxkBAAEKFiNk4yseSJX8wQLyKT6V6MSR7K6N7AACyTAAAhL-wUt17d_gphvbujAE')
    await bot.send_message(message.chat.id, '<b>Ось список доступних команд</b>:\n'
                                            '/quiz: для початку вікторини\n'
                                            '/top: показує найкращий результат у квізі\n'
                                            '/HowRomanAreYou: показує на скільки відсотків ви Локатир Роман\n'
                                            '/rofl: відправляє рандомний анекдот про Романа\n'
                                            '/ban: ( ͡° ͜ʖ ͡°)\n'
                                            '/creators: посилання на авторів бота\n', parse_mode='HTML')
    if message.chat.type == 'private':
        #send loggs to admins in dm and append logging txt file
        for IDs in admins_ID:
            await bot.send_message(IDs  , f" @{message.chat.username} ID: {message.chat.id}\n"
                                          f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                                          f" Just started bot at {datetime.now() + timedelta(hours=2)}\n\n\n")
            with open('results.txt', 'a') as file:
                file.write(f" @{message.chat.username}, ID: {message.chat.id}\n"
                           f" First name: {message.chat.first_name}, Last name: {message.chat.last_name}\n"
                           f" Just started bot at {datetime.now() + timedelta(hours=2)}\n\n\n")
    else:
        for IDs in admins_ID:
            await bot.send_message(IDs, f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                                        f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                                        f" Participants: {await bot.get_chat_members_count(message.chat.id)}\n"
                                        f" Just started bot at {datetime.now() + timedelta(hours=2)}\n\n\n")




@dp.message_handler(commands=['creators'])
# Handle 'creators' command to send links for creators
async def creators(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    creator_links = [
            types.InlineKeyboardButton("OleksandrYanchar GitHub", url="https://github.com/OleksandrYanchar"),
        types.InlineKeyboardButton("YuriiDorosh GitHub", url="https://github.com/YuriiDorosh"),
        types.InlineKeyboardButton("saintqqe Instagram", url="https://www.instagram.com/saintqqe/"),
        types.InlineKeyboardButton("y_u_r_a111 Instagram", url="https://www.instagram.com/y_u_r_a111/"),
        types.InlineKeyboardButton("saintqqe Twitch", url="https://www.twitch.tv/saintqqe"),
        types.InlineKeyboardButton("fortnite_dota Twitch", url="https://www.twitch.tv/fortnite_dota")
    ]

    markup.add(*creator_links)
    await bot.send_message(message.chat.id, "Посилання на авторів бота:", reply_markup=markup)




@dp.message_handler(commands=['HowRomanAreYou'])
#handle the '/HowROmanAreYou' command
#generate random numb in range 0 - 100
async def how_roman_are_you(message: types.Message):
    procent = random.randint(0,100)
    await message.reply(f'ви на {procent}% Роман Локатир')
    for IDs in admins_ID:
        if message.chat.type =="private":
            # send loggs to admins in dm if used in private chat
            await bot.send_message(IDs, f" @{message.chat.username} ID: {message.chat.id}\n"
                                    f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                                    f" is {procent}% roman {datetime.now() + timedelta(hours=2)}\n\n\n")
        else:
            # send loggs to admins in dm if used in group chat
            await bot.send_message(IDs, f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                                             f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                                             f" Participants: {await bot.get_chat_members_count(message.chat.id)}\n"
                                             f" User: ID:{message.from_user.id} Username: @{message.from_user.username} first name: {message.from_user.first_name} last name: {message.from_user.last_name}\n "
                                             f" is {procent}% roman {datetime.now() + timedelta(hours=2)}\n\n\n")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='stop tracking', callback_data='stop'))
    keyboard.add(types.InlineKeyboardButton(text='restart tracking', callback_data='restart'))
@dp.message_handler(commands=['stats'])
# Handle the '/stats' command
async def stats(message: types.Message):
    #works only for admins to geet loggin file from server
    if message.chat.type == 'private':
        if message.from_user.id in admins_ID:
            await bot.send_message(message.chat.id, f'версія бота від {start_time} ')
            await bot.send_document(message.chat.id, open('results.txt', 'rb'))
    else:
        await bot.send_message(message.chat.id, "Недостатньо прав")
@dp.message_handler(commands=['ban'])
async def ban_reply(message: types.Message):
    with open('../pictures/tate.mp4', 'rb') as tate:
        await message.reply_animation(animation=tate)

@dp.message_handler(commands=['rofl'])
async def joke(message: types.Message):
    joke = random.choice(jokes)
    await bot.send_message(message.chat.id, joke)
