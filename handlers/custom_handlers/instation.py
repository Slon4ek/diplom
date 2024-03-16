from telebot.types import CallbackQuery, Message
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from config_data.api_config import get_schedule
from database.database_class import User, InstationRequest
from keyboards.inline import (countries_keyboard, regions_keyboard,
                              cities_keyboard, transport_keyboard, stations_keyboard)
from loader import bot
from utils.api.yandex.info_def import *

all_data = get_all_data()
all_countries = get_all_countries(all_data)
all_regions = get_all_regions(all_data)
all_cities = get_all_cities(all_data)
all_stations = get_all_stations(all_data)
user_choice = dict()


@bot.message_handler(commands=['instation'])
def select_country(message: Message) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, 'Вы не зарегистрированы, введите команду /start')
        return

    bot.send_message(user_id, 'В этом разделе вы можете посмотреть расписание '
                              'движения транспорта по выбранной станции',
                     reply_markup=countries_keyboard.set_interval())
    user_choice[user_id] = dict()
    user_choice[user_id] = {'user_id': user_id}


@bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3'])
def select_country(call: CallbackQuery) -> None:
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
def select_region(call: CallbackQuery):
    country_name = None
    user_id = call.from_user.id
    for key, country in all_countries.items():
        if key == call.data:
            country_name = country
    user_choice[user_id]['country'] = country_name
    if regions_keyboard.create_regions_keyboard(country_name):
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Какой регион страны вас интересует?',
                              reply_markup=regions_keyboard.create_regions_keyboard(country_name))
    else:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='К сожалению страна пока не поддерживается, попробуйте выбрать другую.',
                              reply_markup=countries_keyboard.set_interval())


@bot.callback_query_handler(func=lambda call: call.data in all_regions.keys())
def select_city(call: CallbackQuery) -> None:
    region_name = None
    user_id = call.from_user.id
    for key, region in all_regions.items():
        if key == call.data:
            region_name = region
    user_choice[user_id]['region'] = region_name
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Какой город вас интересует?',
                          reply_markup=cities_keyboard.create_cities_keyboard(region_name))


@bot.callback_query_handler(func=lambda call: call.data in all_cities.keys())
def select_transport(call: CallbackQuery) -> None:
    city_name = None
    user_id = call.from_user.id
    for key, city in all_cities.items():
        if key == call.data:
            city_name = city
    user_choice[user_id]['city'] = city_name
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Какой вид транспорта вас интересует?',
                          reply_markup=transport_keyboard.create_transport_keyboard(all_data, city_name))


@bot.callback_query_handler(func=lambda call: call.data in ['train', 'plane', 'water', 'bus'])
def select_transport(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    user_choice[user_id]['transport_type'] = call.data
    stations = None
    if call.data == 'train':
        stations = get_station_list(all_data,
                                    user_choice[user_id]['city'],
                                    'train')
    elif call.data == 'plane':
        stations = get_station_list(all_data,
                                    user_choice[user_id]['city'],
                                    'plane')
    elif call.data == 'water':
        stations = get_station_list(all_data,
                                    user_choice[user_id]['city'],
                                    'water')
    elif call.data == 'bus':
        stations = get_station_list(all_data,
                                    user_choice[user_id]['city'],
                                    'bus')
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Расписание рейсов по какой станции вы хотели бы увидеть?',
                          reply_markup=stations_keyboard.create_stations_keyboard(stations[call.data]))


@bot.callback_query_handler(func=lambda call: call.data in all_stations.keys())
def set_date(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    station = None
    for key, station_title in all_stations.items():
        if call.data == key:
            station = station_title
    user_choice[user_id]['station'] = station
    user_choice[user_id]['station_code'] = call.data
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Укажите дату',
                          reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def date(call: CallbackQuery):
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
        schedule = get_schedule(user_choice[user_id]['station_code'], result)
        text = schedule_in_station(schedule)
        if text:
            if len(text) > 4096:
                for message in range(0, len(text), 4096):
                    bot.send_message(call.message.chat.id, '{}'.format(text[message: message + 4096]))
            else:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=text)
