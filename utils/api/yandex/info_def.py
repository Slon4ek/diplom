from typing import Dict

from loguru import logger


@logger.catch
def get_all_countries(obj: Dict) -> Dict:
    """
    Функция возвращает словарь, где ключем является яндекс код страны, а значением название страны
    :param obj: JSON всей информации по станциям
    :return: Dict
    """
    all_countries = {country['codes']['yandex_code']: country['title']
                     for country in obj['countries'] if country['title']}
    sorted_countries = sorted(all_countries.items(), key=lambda x: x[1])

    return dict(sorted_countries)


@logger.catch
def get_all_regions(obj: Dict) -> Dict:
    """
    Функция возвращает словарь всех доступных регионов(ключ - яндекс код, значение - название региона)
    :param obj: JSON всей информации по станциям
    :type obj: Dict
    :return: Словарь всех доступных регионов
    """
    all_regions = {}
    for country in obj['countries']:
        for region in country['regions']:
            if region['codes'] and region['codes']['yandex_code']:
                all_regions[region['codes']['yandex_code']] = region['title']

    sorted_regions = sorted(all_regions.items(), key=lambda x: x[1])
    return dict(sorted_regions)


@logger.catch
def get_all_cities(obj: Dict) -> Dict:
    """
    Функция возвращает словарь всех доступных городов(ключ - яндекс код, значение - название города)
    :param obj: JSON всей информации по станциям
    :type obj: Dict
    :return: Словарь всех доступных городов
    """
    all_cities = {}
    for country in obj['countries']:
        for region in country['regions']:
            for city in region['settlements']:
                if city['codes'] and city['codes']['yandex_code']:
                    all_cities[city['codes']['yandex_code']] = city['title']

    sorted_cities = sorted(all_cities.items(), key=lambda x: x[1])
    return dict(sorted_cities)


@logger.catch
def get_all_stations(obj: Dict) -> Dict:
    """
    Функция возвращает словарь всех доступных станций(ключ - яндекс код, значение - название станции)
    :param obj: JSON всей информации по станциям
    :type obj: Dict
    :return: Словарь всех доступных станций
    """
    all_stations = dict()
    if 'stations' in obj.keys():
        for station in obj['stations']:
            if station['codes']['yandex_code']:
                stations = {station['codes']['yandex_code']: station['title']}
                all_stations.update(stations)
    else:
        for value in obj.values():
            if isinstance(value, dict):
                if get_all_stations(value):
                    all_stations.update(get_all_stations(value))
            if isinstance(value, list):
                for item in value:
                    if get_all_stations(item):
                        all_stations.update(get_all_stations(item))
    return all_stations


@logger.catch
def get_region_in_country(obj: Dict, country_name: str) -> Dict:
    """
    Функция принимает словарь и название страны и возвращает список регионов этой страны
    :param obj: JSON всей информации по станциям
    :type obj: Dict
    :param country_name: название страны
    :type country_name: str
    :return: Dict
    """
    if country_name in obj.values() and 'regions' in obj.keys():
        regions = {region['codes']['yandex_code']: region['title']
                   for region in obj['regions']
                   if region['codes'] and region['codes']['yandex_code']}
        all_regions_in_country = sorted(regions.items(), key=lambda x: x[1])

        return dict(all_regions_in_country)

    else:
        for value in obj.values():
            if isinstance(value, dict):
                if get_region_in_country(value, country_name):
                    return get_region_in_country(value, country_name)
            if isinstance(value, list):
                for item in value:
                    if get_region_in_country(item, country_name):
                        return get_region_in_country(item, country_name)


@logger.catch
def get_city_in_region(obj: Dict, region_name: str) -> Dict:
    """
    Функция принимает словарь и название региона страны и возвращает список городов данного региона
    :param obj: JSON всей информации по станциям
    :type obj: Dict
    :param region_name: название региона
    :type region_name: str
    :return: Dict
    """
    if region_name in obj.values() and 'settlements' in obj.keys():
        cities = {city['codes']['yandex_code']: city['title']
                  for city in obj['settlements']
                  if city['codes'] and city['codes']['yandex_code']}
        all_cities_in_region = sorted(cities.items(), key=lambda x: x[1])
        return dict(all_cities_in_region)
    else:
        for value in obj.values():
            if isinstance(value, dict):
                if get_city_in_region(value, region_name):
                    return get_city_in_region(value, region_name)
            if isinstance(value, list):
                for item in value:
                    if get_city_in_region(item, region_name):
                        return get_city_in_region(item, region_name)


@logger.catch
def get_station_in_city(obj: Dict, city_name: str, transport_type: str | None = None) -> Dict:
    """
    Функция принимает словарь и название города и возвращает словарь всех станций этого города
    где ключем является тип транспорта, а значение - список названий станций.
    Если передан параметр transport_type, то функция возвращает только станции для указанного транспорта
    :param obj: JSON всей информации по станциям
    :type obj: Dict
    :param city_name: название города
    :type city_name: str
    :param transport_type: название транспорта(необязательный параметр)
    :type transport_type: str | None
    :return: Dict
    """
    if city_name in obj.values() and 'stations' in obj.keys():
        if transport_type:
            station_dict = dict()
            stations_list = [{'Станция': station['title'], 'Код станции': station['codes']['yandex_code']}
                             for station in obj['stations']
                             if station['transport_type'] == transport_type]
            station_dict[transport_type] = stations_list
            return station_dict
        else:
            transport_types = ['plane', 'bus', 'train', 'water']
            station_dict = {t_type: [{'Станция': station['title'], 'Код станции': station['codes']['yandex_code']}
                                     for station in obj['stations']
                                     if station['transport_type'] == t_type]
                            for t_type in transport_types}
            return station_dict
    else:
        for value in obj.values():
            if isinstance(value, dict):
                if get_station_in_city(value, city_name, transport_type):
                    return get_station_in_city(value, city_name, transport_type)
            if isinstance(value, list):
                for item in value:
                    if get_station_in_city(item, city_name, transport_type):
                        return get_station_in_city(item, city_name, transport_type)


