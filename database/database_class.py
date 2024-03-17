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
    user = ForeignKeyField(User, backref='requests')
    country = CharField()
    region = CharField()
    city = CharField()
    transport_type = CharField()
    request_date = DateTimeField(default=datetime.datetime.now())
    schedule_date = DateField()
    station = CharField()
    station_code = IntegerField()


def create_models() -> None:
    """
    Функция создает таблицы в базе данных
    :return:
    """
    db.create_tables(BaseModel.__subclasses__())
