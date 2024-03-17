from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config_data.api_config import ALL_DATA
from utils.api.yandex.info_def import get_region_in_country


@logger.catch
def create_regions_keyboard(country: str) -> InlineKeyboardMarkup | None:
    """
    Функция создает и возвращает Inline клавиатуру из названий регионов выбранной страны,
    если список регионов не найден возвращает None
    :param country: название страны
    :return: InlineKeyboardMarkup
    """
    regions = get_region_in_country(ALL_DATA, country)
    keyboard = InlineKeyboardMarkup(row_width=2)
    if regions:
        buttons = [InlineKeyboardButton(text=region_title, callback_data=key) for key, region_title in regions.items()]
        keyboard.add(*buttons)
        return keyboard
    else:
        return None
