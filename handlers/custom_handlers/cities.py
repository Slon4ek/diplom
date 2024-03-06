from telebot.types import Message
from config_data.api_config import get_all_stations
from loader import bot
from utils.api.yandex.info_def import get_city_list
from states.help import HelpState


@bot.message_handler(commands=['cities'])
def get_cities(message: Message) -> None:
    bot.set_state(message.from_user.id, HelpState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'Список городов какого региона вы хотели бы посмотреть?')


@bot.message_handler(state=HelpState.city, content_types='text')
def show_cities(message: Message) -> None:
    stations = get_all_stations()
    cities = get_city_list(stations, message.text)
    if cities:
        bot.send_message(message.from_user.id, '\n'.join(cities))
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так, напишите название региона '
                                               'точно как в списке регионов из команды /regions')
