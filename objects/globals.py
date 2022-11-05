from aiogram import Dispatcher, Bot

from models.mongo.models import *

bot: Bot = None
dp: Dispatcher = None

metadata = None
db_engine = None

config: dict = {}

is_mailing: bool = False


def update_download_count(user_id: int):
    user = User.objects(user_id=user_id).first()
    update_fields = {"download_count": user.download_count+1}
    User.objects.update(user.user_id, update_fields)


def update_blocked_status(user_id: int):
    user = User.objects(user_id=user_id).first()
    update_fields = {"is_blocked": True}
    User.objects.update(user.user_id, update_fields)
