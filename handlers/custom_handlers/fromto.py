import peewee
from loguru import logger
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from config_data.api_config import ALL_DATA, get_schedule_between_stations
from database.database_class import User, FromToRequest
from keyboards.inline.transport_keyboard import keyboard_for_schedule_between_stations
from loader import bot
from states.from_to_states import FromTo
from utils.api.yandex.info_def import get_all_cities, get_all_stations, schedule_between_station_text

all_cities = get_all_cities(ALL_DATA)
all_stations = get_all_stations(ALL_DATA)


@bot.message_handler(state='*', commands=['schedule_between_stations'])
def set_departure_point(message: Message) -> None:
    """
    Функция для обработки команды /schedule_between_stations
    :param message: /schedule_between_stations
    :return: None
    """
    user_id = message.from_user.id
    logger.info(f'Пользователь {message.from_user.id} запустил команду /schedule_between_stations')
    if User.get_or_none(User.user_id == message.from_user.id) is None:
        bot.reply_to(message, 'Вы не зарегистрированы, введите команду /start')
        return

    bot.send_message(user_id, 'В этом разделе вы можете посмотреть расписание '
                              'движения транспорта между указанными городами/станциями.\n'
                              'Пожалуйста введите пункт отправления (название'
                              'города или станции).\nУчтите что название города и название станции'
                              'могут быть одинаковыми, поэтому напишите что конкретно вас интересует.\n'
                              '<i>Например: "Город Москва" или "Станция Шереметьево"</i>',
                     parse_mode='HTML')
    bot.set_state(user_id, FromTo.departure)


@bot.message_handler(state=FromTo.departure)
def get_departure_code(message: Message) -> None:
    """
    Функция принимает от пользователя название города или станции отправления и записывает код в
    системе Яндекс расписаний
    :param message: город или станция отправления
    :return: None
    """
    user_id = message.from_user.id
    logger.info(f'Пользователь {user_id} ввел текст: "{message.text}"')
    message_split = message.text.lower().split(' ')
    if 'город' in message_split:
        for code, title in all_cities.items():
            if title.lower() in message_split:
                with bot.retrieve_data(user_id) as data:
                    data['from_city'] = title
                    data['from_code'] = code
    elif 'станция' in message_split:
        for code, title in all_cities.items():
            if title.lower() in message_split:
                with bot.retrieve_data(user_id) as data:
                    data['from_station'] = title
                    data['from_code'] = code
    else:
        bot.send_message(user_id, 'Не удалось получить код пункта отправления. '
                                  'Пожалуйста введите еще раз в соответствии с примером.\n'
                                  'Пример: <i>"Город Москва" или "Станция Шереметьево"</i>',
                         parse_mode='HTML')
        logger.error(f'Неверный ввод: "{message.text}"')
        return

    bot.send_message(user_id, 'Отлично, код пункта отправления получен. Теперь введите пункт назначения. '
                              'Нет, это не название фильма ;)\n'
                              'Формат тот же что и в пункте отправления.\n'
                              'Пример: <i>"Город Москва" или "Станция Шереметьево"</i>',
                     parse_mode='HTML')
    bot.set_state(user_id, FromTo.arrival)


