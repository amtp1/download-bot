from aiogram.types import Message

from models.mongo.models import *
from objects.globals import dp

@dp.message_handler(commands="start")
async def start(message: Message):
    user = User.objects(user_id=message.from_user.id).count() # Get count user by user id. Must be always 1 user.
    if not bool(user):
        user = User(user_id=message.from_user.id, username=message.from_user.username,
            first_name=message.from_user.first_name, last_name=message.from_user.last_name)
        user.save()
    return await message.answer(text="Paste link (YouTube):")