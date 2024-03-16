from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config_data.api_config import get_all_data
from utils.api.yandex.info_def import get_city_list


def create_cities_keyboard(region: str) -> InlineKeyboardMarkup:
    all_data = get_all_data()
    cities = get_city_list(all_data, region)
    keyboard = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=city_name, callback_data=key) for key, city_name in cities.items()]
    keyboard.add(*buttons)

    return keyboard

