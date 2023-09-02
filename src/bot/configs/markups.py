from aiogram import types
from configs.settings import dp, admins_ID


def create_user_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/quiz', '/creators', '/ban').add('/HowRomanAreYou', '/top', '/rofl').add('/sendQuestion', '/help')
    return markup




def create_admin_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/TrackControll', '/UsersControll', '/NotesNStats', '/userMenu')
    return markup

def create_tracks_controll_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/restartTracking', '/stopTracking', '/removeTrackID', '/addTrackID', '/tracks', '/back')
    return markup

def create_users_controll_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/sendAlert', '/sendMessage', '/addUser', '/users', '/back')
    return markup

def create_notes_n_stats_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/addNote', '/notes', '/stats', '/back')
    return markup

@dp.message_handler(commands=['admin','userMenu','TrackControll',
                              'UsersControll', 'NotesNStats', 'back' ])
async def admins_murkups(message: types.Message):
    if message.from_user.id in admins_ID:
        if message.text in ['/admin', '/back']:
            await message.reply("Admin Menu", reply_markup=create_admin_markup())
        elif message.text == '/TrackControll':
            await message.reply("Tracks Controll Menu:", reply_markup=create_tracks_controll_markup())
        elif message.text == '/NotesNStats':
            await message.reply("Notes And Stats Menu:", reply_markup=create_notes_n_stats_markup())
        elif message.text =='/UsersControll':
            await message.reply("Users Controll Menu:", reply_markup=create_users_controll_markup())
        elif message.text == '/userMenu':
            user_markup = create_user_markup()
            if message.from_user.id in admins_ID:
                user_markup.add('/admin')
            await message.reply("User Menu:", reply_markup=user_markup)
