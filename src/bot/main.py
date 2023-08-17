import os
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from settings import questions,answers

photos_directory = "../lokatir/"

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

user_data = {}  # Store current question and score for each user
chat_data = {}

admins_ID = os.getenv("admins_ID")
admins_ID = [int(id) for id in admins_ID.split(',')]

chupa_id = os.getenv("chupa")
chupa_id = int(chupa_id)

group_id = os.getenv('group_id')

start_time = datetime.now() + timedelta(hours=2)

start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_markup.add('/quiz', '/creators', '/stats').add('/HowRomanAreYou')

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer('Привіт, я бот-вікторина Локатира романа.', reply_markup=start_markup)
    if message.chat.type == 'private':
        for IDs in admins_ID:
            await bot.send_message(IDs  , f" @{message.chat.username} ID: {message.chat.id}\n"
                                             f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                                             f" Just started bot at {datetime.now() + timedelta(hours=2)}\n\n\n")
            with open('results.txt', 'a') as file:
                file.write(f" @{message.chat.username}, ID: {message.chat.id}\n"
                           f" First name: {message.chat.first_name}, Last name: {message.chat.last_name}\n"
                           f" Just started bot at {datetime.now() + timedelta(hours=2)}\n\n\n")
    else:
            await bot.send_message(group_id, f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                                             f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                                             f" Participants: {await bot.get_chat_members_count(message.chat.id)}\n"
                                             f" Just started bot at {datetime.now() + timedelta(hours=2)}\n\n\n")

@dp.message_handler(commands=['HowRomanAreYou'])
async def how_roman_are_you(message: types.Message):
    procent = random.randint(0,100)
    await message.reply(f'ви на {procent}% Роман Локатир')
    for IDs in admins_ID:
        if message.chat.type =="private":
            await bot.send_message(IDs, f" @{message.chat.username} ID: {message.chat.id}\n"
                                    f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                                    f" is {procent}% roman {datetime.now() + timedelta(hours=2)}\n\n\n")
        else:
            await bot.send_message(IDs, f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                                             f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                                             f" Participants: {await bot.get_chat_members_count(message.chat.id)}\n"
                                             f" is {procent}% roman {datetime.now() + timedelta(hours=2)}\n\n\n")

@dp.message_handler(commands=['quiz'])
async def start_quiz(message: types.Message):
    await message.answer('Квіз розпочато.')
    user_data[message.chat.id] = {'question_index': 0, 'score': 0, 'username': message.from_user.username}
    chat_data[message.chat.id] = {'question_index': 0, 'score': 0, 'chat_title': message.chat.title,
                                  'chat_tag': message.chat.username,
                                  'chat_partisipants': await bot.get_chat_members_count(message.chat.id),
                                  'chat_id': message.chat.id}
    await send_question(message.chat.id)
    if message.chat.type == 'private':
        for IDs in admins_ID:
            await bot.send_message(IDs, f" @{message.chat.username} ID: {message.chat.id}\n"
                                             f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                                             f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n")
            with open('results.txt', 'a') as file:
                file.write(f" @{message.chat.username} ID: {message.chat.id}\n"
                           f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                           f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n")
    else:
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
async def stats(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id in admins_ID:
            await bot.send_message(message.chat.id, f'версія бота від {start_time} ')
            await bot.send_document(message.chat.id, open('results.txt', 'rb'))
    elif  message.chat.id == group_id:
        await bot.send_message(message.chat.id, f'версія бота від {start_time} ')
        await bot.send_document(message.chat.id, open('results.txt', 'rb'))
    else:
        await bot.send_message(message.chat.id, "Недостатньо прав")

async def send_question(user_id):
    user_info = user_data.get(user_id, {'question_index': 0, 'score': 0})
    question_index = user_info['question_index']

    if question_index < len(questions):
        question = questions[question_index]
        keyboard = types.InlineKeyboardMarkup()
        for ans in answers[question]:
            keyboard.add(types.InlineKeyboardButton(text=ans, callback_data=ans))

        formatted_question = f'{question_index + 1}/16. <b>{question}</b>'
        await bot.send_message(user_id, formatted_question, reply_markup=keyboard, parse_mode='HTML')
    else:
        await send_result_message(user_id, user_info['score'])


async def send_result_message(user_id, score):
    user_info = user_data.get(user_id, {})
    username = user_info.get('username', 'Unknown')
    first_name = user_info.get('first_name', 'Unknown')
    last_name = user_info.get('last_name', 'Unknown')

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
        await bot.send_message(IDs, f" @{username} ID: {user_id}\n"
                                         f" first name : {first_name} last name: {last_name}\n"
                                         f" finished quiz, with score: {score} at {datetime.now() + timedelta(hours=2)}\n\n\n")
    with open('results.txt', 'a') as file:
        file.write(f" @{username} ID: {user_id}\n"
                   f" first name : {first_name} last name: {last_name}\n"
                   f" finished quiz, with score: {score} at {datetime.now() + timedelta(hours=2)}\n\n\n")

@dp.callback_query_handler(lambda call: True)
async def answer(call: types.CallbackQuery):

    answer = call.data
    user_id = call.message.chat.id
    user_info = user_data.get(user_id, {'question_index': 0, 'score': 0})
    question_index = user_info['question_index']
    question = questions[question_index]

    if answer in answers[question]:
        user_info['score'] += answers[question][answer]
        user_info['question_index'] += 1
        await send_question(user_id)

@dp.message_handler(commands=['creators'])
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

@dp.message_handler()
async def chupa(message: types.Message):
    photo_files = [file for file in os.listdir(photos_directory) if file.endswith('.jpg')]
    if message.from_user.id == chupa_id:
        random_photo = random.choice(photo_files)
        with open(os.path.join(photos_directory, random_photo), 'rb') as photo:
            await message.reply_photo(photo)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)