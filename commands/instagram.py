import re
import urllib.request
from io import BytesIO

import requests
from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp, bot
from utils.downloader.instagram import InstagramDownloader
from models.mongo.models import User, Download

@dp.message_handler(lambda message: message.text == 'Instagram Stories', state='*')
async def download(message: Message, state: FSMContext):
    await message.answer("Input username (Without @)👇")
    return await state.set_state('get_username')
    # return await message.answer("Soon to the moon! In processing ...")


@dp.message_handler(state='get_username')
async def get_username(message: Message, state: FSMContext, n=0):
    await state.finish()
    username = message.text
    instagram_downloader = InstagramDownloader(username)
    stories = instagram_downloader.stories()
    proxies = instagram_downloader.get_proxies()
    for story in stories:
        n+=1
        if n % 2 == 0:
            content_id, content_type, url = story.get('id'), story.get('type'), story.get('url')
            f_url = re.sub('/api/proxy/', '', url)
            if content_type == "photo":
                #photo = requests.get(url=f_url, stream=True).content
                proxy_handler = urllib.request.ProxyHandler(proxies)
                opener = urllib.request.build_opener(proxy_handler)
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                photo = urllib.request.urlopen(f_url).read()
                b_photo: BytesIO = BytesIO(photo)
                await bot.send_photo(message.from_user.id, photo=b_photo, caption=f"Photo ID: {content_id}")
    user = User.objects.get(user_id=message.from_user.id)
    download = Download(user=user, link=f"https://www.instagram.com/{username}", content_type="story", service="youtube")
    download.save()