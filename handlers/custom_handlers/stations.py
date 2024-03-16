from telebot.types import Message, ReplyKeyboardRemove

from config_data.api_config import get_all_data
from keyboards.reply.transport_choice import transport_choice
from loader import bot
from states.help import HelpState
from utils.api.yandex.info_def import get_station_list


@bot.message_handler(commands=['stations'])
def set_city(message: Message) -> None:
    """
    Функция запрашивает у пользователя название города для поиска
    :param message: команда /stations
    :type message: Message
    :return: None
    """
    bot.set_state(message.from_user.id, HelpState.city_choice, message.chat.id)
    bot.send_message(message.from_user.id, 'Список станций какого города вы хотели бы посмотреть?')


@bot.message_handler(state=HelpState.city_choice)
def set_transport(message: Message) -> None:
    """
    Функция сохраняет введенное пользователем название города и запрашивает вид транспорта для поиска
    :param message: название города
    :type message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, 'Какой вид транспорта вас интересует?',
                     reply_markup=transport_choice())
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text.title()
    bot.set_state(message.from_user.id, HelpState.transport, message.chat.id)


@bot.message_handler(state=HelpState.transport)
def show_stations(message: Message) -> None:
    """
    Функция сохраняет вид транспорта выбранный пользователем, делает запрос к API Яндекс расписаний и выводит результат
    :param message: вид транспорта
    :type message: Message
    :return: None
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == 'Самолеты':
            data['transport_type'] = 'plane'
        elif message.text == 'Поезда':
            data['transport_type'] = 'train'
        elif message.text == 'Водный транспорт':
            data['transport_type'] = 'water'
        elif message.text == 'Автобусы':
            data['transport_type'] = 'bus'
        elif message.text == 'Весь транспорт':
            data['transport_type'] = None
        else:
            bot.send_message(message.from_user.id, 'Ой! Такого я не знаю :( '
                                                   'Введите вид транспорта или нажмите на кнопочку')
            return
    stations = get_all_data()
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
        keyboard = ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, text, reply_markup=keyboard)
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так, напишите название региона '
                                               'точно как в списке стран из команды /cities')
