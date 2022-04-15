import urllib.request
from io import BytesIO

import yarl
from loguru import logger
from pytube import YouTube
from dataclasses import dataclass
from pytube.exceptions import RegexMatchError
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from objects.globals import dp, bot, update_download_count
from models.mongo.models import *
from states.states import *

SCHEME = {"https", "http"} # Scheme types.


@dataclass
class MetaDownload:
    is_error: bool = False
    message: str = ""
    stream: str = ""

    author: str = ""
    title: str = ""

    def __init__(self, is_error=False, message="", stream="", author="", title=""):
        self.is_error = is_error
        self.message = message
        self.stream = stream
        self.author = author
        self.title = title


@dp.message_handler()
async def download(message: Message, state: FSMContext):
    base_url: str = message.text # Set base url from message.
    url: yarl.URL = yarl.URL(base_url) # Init URL class.
    # Check scheme in url.
    if url.scheme in SCHEME:
        try:
            yt = YouTube(base_url) # Init YouTube class.
            await state.update_data(url=base_url, video_id=yt.video_id) # Set states (url and video id).
            inline_choose_type = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Audio", callback_data="audio")],
                    [InlineKeyboardButton(text="Video", callback_data="video")]
                ])
            return await message.answer(text="Select content type", reply_markup=inline_choose_type) # Return message with choose type.
        except RegexMatchError:
            return await message.answer(text="Invalid link!")
        except Exception as e:
            logger.error(e)

@dp.callback_query_handler(lambda query: query.data=="audio")
async def download_audio(query: CallbackQuery, state: FSMContext):
    cht_id = query.from_user.id # Set user id.
    msg_id = query.message.message_id # Set message id.

    content_data: dict = await state.get_data() # Get state data.
    response = yt_download(content_data.get("url"), is_audio=True)
    
    if response.is_error:
        return await bot.send_message(chat_id=cht_id, text=response.message)
    else:
        await bot.edit_message_text(chat_id=cht_id, message_id=msg_id, text=f"⏳Downloading best audio")
        audio = urllib.request.urlopen(response.stream).read() # Read audio content.
        bytes_audio: BytesIO = BytesIO(audio) # Convert audio content in bytes.

        # Update user download count.
        update_download_count(cht_id)

        return await bot.send_audio(cht_id, 
            InputFile(bytes_audio, filename=f"{response.author} - {response.title}"),
            caption=f"✅ <b>{response.author}</b> - {response.title}\n\n"
            f"Channel: @downloader_video") # Return audio with description.

@dp.callback_query_handler(lambda query: query.data=="video")
async def download_video(query: CallbackQuery, state:FSMContext):
    cht_id = query.from_user.id # Set user id.
    msg_id = query.message.message_id # Set message id.

    content_data = await state.get_data() # Get state data.

    response = yt_download(content_data.get("url"))

    if response.is_error:
        return await bot.edit_message_text(chat_id=cht_id, message_id=msg_id, text=response.message)
    else:
        await bot.edit_message_text(chat_id=cht_id, message_id=msg_id, text=f"⏳Downloading best video")
        video = urllib.request.urlopen(response.stream).read() # Read video content.
        bytes_video: BytesIO = BytesIO(video) # Convert video content in bytes.

        # Update user download count.
        update_download_count(cht_id)

        return await bot.send_video(cht_id,
            InputFile(bytes_video, filename=f"{response.author} - {response.title}"),
            caption=f"✅ <b>{response.author}</b> - {response.title}\n\n"
            f"Channel: @downloader_video") # Return video with description.

def yt_download(url: str, is_audio: bool = False) -> dict:
    try:
        yt: YouTube = YouTube(url) # Init YouTube class.
    except TypeError:
        return MetaDownload(is_error=True, message=f"Paste new link")
        
    if is_audio:
        stream = yt.streams.filter(only_audio=is_audio)[0]
    else:
        stream = yt.streams.filter(only_video=True)[0]
    mb_size: float = float(stream.filesize / 8 / 8 / 16 / 1024) # Convert to mb value size.
    if mb_size < 1024:
        str_filesize: str = "{:.2}MB".format(mb_size) # Format in string file size.
    elif mb_size > 1024:
        _mb_size = mb_size / 1024
        str_filesize: str = "{:.2}GB".format(_mb_size) # Format in string file size.
    if mb_size > 50:
        return MetaDownload(is_error=True, message=f"Video size ({str_filesize}) large then 50MB")
    else:
        return MetaDownload(stream=stream.url, author=yt.author, title=yt.title)