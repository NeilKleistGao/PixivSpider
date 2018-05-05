class CrawlData(object):
    def __init__(self):
        super().__init__()
        self.url = ""
        self.is_customize = False

class ImageData(object):
    def __init__(self):
        super().__init__()
        self.parent = ""
        self.url = ""
        self.name = ""
        self.pid = 0