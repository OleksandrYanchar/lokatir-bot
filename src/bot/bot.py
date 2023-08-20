from settings import bot, dp
from aiogram import executor

if __name__ == '__main__':
    from questions import *
    from quiz import *
    from settings import *
    from user_commands import *
    from admin_commands import *

    executor.start_polling(dp)
