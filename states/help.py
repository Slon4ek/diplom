from telebot.handler_backends import State, StatesGroup


class HelpState(StatesGroup):
    regions = State()
    transport = State()
    city = State()
    city_choice = State()
