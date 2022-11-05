from datetime import datetime as dt

from aiogram.types import Message
from aiogram.utils.exceptions import ChatNotFound, UserDeactivated, BotBlocked
from aiogram.dispatcher.storage import FSMContext

from objects import globals
from states.states import Mailing
from models.mongo.models import *


@globals.dp.message_handler(lambda message: message.text == "Conduct mailing")
async def get_mailing_content(message: Message):
    if globals.config.get("ADMIN_ID") == message.from_user.id:
        if globals.is_mailing:
            return await message.answer("Mailing now ...")

        await message.answer("Enter message [/start - Cancel]:")
        await Mailing.condunt_mailing.set()


@globals.dp.message_handler(state=Mailing.condunt_mailing)
async def condunt_mailing(message: Message, state: FSMContext):
    await state.finish()
    if message.text == "/start":
        return await message.answer("Canceled")
    globals.is_mailing = True
    users = User.objects.all()
    start_time = dt.now()
    for user in users:
        try:
            await globals.bot.send_message(user.user_id, message.text)
        except (BotBlocked, UserDeactivated, ChatNotFound):
            globals.update_blocked_status(user.user_id)
    end_time = dt.now()
    total_sec = (end_time - start_time).total_seconds()
    globals.is_mailing = False
    return await message.answer("Time mailing: {:.2f} seconds.".format(total_sec))
