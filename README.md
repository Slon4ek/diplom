### Телеграм Бот для работы с API Яндекс расписаний

#### Возможности бота
1. Вывод расписания рейсов между станциями
2. Вывод расписания рейсов по станции

#### Команды бота
1. /countries - показать список доступных стран
2. /regions - показать список регионов выбранной страны
3. /cities - показать список городов выбранного региона
4. /stations - показать список станций выбранного города
5. /fromto - показать расписание транспорта от станции А до станции Б
6. /instation - показать расписание транспорта по станции

#### Основная ссылка
- https://api.rasp.yandex.net/

#### Эндпоинты
1. v3.0/search/ - расписание рейсов между станциями
2. v3.0/schedule/ - расписание рейсов по станции
3. v3.0/stations_list/ - список всех доступных станций

### Примеры запросов к API
### Расписание рейсов между станциями:
`https://api.rasp.yandex.net/v3.0/search/?apikey={ключ}&from=s9623358&to=s9600213&date=2024-03-05`

#### Синтаксис запроса:
```commandline
https://api.rasp.yandex.net/v3.0/search/?
  apikey=<ключ>
& from=<код станции отправления>
& to=<код станции прибытия>
& [transport_types=<тип транспорта>]
```

#### Пример ответа:
```JSON
{
    "search": {
        "from": {
            "type": "station",
            "title": "Чебоксары",
            "short_title": "",
            "popular_title": "",
            "code": "s9623358",
            "station_type": "airport",
            "station_type_name": "аэропорт",
            "transport_type": "plane"
        },
        "to": {
            "type": "station",
            "title": "Шереметьево",
            "short_title": null,
            "popular_title": null,
            "code": "s9600213",
            "station_type": "airport",
            "station_type_name": "аэропорт",
            "transport_type": "plane"
        },
        "date": "2024-03-05"
    },
    "segments": [
        {
            "thread": {
                "number": "DP 6808",
                "title": "Чебоксары — Москва",
                "short_title": "Чебоксары — Москва",
                "carrier": {
                    "code": 9144,
                    "title": "Победа",
                    "codes": {
                        "sirena": "ДР",
                        "iata": "DP",
                        "icao": null
                    },
                    "address": null,
                    "url": "https://pobeda.aero/",
                    "email": null,
                    "contacts": "115114 Москва, ул. Кожевническая, д.7, стр.1.\r\nТелефон колл-центра 8 (809) 505-47-77. Цена от 55 руб. до 60 руб. 17 коп./минута, не включая НДС, в зависимости от региона и оператора (по данным на ноябрь 2014). \r\nДля звонков не из России: +7 (499) 215-23-00 (тарифицируется оператором как междугородный звонок).",
                    "phone": "",
                    "logo": "https://yastat.net/s3/rasp/media/data/company/logo/ru_2.png",
                    "logo_svg": "https://yastat.net/s3/rasp/media/data/company/svg/pobeda_ak.svg"
                },
                "vehicle": "Boeing 737-800",
                "express_type": null,
                "transport_type": "plane",
                "transport_subtype": {
                    "title": null,
                    "code": null,
                    "color": null
                },
                "uid": "DP-6808_240305_c9144_12",
                "thread_method_link": "api.rasp.yandex.net/v3/thread/?date=2024-03-05&uid=DP-6808_240305_c9144_12"
            },
            "from": {
                "type": "station",
                "title": "Чебоксары",
                "short_title": "",
                "popular_title": "",
                "code": "s9623358",
                "station_type": "airport",
                "station_type_name": "аэропорт",
                "transport_type": "plane"
            },
            "to": {
                "type": "station",
                "title": "Шереметьево",
                "short_title": null,
                "popular_title": null,
                "code": "s9600213",
                "station_type": "airport",
                "station_type_name": "аэропорт",
                "transport_type": "plane"
            },
            "departure_platform": "",
            "arrival_platform": "",
            "departure_terminal": "",
            "arrival_terminal": "B",
            "stops": "",
            "duration": 5700.0,
            "start_date": "2024-03-05",
            "departure": "2024-03-05T10:55:00+03:00",
            "arrival": "2024-03-05T12:30:00+03:00",
            "has_transfers": false,
            "tickets_info": {
                "et_marker": false,
                "places": []
            }
        },
        {
            "thread": {
                "number": "DP 6818",
                "title": "Чебоксары — Москва",
                "short_title": "Чебоксары — Москва",
                "carrier": {
                    "code": 9144,
                    "title": "Победа",
                    "codes": {
                        "sirena": "ДР",
                        "iata": "DP",
                        "icao": null
                    },
                    "address": null,
                    "url": "https://pobeda.aero/",
                    "email": null,
                    "contacts": "115114 Москва, ул. Кожевническая, д.7, стр.1.\r\nТелефон колл-центра 8 (809) 505-47-77. Цена от 55 руб. до 60 руб. 17 коп./минута, не включая НДС, в зависимости от региона и оператора (по данным на ноябрь 2014). \r\nДля звонков не из России: +7 (499) 215-23-00 (тарифицируется оператором как междугородный звонок).",
                    "phone": "",
                    "logo": "https://yastat.net/s3/rasp/media/data/company/logo/ru_2.png",
                    "logo_svg": "https://yastat.net/s3/rasp/media/data/company/svg/pobeda_ak.svg"
                },
                "vehicle": "Boeing 737-800",
                "express_type": null,
                "transport_type": "plane",
                "transport_subtype": {
                    "title": null,
                    "code": null,
                    "color": null
                },
                "uid": "DP-6818_240305_c9144_12",
                "thread_method_link": "api.rasp.yandex.net/v3/thread/?date=2024-03-05&uid=DP-6818_240305_c9144_12"
            },
            "from": {
                "type": "station",
                "title": "Чебоксары",
                "short_title": "",
                "popular_title": "",
                "code": "s9623358",
                "station_type": "airport",
                "station_type_name": "аэропорт",
                "transport_type": "plane"
            },
            "to": {
                "type": "station",
                "title": "Шереметьево",
                "short_title": null,
                "popular_title": null,
                "code": "s9600213",
                "station_type": "airport",
                "station_type_name": "аэропорт",
                "transport_type": "plane"
            },
            "departure_platform": "",
            "arrival_platform": "",
            "departure_terminal": "",
            "arrival_terminal": "B",
            "stops": "",
            "duration": 6000.0,
            "start_date": "2024-03-05",
            "departure": "2024-03-05T17:50:00+03:00",
            "arrival": "2024-03-05T19:30:00+03:00",
            "has_transfers": false,
            "tickets_info": {
                "et_marker": false,
                "places": []
            }
        },
        {
            "thread": {
                "number": "DP 6816",
                "title": "Чебоксары — Москва",
                "short_title": "Чебоксары — Москва",
                "carrier": {
                    "code": 9144,
                    "title": "Победа",
                    "codes": {
                        "sirena": "ДР",
                        "iata": "DP",
                        "icao": null
                    },
                    "address": null,
                    "url": "https://pobeda.aero/",
                    "email": null,
                    "contacts": "115114 Москва, ул. Кожевническая, д.7, стр.1.\r\nТелефон колл-центра 8 (809) 505-47-77. Цена от 55 руб. до 60 руб. 17 коп./минута, не включая НДС, в зависимости от региона и оператора (по данным на ноябрь 2014). \r\nДля звонков не из России: +7 (499) 215-23-00 (тарифицируется оператором как междугородный звонок).",
                    "phone": "",
                    "logo": "https://yastat.net/s3/rasp/media/data/company/logo/ru_2.png",
                    "logo_svg": "https://yastat.net/s3/rasp/media/data/company/svg/pobeda_ak.svg"
                },
                "vehicle": "Boeing 737-800",
                "express_type": null,
                "transport_type": "plane",
                "transport_subtype": {
                    "title": null,
                    "code": null,
                    "color": null
                },
                "uid": "DP-6816_240305_c9144_12",
                "thread_method_link": "api.rasp.yandex.net/v3/thread/?date=2024-03-05&uid=DP-6816_240305_c9144_12"
            },
            "from": {
                "type": "station",
                "title": "Чебоксары",
                "short_title": "",
                "popular_title": "",
                "code": "s9623358",
                "station_type": "airport",
                "station_type_name": "аэропорт",
                "transport_type": "plane"
            },
            "to": {
                "type": "station",
                "title": "Шереметьево",
                "short_title": null,
                "popular_title": null,
                "code": "s9600213",
                "station_type": "airport",
                "station_type_name": "аэропорт",
                "transport_type": "plane"
            },
            "departure_platform": "",
            "arrival_platform": "",
            "departure_terminal": "",
            "arrival_terminal": "B",
            "stops": "",
            "duration": 6000.0,
            "start_date": "2024-03-05",
            "departure": "2024-03-05T21:50:00+03:00",
            "arrival": "2024-03-05T23:30:00+03:00",
            "has_transfers": false,
            "tickets_info": {
                "et_marker": false,
                "places": []
            }
        }
    ],
    "interval_segments": [],
    "pagination": {
        "total": 3,
        "limit": 100,
        "offset": 0
    }
}
```



