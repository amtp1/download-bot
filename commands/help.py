from aiogram.types import Message

from objects.globals import dp

from utils.update.update import Update

@dp.message_handler(lambda message: message.text == "❗️Help", state='*')
async def help(message: Message):
    Update.update_user_data(message)
    help_page = ("1) Bot is designed to upload video and audio from YouTube.\n"
                 "2) Bot will not be able to send a file that weighs more than 50mb.\n"
                 "3) To upload video or audio from YouTube, just paste the link.\n\n"
                 "Help chat: @AnyswapNetwork")
    return await message.answer(text=help_page)
