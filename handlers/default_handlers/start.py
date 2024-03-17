from telebot.types import Message
from database.database_class import User
import peewee

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        User.create(
            user_id=user_id,
            user_name=username
        )
        bot.send_message(message.from_user.id,
                         f"Привет, {username}! Приятно познакомиться.\n"
                         f"Я бот расписания движения всякого разного транспорта :)\n"
                         f"Данные предоставлены сервисом Яндекс Расписания'\n"
                         f"Введите команду /help, чтобы узнать что я могу.")
    except peewee.IntegrityError:
        user = User.get(User.user_id == user_id)
        bot.send_message(message.from_user.id,
                         f"Рад вас снова видеть {user.user_name}.\n"
                         f"Я бот расписания движения всякого разного транспорта :)\n"
                         f"Данные предоставлены сервисом Яндекс Расписания'\n"
                         f"Введите команду /help, чтобы узнать что я могу.")