@bot.message_handler(state=FromTo.arrival)
def set_arrival_point(message: Message) -> None:
    """
    Функция принимает от пользователя название города или станции прибытия и записывает код в
    системе Яндекс расписаний
    :param message: город или станция прибытия
    :return: None
    """
    user_id = message.from_user.id
    logger.info(f'Пользователь {user_id} ввел текст: "{message.text}"')
    message_split = message.text.lower().split(' ')
    if 'город' in message_split:
        for code, title in all_cities.items():
            if title.lower() in message_split:
                with bot.retrieve_data(user_id) as data:
                    data['to_city'] = title
                    data['to_code'] = code
    elif 'станция' in message_split:
        for code, title in all_cities.items():
            if title.lower() in message_split:
                with bot.retrieve_data(user_id) as data:
                    data['to_station'] = title
                    data['to_code'] = code
    else:
        bot.send_message(user_id, 'Не удалось получить код пункта назначения. '
                                  'Пожалуйста введите еще раз в соответствии с примером.\n'
                                  'Пример: <i>"Город Москва" или "Станция Шереметьево"</i>',
                         parse_mode='HTML')
        logger.error(f'Неверный ввод: "{message.text}"')
        return
    bot.set_state(user_id, FromTo.date)
    calendar, step = DetailedTelegramCalendar(locale='ru', calendar_id=2).build()
    bot.send_message(user_id, 'Отлично, код пункта назначения получен, теперь давайте '
                              'интересующую вас дату', reply_markup=calendar)


@bot.callback_query_handler(state=FromTo.date, func=DetailedTelegramCalendar.func(calendar_id=2))
def set_date(call: CallbackQuery) -> None:
    """
    Выбор интересующей даты. После выбора даты, идет запрос к сервису Яндекс расписаний и
    выводится клавиатура с видами транспорта доступного для поездки между выбранными пунктами.
    :return: None
    """
    user_id = call.from_user.id
    result, key, step = DetailedTelegramCalendar(locale='ru', calendar_id=2).process(call.data)
    if not result:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'Выбрать {LSTEP[step]}',
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(user_id) as data:
            data['schedule_date'] = result
        bot.set_state(user_id, FromTo.transport)
        schedule_between_stations = get_schedule_between_stations(departure_code=data['from_code'],
                                                                  arrival_code=data['to_code'],
                                                                  date=data['schedule_date'])
        logger.info(f'Пользователь {user_id} выбрал дату {result}')

        if schedule_between_stations['segments']:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Отлично. Осталось выбрать транспорт который вас интересует. '
                                       'Вот список транспорта который доступен для путешествия между выбранными '
                                       'пунктами:',
                                  reply_markup=keyboard_for_schedule_between_stations(schedule_between_stations))
        else:
            bot.send_message(user_id, 'Не удалось найти транспорт для путешествия между выбранными '
                                      'пунктами.')
            bot.delete_state(user_id)


@logger.catch
@bot.callback_query_handler(state=FromTo.transport, func=lambda call: call.data in ['Train', 'Plane', 'Water', 'Bus'])
def show_schedule_between_stations(call: CallbackQuery) -> None:
    """
    Функция принимает вид транспорта, записывает всю полученную информацию в БД,
    делает запрос к сервису Яндекс расписаний и выводит результат пользователю.
    :param call:
    :return:
    """
    user_id = call.from_user.id
    logger.info(f'Пользователь {user_id} выбрал транспорт {call.data}')
    with bot.retrieve_data(user_id) as data:
        data['transport_type'] = call.data.lower()
        data['user_id'] = user_id

    try:
        request = FromToRequest(**data)
        request.save()
    except peewee.IntegrityError as exc:
        logger.error(f'Ошибка записи в бд: {exc}')
    schedule = get_schedule_between_stations(departure_code=data['from_code'],
                                             arrival_code=data['to_code'],
                                             date=data['schedule_date'],
                                             transport_type=data['transport_type'])
    all_text = schedule_between_station_text(schedule)
    text = all_text.split('*')
    if len(all_text) < 4096:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='\n'.join(text),
                              parse_mode='HTML')
        bot.send_message(user_id, f'Найдено {len(text) - 1} рейсов соответствующих указанным данным')
    else:
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        message = ''
        for item in text:
            if len(message) + len(item) < 4096:
                message += item
            else:
                bot.send_message(user_id, message, parse_mode='HTML')
                message = item
        else:
            if len(message) > 0:
                bot.send_message(user_id, message, parse_mode='HTML')
                bot.send_message(user_id, f'Найдено {len(text) - 1} рейсов соответствующих указанным данным')
    bot.delete_state(user_id)
