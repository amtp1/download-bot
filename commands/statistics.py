from aiogram.types import Message

from objects.globals import dp, config
from models.models import *


@dp.message_handler(commands=["stat"])
async def statistics(message: Message):
    if int(config.get("ADMIN_ID")) == message.from_user.id:
        users = await User.objects.all()
        stat_page: str = (f"<b>Statistics</b>\n"
            f"<code>|--</code><i>Общее количество</i>: {users.__len__()}\n"
            )
        return await message.answer(text=stat_page)