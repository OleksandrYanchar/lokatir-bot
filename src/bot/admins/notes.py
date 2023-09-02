import asyncio
from aiogram import types
from configs.settings import admins_ID, bot, dp, admins_ID


get_notes_status = False


@dp.message_handler(commands=["addNote"])
async def add_note(message: types.Message) -> None:
    global get_notes_status
    if message.from_user.id in admins_ID:
        await message.answer("Enter notes")
        get_notes_status = True


@dp.message_handler(commands=["notes"])
async def get_notes(message: types.message) -> None:
    if message.chat.type == "private":
        if message.from_user.id in admins_ID:
            await bot.send_document(message.chat.id, open("../../notes.txt", "rb"))
    else:
        await message.answer("Недостатньо прав")


async def append_notes(message: types.Message) -> None:
    global get_notes_status
    if message.from_user.id in admins_ID:
        if get_notes_status:
            try:
                with open("../../notes.txt", "a") as file:
                    file.write(message.text + "\n")
                    await message.answer("Note added")
            except Exception as e:
                await message.answer(str(e))
            get_notes_status = False
