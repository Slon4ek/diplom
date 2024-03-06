from typing import Dict

import requests

from config_data.config import (API_YANDEX_URL,
                                API_YANDEX_KEY,
                                STATION_LIST_ENDPOINT)


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


def get_all_stations() -> Dict:
    response = api_request(endpoint=STATION_LIST_ENDPOINT)
    if response.status_code == requests.codes.ok:
        return response.json()
