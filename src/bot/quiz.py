from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta
from settings import chat_data, user_data, bot, dp, bot, admins_ID
from questions import  questions, answers

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

async def send_question(user_id):
    # func which send bext qurstions
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

async def send_result_message( user_id, score):
    # func which sends result message after quiz
    user_info = user_data.get(user_id, {})
    username = user_info.get('username', 'Unknown')
    first_name = user_info.get('first_name', 'Unknown')
    last_name = user_info.get('last_name', 'Unknown')

    # def result messages depended on users score
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
async def answer(call: types.CallbackQuery):
    # Handle callback queries for answers to quiz questions
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

