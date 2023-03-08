import re
import urllib.request
from io import BytesIO

from aiogram.types import Message, InputFile
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp, bot
from utils.downloader.instagram import InstagramDownloader
from models.mongo.models import User, Download
from exceptions.exceptions import UserNotFound, NetworkError


@dp.message_handler(lambda message: message.text == 'Instagram Stories', state='*')
async def download(message: Message, state: FSMContext):
    await message.answer("Input username (Without @)👇")
    return await state.set_state('get_username')


@dp.message_handler(state='get_username')
async def get_username(message: Message, state: FSMContext, n=0):
    await state.finish()
    username = message.text
    instagram_downloader = InstagramDownloader(username)
    try:
        stories = instagram_downloader.stories()
        if stories:
            proxies = instagram_downloader.get_proxies()
            for story in stories:
                n+=1
                if n % 2 == 0:
                    content_id, content_type, url = story.get('id'), story.get('type'), story.get('url')
                    f_url = re.sub('/api/proxy/', '', url)
                    f_content_id = content_id.split('-')[0]
                    if content_type == "photo":
                        content = download_content(f_url, proxies)
                        await bot.send_photo(message.from_user.id, photo=content,
                                             caption=f"Photo ID: {f_content_id}\nChannel: @downloader_video")
                    elif content_type == "video":
                        content = download_content(f_url, proxies)
                        return await bot.send_video(message.from_user.id,
                                    InputFile(content, filename=f_content_id),
                                    caption=f"Video ID: {f_content_id}\n Channel: @downloader_video")  # Return video with description.
            user = User.objects.get(user_id=message.from_user.id)
            download = Download(user=user, link=f"https://www.instagram.com/{username}", content_type="story",
                                service="instagram")
            download.save() 
        elif stories == []:
            return await message.answer("Stories is not found ☹️")
    except UserNotFound:
        return await message.answer("User is not found ☹️")
    except NetworkError:
        return await message.answer("Network error. Try again later ☹️")


def download_content(url, proxies=None):
    proxy_handler = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    content = urllib.request.urlopen(url).read()
    b_content: BytesIO = BytesIO(content)
    return b_content
