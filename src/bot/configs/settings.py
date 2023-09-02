from datetime import datetime, timedelta
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

import os

#set the phot dir for chupa function
photos_directory = "../pictures/lokatir/"

quiz_picks = '../pictures/quiz_pictures'

# Get the absolute path to results.txt
results_file = '../../results.txt'
# Use results_file in your code

#load enviroment from environment .env file
load_dotenv()

#get bot TOKEN from .env file
TOKEN = os.getenv("TOKEN")

#initialize the bot and dispatcher
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)

# Dictionary to store user-specific data during the quiz
user_data = {}

#dictionary to store chat-specific data
chat_data = {}

questions= {}

#IDs of bot administrators from environment .env file
admins_ID = os.getenv("admins_ID")
admins_ID = [int(id) for id in admins_ID.split(',')]

#ID for tracking specific user's messages
#used in restartTracking, stopTracking and changeTrackID funcs
chupa_id_str = os.getenv("chupa")
chupa_id = []

tracking_enabled = True

if chupa_id_str:
    chupa_id = [int(id_str) for id_str in chupa_id_str.split(',') if id_str.strip()]


#varieble used to control bot version at launch
start_time = datetime.now() + timedelta(hours=2)

creator_links = [
            types.InlineKeyboardButton("OleksandrYanchar GitHub", url="https://github.com/OleksandrYanchar"),
        types.InlineKeyboardButton("YuriiDorosh GitHub", url="https://github.com/YuriiDorosh"),
        types.InlineKeyboardButton("saintqqe Instagram", url="https://www.instagram.com/saintqqe/"),
        types.InlineKeyboardButton("y_u_r_a111 Instagram", url="https://www.instagram.com/y_u_r_a111/"),
        types.InlineKeyboardButton("saintqqe Twitch", url="https://www.twitch.tv/saintqqe"),
        types.InlineKeyboardButton("fortnite_dota Twitch", url="https://www.twitch.tv/fortnite_dota"),
        types.InlineKeyboardButton("Donation", url="https://send.monobank.ua/jar/4J4iy8p8i3"),
        types.InlineKeyboardButton("All links", url="https://linktr.ee/lokatirbot"),
    ]

