from Base import BaseCrawler
from parsel import Selector
from pyquery import PyQuery as pq

MAX_PAGE = 5
BASE_URL = 'http://www.66ip.cn/%d.html'


class Daili66Crawler(BaseCrawler):
    def __init__(self, p):
        super().__init__()
        self.url = BASE_URL % p

    @BaseCrawler().log
    def parse(self, link):
        html = self.fetch(link)
        sel = Selector(text=html)
        temp = sel.css('.containerbox.boxindex table tr:nth-child(n+2)')
        for t in temp:
            ip = t.css('td:nth-child(1)::text').get()
            port = t.css('td:nth-child(2)::text').get()
            proxy = ip + ':' + str(port)
            yield proxy


if __name__ == '__main__':
    for _ in range(1, MAX_PAGE + 1):
        crawler = Daili66Crawler(_)
        url = BASE_URL % _
        proxies = crawler.parse(url)
