import os
import random
import re
from dotenv import load_dotenv
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from settings import questions,answers

#et the phot dir for chupa function
photos_directory = "../lokatir/"

#load enviroment from environment .env file
load_dotenv()

#get bot TOKEN from .env file
TOKEN = os.getenv("TOKEN")

#initialize the bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# Dictionary to store user-specific data during the quiz
user_data = {}

#dictionary to store chat-specific data
chat_data = {}

#IDs of bot administrators from environment .env file
admins_ID = os.getenv("admins_ID")
admins_ID = [int(id) for id in admins_ID.split(',')]

#ID for tracking specific user's messages
#used in restartTracking, stopTracking and changeTrackID funcs
chupa_id = os.getenv("chupa")
chupa_id = int(chupa_id)
chupa_ID = chupa_id

#varieble used to control bot version at launch
start_time = datetime.now() + timedelta(hours=2)

#define the start keyboard for users
start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_markup.add('/quiz', '/creators', '/stats').add('/HowRomanAreYou')


@dp.message_handler(commands=['start'])
#handle the '/start' command

async def cmd_start(message: types.Message):
    #makes commands board for users
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.add('/quiz', '/creators', '/stats').add('/HowRomanAreYou')
    # makes commands board for admins
    if message.from_user.id in admins_ID:
        user_markup.add('/restartTracking', '/stopTracking', '/changeTrackID')

    await message.answer('Привіт, я бот-вікторина Локатира романа.', reply_markup=user_markup)
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
    keyboard.add(types.InlineKeyboardButton(text='stop tracking', callback_data=stop))
    keyboard.add(types.InlineKeyboardButton(text='restart tracking', callback_data=restart))
