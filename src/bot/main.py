import telebot
import os
from dotenv import load_dotenv
from telebot import types
from settings import questions, answers
from telebot import types
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

user_data = {}  # Store current question and score for each user

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    start_button = types.KeyboardButton('/quiz')
    creators_button = types.KeyboardButton('/creators')  # Нова кнопка
    markup.add(start_button, creators_button)  # Додаємо кнопку до розмітки

    bot.send_message(message.chat.id, 'Привіт, я бот-вікторина Локатира романа.', reply_markup=markup)
    with open('results.txt', 'a') as file:
        file.write(f" @{message.from_user.username}  ID : {message.chat.id} just started bot at {datetime.now()}\n")


def check_create_folder_and_file(folder_name, file_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass


check_create_folder_and_file('stats', 'results.txt')

@bot.message_handler(commands=['quiz'])
def start(message):
    bot.send_message(message.chat.id, 'Квіз розпочато.')
    user_data[message.chat.id] = {'question_index': 0, 'score': 0, 'username': message.from_user.username}  # Set the username here
    send_question(message.chat.id)
    with open('results.txt', 'a') as file:
        file.write(f" @{message.from_user.username} , ID : {message.chat.id} just started quiz at {datetime.now()}\n")


def send_question(user_id):
    user_info = user_data.get(user_id, {'question_index': 0, 'score': 0})
    question_index = user_info['question_index']

    if question_index < len(questions):
        question = questions[question_index]
        keyboard = types.InlineKeyboardMarkup()
        for ans in answers[question]:
            keyboard.add(types.InlineKeyboardButton(text=ans, callback_data=ans))

        formatted_question = f'<b>{question}</b>'  # Додайте тег <b> для жирного шрифту
        bot.send_message(user_id, formatted_question, reply_markup=keyboard, parse_mode='HTML')
    else:
        send_result_message(user_id, user_info['score'])


def send_result_message(user_id, score):
    user_info = user_data.get(user_id, {'username': 'Unknown', 'score': 0})
    username = user_info['username']
    if -1000 < score <= 0:
        result_message = 'Ви взагалі не знаєте Романа, ідіть підівчіться та не позортесь'
        bot.send_photo(user_id, photo=open('../pictures/pidyob.png' ,'rb'))
    elif 0 < score <= 10:
        result_message = 'Дуже слабенько, ви напевно лише вчора дізналися хто такий Роман'
        bot.send_photo(user_id, photo=open('../pictures/ok.png', 'rb'))
    elif 10 < score <= 30:
        result_message = 'Ви знаєте Романа не перший день, але все одно цього недостатньо'
        bot.send_photo(user_id, photo=open('../pictures/patriot.png', 'rb'))
    elif 30 < score <= 70:
        result_message = 'Непогано, ще трішки і ви зможете сказати, що ви фанат Романа'
        bot.send_photo(user_id, photo=open('../pictures/dovolniy.png', 'rb'))
    elif 70 < score <= 130:
        result_message = 'Ви справжній фанат Романа'
        bot.send_photo(user_id, photo=open('../pictures/cool_1.png', 'rb'))
    elif 130 < score <= 140:
        result_message = 'Ви Локатир Романа, або його кращий друг'
        bot.send_photo(user_id, photo=open('../pictures/bratva.png', 'rb'))
    else:
        result_message = 'Сама ти нікому не потрібна, шмара'
        bot.send_photo(user_id, photo=open('../pictures/minus.jpg', 'rb'))

    bot.send_message(user_id, f'Ваш рахунок: {score}')
    result_text = f"{result_message}\n https://t.me/lokatir_bot"
    bot.send_message(user_id, result_text)
    with open('results.txt', 'a') as file:
        file.write(f" @{username} {user_id} finished quiz, with score: {score} at {datetime.now()}\n")


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    answer = call.data
    user_id = call.message.chat.id
    user_info = user_data.get(user_id, {'question_index': 0, 'score': 0})
    question_index = user_info['question_index']
    question = questions[question_index]

    if answer in answers[question]:
        user_info['score'] += answers[question][answer]
        user_info['question_index'] += 1
        send_question(user_id)

@bot.message_handler(commands=['creators'])
def creators(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    creator_links = [
        types.InlineKeyboardButton("OleksandrYanchar GitHub", url="https://github.com/OleksandrYanchar"),
        types.InlineKeyboardButton("YuriiDorosh GitHub", url="https://github.com/YuriiDorosh"),
        types.InlineKeyboardButton("saintqqe Instagram", url="https://www.instagram.com/saintqqe/"),
        types.InlineKeyboardButton("y_u_r_a111 Instagram", url="https://www.instagram.com/y_u_r_a111/"),
        types.InlineKeyboardButton("saintqqe Twitch", url="https://www.twitch.tv/saintqqe"),
        types.InlineKeyboardButton("fortnite_dota Twitch", url="https://www.twitch.tv/fortnite_dota")
    ]

    markup.add(*creator_links)  # Додаємо кнопки у розмітку

    bot.send_message(message.chat.id, "Посилання на авторів бота:", reply_markup=markup)

bot.polling()
