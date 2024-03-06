from telebot.types import Message
from config_data.api_config import get_all_stations
from loader import bot
from states.help import HelpState
from utils.api.yandex.info_def import get_station_list


@bot.message_handler(commands=['stations'])
def set_city(message: Message) -> None:
    bot.set_state(message.from_user.id, HelpState.city_choice, message.chat.id)
    bot.send_message(message.from_user.id, 'Список станций какого города вы хотели бы посмотреть?')


@bot.message_handler(state=HelpState.city_choice)
def set_transport(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Какой транспорт вас интересует(самолет, поезд, водный)?\n'
                                           'Либо напишите "Все" для отображения списка всех станций')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text.title()
    bot.set_state(message.from_user.id, HelpState.transport, message.chat.id)


@bot.message_handler(state=HelpState.transport)
def show_stations(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.lower() == 'самолет':
            data['transport_type'] = 'plane'
        elif message.text.lower() == 'поезд':
            data['transport_type'] = 'train'
        elif message.text.lower() == 'водный':
            data['transport_type'] = 'water'
        else:
            data['transport_type'] = None
    stations = get_all_stations()
    stations_list = get_station_list(stations, data['city'], data['transport_type'])
    if stations_list:
        text = ''
        for key, val in stations_list.items():
            if key == 'plane':
                text += 'Аэропорты:\n\n'
            elif key == 'train':
                text += 'Ж\\Д станции:\n\n'
            elif key == 'bus':
                text += 'Автобусные станции:\n\n'
            elif key == 'water':
                text += 'Порты:\n\n'
            for item in val:
                text += f'\t\t{item['Станция']}\n'
            else:
                text += '\n'
        bot.send_message(message.from_user.id, text)
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так, напишите название региона '
                                               'точно как в списке стран из команды /cities')
