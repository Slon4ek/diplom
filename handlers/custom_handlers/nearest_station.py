from loguru import logger
from telebot.types import Message, ReplyKeyboardRemove

from config_data.api_config import get_nearest_stations
from keyboards.reply.location import request_location
from keyboards.reply.transport_choice import transport_choice
from loader import bot
from states.location_state import LocationState
from utils.api.yandex.info_def import nearest_station_text


@bot.message_handler(commands=['nearest_station'])
def set_coordinates(message: Message) -> None:
    """
    Функция запрашивает у пользователя координаты его местоположения
    :param message: команда /nearest_station
    :type message: Message
    :return: None
    """
    logger.info(f'Пользователь {message.from_user.id} запустил команду /nearest_station')
    bot.send_message(message.from_user.id, 'Чтобы найти ближайшие станции мне нужны ваши координаты.'
                                           'Отправьте их нажав на кнопку "Отправить местонахождение"',
                     reply_markup=request_location())
    bot.set_state(message.from_user.id, LocationState.get_location)


@bot.message_handler(content_types=['text', 'location'], state=LocationState.get_location)
def set_transport_type(message: Message) -> None:
    """
    Функция сохраняет координаты пользователя и запрашивает вид транспорта по которому нужно сделать запрос
    :param message: координаты местоположения пользователя
    :type message: Message
    :return: None
    """
    if message.content_type == 'location':
        logger.info(f'Пользователь {message.from_user.id} отправил свои координаты')
        with bot.retrieve_data(message.from_user.id) as data:
            data['latitude'] = message.location.latitude
            data['longitude'] = message.location.longitude
        bot.send_message(message.from_user.id, f'Отлично, ваши координаты:\n'
                                               f'Широта: {message.location.latitude}\n'
                                               f'Долгота: {message.location.longitude}\n'
                                               f'Какой вид транспорта вас интересует?',
                         reply_markup=transport_choice())
        bot.set_state(message.from_user.id, LocationState.transport_type)
    else:
        logger.error(f'Пользователь {message.from_user.id} не отправил свои координаты')
        bot.send_message(message.from_user.id, 'Без ваших координат я не смогу помочь :(')


@bot.message_handler(state=LocationState.transport_type)
def set_search_radius(message: Message) -> None:
    """
    Функция сохраняет вид транспорта введенный пользователем и запрашивает радиус поиска
    :param message: вид транспорта
    :type message: Message
    :return: None
    """
    logger.info(f'Выбор транспорта пользователем {message.from_user.id}: {message.text}')
    with bot.retrieve_data(message.from_user.id) as data:
        if message.text == 'Самолеты':
            data['transport_type'] = 'plane'
        elif message.text == 'Поезда':
            data['transport_type'] = 'train'
        elif message.text == 'Водный транспорт':
            data['transport_type'] = 'water'
        elif message.text == 'Автобусы':
            data['transport_type'] = 'bus'
        elif message.text == 'Весь транспорт':
            data['transport_type'] = 'all'
        else:
            bot.send_message(message.from_user.id, 'Вы что-то не то ввели. '
                                                   'Для выбора транспорта нажмите на кнопочку:)')
            return
    if data['transport_type']:
        keyboard = ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Отлично, транспорт выбрали. '
                                               'Теперь введите радиус поиска(максимум 50км)',
                         reply_markup=keyboard)
        bot.set_state(message.from_user.id, LocationState.get_radius)


@bot.message_handler(state=LocationState.get_radius)
def show_nearest_stations(message: Message) -> None:
    """
    Функция принимает от пользователя радиус поиска, делает запрос к API Яндекс расписаний и выводит результат
    :param message: радиус поиска
    :type message: Message
    :return: None
    """
    logger.info(f'Пользователь {message.from_user.id} ввел радиус: {message.text}')
    if message.text.isdigit():
        if 0 < int(message.text) < 51:
            with bot.retrieve_data(message.from_user.id) as data:
                stations = get_nearest_stations(latitude=data['latitude'],
                                                longitude=data['longitude'],
                                                radius=int(message.text),
                                                transport_type=data['transport_type'])
                text = nearest_station_text(stations)
            if text:
                if len(text) > 4096:
                    for txt in range(0, len(text), 4096):
                        bot.send_message(message.from_user.id, '{}'.format(text[txt: txt + 4096]))
                else:
                    bot.edit_message_text(chat_id=message.chat.id,
                                          message_id=message.message_id,
                                          text=text)
            else:
                bot.send_message(message.from_user.id, 'По вашем параметрам ни одной станции не найдено.')
                bot.delete_state(message.from_user.id)
        else:
            bot.send_message(message.from_user.id, 'Поддерживаемый радиус поиска от 1 до 50 км')
    else:
        bot.send_message(message.from_user.id, 'Ошибка: Должно быть целое число от 1 до 50')
