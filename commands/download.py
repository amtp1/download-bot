import re
import traceback
import urllib.request
from io import BytesIO

import yarl
from loguru import logger
from pytube import YouTube
from dataclasses import dataclass
from pytube.exceptions import RegexMatchError, VideoUnavailable
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from objects.globals import dp, bot, update_download_count
from models.mongo.models import *
from states.states import *

SCHEME = {"https", "http"}  # Scheme types.


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
    base_url: str = message.text  # Set base url from message.
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie|music.youtube)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    instagram_regex = (
        r'(https?://)?(www\.)?'
        r'(instagram|insta)\.(com)/')

    youtube_regex = re.match(youtube_regex, base_url)
    instagram_regex = re.match(instagram_regex, base_url)
    if youtube_regex:
        url: yarl.URL = yarl.URL(base_url)  # Init URL class.
        # Check scheme in url.
        if url.scheme in SCHEME:
            try:
                yt = YouTube(base_url)  # Init YouTube class.
                # Set states (url and video id).
                await state.update_data(url=base_url, video_id=yt.video_id)
                inline_choose_type = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(
                            text="Audio", callback_data="audio")],
                        [InlineKeyboardButton(text="Video", callback_data="video")]
                    ])
                # Return message with choose type.
                return await message.answer(text="Select content type", reply_markup=inline_choose_type)
            except RegexMatchError:
                return await message.answer(text="Invalid link!")
            except Exception as e:
                logger.error(e)
    elif instagram_regex:
        return await message.answer("Soon to the moon!")



@dp.callback_query_handler(lambda query: query.data == "audio")
async def download_audio(query: CallbackQuery, state: FSMContext):
    cht_id = query.from_user.id  # Set user id.
    msg_id = query.message.message_id  # Set message id.

    content_data: dict = await state.get_data()  # Get state data.
    response = yt_download(content_data.get("url"), is_audio=True)

    if response.is_error:
        return await bot.send_message(chat_id=cht_id, text=response.message)
    else:
        await bot.edit_message_text(chat_id=cht_id, message_id=msg_id,
                                    text="⏳Downloading best audio. Please, wait.\n"
                                         "⚠️If the file size is large, the download will take longer.")
        # Read audio content.
        audio = urllib.request.urlopen(response.stream).read()
        # Convert audio content in bytes.
        bytes_audio: BytesIO = BytesIO(audio)

        # Update user download count.
        update_download_count(cht_id)

        return await bot.send_audio(cht_id,
                                    InputFile(
                                        bytes_audio, filename=f"{response.author} - {response.title}"),
                                    caption=f"✅ <b>{response.author}</b> - {response.title}\n\n"
                                    f"Channel: @downloader_video")  # Return audio with description.


@dp.callback_query_handler(lambda query: query.data == "video")
async def download_video(query: CallbackQuery, state: FSMContext):
    cht_id = query.from_user.id  # Set user id.
    msg_id = query.message.message_id  # Set message id.

    await bot.edit_message_text(chat_id=cht_id, message_id=msg_id, text=f"⏳Formatting streams. Please, wait...")

    content_data = await state.get_data()  # Get state data.
    yt = YouTube(content_data.get("url"))
    try:
        streams = list(yt.streams.filter(
            progressive=True, file_extension='mp4'))[::-1]

        streams_markup = InlineKeyboardMarkup()
        for stream in streams:
            streams_markup.add(InlineKeyboardButton(
                text=f"{stream.resolution} - {stream.fps}fps", callback_data=f"stream#{stream.itag}"))
        return await query.message.answer("Select stream", reply_markup=streams_markup)
    except VideoUnavailable:
        return await query.message.answer(text="Video unavailable!")


@dp.callback_query_handler(lambda query: query.data.startswith("stream"))
async def download_by_select_stream(query: CallbackQuery, state: FSMContext):
    cht_id = query.from_user.id  # Set user id.
    msg_id = query.message.message_id  # Set message id.

    await bot.edit_message_text(chat_id=cht_id, message_id=msg_id, text=f"⏳Downloading best video. Please, wait...")

    itag = re.sub("stream#", "", query.data)
    content_data = await state.get_data()  # Get state data.

    response = yt_download(content_data.get("url"), itag=itag)
    await bot.send_chat_action(chat_id=cht_id, action="upload_video")

    if response.is_error:
        return await bot.edit_message_text(chat_id=cht_id, message_id=msg_id, text=response.message)
    else:
        # await bot.edit_message_text(chat_id=cht_id, message_id=msg_id, text=f"⏳Downloading best video")
        # Read video content.
        video = urllib.request.urlopen(response.stream).read()
        # Convert video content in bytes.
        bytes_video: BytesIO = BytesIO(video)

        # Update user download count.
        update_download_count(cht_id)

        return await bot.send_video(cht_id,
                                    InputFile(
                                        bytes_video, filename=f"{response.author} - {response.title}"),
                                    caption=f"✅ <b>{response.author}</b> - {response.title}\n\n"
                                    f"Channel: @downloader_video")  # Return video with description.


def yt_download(url: str, is_audio: bool = False, itag: int = None) -> dict:
    try:
        yt: YouTube = YouTube(url)  # Init YouTube class.
    except TypeError:
        return MetaDownload(is_error=True, message=f"Paste new link")

    if is_audio:
        try:
            stream = yt.streams.filter(only_audio=True).desc().first()
        except:
            traceback.print_exc()
            return MetaDownload(is_error=True, message=f"Unknow error")
    else:
        try:
            stream = yt.streams.get_by_itag(itag)
        except VideoUnavailable as e:
            return MetaDownload(is_error=True, message=e)
        except:
            traceback.print_exc()
            return MetaDownload(is_error=True, message=f"Unknow error")
    # Convert to mb value size.
    mb_size: float = float(stream.filesize / 8 / 8 / 16 / 1024)
    if mb_size < 1024:
        # Format in string file size.
        str_filesize: str = "{:.2}MB".format(mb_size)
    elif mb_size > 1024:
        _mb_size = mb_size / 1024
        # Format in string file size.
        str_filesize: str = "{:.2}GB".format(_mb_size)
    if mb_size > 50:
        return MetaDownload(is_error=True, message=f"Video size ({str_filesize}) large then 50MB")
    else:
        return MetaDownload(stream=stream.url, author=yt.author, title=yt.title)
