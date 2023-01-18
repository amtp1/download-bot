import os
import json
import unittest
import logging

import requests
from dotenv import dotenv_values

config = dict(dotenv_values("../.proxy_env"))

logger = logging.getLogger(__name__)
loglevel = logging.DEBUG
logging.basicConfig(level=loglevel)

class TestConnectProxy(unittest.TestCase):

    def check_connect(self):
        proxy_url = (f"http://{config.get('SERVER_USER')}:{config.get('SERVER_PASSWORD')}"
                     f"@{config.get('SERVER_HOST')}:{config.get('SERVER_PORT')}")
        request = requests.get('https://api.ipify.org?format=json',
                                proxies={'http': proxy_url, 'https': proxy_url})
        response = json.loads(request.text)
        ip = response.get("ip")
        self.assertEqual(ip, config.get('SERVER_HOST'))

if __name__ == "__main__":
    unittest.main()
