from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_location() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Отправить местонахождение', request_location=True))
    return keyboard
