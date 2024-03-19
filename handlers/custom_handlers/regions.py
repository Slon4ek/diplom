from loguru import logger
from telebot.types import Message

from config_data.api_config import ALL_DATA
from loader import bot
from states.help import HelpState
from utils.api.yandex.info_def import get_region_in_country, get_all_countries


@bot.message_handler(commands=['regions'])
def set_country_name(message: Message) -> None:
    """
    Функция запрашивает у пользователя название страны по которой нужно произвести поиск регионов
    :param message: команда /regions
    :type message: Message
    :return: None
    """
    logger.info(f'Пользователь {message.from_user.id} запустил команду /regions')
    bot.set_state(message.from_user.id, HelpState.regions, message.chat.id)
    bot.send_message(message.from_user.id, 'Список регионов какой страны вы хотели бы посмотреть?')


@bot.message_handler(state=HelpState.regions)
def show_regions(message: Message) -> None:
    """
    Функция принимает от пользователя название страны, делает запрос к API Яндекс расписаний и выводит
    список регионов этой страны
    :param message: название страны для поиска
    :type message: Message
    :return: None
    """
    logger.info(f'Пользователь {message.from_user.id} ввел название страны: {message.text}')
    countries = get_all_countries(ALL_DATA)
    country_name = ''
    for key, country in countries.items():
        if message.text.lower() == country.lower():
            country_name = country
    regions = get_region_in_country(ALL_DATA, country_name)
    if regions:
        regions = regions.values()
        bot.send_message(message.from_user.id, '\n'.join(regions))
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так, напишите название страны '
                                               'точно как в списке стран из команды /countries')
