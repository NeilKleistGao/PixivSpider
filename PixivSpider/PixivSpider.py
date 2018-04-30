from PixivSpider.CrawlData import CrawlData
from http import cookiejar
from bs4 import BeautifulSoup
import requests
import re
import math

__all__ = ["crawl", "login", "getSchedule", "hasFinished"]

class PixivSpider(object):

    def __init__(self):
        super().__init__()

        self.login_url = "https://accounts.pixiv.net/api/login?lang=zh"
        self.return_url = "https://www.pixiv.net"
        self.key_url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"

        self.header = { "Referer": "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" }  

        self.session = requests.session()

        self.total_count = 1
        self.done_count = 0
        self.page_count = 0

        self.PAGE_MAX = 1000
        self.COUNT_IN_PAGE = 40
        self.COUNT_IN_RANK = 50
        self.TOTAL_RANK = 500

    def crawl(self, crawldata):
        self.getCount(crawldata.url, crawldata.is_customize)
    
    def login(self, username, password):
        flag = True
        key = self.getPostKey()

        data = {
            "pixiv_id":username,
            "password":password,
            "return_to":self.return_url,
            "post_key":key
        }

        response = self.session.post(self.login_url, headers = self.header, data = data)
        res = re.search("failure", response.text)

        if not res == None:
            flag = False

        return flag

    def getSchedule(self):
        return 100 * self.done_count / self.total_count
    
    def hasFinished(self):
        flag = False
        if self.done_count == self.total_count:
            flag = True
        return flag

    def getCount(self, url, is_customize):
        response = self.session.get(url, headers = self.header)
        print(response.text)
        if is_customize:
            bs = BeautifulSoup(response.text, "lxml")
            self.total_count = int(bs.find('span').string[:-1])
            self.page_count = int(math.ceil(float(self.total_count) / self.COUNT_IN_PAGE))
            if self.page_count > self.PAGE_MAX:
                self.page_count = self.PAGE_MAX
                self.total_count = self.page_count * self.COUNT_IN_PAGE
        else:
            self.total_count = self.TOTAL_RANK
            self.page_count = self.TOTAL_RANK / self.COUNT_IN_RANK

    def getPostKey(self):
        response = self.session.get(self.key_url, headers = self.header)
        bs = BeautifulSoup(response.text, "lxml")
        key = bs.find("input")["value"]
        return key
