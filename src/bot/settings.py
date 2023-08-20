from datetime import datetime, timedelta
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

import os

#set the phot dir for chupa function
photos_directory = "../lokatir/"

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

#IDs of bot administrators from environment .env file
admins_ID = os.getenv("admins_ID")
admins_ID = [int(id) for id in admins_ID.split(',')]

#ID for tracking specific user's messages
#used in restartTracking, stopTracking and changeTrackID funcs
chupa_id = os.getenv("chupa")
chupa_id = int(chupa_id)
chupa_ID = chupa_id

#varieble used to control bot version at launch
start_time = datetime.now() + timedelta(hours=2)


