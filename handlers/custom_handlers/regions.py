from telebot.types import Message
from config_data.api_config import get_all_data
from loader import bot
from utils.api.yandex.info_def import get_region_list, get_all_countries
from states.help import HelpState


@bot.message_handler(commands=['regions'])
def get_regions(message: Message) -> None:
    """
    Функция запрашивает у пользователя название страны по которой нужно произвести поиск
    :param message: команда /regions
    :type message: Message
    :return: None
    """
    bot.set_state(message.from_user.id, HelpState.regions, message.chat.id)
    bot.send_message(message.from_user.id, 'Список регионов какой страны вы хотели бы посмотреть?')


@bot.message_handler(state=HelpState.regions)
def show_regions(message: Message) -> None:
    """
    Функция принимает от пользователя название страны, делает запрос к API Яндекс расписаний и выводит результат
    :param message: название страны для поиска
    :type message: Message
    :return: None
    """
    stations = get_all_data()
    countries = get_all_countries(stations)
    country_name = ''
    for key, country in countries.items():
        if message.text.lower() == country.lower():
            country_name = country
    regions = get_region_list(stations, country_name)
    if regions:
        regions = regions.values()
        bot.send_message(message.from_user.id, '\n'.join(regions))
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так, напишите название страны '
                                               'точно как в списке стран из команды /countries')

