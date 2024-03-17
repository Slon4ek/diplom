from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config_data.api_config import ALL_DATA
from utils.api.yandex.info_def import get_city_in_region


@logger.catch
def create_cities_keyboard(region: str) -> InlineKeyboardMarkup:
    """
    Функция создает и возвращает Inline клавиатуру с названиями городов выбранного региона
    :param region: название региона
    :return: InlineKeyboardMarkup
    """
    cities = get_city_in_region(ALL_DATA, region)
    keyboard = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=city_name, callback_data=key) for key, city_name in cities.items()]
    keyboard.add(*buttons)

    return keyboard
