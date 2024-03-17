from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.api.yandex.info_def import get_transport


@logger.catch
def create_transport_keyboard(all_data, city_name):
    """
    Функция создает и возвращает Inline клавиатуру с видами транспорта доступными в выбранном городе
    :param all_data: общая информация по всем станциям
    :param city_name: название города
    :return: InlineKeyboardMarkup
    """
    transport_types = get_transport(all_data, city_name)
    transport_types_dict = dict()
    for t_type in transport_types:
        if t_type == 'train':
            transport_types_dict['train'] = 'Поезд'
        elif t_type == 'plane':
            transport_types_dict['plane'] = 'Самолет'
        elif t_type == 'water':
            transport_types_dict['water'] = 'Водный транспорт'
        elif t_type == 'bus':
            transport_types_dict['bus'] = 'Автобус'
    buttons = [InlineKeyboardButton(text=val, callback_data=key) for key, val in transport_types_dict.items()]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
