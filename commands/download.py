import urllib.request
from io import BytesIO

from loguru import logger
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from aiogram.types import Message, InputFile

from objects.globals import dp, bot
from models.models import *

@dp.message_handler()
async def download(message: Message):
    try:
        await message.answer(text="Downloading...")
        yt = YouTube(message.text)
        stream = yt.streams.get_by_itag(22)
        video = urllib.request.urlopen(stream.url).read()
        bytes_video = BytesIO(video)
        user = await User.objects.get(user_id=message.from_user.id)
        download_count = user.download_count + 1
        await user.update(download_count=download_count)
        return await bot.send_video(
            message.from_user.id, InputFile(bytes_video, filename=f"{yt.author} - {yt.title}"),
            caption=f"{yt.author} - {yt.title}\n\n"
            f"Channel: @downloader_video"
        )
    except RegexMatchError:
        return await message.answer(text="Invalid link!")
    except Exception as e:
        logger.error(e)