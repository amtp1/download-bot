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
        yt = YouTube(message.text)
        stream = yt.streams.get_by_itag(22)
        mb_size = int(stream.filesize / 8 / 8 / 16 / 1024)
        if mb_size > 50:
            return await message.answer(text=f"Video size ({mb_size}MB) large then 50MB")
        await message.answer(text=f"⏳Downloading best video ({mb_size}MB)")
        video = urllib.request.urlopen(stream.url).read()
        bytes_video = BytesIO(video)
        user = await User.objects.get(user_id=message.from_user.id)
        download_count = user.download_count + 1
        await user.update(download_count=download_count)
        return await bot.send_video(
            message.from_user.id, InputFile(bytes_video, filename=f"{yt.author} - {yt.title}"),
            caption=f"✅ <b>{yt.author}</b> - {yt.title}\n\n"
            f"Channel: @downloader_video"
        )

    except RegexMatchError:
        return await message.answer(text="Invalid link!")
    except Exception as e:
        logger.error(e)