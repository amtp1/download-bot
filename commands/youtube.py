import re
import traceback
import urllib.request
from io import BytesIO

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.storage import FSMContext
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

from objects.globals import dp, bot
from keyboards.keyboards import stream_markup
from utils.downloader.youtube import YoutubeDownloader
from models.mongo.models import User, Download

@dp.message_handler(lambda message: message.text == 'YouTube or YouTube Music', state='*')
async def download(message: Message, state: FSMContext):
    await message.answer("Paste link👇")
    return await state.set_state('get_youtube_link')


@dp.message_handler(state='get_youtube_link')
async def get_youtube_link(message: Message, state: FSMContext):
    regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie|music.youtube)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    link = re.match(regex, message.text)

    if not link:
        return await message.answer('Incorrect link!')
    yt = YouTube(message.text)  # Init YouTube class.
    # Set states (url and video id).
    await state.update_data(url=message.text, video_id=yt.video_id)
    await state.reset_state(with_data=False)
    # Return message with choose type.
    return await message.answer(text="Select content type", reply_markup=stream_markup)


@dp.callback_query_handler(lambda query: query.data == "audio")
async def download_audio(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id  # Set user id.
    msg_id = query.message.message_id  # Set message id.

    content_data: dict = await state.get_data()  # Get state data.
    response = YoutubeDownloader().download(content_data.get("url"), is_audio=True)

    if response.is_error:
        return await bot.send_message(chat_id=user_id, text=response.message)
    else:
        try:
            await bot.edit_message_text(chat_id=user_id, message_id=msg_id,
                                        text="⏳Downloading best audio. Please, wait.\n"
                                         "⚠️If the file size is large, the download will take longer.")
        except MessageNotModified:
            pass
        # Read audio content.
        audio = urllib.request.urlopen(response.stream).read()
        # Convert audio content in bytes.
        bytes_audio: BytesIO = BytesIO(audio)

        user = User.objects.get(user_id=user_id)
        download = Download(user=user, link=content_data.get("url"), content_type="audio", service="youtube")
        download.save()

        return await bot.send_audio(user_id,
                                    InputFile(bytes_audio, filename=f"{response.author} - {response.title}"),
                                    caption=f"✅ <b>{response.author}</b> - {response.title}\n\n"
                                    f"Channel: @downloader_video")  # Return audio with description.


@dp.callback_query_handler(lambda query: query.data == "video")
async def download_video(query: CallbackQuery, state: FSMContext):
    cht_id = query.from_user.id  # Set user id.
    msg_id = query.message.message_id  # Set message id.

    await bot.edit_message_text(chat_id=cht_id, message_id=msg_id, text="⏳Formatting streams. Please, wait...")

    content_data = await state.get_data()  # Get state data.
    yt = YouTube(content_data.get("url"))
    try:
        streams = list(yt.streams.filter(progressive=True, file_extension='mp4'))[::-1]

        streams_markup = InlineKeyboardMarkup()
        for stream in streams:
            streams_markup.add(InlineKeyboardButton(
                text=f"{stream.resolution} - {stream.fps}fps", callback_data=f"stream#{stream.itag}"))
        return await query.message.answer("Select stream", reply_markup=streams_markup)
    except (VideoUnavailable, RegexMatchError):
        traceback.print_exc()
        return await query.message.answer(text="Video unavailable!")


@dp.callback_query_handler(lambda query: query.data.startswith("stream"))
async def download_by_select_stream(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id  # Set user id.
    msg_id = query.message.message_id  # Set message id.

    await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text="⏳Downloading best video. Please, wait...")

    itag = re.sub("stream#", "", query.data)
    content_data = await state.get_data()  # Get state data.

    response = YoutubeDownloader().download(content_data.get("url"), itag=itag)
    await bot.send_chat_action(chat_id=user_id, action="upload_video")

    if response.is_error:
        return await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=response.message)
    else:
        # await bot.edit_message_text(chat_id=cht_id, message_id=msg_id, text=f"⏳Downloading best video")
        # Read video content.
        video = urllib.request.urlopen(response.stream).read()
        # Convert video content in bytes.
        bytes_video: BytesIO = BytesIO(video)

        user = User.objects.get(user_id=user_id)
        download = Download(user=user, link=content_data.get("url"), content_type="video", service="youtube")
        download.save()

        return await bot.send_video(user_id,
                                    InputFile(bytes_video, filename=f"{response.author} - {response.title}"),
                                    caption=f"✅ <b>{response.author}</b> - {response.title}\n\n"
                                    f"Channel: @downloader_video")  # Return video with description.
