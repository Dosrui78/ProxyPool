import json
from Base import BaseCrawler
from parsel import Selector
from pyquery import PyQuery as pq

BASE_URL = 'http://proxylist.fatezero.org/proxy.list'


class FateCrawler(BaseCrawler):
    def __init__(self, p=None):
        super().__init__()
        self.url = BASE_URL

    @BaseCrawler().log
    def parse(self, link):
        html = self.fetch(link)
        hosts_ports = html.split('\n')
        for ad in hosts_ports:
            if ad:
                ip_address = json.loads(ad)
                if ip_address['anonymity'] == 'high_anonymous':
                    host = ip_address['host']
                    port = ip_address['port']
                    proxy = str(host) + ':' + str(port)
                    yield proxy
            else:
                continue


if __name__ == '__main__':
    crawler = FateCrawler()
    url = BASE_URL
    proxies = crawler.parse(url)
