from aiogram import types

def create_user_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/quiz', '/creators', '/ban', '/HowRomanAreYou', '/top', '/rofl')
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
