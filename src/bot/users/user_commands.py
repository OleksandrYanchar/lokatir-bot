import random
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta
from configs.markups import create_user_markup
from configs.settings import chat_data, user_data, bot, dp, admins_ID, questions, results_file, creator_links, tate_pics
from configs.questions import original_questions
from data_storge.users_database import UsersDatabase
from configs.jokes import jokes


users_db = UsersDatabase()
get_question_status = False


@dp.message_handler(commands=["start"])
# handle the '/start' command
async def cmd_start(message: types.Message) ->None:
    user_id = message.chat.id
    user_markup = create_user_markup()
    if not users_db.user_exists(user_id):
        users_db.add_user(user_id)
    if message.from_user.id in admins_ID:
        user_markup.add("/admin")
    for IDs in admins_ID:
        await bot.forward_message(IDs, message.chat.id, message.message_id)
    await message.answer("Привіт, я бот-вікторина Локатира романа.", reply_markup=user_markup)
    await message.answer_sticker("CAACAgIAAxkBAAEKFiNk4yseSJX8wQLyKT6V6MSR7K6N7AACyTAAAhL-wUt17d_gphvbujAE")
    await help_menu(message)
    if message.chat.type == "private":
        # send loggs to admins in dm and append logging txt file
        for IDs in admins_ID:
            await bot.send_message(
                IDs,
                f" @{message.chat.username} ID: {message.chat.id}\n"
                f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                f" Just started bot at {datetime.now() + timedelta(hours=2)}\n\n\n",
            )
            with open(results_file, "a") as file:
                file.write(
                    f" @{message.chat.username}, ID: {message.chat.id}\n"
                    f" First name: {message.chat.first_name}, Last name: {message.chat.last_name}\n"
                    f" Just started bot at {datetime.now() + timedelta(hours=2)}\n\n\n"
                )
    else:
        for IDs in admins_ID:
            await bot.send_message(
                IDs,
                f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                f" Participants: {await bot.get_chat_members_count(message.chat.id)}\n"
                f" Just started bot at {datetime.now() + timedelta(hours=2)}\n\n\n",
            )


@dp.message_handler(commands=["help"])
async def help_menu(message: types.Message)->None:
    await bot.send_message(
        message.chat.id,
        "<b>Ось список доступних команд</b>:\n"
        "/quiz: для початку вікторини\n"
        "/top: показує найкращий результат у квізі\n"
        "/HowRomanAreYou: показує на скільки відсотків ви Локатир Роман\n"
        "/rofl: відправляє рандомний анекдот про Романа\n"
        "/ban: ( ͡° ͜ʖ ͡°)\n"
        "/sendFeedBack: відправляє ваше повідомлення для адміністрації\n"
        "/help: показує список доступних команд"
        "/creators: посилання на авторів бота\n",
        parse_mode="HTML",
    )


@dp.message_handler(commands=["creators"])
# Handle 'creators' command to send links for creators
async def creators(message: types.Message) ->None:
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(*creator_links)
    await bot.send_message(message.chat.id, "Посилання на авторів бота:", reply_markup=markup)


@dp.message_handler(commands=['HowRomanAreYou'])
#handle the '/HowROmanAreYou' command
#generate random numb in range 0 - 100
async def how_roman_are_you(message: types.Message):
    procent = random.randint(0,100)
    await message.reply(f'ви на {procent}% Роман Локатир')
    if message.chat.type == "private":
        for IDs in admins_ID:
            # send loggs to admins in dm if used in private chat
            await bot.send_message(
                IDs,
                f" @{message.chat.username} ID: {message.chat.id}\n"
                f" first name: {message.chat.first_name} last name: {message.chat.last_name}\n"
                f" is {procent}% roman ",
            )
    else:
        for IDs in admins_ID:
            # send loggs to admins in dm if used in group chat
            await bot.send_message(
                IDs,
                f" Type: {message.chat.type}, Tag: @{message.chat.username}\n"
                f" Title: '{message.chat.title}', ID: {message.chat.id}\n"
                f" Participants: {await bot.get_chat_members_count(message.chat.id)}\n"
                f" User: ID:{message.from_user.id} Username: @{message.from_user.username} \n"
                f"first name: {message.from_user.first_name} last name: {message.from_user.last_name}\n "
                f" is {procent}% roman ",
            )


@dp.message_handler(commands=["ban"])
async def ban_reply(message: types.Message) ->None:
    with open(f"{tate_pics}/tate.mp4", "rb") as tate:
        await message.reply_animation(animation=tate)


@dp.message_handler(commands=["rofl"])
async def joke(message: types.Message) ->None:
    joke = random.choice(jokes)
    await bot.send_message(message.chat.id, joke)


@dp.message_handler(commands=["sendFeedBack"])
async def send_question(message: types.Message)->None:
    global get_question_status
    await message.answer("Напишіть ваше повідомлення")
    get_question_status = True


async def get_question(message: types.Message) ->None:
    global get_question_status
    if get_question_status:
        try:
            for IDs in admins_ID:
                await bot.send_message(
                    IDs,
                    f" Question from user:\n"
                    f" Username: @{message.from_user.username}, ID: {message.from_user.id}\n"
                    f" First name: {message.from_user.first_name}, Last name: {message.from_user.last_name}\n\n"
                    f" <b>{message.text}</b>",parse_mode="HTML"
                )
            await message.answer("Повідомлення відправлене")
        except Exception as e:
            await message.answer(str(e))
        get_question_status = False
