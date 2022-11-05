from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from models.mongo.models import *
from objects.globals import dp, config


@dp.message_handler(commands="start")
async def start(message: Message):
    # Get count user by user id. Must be always 1 user.
    user = User.objects(user_id=message.from_user.id).count()
    if not bool(user):
        user = User(user_id=message.from_user.id, username=message.from_user.username,
                    first_name=message.from_user.first_name, last_name=message.from_user.last_name)
        user.save()
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                       keyboard=[
                                           [KeyboardButton(text="❗️Help")]
                                       ])
    if config.get("ADMIN_ID") == message.from_user.id:
        reply_markup.add(KeyboardButton("Conduct mailing"))
    return await message.answer(text="Paste link (YouTube):", reply_markup=reply_markup)
