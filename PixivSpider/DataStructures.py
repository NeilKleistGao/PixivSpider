class CrawlData(object):
    def __init__(self):
        super().__init__()
        self.url = ""
        self.lowest_stars = 0
        self.is_customize = False

class ImageData(object):
    def __init__(self):
        super().__init__()
        self.parent = ""
        self.url = ""
        self.name = ""
        self.count = 0