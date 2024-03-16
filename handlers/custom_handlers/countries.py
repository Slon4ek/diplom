from telebot.types import Message
from config_data.api_config import get_all_data
from loader import bot
from utils.api.yandex.info_def import get_all_countries


@bot.message_handler(state='*', commands=['countries'])
def get_counties(message: Message) -> None:
    """
    Функция принимает от пользователя команду и выводит список доступных стран в алфавитном порядке
    :param message: команда /countries
    :type message: Message
    :return: None
    """
    stations = get_all_data()
    countries = get_all_countries(stations)
    bot.send_message(message.from_user.id, '\n'.join(countries.values()))
