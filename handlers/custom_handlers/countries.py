from loguru import logger
from telebot.apihelper import ApiException, ApiTelegramException
from telebot.types import Message

from config_data.api_config import ALL_DATA
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
    logger.info(f'Пользователь {message.from_user.id} запустил команду /countries')
    try:
        countries = get_all_countries(ALL_DATA)
        bot.send_message(message.from_user.id, '\n'.join(countries.values()))
    except (ApiException, ApiTelegramException, TypeError) as exc:
        logger.error(exc)
