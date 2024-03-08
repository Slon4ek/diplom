from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_location() -> ReplyKeyboardMarkup:
    """
    Функция создает объект клавиатуры для отправки местоположения пользователя и возвращает его
    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Отправить местонахождение', request_location=True))
    return keyboard
