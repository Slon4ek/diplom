from telebot.handler_backends import State, StatesGroup


class LocationState(StatesGroup):
    """
    Класс состояний для команды /nearest_station
    """
    get_location = State()
    get_radius = State()
    transport_type = State()
