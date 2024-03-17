from typing import Dict

from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@logger.catch
def create_stations_keyboard(stations: Dict) -> InlineKeyboardMarkup:
    """
    Функция создает и возвращает Inline клавиатуру из названий станций удовлетворяющих запросу
    :param stations: словарь станций
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=station['Станция'], callback_data=station['Код станции'])
               for station in stations]
    keyboard.add(*buttons)

    return keyboard
