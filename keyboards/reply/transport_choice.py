from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def transport_choice() -> ReplyKeyboardMarkup:
    """
    Функция создает объект клавиатуры для выбора вида транспорта и возвращает его
    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton('Самолеты')
    button2 = KeyboardButton('Поезда')
    button3 = KeyboardButton('Водный транспорт')
    button4 = KeyboardButton('Автобусы')
    button5 = KeyboardButton('Весь транспорт')
    keyboard.add(button1, button2, button3, button4, button5)
    return keyboard
