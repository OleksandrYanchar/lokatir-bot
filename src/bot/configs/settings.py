from datetime import datetime, timedelta
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

import os

#set the phot dir for chupa function
photos_directory = "../lokatir/"

quiz_picks = '../pictures'

# Get the absolute path to results.txt
results_file = '../../results.txt'
# Use results_file in your code

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


