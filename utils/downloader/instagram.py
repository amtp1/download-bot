import json
from json.decoder import JSONDecodeError
import random
from dataclasses import dataclass

import requests
from dotenv import dotenv_values

from exceptions.exceptions import UserNotFound, NetworkError

config = dict(dotenv_values('.proxy_env'))
PROXIES = list(dotenv_values('.proxies'))
headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')}

MULTI_PROXY = False

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
        link = 'https://instastories.watch/api/profile/stories?username=%s' % self.username
        request = requests.get(url=link)
        if request.status_code == 200:
            try:
                response = request.text
                response = json.loads(response)
                return response
            except JSONDecodeError:
                raise UserNotFound('User not found')
        else:
            raise NetworkError('Network error')

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
