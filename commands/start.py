from aiogram.types import Message

from models.models import *
from objects.globals import dp

@dp.message_handler(commands="start")
async def start(message: Message):
    user = User.objects.filter(user_id=message.from_user.id)

    if not await user.exists():
        await User.objects.create(
            user_id=message.from_user.id, username=message.from_user.username,
            first_name=message.from_user.first_name, last_name=message.from_user.last_name,
            download_count=0
        )

    user = await user.all()

    return await message.answer(text="Paste link (YouTube):")