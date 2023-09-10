import os
import asyncio
import random
import re
from aiogram import types
from configs.settings import dp, bot, admins_ID, chupa_id, photos_directory, tate_pics
from admins.notes import get_notes_status, append_notes
from users.user_commands import get_question_status, get_question


@dp.message_handler(lambda message: all(
    re.search(rf'(?i)\b{word}\b', message.text) for word in ['на', 'як[уі]', 'завтра', 'пар[аиу]']))
async def para(message: types.Message):
     with open(f'{tate_pics}/nigga.png', 'rb') as photo:
        await message.reply_photo(photo)

@dp.message_handler(lambda message: all(
    re.search(rf'(?i)\b{word}\b', message.text) for word in ['[шщ]о','на','завтра']))
async def para(message: types.Message):
     with open(f'{tate_pics}/school.mp4', 'rb') as school:
        await message.reply_animation(animation=school)

@dp.message_handler(lambda message: all(
    re.search(rf'(?i)\b{word}\b', message.text) for word in ['перш[ау]', 'пар[аиу]']))
async def para(message: types.Message):
     with open(f'{tate_pics}/first.mp4', 'rb') as first:
        await message.reply_animation(animation=first)



@dp.message_handler()
async def process_message(message: types.Message) -> None:
    append_notes_task = asyncio.create_task(append_notes(message))
    chupa_task = asyncio.create_task(chupa(message))
    forward_task = asyncio.create_task(forward(message))
    get_question_task = asyncio.create_task(get_question(message))

    if get_notes_status:
        await append_notes_task
    elif get_question_status:
        get_question_task
    else:
        await asyncio.gather(chupa_task, forward_task)



@dp.message_handler(lambda message: message.from_user.id in chupa_id)
async def chupa(message: types.Message) -> None:
    from admins.tracks import tracking_enabled, chupa_id
    from admins.notes import get_notes_status
    from users.user_commands import get_question_status

    if str(message.from_user.id) in str(chupa_id) and tracking_enabled and not get_notes_status and not get_question_status:
        photo_files = [file for file in os.listdir(photos_directory) if file.endswith(".jpg")]
        random_photo = random.choice(photo_files)
        with open(os.path.join(photos_directory, random_photo), "rb") as photo:
            await message.reply_photo(photo)


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def forward(message: types.Message) -> None:
    from admins.tracks import tracking_enabled
    from admins.notes import get_notes_status
    from users.user_commands import get_question_status
    if not get_notes_status and not get_question_status:
        for IDs in admins_ID:
            await bot.forward_message(IDs, message.chat.id, message.message_id)
            if message.chat.type == "private":
                await bot.send_message(IDs,
                                       f'from user: @{message.from_user.username}, ID: {message.from_user.id}\n'
                                       f'first name: {message.from_user.first_name}, last name: {message.from_user.last_name}\n')
            else:
                await bot.send_message(IDs, f'at: @{message.chat.username}, Name: {message.chat.title} \n'
                                            f'Participants: {await bot.get_chat_members_count(message.chat.id)}\n'
                                            f'ID: {message.chat.id}, Type: {message.chat.type}\n'
                                    f'from user: @{message.from_user.username}, ID: {message.from_user.id}\n'
                                    f'first name: {message.from_user.first_name}, last name: {message.from_user.last_name}\n'
                                    )
