from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta
from settings import dp,bot, start_time, admins_ID
import os
import random
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


