from aiogram.utils import executor
from configs.settings import dp



if __name__ == '__main__':
    from users import quiz, user_commands
    from admins import tracks, users, notes
    from message_handlers import messages_handler
    executor.start_polling(dp, skip_updates=True)
