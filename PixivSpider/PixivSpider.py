from PixivSpider.DataStructures import CrawlData, ImageData
from http import cookiejar
from bs4 import BeautifulSoup
import requests
import re
import math
import threading
import os
import time

__all__ = ["crawl", "login", "getSchedule", "hasFinished"]

class PixivSpider(object):

    def __init__(self):
        super().__init__()

        self.login_url = "https://accounts.pixiv.net/api/login?lang=zh"
        self.return_url = "https://www.pixiv.net"
        self.key_url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
        self.detail_url = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="
        self.main_url = ""

        self.path = ""

        self.header = { "Referer": "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" }
        self.headerForDetail = { "Referer": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" } 
        self.headerForDownload = { "Referer": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" } 

        self.session = requests.session()

        self.img_list = []

        self.total_count = 1
        self.done_count = 0
        self.page_count = 0
        self.real_count = 0
        self.min = 0

        self.PAGE_MAX = 1000
        self.COUNT_IN_PAGE = 40
        self.COUNT_IN_RANK = 50
        self.TOTAL_RANK = 500

        self.is_customize = False

    def crawl(self, name, crawldata, min_view):
        self.main_url = crawldata.url
        self.min = min_view
        self.is_customize = crawldata.is_customize
        self.path = name + "/"

        self.getCount()
        os.makedirs(name, exist_ok = True)
        
        ts = threading.Thread(target = self.getDataThreading, name = "crawling", daemon = True)
        td = threading.Thread(target = self.downloadThreading, name = "downloading", daemon = True)

        ts.start()
        td.start()
    
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

    def getCount(self):
        response = self.session.get(self.main_url, headers = self.header)
        if self.is_customize:
            bs = BeautifulSoup(response.text, "lxml")
            self.total_count = int(bs.find_all('span')[12].string[:-1])
            self.page_count = int(math.ceil(float(self.total_count) / self.COUNT_IN_PAGE))
            if self.page_count > self.PAGE_MAX:
                self.page_count = self.PAGE_MAX
                self.total_count = self.page_count * self.COUNT_IN_PAGE
        else:
            self.total_count = self.TOTAL_RANK
            self.page_count = int(self.TOTAL_RANK / self.COUNT_IN_RANK)

    def getPostKey(self):
        response = self.session.get(self.key_url, headers = self.header)
        bs = BeautifulSoup(response.text, "lxml")
        key = bs.find("input")["value"]
        return key

    def getDataThreading(self):
        for i in range(1, self.page_count + 1):
            self.getImagePage(self.main_url + "&p=" + str(i))
        if self.real_count > 0:
            self.total_count = self.real_count

    def getImagePage(self, url):
        response = self.session.get(self.main_url, headers = self.header)
        bs = BeautifulSoup(response.text, "lxml")
        if self.is_customize:
            item = bs.find_all("input")[3]
            ptn = r'"illustId":"(?P<pid>\d+)"'
            pid_list = re.findall(ptn, item["data-items"])
            for i in pid_list:
                self.getDetail(self.detail_url + str(i), url, i)
        else:
            items = bs.find_all("img")
            for i in items:
                if i.has_attr("data-src"):
                    item = i["data-src"]
                    ptn = r"(?P<pid>\d+)_"
                    pid = re.search(ptn, item).group("pid")
                    self.getDetail(self.detail_url + str(pid), url, pid)

                    self.real_count = self.real_count + 1

    def getDetail(self, url, parent, pid):
        self.headerForDetail["Referer"] = parent
        response = self.session.get(url, headers = self.headerForDetail)
        bs = BeautifulSoup(response.text, "lxml")
        view = bs.find("dd").string
        if int(view) >= self.min:
            img = ImageData()
            ptn = r"<span>(?P<cnt>\d+)"
            res = re.search(ptn, response.text)
            if res == None:
                img.count = 1#img-original直接从这个链接获取下载地址
            else:
                img.count = int(res.group("cnt"))#mode=manga进入这个模式可以找到其他项
    
    def downloadThreading(self):
        while not self.hasFinished():
            if len(self.img_list) > 0:
                self.downloadImage(self.img_list[0])
                del self.img_list[0]
                self.done_count = self.done_count + 1
            else:
                time.sleep(1)

    def downloadImage(self, image_data):
        self.headerForDownload["Referer"] = image_data.parent
        for i in range(0, image_data.count, headers = self.headerForDownload):
            url = image_data.url % i
            response = requests.get(url)
            with open(path + (image_data.name % i), "wb") as fp:
                fp.write(response.content)