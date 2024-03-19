import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_YANDEX_KEY = os.getenv("API_YANDEX_KEY")
API_YANDEX_URL = 'https://api.rasp.yandex.net/'
STATION_LIST_ENDPOINT = 'v3.0/stations_list/'
NEAREST_STATION_ENDPOINT = 'v3.0/nearest_stations/'
FROMTO_ENDPOINT = 'v3.0/search/'
INSTATION_ENDPOINT = 'v3.0/schedule/'
DB_PATH = 'database.db'
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("nearest_station", "Поиск ближайшей станции"),
    ("schedule_between_stations", "Расписание рейсов между станциями"),
    ("in_station", "Расписание рейсов по станции"),
    ("countries", "Список стран"),
    ("regions", "Список регионов"),
    ("cities", "Список городов"),
    ("stations", "Список станций"),
)
