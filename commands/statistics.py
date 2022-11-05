from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from objects.globals import dp, config
from models.mongo.models import *


@dp.message_handler(commands=["stat"])
async def statistics(message: Message):
    if int(config.get("ADMIN_ID")) == message.from_user.id:
        users = User.objects.all()  # Get all users.
        # Sum count of downdloads.
        download_count = sum(list(obj.download_count for obj in users))
        mail_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                          keyboard=[
                                              [KeyboardButton(
                                                  text="Conduct mailing")]
                                          ])
        stat_page: str = (f"<b>Statistics</b>\n"
                          f"<code>|--</code><i>All users</i>: {users.__len__()}\n"
                          f"<code>|--</code><i>Download count</i>: {download_count}\n"
                          )
        # Return message with stat page.
        return await message.answer(text=stat_page, reply_markup=mail_markup)
