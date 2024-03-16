from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config_data.api_config import get_all_data
from utils.api.yandex.info_def import get_region_list


def create_regions_keyboard(country: str) -> InlineKeyboardMarkup | None:
    all_data = get_all_data()
    regions = get_region_list(all_data, country)
    keyboard = InlineKeyboardMarkup(row_width=2)
    if regions:
        buttons = [InlineKeyboardButton(text=region_title, callback_data=key) for key, region_title in regions.items()]
        keyboard.add(*buttons)
        return keyboard
    else:
        return None