@logger.catch
def nearest_station_text(obj: Dict) -> str:
    """
    Функция принимает объект(словарь станций) и возвращает стоку содержащую название станции, тип станции и расстояние
    до этой станции
    :param obj: JSON всей информации по станциям
    :type obj: Dict
    :return: str
    """
    text = ''
    for item in obj['stations']:
        text += (f'"{item['title']}":\n\t\t\t'
                 f'Тип станции: {item['station_type_name']}\n\t\t\t'
                 f'Расстояние до станции: {round(item['distance'])}км\n'
                 f'{'-' * 60}\n\n')
    return text


@logger.catch
def schedule_in_station_text(obj: Dict) -> str:
    """
    Функция возвращает расписание движения транспорта
    :param obj: JSON всей информации по станциям
    :return: текст
    """
    try:
        schedule_text = (f'<b>Выбранная дата:</b> <i>{obj['date']}</i>\n'
                         f'<b>Информация о станции:</b>\n'
                         f'\t\t<b>Название станции:</b> <i>{obj['station']['title']}</i>\n'
                         f'\t\t<b>Тип станции:</b> <i>{obj['station']['station_type_name']}</i>\n'
                         f'<b><u>Расписание движения транспорта:</u></b>\n\n')
        for item in obj['schedule']:
            if item['departure']:
                departure = (f'\t >> <i>Время: {item['departure'][14:19]}</i>\n'
                             f'\t >> <i>Часовой пояс: {item['departure'][19:]}</i>\n')
            else:
                departure = f'\t >> Не определено\n'
            schedule_text += (f'\t >> <b>Номер рейса:</b> <i>{item['thread']['number']}</i>\n'
                              f'\t >> <b>Направление:</b> <i>{item['thread']['title']}</i>\n'
                              f'\t >> <b>Перевозчик:</b> <i>{item['thread']['carrier']['title']}</i>\n'
                              f'\t >> <b>Время отправления:</b>\n{departure}'
                              f'\t >> <b>Дни курсирования:</b> <i>{item['days']}</i>\n'
                              f'{'-' * 75}\n*')

        return schedule_text
    except TypeError:
        return 'Что-то пошло не так, видимо в системе Яндекс Расписаний нет информации по вашему запросу :('


@logger.catch
def get_transport(obj: Dict, city_name: str) -> set:
    """
    Функция возвращает виды транспорта доступного в выбранном городе
    :param obj: JSON всей информации по станциям
    :param city_name: название города
    :return: set
    """
    if city_name in obj.values() and 'stations' in obj.keys():
        transport_types = [station['transport_type']
                           for station in obj['stations']]
        return set(transport_types)
    else:
        for value in obj.values():
            if isinstance(value, dict):
                if get_transport(value, city_name):
                    return get_transport(value, city_name)
            if isinstance(value, list):
                for item in value:
                    if get_transport(item, city_name):
                        return get_transport(item, city_name)


@logger.catch
def get_transport_between_stations(obj: Dict) -> set:
    """
    Функция возвращает список доступного транспорта между выбранными пунктами
    :param obj: JSON объект содержащий всю информацию о доступных рейсах между выбранными пунктами
    :return: set доступных видов транспорта
    """
    transport_types = []
    for segment in obj['segments']:
        transport_types.append(segment['from']['transport_type'])
        transport_types.append(segment['to']['transport_type'])

    return set(transport_types)


@logger.catch
def schedule_between_station_text(obj: Dict) -> str:
    """
    Функция возвращает в текстовом виде информацию по рейсам между выбранными пунктами
    :param obj: JSON объект содержащий всю информацию о доступных рейсах между выбранными пунктами
    :return: текст расписания
    """
    text = (f'<b>Выбранная дата:</b> <i>{obj['search']['date']}</i>\n'
            f'<b>Пункт отправления:</b> <i>{obj['search']['from']['title']}</i>\n'
            f'<b>Пункт прибытия:</b> <i>{obj['search']['to']['title']}</i>\n'
            f'<b>Расписание:</b>\n\n')

    for segment in obj['segments']:
        travel_time = (f'{str(int(segment['duration']) // 3600)}ч. '
                       f'{str(round((int(segment['duration']) % 3600) / 60))}мин.')
        departure_time = (f'\t >> <i>Время: {segment['departure'][11:19]}</i>\n'
                          f'\t >> <i>Часовой пояс: {segment['departure'][19:]}</i>\n')
        arrival_time = (f'\t >> <i>Время: {segment['arrival'][11:19]}</i>\n'
                        f'\t >> <i>Часовой пояс: {segment['arrival'][19:]}</i>\n')
        text += (f'<b>Номер рейса:</b> {segment['thread']['number']}\n'
                 f'<b>Направление:</b> {segment['thread']['title']}\n'
                 f'<b>Перевозчик:</b> {segment['thread']['carrier']['title']}\n'
                 f'<b>Название транспортного средства:</b> {segment['thread']['vehicle']}\n'
                 f'<b>Станция отправления:</b> {segment['from']['title']}\n'
                 f'<b>Станция прибытия:</b> {segment['to']['title']}\n'
                 f'<b>Время в пути:</b> {travel_time}\n'
                 f'<b>Время отправления:</b>\n{departure_time}'
                 f'<b>Время прибытия:</b>\n{arrival_time}'
                 f'{'-' * 75}\n*')
    return text
