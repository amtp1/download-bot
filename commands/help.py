from aiogram.types import Message

from objects.globals import dp

@dp.message_handler(lambda message: message.text == "❗️Help")
async def help(message: Message):
    help_page = ("1) Bot is designed to upload video and audio from YouTube.\n"
                 "2) Bot will not be able to send a file that weighs more than 50mb.\n"
                 "3) To upload video or audio from YouTube, just paste the link.")
    return await message.answer(text=help_page)