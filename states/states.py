from aiogram.dispatcher.filters.state import StatesGroup, State

class Type(StatesGroup):
    url = State()
    video_id = State()

class Mailing(StatesGroup):
    condunt_mailing = State()
