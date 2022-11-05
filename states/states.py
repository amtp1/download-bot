
from aiogram.dispatcher.filters.state import StatesGroup, State


class Type(StatesGroup):
    url = State()


class Mailing(StatesGroup):
    condunt_mailing = State()
