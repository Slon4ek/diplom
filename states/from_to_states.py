from telebot.handler_backends import State, StatesGroup


class FromTo(StatesGroup):
    departure = State()
    arrival = State()
    date = State()
    transport = State()