### Расписание рейсов по станции:
`https://api.rasp.yandex.net/v3.0/schedule/?station=s9623358&apikey={ключ}&date=2024-03-05`

#### Синтаксис запроса:
```commandline
https://api.rasp.yandex.net/v3.0/schedule/?
  apikey=<ключ>
& station=<код станции>
& [date=<дата>]
& [transport_types=<тип транспорта>]
```

### Пример ответа:
```JSON
{
    "date": "2024-03-05",
    "station": {
        "type": "station",
        "title": "Чебоксары",
        "short_title": "",
        "popular_title": "",
        "code": "s9623358",
        "station_type": "airport",
        "station_type_name": "аэропорт",
        "transport_type": "plane"
    },
    "event": "departure",
    "pagination": {
        "total": 4,
        "limit": 100,
        "offset": 0
    },
    "schedule": [
        {
            "thread": {
                "number": "DP 6808",
                "title": "Чебоксары — Москва",
                "short_title": "Чебоксары — Москва",
                "carrier": {
                    "code": 9144,
                    "title": "Победа",
                    "codes": {
                        "sirena": "ДР",
                        "iata": "DP",
                        "icao": null
                    }
                },
                "vehicle": "Boeing 737-800",
                "transport_type": "plane",
                "express_type": null,
                "transport_subtype": {
                    "title": null,
                    "code": null,
                    "color": null
                },
                "uid": "DP-6808_240305_c9144_12"
            },
            "terminal": null,
            "is_fuzzy": false,
            "stops": "",
            "platform": "",
            "except_days": null,
            "departure": "2024-03-05T10:55:00+03:00",
            "arrival": null,
            "days": "5, 12, 19, 26 марта"
        },
        {
            "thread": {
                "number": "N4 448",
                "title": "Чебоксары — Сочи",
                "short_title": "Чебоксары — Сочи",
                "carrier": {
                    "code": 2543,
                    "title": "Nordwind",
                    "codes": {
                        "sirena": "КЛ",
                        "iata": "N4",
                        "icao": "NWS"
                    }
                },
                "vehicle": "Boeing 737-800",
                "transport_type": "plane",
                "express_type": null,
                "transport_subtype": {
                    "title": null,
                    "code": null,
                    "color": null
                },
                "uid": "N4-448_240305_c2543_12"
            },
            "terminal": null,
            "is_fuzzy": false,
            "stops": "",
            "platform": "",
            "except_days": null,
            "departure": "2024-03-05T16:10:00+03:00",
            "arrival": null,
            "days": "5, 12, 19, 26 марта"
        },
        {
            "thread": {
                "number": "DP 6818",
                "title": "Чебоксары — Москва",
                "short_title": "Чебоксары — Москва",
                "carrier": {
                    "code": 9144,
                    "title": "Победа",
                    "codes": {
                        "sirena": "ДР",
                        "iata": "DP",
                        "icao": null
                    }
                },
                "vehicle": "Boeing 737-800",
                "transport_type": "plane",
                "express_type": null,
                "transport_subtype": {
                    "title": null,
                    "code": null,
                    "color": null
                },
                "uid": "DP-6818_240305_c9144_12"
            },
            "terminal": null,
            "is_fuzzy": false,
            "stops": "",
            "platform": "",
            "except_days": null,
            "departure": "2024-03-05T17:50:00+03:00",
            "arrival": null,
            "days": "5, 12, 19, 26 марта"
        },
        {
            "thread": {
                "number": "DP 6816",
                "title": "Чебоксары — Москва",
                "short_title": "Чебоксары — Москва",
                "carrier": {
                    "code": 9144,
                    "title": "Победа",
                    "codes": {
                        "sirena": "ДР",
                        "iata": "DP",
                        "icao": null
                    }
                },
                "vehicle": "Boeing 737-800",
                "transport_type": "plane",
                "express_type": null,
                "transport_subtype": {
                    "title": null,
                    "code": null,
                    "color": null
                },
                "uid": "DP-6816_240305_c9144_12"
            },
            "terminal": null,
            "is_fuzzy": false,
            "stops": "",
            "platform": "",
            "except_days": null,
            "departure": "2024-03-05T21:50:00+03:00",
            "arrival": null,
            "days": "ежедневно по 30.03"
        }
    ],
    "interval_schedule": []
}
```
