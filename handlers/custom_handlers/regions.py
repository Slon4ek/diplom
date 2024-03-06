from telebot.types import Message
from config_data.api_config import get_all_stations
from loader import bot
from utils.api.yandex.info_def import get_region_list
from states.help import HelpState


@bot.message_handler(commands=['regions'])
def get_regions(message: Message) -> None:
    bot.set_state(message.from_user.id, HelpState.regions, message.chat.id)
    bot.send_message(message.from_user.id, 'Список регионов какой страны вы хотели бы посмотреть?')


@bot.message_handler(state=HelpState.regions)
def show_regions(message: Message) -> None:
    stations = get_all_stations()
    regions = get_region_list(stations, message.text)
    if regions:
        regions = sorted(regions)
        bot.send_message(message.from_user.id, '\n'.join(regions))
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так, напишите название страны '
                                               'точно как в списке стран из команды /countries')

