from typing import Dict

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_stations_keyboard(stations: Dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=station['Станция'], callback_data=station['Код станции'])
               for station in stations]
    keyboard.add(*buttons)

    return keyboard
