from typing import Dict, List


def get_country_list(obj: Dict) -> List:
    """
    Функция возвращает список стран из словаря
    :param obj: словарь всех станций
    :type obj: Dict
    :return: List
    """
    return [country['title'] for country in obj['countries'] if country['title']]


def get_region_list(obj: Dict, country_name: str) -> List:
    """
    Функция принимает словарь и название страны и возвращает список регионов этой страны
    :param obj: словарь всех станций
    :type obj: Dict
    :param country_name: название страны
    :type country_name: str
    :return: List
    """
    if country_name in obj.values() and 'regions' in obj.keys():
        return [region['title'] for region in obj['regions'] if region['title']]
    else:
        for value in obj.values():
            if isinstance(value, dict):
                if get_region_list(value, country_name):
                    return get_region_list(value, country_name)
            if isinstance(value, list):
                for item in value:
                    if get_region_list(item, country_name):
                        return get_region_list(item, country_name)


def get_city_list(obj: Dict, region_name: str) -> List:
    """
    Функция принимает словарь и название региона страны и возвращает список городов данного региона
    :param obj: словарь всех станций
    :type obj: Dict
    :param region_name: название региона
    :type region_name: str
    :return: List
    """
    if region_name in obj.values() and 'settlements' in obj.keys():
        return [city['title'] for city in obj['settlements'] if city['title']]
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


def get_code(obj: Dict, search_name: str) -> str:
    """
    Функция принимает словарь и название города или станции и возвращает его код в системе
    кодирования Яндекс Расписаний
    :param search_name: название города или станции
    :type search_name: str
    :param obj: словарь всех станций
    :type obj: Dict
    :return: str
    """
    if search_name.title() in obj.values():
        return obj['codes']['yandex_code']
    else:
        for value in obj.values():
            if isinstance(value, dict):
                if get_code(value, search_name):
                    return get_code(value, search_name)
            if isinstance(value, list):
                for item in value:
                    if get_code(item, search_name):
                        return get_code(item, search_name)


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
