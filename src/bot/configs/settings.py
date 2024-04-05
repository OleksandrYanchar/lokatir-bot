from datetime import datetime, timedelta
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
import os
from typing import List, Dict, Optional

# Directory for photos used in the 'chupa' function
photos_directory = './src/pictures/lokatir'
quiz_picks = './src/pictures/quiz_pictures'
tate_pics = './src/pictures/trash'

# Absolute path to the results file
results_file = "../../results.txt"

# Load environment variables from the .env file
load_dotenv()

# Retrieve bot TOKEN from the .env file
TOKEN = os.getenv("TOKEN")

# Initialize the bot and dispatcher
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)

# Dictionary to store user-specific data for the quiz
user_data: Dict["str", "str"]= {}

# Dictionary to store chat-specific data
chat_data: Dict["str", "str"]= {}

questions: Dict["str", "str"]= {}

# Retrieve and process admin IDs from the .env file
env_admins_ID: Optional[str]  = os.getenv("admins_ID")
admins_ID: List[int] = [int(id) for id in (env_admins_ID or "").split(",") if id.strip()]

# IDs to track specific user messages; used in 'restartTracking', 'stopTracking', and 'changeTrackID' functions
chupa_id_str = os.getenv("chupa")
chupa_id = []
tracking_enabled = True

if chupa_id_str:
    chupa_id = [int(id_str) for id_str in chupa_id_str.split(",") if id_str.strip()]

# Variable to control bot version upon launch
start_time = datetime.now() + timedelta(hours=2)

# Inline keyboard buttons for creator links
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
