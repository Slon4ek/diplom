import datetime
import json
from typing import Dict

import requests

from config_data.config import (API_YANDEX_URL,
                                API_YANDEX_KEY,
                                STATION_LIST_ENDPOINT,
                                NEAREST_STATION_ENDPOINT,
                                INSTATION_ENDPOINT)


def api_request(endpoint: str, params: Dict | None = None) -> requests.Response:
    if params is None:
        params = dict()
    headers = {'Authorization': API_YANDEX_KEY}
    return requests.get(
        url=f'{API_YANDEX_URL}{endpoint}',
        headers=headers,
        params=params,
        timeout=10
    )


def get_all_data() -> Dict:
    response = api_request(endpoint=STATION_LIST_ENDPOINT)
    if response.status_code == requests.codes.ok:
        return response.json()


def nearest_stations(latitude: float, longitude: float, radius: int, transport_type: str) -> Dict:
    params = {'lat': latitude,
              'lng': longitude,
              'distance': radius,
              'transport_types': transport_type
              }
    response = api_request(endpoint=NEAREST_STATION_ENDPOINT, params=params)
    if response.status_code == requests.codes.ok:
        return response.json()


def get_schedule(station_code: str, date: datetime = datetime.date.today()):
    params = {
        'station': station_code,
        'date': date
    }
    response = api_request(endpoint=INSTATION_ENDPOINT, params=params)
    if response.status_code == requests.codes.ok:
        return response.json()
