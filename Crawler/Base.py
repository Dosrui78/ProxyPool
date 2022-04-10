import requests
import time

import urllib3
from fake_headers import Headers
from loguru import logger
from retrying import retry, RetryError


class BaseCrawler(object):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    def __init__(self):
        self.url = ''

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    def fetch(self, url, **kwargs):
        kwargs.setdefault('timeout', 10)
        kwargs.setdefault('verify', False)
        kwargs.setdefault('allow_redirects', False)
        kwargs.setdefault('headers', Headers().generate())
        kwargs.setdefault('proxies', {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'})
        try:
            response = requests.get(url, **kwargs)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
        except (requests.ConnectionError, requests.Timeout):
            return

    def log(self, fn):
        def wrapper(*args, **kwargs):
            for proxy in fn(*args, **kwargs):
                time.sleep(.3)
                logger.info('fetching {} from {}'.format(proxy, args[1]))
        return wrapper

if __name__ == '__main__':
    url = 'https://www.kuaidaili.com/free/inha/2/'
    crawler = BaseCrawler()
    print(crawler.fetch(url))
