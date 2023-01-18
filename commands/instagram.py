from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp
from utils.downloader.instagram import InstagramDownloader

@dp.message_handler(lambda message: message.text == 'Instagram Stories', state='*')
async def download(message: Message, state: FSMContext):
    #  await message.answer("Input username (Without @)👇")
    #  return await state.set_state('get_username')
    return await message.answer("Soon to the moon! In processing ...")


@dp.message_handler(state='get_username')
async def get_username(message: Message):
    username = message.text
    stories = InstagramDownloader(username).stories()
