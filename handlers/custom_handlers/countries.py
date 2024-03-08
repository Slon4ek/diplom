from telebot.types import Message
from config_data.api_config import get_all_stations
from loader import bot
from utils.api.yandex.info_def import get_country_list


@bot.message_handler(state='*', commands=['countries'])
def get_counties(message: Message) -> None:
    """
    Функция принимает от пользователя команду и выводит список доступных стран в алфавитном порядке
    :param message: команда /countries
    :type message: Message
    :return: None
    """
    stations = get_all_stations()
    countries = get_country_list(stations)
    countries = sorted(countries)
    bot.send_message(message.from_user.id, '\n'.join(countries))
