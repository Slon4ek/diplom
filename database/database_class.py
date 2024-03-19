import datetime

from peewee import *

from config_data.config import DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    """
    Базовый класс для работы с базой данных
    """

    class Meta:
        database = db


class User(BaseModel):
    """
    Класс данных о пользователе
    """
    user_id = IntegerField(primary_key=True)
    user_name = CharField()
    created_date = DateField(default=datetime.datetime.now())


class InstationRequest(BaseModel):
    """
    Класс данных об истории запроса пользователя
    """
    request_id = AutoField()
    user = ForeignKeyField(User, backref='requests_in_station')
    country = CharField()
    region = CharField()
    city = CharField()
    transport_type = CharField()
    request_date = DateTimeField(default=datetime.datetime.now())
    schedule_date = DateField()
    station = CharField()
    station_code = IntegerField()


class FromToRequest(BaseModel):
    """
    Класс данных для записи истории запросов расписаний между станциями
    """
    request_id = AutoField()
    user = ForeignKeyField(User, backref='requests_between_stations')
    from_city = CharField(null=True)
    from_station = CharField(null=True)
    from_code = IntegerField()
    to_city = CharField(null=True)
    to_station = CharField(null=True)
    to_code = IntegerField()
    transport_type = CharField()
    request_date = DateTimeField(default=datetime.datetime.now())
    schedule_date = DateField()


def create_models() -> None:
    """
    Функция создает таблицы в базе данных
    :return:
    """
    db.create_tables(BaseModel.__subclasses__())
