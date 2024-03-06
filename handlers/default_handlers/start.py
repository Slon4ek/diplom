from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    bot.reply_to(message, f"Привет, {message.from_user.full_name}! Приятно познакомиться.\n"
                          f"Я бот расписания движения всякого разного транспорта :)\n"
                          f"Введи команду /help, чтобы узнать что я могу.")

