import datetime
from typing import Dict, Any

import requests
from loguru import logger

from config_data.config import (API_YANDEX_URL, API_YANDEX_KEY, STATION_LIST_ENDPOINT,
                                NEAREST_STATION_ENDPOINT, INSTATION_ENDPOINT, FROMTO_ENDPOINT)


@logger.catch
def api_request(endpoint: str, params: Dict | None = None) -> requests.Response:
    """
    Функция для запроса к API Яндекс Расписаний
    :param endpoint: эндпоинт к основной ссылке
    :param params: словарь параметров в зависимости от эндпоинта
    :return: запрос
    """
    if params is None:
        params = dict()
    headers = {'Authorization': API_YANDEX_KEY}
    return requests.get(
        url=f'{API_YANDEX_URL}{endpoint}',
        headers=headers,
        params=params,
        timeout=10
    )


@logger.catch
def get_all_data() -> Dict:
    """
    Функция-запрос возвращает полный список станций, информацию о которых предоставляют Яндекс Расписания.
    Список структурирован географически: ответ содержит список стран со вложенными списками регионов и
    населенных пунктов, в которых находятся станции.
    :return: JSON
    """
    response = api_request(endpoint=STATION_LIST_ENDPOINT)
    logger.info(f'Запрос к {API_YANDEX_URL}{STATION_LIST_ENDPOINT}. Status code: {response.status_code}')
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        logger.error(f'Status code: {response.status_code}')


@logger.catch
def get_nearest_stations(latitude: float, longitude: float, radius: int, transport_type: str) -> Dict:
    """
    Функция-запрос позволяет получить список станций, находящихся в указанном радиусе от указанной точки.
    Максимальное количество возвращаемых станций — 50.
    Точка определяется географическими координатами (широтой и долготой) согласно WGS84
    :param latitude: широта
    :param longitude: долгота
    :param radius: радиус поиска
    :param transport_type: тип транспорта
    :return: JSON
    """
    params = {'lat': latitude,
              'lng': longitude,
              'distance': radius,
              'transport_types': transport_type
              }
    response = api_request(endpoint=NEAREST_STATION_ENDPOINT, params=params)
    logger.info(f'Запрос к {API_YANDEX_URL}{NEAREST_STATION_ENDPOINT}. Status code: {response.status_code}')
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        logger.error(f'Status code: {response.status_code}')


@logger.catch
def get_schedule_in_station(station_code: str, date: datetime = datetime.date.today()) -> Dict:
    """
    Функция-запрос позволяет получить список рейсов, отправляющихся от указанной станции
    и информацию по каждому рейсу.
    :param station_code: Код станции в системе кодирования Яндекс Расписаний
    :param date: дата на которую нужно запросить расписание, по умолчанию - текущая дата
    :return: JSON
    """
    params = {
        'station': station_code,
        'date': date
    }
    response = api_request(endpoint=INSTATION_ENDPOINT, params=params)
    logger.info(f'Запрос к {API_YANDEX_URL}{INSTATION_ENDPOINT}. Status code: {response.status_code}')
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        logger.error(f'Status code: {response.status_code}')


@logger.catch
def get_schedule_between_stations(departure_code: str, arrival_code: str,
                                  date: datetime = datetime.date.today(),
                                  transport_type: str | None = None) -> Dict:
    """
    Функция-запрос позволяет получить список рейсов, следующих от указанной станции отправления к указанной
    станции прибытия и информацию по каждому рейсу
    :param departure_code: Код станции отправления в системе Яндекс расписаний
    :param arrival_code: Код станции прибытия в системе Яндекс расписаний
    :param date: Дата, на которую необходимо получить список рейсов
    :param transport_type: Тип транспортного средства
    :return: JSON
    """
    params = {
        'from': departure_code,
        'to': arrival_code,
        'date': date,
        'transport_types': transport_type
    }
    response = api_request(endpoint=FROMTO_ENDPOINT, params=params)
    logger.info(f'Запрос к {API_YANDEX_URL}{FROMTO_ENDPOINT}. Status code: {response.status_code}')
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        logger.error(f'Status code: {response.status_code}')


ALL_DATA = get_all_data()
