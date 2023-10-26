import random
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta
from configs.settings import chat_data, user_data, bot, dp, bot, admins_ID, questions, results_file, quiz_picks
from configs.questions import original_questions
from data_storge.quiz_database import QuizDatabase
from data_storge.users_database import UsersDatabase

users_db = UsersDatabase()
quiz_db = QuizDatabase()


@dp.message_handler(commands=["quiz"])
async def start_quiz(message: types.Message) ->None:
    global questions
    keys = list(original_questions.keys())
    random.shuffle(keys)  # Shuffle the keys
    questions = {key: original_questions[key] for key in keys}
    if not users_db.user_exists(message.chat.id):
        users_db.add_user(message.chat.id)
    await message.answer("Квіз розпочато.")
    # collect user date depended on chat type
    user_data[message.chat.id] = {"question_index": 0, "score": 0, "username": message.from_user.username}
    chat_data[message.chat.id] = {
        "question_index": 0,
        "score": 0,
        "chat_title": message.chat.title,
        "chat_tag": message.chat.username,
        "chat_partisipants": await bot.get_chat_members_count(message.chat.id),
        "chat_id": message.chat.id,
    }
    await send_question(message.chat.id)
    if message.chat.type == "private":
        for IDs in admins_ID:
            # send loggs to admins in dm if used in private chat  and append loggs file
            await bot.send_message(
                IDs,
                f" @{message.chat.username} ID: {message.chat.id}\n"
                f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n",
            )
            with open(results_file, "a") as file:
                file.write(
                    f" @{message.chat.username} ID: {message.chat.id}\n"
                    f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                    f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n"
                )
    else:
        # send loggs to admins in dm if used in group chat and append loggs file
        for IDs in admins_ID:
            await bot.send_message(
                IDs,
                f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                f" Participants: {await bot.get_chat_members_count(message.chat.id)}"
                f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n",
            )
            with open(results_file, "a") as file:
                file.write(
                    f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                    f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                    f" Participants: {await bot.get_chat_members_count(message.chat.id)}\n"
                    f" Just started quiz at {datetime.now() + timedelta(hours=2)}\n\n\n"
                )


async def send_question(user_id: int) ->None:
    questions_list = list(questions.keys())
    user_info = user_data.get(user_id, {"question_index": 0, "score": 0})
    question_index = user_info["question_index"]

    if question_index < len(questions_list):
        question = questions_list[question_index]
        keyboard = types.InlineKeyboardMarkup()
        for ans, score in questions[question].items():
            keyboard.add(types.InlineKeyboardButton(text=ans, callback_data=ans))

        formatted_question = f"{question_index + 1}/{len(questions_list)}. <b>{question}</b>"
        await bot.send_message(user_id, formatted_question, reply_markup=keyboard, parse_mode="HTML")
    else:
        await send_result_message(user_id, user_info["score"])


@dp.callback_query_handler(lambda call: True)
async def answer(call: types.CallbackQuery) ->None:
    answer = call.data
    user_id = call.message.chat.id
    user_info = user_data.get(user_id, {"question_index": 0, "score": 0})
    question_index = user_info["question_index"]
    question = list(questions.keys())[question_index]

    if answer in questions[question]:
        user_info["score"] += questions[question][answer]
        user_info["question_index"] += 1
        await send_question(user_id)


async def send_result_message(user_id: int, score: int) ->None:
    # func which sends result message after quiz
    user_info = user_data.get(user_id, {})
    username = user_info.get("username", "Unknown")
    first_name = user_info.get("first_name", "Unknown")
    last_name = user_info.get("last_name", "Unknown")

    # def result messages depended on users score
    if -1000 < score <= 0:
        result_message = "Ви взагалі не знаєте Романа, ідіть підівчіться та не позортесь"
        await bot.send_photo(user_id, photo=open(f"{quiz_picks}/pidyob.png", "rb"))
    elif 0 < score <= 10:
        result_message = "Дуже слабенько, ви напевно лише вчора дізналися хто такий Роман"
        await bot.send_photo(user_id, photo=open(f"{quiz_picks}/ok.png", "rb"))
    elif 10 < score <= 35:
        result_message = "Ви знаєте Романа не перший день, але все одно цього недостатньо"
        await bot.send_photo(user_id, photo=open(f"{quiz_picks}/patriot.png", "rb"))
    elif 30 < score <= 72:
        result_message = "Непогано, ще трішки і ви зможете сказати, що ви фанат Романа"
        await bot.send_photo(user_id, photo=open(f"{quiz_picks}/dovolniy.png", "rb"))
    elif 70 < score <= 130:
        result_message = "Ви справжній фанат Романа"
        await bot.send_photo(user_id, photo=open(f"{quiz_picks}/cool_1.png", "rb"))
    elif 130 < score:
        result_message = "Ви Локатир Романа, або його кращий друг"
        await bot.send_photo(user_id, photo=open(f"{quiz_picks}/bratva.png", "rb"))
    else:
        result_message = "Дуже негативно"
        await bot.send_photo(user_id, photo=open(f"{quiz_picks}/minus.jpg", "rb"))

    await bot.send_message(user_id, f"Ваш рахунок: {score}")
    await bot.send_message(
        user_id, f"{result_message}\n<a href='https://t.me/lokatir_bot'>Перейти до бота</a>", parse_mode="HTML"
    )
    for IDs in admins_ID:
        # send loggs to admins in dm if used in private chat
        await bot.send_message(
            IDs,
            f" @{username} ID: {user_id}\n"
            f" first name : {first_name} last name: {last_name}\n"
            f" finished quiz, with score: {score} at {datetime.now() + timedelta(hours=2)}\n\n\n",
        )
    with open(results_file, "a") as file:
        file.write(
            f" @{username} ID: {user_id}\n"
            f" first name : {first_name} last name: {last_name}\n"
            f" finished quiz, with score: {score} at {datetime.now() + timedelta(hours=2)}\n\n\n"
        )
    quiz_db.save_quiz_result(user_id, username, score)


@dp.message_handler(commands=["top"])
async def get_top(message: types.Message) ->None:
    top_results = quiz_db.get_top_results(limit=10)
    if top_results:
        response = "Топ 10 результатів:\n"
        for index, (username, score) in enumerate(top_results, start=1):
            response += f"{index}. <b>{username}</b>: {score} очків\n"
        await message.answer(response, parse_mode="HTML")
    else:
        await message.answer("Жодного результату зараз немає")
