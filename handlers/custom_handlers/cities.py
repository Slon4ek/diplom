from loguru import logger
from telebot.types import Message

from config_data.api_config import ALL_DATA
from loader import bot
from states.help import HelpState
from utils.api.yandex.info_def import get_city_in_region, get_all_regions


@bot.message_handler(state='*', commands=['cities'])
def set_region_name(message: Message) -> None:
    """
    Функция запрашивает у пользователя название региона для поиска городов
    :param message: команда /cities
    :type message: Message
    :return: None
    """
    logger.info(f'Пользователь с ID {message.from_user.id} запустил команду /cities')
    bot.set_state(message.from_user.id, HelpState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'Список городов какого региона вы хотели бы посмотреть?')


@bot.message_handler(state=HelpState.city, content_types='text')
def show_cities(message: Message) -> None:
    """
    Функция принимает от пользователя название региона, делает запрос к API Яндекс расписаний и выводит результат
    :param message: текст пользователя
    :type message: Message
    :return: None
    """
    logger.info(f'Пользователь с ID {message.from_user.id} ввел название региона: {message.text}')
    regions = get_all_regions(ALL_DATA)
    region_name = ''
    for key, region in regions.items():
        if message.text.lower() == region.lower():
            region_name = region
    cities = get_city_in_region(ALL_DATA, region_name)
    if cities:
        cities = cities.values()
        bot.send_message(message.from_user.id, '\n'.join(cities))
        bot.delete_state(message.from_user.id)
    else:
        logger.error('Неверно указан регион.')
        bot.send_message(message.from_user.id, 'Что-то пошло не так, напишите название региона '
                                               'точно как в списке регионов из команды /regions')
