from aiogram.types import Message

from objects.globals import dp, config
from models.mongo.models import *


@dp.message_handler(commands=["stat"])
async def statistics(message: Message):
    if int(config.get("ADMIN_ID")) == message.from_user.id:
        users = User.objects.all() # Get all users.
        download_count = sum(list(obj.download_count for obj in users)) # Sum count of downdloads.
        stat_page: str = (f"<b>Statistics</b>\n"
            f"<code>|--</code><i>All users</i>: {users.__len__()}\n"
            f"<code>|--</code><i>Download count</i>: {download_count}\n"
            )
        return await message.answer(text=stat_page) # Return message with stat page.