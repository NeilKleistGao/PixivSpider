from PixivSpider.CrawlData import CrawlData
from http import cookiejar
from bs4 import BeautifulSoup
import requests
import re

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

    def crawl(self, CrawlData):
        pass
    
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
        return 23
    
    def hasFinished(self):
        return False

    def getPostKey(self):
        response = self.session.get(self.key_url, headers = self.header)
        bs = BeautifulSoup(response.text, "lxml")
        key = bs.find("input")["value"]
        return key
