from typing import Dict

from config_data.api_config import get_all_data

all_data = get_all_data()


def get_all_countries(obj: Dict) -> Dict:
    """
    Функция возвращает словарь, где ключем является яндекс код страны, а значением название страны
    :param obj: словарь всех станций
    :return: Dict
    """
    all_countries = {country['codes']['yandex_code']: country['title']
                     for country in obj['countries'] if country['title']}
    sorted_countries = sorted(all_countries.items(), key=lambda x: x[1])

    return dict(sorted_countries)


def get_all_regions(obj: Dict) -> Dict:
    """
    Функция возвращает словарь всех доступных регионов(ключ - яндекс код, значение - название региона)
    :param obj: словарь всех станций
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


def get_all_cities(obj: Dict) -> Dict:
    """
    Функция возвращает словарь всех доступных городов(ключ - яндекс код, значение - название города)
    :param obj: словарь всех станций
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


def get_all_stations(obj: Dict) -> Dict:
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


def get_region_list(obj: Dict, country_name: str) -> Dict:
    """
    Функция принимает словарь и название страны и возвращает список регионов этой страны
    :param obj: словарь всех станций
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
                if get_region_list(value, country_name):
                    return get_region_list(value, country_name)
            if isinstance(value, list):
                for item in value:
                    if get_region_list(item, country_name):
                        return get_region_list(item, country_name)


def get_city_list(obj: Dict, region_name: str) -> Dict:
    """
    Функция принимает словарь и название региона страны и возвращает список городов данного региона
    :param obj: словарь всех станций
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
                if get_city_list(value, region_name):
                    return get_city_list(value, region_name)
            if isinstance(value, list):
                for item in value:
                    if get_city_list(item, region_name):
                        return get_city_list(item, region_name)


def get_station_list(obj: Dict, city_name: str, transport_type: str | None = None) -> Dict:
    """
    Функция принимает словарь и название города и возвращает словарь всех станций этого города
    где ключем является тип транспорта, а значение - список названий станций.
    Если передан параметр transport_type, то функция возвращает только станции для указанного транспорта
    :param obj: словарь всех станций
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
                if get_station_list(value, city_name, transport_type):
                    return get_station_list(value, city_name, transport_type)
            if isinstance(value, list):
                for item in value:
                    if get_station_list(item, city_name, transport_type):
                        return get_station_list(item, city_name, transport_type)


def get_nearest_station(obj: Dict) -> str:
    """
    Функция принимает объект(словарь станций) и возвращает стоку содержащую название станции, тип станции и расстояние
    до этой станции
    :param obj: словарь всех станций
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


def schedule_in_station(obj: Dict) -> str:
    try:
        schedule_text = (f'Выбранная дата: {obj['date']}\n'
                         f'Информация о станции:\n'
                         f'\t\t__Название станции: {obj['station']['title']}__\n'
                         f'\t\t__Тип станции: {obj['station']['station_type_name']}__\n'
                         f'Расписание движения транспорта:\n\n')
        for item in obj['schedule']:
            if item['departure']:
                departure = (f'\t >> Дата: {item['departure'][:10]}\n'
                             f'\t >> Время: {item['departure'][14:19]}\n'
                             f'\t >> Часовой пояс: {item['departure'][19:]}\n')
            else:
                departure = f'\t >> Не определено\n'
            schedule_text += (f'\t >> Номер: {item['thread']['number']}\n'
                              f'\t >> Направление: {item['thread']['title']}\n'
                              f'\t >> Перевозчик: {item['thread']['carrier']['title']}\n'
                              f'\t >> Время отправления: \n{departure}'
                              f'\t >> Дни курсирования: {item['days']}\n'
                              f'{'-'*75}\n\n')

        return schedule_text
    except TypeError:
        return 'Что-то пошло не так, видимо Яндекс пока не знает расписания по вашему запросу :('


def get_transport(obj, city_name):
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
