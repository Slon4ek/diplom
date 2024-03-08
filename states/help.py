from telebot.handler_backends import State, StatesGroup


class HelpState(StatesGroup):
    """
    Класс состояний для команды /stations
    """
    regions = State()
    transport = State()
    city = State()
    city_choice = State()
