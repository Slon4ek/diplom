from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config_data.api_config import ALL_DATA
from utils.api.yandex.info_def import get_all_countries


@logger.catch
def create_countries_keyboard(interval: int) -> InlineKeyboardMarkup:
    """
    Функция создает и возвращает Inline клавиатуру с названиями стран в зависимости от выбранного интервала
    :param interval: интервал из начальных букв названий стран
    :return: InlineKeyboardMarkup
    """
    interval1 = 'АБВГДЕЁЖЗИ'
    interval2 = 'ЙКЛМНОПРСТ'
    interval3 = 'УФХЦЧШЩЭЮЯ'
    all_countries = get_all_countries(ALL_DATA)
    if interval == 1:
        countries = {key: val for key, val in all_countries.items() if val[0] in interval1}
    elif interval == 2:
        countries = {key: val for key, val in all_countries.items() if val[0] in interval2}
    elif interval == 3:
        countries = {key: val for key, val in all_countries.items() if val[0] in interval3}
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=title, callback_data=key) for key, title in countries.items()]
    keyboard.add(*buttons)

    return keyboard


@logger.catch
def set_interval() -> InlineKeyboardMarkup:
    """
    Функция создает клавиатуру для выбора интервала названий стран
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text='Страны от А до И', callback_data=1)
    button2 = InlineKeyboardButton(text='Страны от Й до Т', callback_data=2)
    button3 = InlineKeyboardButton(text='Страны от У до Я', callback_data=3)
    keyboard.add(button1, button2, button3)
    return keyboard
