from telebot.types import CallbackQuery, Message
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from database.database_class import User, InstationRequest
from keyboards.inline import (countries_keyboard, regions_keyboard,
                              cities_keyboard, transport_keyboard, stations_keyboard)
from loader import bot
from config_data.api_config import ALL_DATA, get_schedule_in_station
from utils.api.yandex.info_def import *

all_countries = get_all_countries(ALL_DATA)
all_regions = get_all_regions(ALL_DATA)
all_cities = get_all_cities(ALL_DATA)
all_stations = get_all_stations(ALL_DATA)
user_choice = dict()  # словарь для записи данных от пользователя


@bot.message_handler(commands=['instation'])
def set_country_interval(message: Message) -> None:
    """
    Функция предлагает пользователю выбрать интервал в зависимости от первой буквы названия страны
    """
    user_id = message.from_user.id
    username = message.from_user.username
    logger.info(f'Пользователь {username} c ID {user_id} запустил команду /instation')
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, 'Вы не зарегистрированы, введите команду /start')
        return

    bot.send_message(user_id, 'В этом разделе вы можете посмотреть расписание '
                              'движения транспорта по выбранной станции',
                     reply_markup=countries_keyboard.set_interval())
    user_choice[user_id] = dict()
    user_choice[user_id] = {'user_id': user_id}


@bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3'])
def set_country_name(call: CallbackQuery) -> None:
    """
    В зависимости от выбранного интервала функция предлагает пользователю выбрать интересующую его страну
    нажав на соответствующую кнопку
    """
    keyboard = None
    if call.data:
        if call.data == '1':
            keyboard = countries_keyboard.create_countries_keyboard(1)
        elif call.data == '2':
            keyboard = countries_keyboard.create_countries_keyboard(2)
        elif call.data == '3':
            keyboard = countries_keyboard.create_countries_keyboard(3)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Какая страна вас интересует?',
                              reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in all_countries.keys())
def set_region_name(call: CallbackQuery):
    """
    Функция предлагает пользователю выбрать интересующий его регион
    нажав на соответствующую кнопку
    """
    country_name = None
    user_id = call.from_user.id
    for key, country in all_countries.items():
        if key == call.data:
            country_name = country
    user_choice[user_id]['country'] = country_name
    logger.info(f'Выбор страны пользователем {user_id}: {country_name}')
    if regions_keyboard.create_regions_keyboard(country_name):
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Какой регион страны вас интересует?',
                              reply_markup=regions_keyboard.create_regions_keyboard(country_name))
    else:
        logger.error(f'Нет списка регионов страны {country_name}')
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='К сожалению страна пока не поддерживается, попробуйте выбрать другую.',
                              reply_markup=countries_keyboard.set_interval())


@bot.callback_query_handler(func=lambda call: call.data in all_regions.keys())
def set_city_name(call: CallbackQuery) -> None:
    """
    Функция предлагает пользователю выбрать интересующий его город
    нажав на соответствующую кнопку
    """
    region_name = None
    user_id = call.from_user.id
    for key, region in all_regions.items():
        if key == call.data:
            region_name = region
    user_choice[user_id]['region'] = region_name
    logger.info(f'Выбор региона пользователем {user_id}: {region_name}')
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Какой город вас интересует?',
                          reply_markup=cities_keyboard.create_cities_keyboard(region_name))


@bot.callback_query_handler(func=lambda call: call.data in all_cities.keys())
def set_transport_type(call: CallbackQuery) -> None:
    """
    Функция предлагает пользователю выбрать интересующий его тип транспорта
    нажав на соответствующую кнопку
    """
    city_name = None
    user_id = call.from_user.id
    for key, city in all_cities.items():
        if key == call.data:
            city_name = city
    user_choice[user_id]['city'] = city_name
    logger.info(f'Выбор города пользователем {user_id}: {city_name}')
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Какой вид транспорта вас интересует?',
                          reply_markup=transport_keyboard.create_transport_keyboard(ALL_DATA, city_name))


@bot.callback_query_handler(func=lambda call: call.data in ['train', 'plane', 'water', 'bus'])
def set_station_name(call: CallbackQuery) -> None:
    """
    Функция предлагает пользователю выбрать интересующую его станцию
    нажав на соответствующую кнопку
    """
    user_id = call.from_user.id
    user_choice[user_id]['transport_type'] = call.data
    stations = None
    logger.info(f'Выбор транспорта пользователем {user_id}: {call.data}')
    if call.data == 'train':
        stations = get_station_in_city(ALL_DATA,
                                       user_choice[user_id]['city'],
                                       'train')
    elif call.data == 'plane':
        stations = get_station_in_city(ALL_DATA,
                                       user_choice[user_id]['city'],
                                       'plane')
    elif call.data == 'water':
        stations = get_station_in_city(ALL_DATA,
                                       user_choice[user_id]['city'],
                                       'water')
    elif call.data == 'bus':
        stations = get_station_in_city(ALL_DATA,
                                       user_choice[user_id]['city'],
                                       'bus')
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Расписание рейсов по какой станции вы хотели бы увидеть?',
                          reply_markup=stations_keyboard.create_stations_keyboard(stations[call.data]))


@bot.callback_query_handler(func=lambda call: call.data in all_stations.keys())
def set_date(call: CallbackQuery) -> None:
    """
    Функция предлагает пользователю выбрать дату на которую требуется вывести расписание
    движения транспорта по выбранной станции
    """
    user_id = call.from_user.id
    station = None
    for key, station_title in all_stations.items():
        if call.data == key:
            station = station_title
    logger.info(f'Выбор станции пользователем {user_id}: {station}')
    user_choice[user_id]['station'] = station
    user_choice[user_id]['station_code'] = call.data
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Укажите дату',
                          reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def get_station_schedule(call: CallbackQuery):
    """
    Функция обрабатывает всю полученную информацию, записывает ее в базу данных для хранения запросов
    и отправляет пользователю сообщение содержащее информацию по его запросу
    """
    user_id = call.from_user.id
    result, key, step = DetailedTelegramCalendar(locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'Выбрать {LSTEP[step]}',
                              reply_markup=key)
    elif result:
        user_choice[user_id]['schedule_date'] = result
        request = InstationRequest(**user_choice[user_id])
        request.save()
        schedule = get_schedule_in_station(user_choice[user_id]['station_code'], result)
        text = schedule_in_station_text(schedule)
        logger.info(f'Выбор даты пользователем {user_id}: {result}')
        text = text.split('*')
        message = ''
        for item in text:
            if len(message) < 4096 and len(message) + len(item) < 4096:
                message += item
                if len(message) + len(item) > 4095:
                    bot.send_message(call.message.chat.id, message, parse_mode='HTML')
            else:
                message = ' '
                continue
