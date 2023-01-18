import re
import random
from dataclasses import dataclass

import requests
from requests.exceptions import HTTPError, ProxyError, ConnectTimeout, SSLError, ConnectionError
from loguru import logger
from dotenv import dotenv_values

config = dict(dotenv_values('.proxy_env'))
PROXIES = list(dotenv_values('.proxies'))
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

MULTI_PROXY = True

@dataclass
class ContentMeta:
    is_error: bool
    message: str
    content_type: str

    def __init__(self, is_error=False, message="", content_type=""):
        self.is_error = is_error
        self.message = message
        self.content_type = content_type

class InstagramDownloader:
    def __init__(self, username: str):
        self.username = username

    def stories(self):
        try:
            user_id = self.get_user_id()
            if user_id:
                proxies = self.get_proxies()
                link = 'https://igs.sf-converter.com/api/stories/%s' % user_id
                request = requests.get(url=link, proxies=proxies, timeout=3)
                response = request.text
                return response
        except (ProxyError, ConnectTimeout, SSLError):
            self.stories()

    def get_user_id(self) -> str:
        try:
            link = 'https://www.instagram.com/%s/?__a=1' % self.username
            request = requests.get(url=link, proxies=self.get_proxies(), timeout=3)
            response = request.text
            if response:
                profile_id = re.search('"profile_id"', response)
                sub_path = re.search('"sub_path"', response)
                profile_id = response[profile_id.end():sub_path.start()]
                profile_id = re.sub('[:",]', '', profile_id)
                return profile_id
        except ConnectionError:
            self.get_user_id()
        except HTTPError as e:
            logger.error(e)

    def get_proxies(self):
        if MULTI_PROXY:
            proxy_url = random.choice(PROXIES)
            proxies = {
                'http': f'http://{proxy_url}',
                'https': f'http://{proxy_url}'
            }
        else:
            host = config.get('SERVER_HOST')
            port = config.get('SERVER_PORT')
            user = config.get('SERVER_USER')
            password = config.get('SERVER_PASSWORD')
            proxies = {
                'http': f'http://{user}:{password}@{host}:{port}',
                'https': f'http://{user}:{password}@{host}:{port}'
            }
        return proxies
