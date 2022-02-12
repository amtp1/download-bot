import urllib.request
from io import BytesIO

import yarl
from loguru import logger
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, InputFile, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from objects.globals import dp, bot
from models.models import *
from states.states import *

SCHEME = ["https", "http"]

@dp.message_handler()
async def download(message: Message, state: FSMContext):
    print(message)
    base_url: str = message.text
    url = yarl.URL(base_url)
    if url.scheme in SCHEME:
        try:
            yt = YouTube(base_url)
            await state.update_data(url=base_url, video_id=yt.video_id)
            inline_choose_type = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Audio", callback_data="audio")],
                    [InlineKeyboardButton(text="Video", callback_data="video")]
                ])
            return await message.answer(text="Select content type", reply_markup=inline_choose_type)
        except RegexMatchError:
            return await message.answer(text="Invalid link!")
        except Exception as e:
            logger.error(e)

@dp.callback_query_handler(lambda query: query.data=="audio")
async def download_audio(query: CallbackQuery, state: FSMContext):
    content_data = await state.get_data()
    yt: YouTube = YouTube(content_data.get("url"))
    stream = yt.streams.filter(only_audio=True)[0]
    mb_size: float = float(stream.filesize / 8 / 8 / 16 / 1024)
    str_filesize: str = "{:.2}".format(mb_size)
    if mb_size > 50:
        return await bot.send_message(chat_id=query.from_user.id, text=f"Audio size ({str_filesize})MB) large then 50MB")
    await bot.send_message(chat_id=query.from_user.id, text=f"⏳Downloading best audio ({str_filesize}MB)")
    audio = urllib.request.urlopen(stream.url).read()
    bytes_audio: BytesIO = BytesIO(audio)
    user = await User.objects.get(user_id=query.from_user.id)
    download_count: int = user.download_count + 1
    await user.update(download_count=download_count)
    #await bot.delete_message(query.from_user.id, query.message.message_id)
    return await bot.send_audio(
        query.from_user.id, InputFile(bytes_audio, filename=f"{yt.author} - {yt.title}"),
        caption=f"✅ <b>{yt.author}</b> - {yt.title}\n\n"
        f"Channel: @downloader_video")

@dp.callback_query_handler(lambda query: query.data=="video")
async def download_video(query: CallbackQuery, state:FSMContext):
    content_data = await state.get_data()
    yt: YouTube = YouTube(content_data.get("url"))
    stream = yt.streams.filter(only_video=True)[0]
    mb_size: float = float(stream.filesize / 8 / 8 / 16 / 1024)
    str_filesize: str = "{:.2}".format(mb_size)
    if mb_size > 50:
        return await bot.send_message(chat_id=query.from_user.id, text=f"Video size ({str_filesize})MB) large then 50MB")
    await bot.send_message(chat_id=query.from_user.id, text=f"⏳Downloading best video ({str_filesize}MB)")
    video = urllib.request.urlopen(stream.url).read()
    bytes_video: BytesIO = BytesIO(video)
    user = await User.objects.get(user_id=query.from_user.id)
    download_count: int = user.download_count + 1
    await user.update(download_count=download_count)
    #await bot.delete_message(query.from_user.id, query.message.message_id)
    return await bot.send_video(
        query.from_user.id, InputFile(bytes_video, filename=f"{yt.author} - {yt.title}"),
        caption=f"✅ <b>{yt.author}</b> - {yt.title}\n\n"
        f"Channel: @downloader_video")