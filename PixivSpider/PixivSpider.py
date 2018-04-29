from PixivSpider.CrawlData import CrawlData
from urllib import request, parse
from http import cookiejar
from bs4 import BeautifulSoup

class PixivSpider(object):

    def __init__(self):
        super().__init__()

        self.login_url = "https://www.pixiv.net/login.php"
        self.login_header = { 'Accept-Language':'zh-CN,zh;q=0.8',
         'Referer':'https://www.pixiv.net/login.php?return_to=0',
          'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0' }  

        self.cookie = cookiejar.CookieJar()
        self.handler = request.HTTPCookieProcessor(self.cookie)
        self.opener = request.build_opener(self.handler)

    def crawl(self, CrawlData):
        pass
    
    def login(self, username, password):
        flag = True
        return flag

    def getSchedule(self):
        return 23
    
    def hasFinished(self):
        return False