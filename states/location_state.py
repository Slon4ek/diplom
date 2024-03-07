from telebot.handler_backends import State, StatesGroup


class LocationState(StatesGroup):
    get_location = State()
    get_radius = State()
    transport_type = State()