@dp.message_handler(commands=['quiz'])
async def start_quiz(message: types.Message):
    #handle the '/quiz' command to start the quiz
    await message.answer('Квіз розпочато.')
    #collect user date depended on chat type
    user_data[message.chat.id] = {'question_index': 0, 'score': 0, 'username': message.from_user.username}
    chat_data[message.chat.id] = {'question_index': 0, 'score': 0, 'chat_title': message.chat.title,
                                  'chat_tag': message.chat.username,
                                  'chat_partisipants': await bot.get_chat_members_count(message.chat.id),
                                  'chat_id': message.chat.id}
    await send_question(message.chat.id)
    if message.chat.type == 'private':
        for IDs in admins_ID:
            # send loggs to admins in dm if used in private chat  and append loggs file
            await bot.send_message(IDs, f" @{message.chat.username} ID: {message.chat.id}\n"
                                             f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                                             f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n")
            with open('results.txt', 'a') as file:
                file.write(f" @{message.chat.username} ID: {message.chat.id}\n"
                           f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                           f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n")
    else:
        # send loggs to admins in dm if used in group chat and append loggs file
        for IDs in admins_ID:
            await bot.send_message(IDs, f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                                             f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                                             f" Participants: {await bot.get_chat_members_count(message.chat.id)}"
                                             f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n")
            with open('results.txt', 'a') as file:
                file.write(f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                           f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                           f" Participants: {await bot.get_chat_members_count(message.chat.id)}\n"
                           f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n")

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

async def send_question(user_id):
    #func which send bext qurstions
    user_info = user_data.get(user_id, {'question_index': 0, 'score': 0})
    question_index = user_info['question_index']

    if question_index < len(questions):
        question = questions[question_index]
        keyboard = types.InlineKeyboardMarkup()
        for ans in answers[question]:
            keyboard.add(types.InlineKeyboardButton(text=ans, callback_data=ans))

        formatted_question = f'{question_index + 1}/{len(questions)}. <b>{question}</b>'
        await bot.send_message(user_id, formatted_question, reply_markup=keyboard, parse_mode='HTML')
    else:
        await send_result_message(user_id, user_info['score'])


async def send_result_message(top_score, user_id, score):
    #func which sends result message after quiz
    user_info = user_data.get(user_id, {})
    username = user_info.get('username', 'Unknown')
    first_name = user_info.get('first_name', 'Unknown')
    last_name = user_info.get('last_name', 'Unknown')

    #def result messages depended on users score
    if -1000 < score <= 0:
        result_message = 'Ви взагалі не знаєте Романа, ідіть підівчіться та не позортесь'
        await bot.send_photo(user_id, photo=open('../pictures/pidyob.png', 'rb'))
    elif 0 < score <= 10:
        result_message = 'Дуже слабенько, ви напевно лише вчора дізналися хто такий Роман'
        await bot.send_photo(user_id, photo=open('../pictures/ok.png', 'rb'))
    elif 10 < score <= 35:
        result_message = 'Ви знаєте Романа не перший день, але все одно цього недостатньо'
        await bot.send_photo(user_id, photo=open('../pictures/patriot.png', 'rb'))
    elif 30 < score <= 72:
        result_message = 'Непогано, ще трішки і ви зможете сказати, що ви фанат Романа'
        await bot.send_photo(user_id, photo=open('../pictures/dovolniy.png', 'rb'))
    elif 70 < score <= 130:
        result_message = 'Ви справжній фанат Романа'
        await bot.send_photo(user_id, photo=open('../pictures/cool_1.png', 'rb'))
    elif 130 < score:
        result_message = 'Ви Локатир Романа, або його кращий друг'
        await bot.send_photo(user_id, photo=open('../pictures/bratva.png', 'rb'))
    else:
        result_message = 'Сама ти нахуй нікому не потрібна, шмара'
        await bot.send_photo(user_id, photo=open('../pictures/minus.jpg', 'rb'))
    result_text = f"{result_message}\n https://t.me/lokatir_bot"

    await bot.send_message(user_id, f'Ваш рахунок: {score}')
    await bot.send_message(user_id, result_text)
    for IDs in admins_ID:
        # send loggs to admins in dm if used in private chat
        await bot.send_message(IDs, f" @{username} ID: {user_id}\n"
                                         f" first name : {first_name} last name: {last_name}\n"
                                         f" finished quiz, with score: {score} at {datetime.now() + timedelta(hours=2)}\n\n\n")
    with open('results.txt', 'a') as file:
        file.write(f" @{username} ID: {user_id}\n"
                   f" first name : {first_name} last name: {last_name}\n"
                   f" finished quiz, with score: {score} at {datetime.now() + timedelta(hours=2)}\n\n\n")


@dp.callback_query_handler(lambda call: True)
    # Handle callback queries for answers to quiz questions
async def answer(call: types.CallbackQuery):
    # Get the selected answer from the callback data
    answer = call.data
    user_id = call.message.chat.id
    # Get user-specific information or initialize with default values
    user_info = user_data.get(user_id, {'question_index': 0, 'score': 0})
    question_index = user_info['question_index']
    # Get the question text for the current question index
    question = questions[question_index]
    # Check if the selected answer is among the valid answers for the question
    if answer in answers[question]:
        # Increment the user's score based on the selected answer's value
        user_info['score'] += answers[question][answer]
        # Move to the next question by incrementing the question index
        user_info['question_index'] += 1
        # Send the next question to the user
        await send_question(user_id)


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


@dp.message_handler(commands=['restartTracking'])
# Handle 'restartTracking' command to restart tracking
async def switch(message: types.Message):
    global chupa_id
    if message.from_user.id in admins_ID:
        chupa_id = chupa_ID
        await bot.send_message(message.chat.id, 'tracking started')

@dp.message_handler(commands=['stopTracking'])
# Handle 'stopTracking' command to stop Tracking

async def switch(message: types.Message):
    global chupa_id
    if message.from_user.id in admins_ID:
        chupa_id +=1
        await bot.send_message(message.chat.id,   'tracking stopped')


@dp.message_handler(commands=['changeTrackID'])
# Handle 'changeTrackID' command to change tracked users ID defined in chupa_id

async def cmd_change_track_id(message: types.Message):
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


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)