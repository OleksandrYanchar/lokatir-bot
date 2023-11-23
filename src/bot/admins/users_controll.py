from aiogram import types
from data_storge.users_database import UsersDatabase
from configs.settings import bot, dp, admins_ID, start_time, results_file, tate_pics

users_db = UsersDatabase()


@dp.message_handler(commands=["users"])
async def get_ids(message: types.Message) -> None:
    users = []
    db_entries = users_db.get_all_entries()
    for entry in db_entries:
        users.append(entry[0])
    await bot.send_message(message.chat.id, f"{users} ")


@dp.message_handler(commands=["addUser"])
async def add_user(message: types.Message) -> None:
    if message.from_user.id in admins_ID:
        if len(message.text.split()) > 1:
            user_ids = [id.strip() for id in message.text.split()[1:] if id.strip().isdigit()]
            added_users = 0
            for user_id in user_ids:
                if not users_db.user_exists(user_id):
                    users_db.add_user(user_id)
                    added_users += 1
            if added_users > 0:
                await message.reply(f"додано {added_users} користувачів до бд")
            else:
                await message.reply(" всі  користувачі вже існують у бд")
        else:
            await message.reply(" введи айді")


@dp.message_handler(commands=["sendAlert"])
async def send_alert    (message: types.Message) -> None:
    if message.from_user.id in admins_ID:
        if len(message.text.split()) > 1:
            alert_text = message.text.replace("/sendAlert", "").strip()
            db_entries = users_db.get_all_entries()
            for entry in db_entries:
                user_id = entry[0]
                try:
                    await bot.send_message(user_id, alert_text)
                except Exception as e:
                    await bot.send_message(message.chat.id, f"{e}:{user_id}")
        else:
            await message.reply("введи текст")


@dp.message_handler(commands=["sendMessage"])
async def send_message(message: types.Message) -> None:
    if message.from_user.id in admins_ID:
        if len(message.text.split()) > 1:
            if len(message.text.split()) > 2:
                if not message.text.split()[1].lstrip("-").isdigit():
                    await message.reply("айді повинно бути цифрами")
                else:
                    alert_text = " ".join(message.text.split()[2:])
                    user_id = int(message.text.split()[1])
                    try:
                        await bot.send_message(user_id, alert_text)
                    except Exception as e:
                        await message.reply(f"Error: {e}")
            else:
                await message.reply("введи текст повідомлення")
        else:
            await message.reply("введи айді і текст")


@dp.message_handler(commands=["stats"])
async def stats(message: types.Message) -> None:
    # works only for admins to geet loggin file from server
    if message.chat.type == "private":
        if message.from_user.id in admins_ID:
            await bot.send_message(message.chat.id, f"версія бота від {start_time} ")
            await bot.send_document(message.chat.id, open(results_file, "rb"))
    else:
        await bot.send_message(message.chat.id, "Недостатньо прав")

@dp.message_handler(commands=["chica"])
async def chica(message: types.Message) -> None:
    if message.from_user.id in admins_ID:
        db_entries = users_db.get_all_entries()
        for entry in db_entries:
            user_id = entry[0]
            with open(f'{tate_pics}/chica.mp4', 'rb') as chica:
                try:
                    await bot.send_animation(user_id, animation=chica)
                except Exception as e:
                    await bot.send_message(message.chat.id, f"{e}:{user_id}")