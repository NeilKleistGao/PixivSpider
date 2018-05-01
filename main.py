import sys  
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PixivSpider.DataStructures import CrawlData
from PixivSpider.PixivSpider import PixivSpider

class mainWidget(QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(730, 465)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pixiv.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.LoginBox = QtWidgets.QGroupBox(Form)
        self.LoginBox.setGeometry(QtCore.QRect(20, 10, 291, 151))
        self.LoginBox.setObjectName("LoginBox")
        self.label = QtWidgets.QLabel(self.LoginBox)
        self.label.setGeometry(QtCore.QRect(0, 30, 101, 17))
        self.label.setObjectName("label")
        self.userEdit = QtWidgets.QLineEdit(self.LoginBox)
        self.userEdit.setGeometry(QtCore.QRect(100, 30, 161, 27))
        self.userEdit.setObjectName("userEdit")
        self.label_2 = QtWidgets.QLabel(self.LoginBox)
        self.label_2.setGeometry(QtCore.QRect(0, 60, 101, 17))
        self.label_2.setObjectName("label_2")
        self.passwordEdit = QtWidgets.QLineEdit(self.LoginBox)
        self.passwordEdit.setGeometry(QtCore.QRect(100, 60, 161, 27))
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.pushButton = QtWidgets.QPushButton(self.LoginBox)
        self.pushButton.setGeometry(QtCore.QRect(100, 90, 99, 27))
        self.pushButton.setObjectName("pushButton")
        self.state_label = QtWidgets.QLabel(self.LoginBox)
        self.state_label.setGeometry(QtCore.QRect(100, 120, 111, 20))
        self.state_label.setObjectName("state_label")
        self.tagBox = QtWidgets.QGroupBox(Form)
        self.tagBox.setGeometry(QtCore.QRect(10, 210, 291, 151))
        self.tagBox.setObjectName("tagBox")
        self.typeBox = QtWidgets.QComboBox(self.tagBox)
        self.typeBox.setGeometry(QtCore.QRect(60, 30, 150, 27))
        self.typeBox.setObjectName("typeBox")
        self.label_3 = QtWidgets.QLabel(self.tagBox)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 68, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tagBox)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 131, 17))
        self.label_4.setObjectName("label_4")
        self.tagEdit = QtWidgets.QLineEdit(self.tagBox)
        self.tagEdit.setGeometry(QtCore.QRect(10, 100, 201, 27))
        self.tagEdit.setObjectName("tagEdit")
        self.selectBox = QtWidgets.QGroupBox(Form)
        self.selectBox.setGeometry(QtCore.QRect(330, 10, 281, 171))
        self.selectBox.setObjectName("selectBox")
        self.label_5 = QtWidgets.QLabel(self.selectBox)
        self.label_5.setGeometry(QtCore.QRect(10, 30, 68, 17))
        self.label_5.setObjectName("label_5")
        self.lv1Button = QtWidgets.QRadioButton(self.selectBox)
        self.lv1Button.setGeometry(QtCore.QRect(10, 50, 141, 22))
        self.lv1Button.setChecked(True)
        self.lv1Button.setObjectName("lv1Button")
        self.lv2Button = QtWidgets.QRadioButton(self.selectBox)
        self.lv2Button.setGeometry(QtCore.QRect(10, 70, 151, 22))
        self.lv2Button.setObjectName("lv2Button")
        self.lv3Button = QtWidgets.QRadioButton(self.selectBox)
        self.lv3Button.setGeometry(QtCore.QRect(10, 90, 131, 22))
        self.lv3Button.setObjectName("lv3Button")
        self.lv4Button = QtWidgets.QRadioButton(self.selectBox)
        self.lv4Button.setGeometry(QtCore.QRect(10, 110, 151, 22))
        self.lv4Button.setObjectName("lv4Button")
        self.lv5Button = QtWidgets.QRadioButton(self.selectBox)
        self.lv5Button.setGeometry(QtCore.QRect(10, 130, 151, 22))
        self.lv5Button.setObjectName("lv5Button")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(340, 210, 301, 181))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 50, 99, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(75, 90, 200, 17))
        self.label_6.setObjectName("label_6")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(40, 140, 211, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton.setGeometry(QtCore.QRect(200, 420, 300, 31))
        self.commandLinkButton.setObjectName("commandLinkButton")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        self.retranslateUi(Form)
        self.init()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PixivSpider"))
        self.LoginBox.setTitle(_translate("Form", "哦！在这登录！"))
        self.label.setText(_translate("Form", "用户名/邮箱："))
        self.label_2.setText(_translate("Form", "密码："))
        self.pushButton.setText(_translate("Form", "登录"))
        self.state_label.setText(_translate("Form", "状态：未登录"))
        self.tagBox.setTitle(_translate("Form", "爬虫目标"))
        self.label_3.setText(_translate("Form", "类型："))
        self.label_4.setText(_translate("Form", "自定义搜索标签："))
        self.selectBox.setTitle(_translate("Form", "筛选过滤"))
        self.label_5.setText(_translate("Form", "过滤类型："))
        self.lv1Button.setText(_translate("Form", "无"))
        self.lv2Button.setText(_translate("Form", "100users入り"))
        self.lv3Button.setText(_translate("Form", "500users入り"))
        self.lv4Button.setText(_translate("Form", "1000users入り"))
        self.lv5Button.setText(_translate("Form", "5000users入り"))
        self.groupBox.setTitle(_translate("Form", "启动爬虫"))
        self.pushButton_2.setText(_translate("Form", "点我启动"))
        self.label_6.setText(_translate("Form", "状态：未启动"))
        self.commandLinkButton.setText(_translate("Form", "https://github.com/NeilKleistGao/PixivSpider"))

    def init(self):
        _translate = QtCore.QCoreApplication.translate
        self.typeBox.insertItem(0, _translate("Form", "自定义搜索"))
        self.typeBox.insertItem(1, _translate("Form", "今日综合排行榜"))
        self.typeBox.insertItem(2, _translate("Form", "本周综合排行榜"))
        self.typeBox.insertItem(3, _translate("Form", "本月综合排行榜"))
        self.typeBox.insertItem(4, _translate("Form", "新人综合排行榜"))
        self.typeBox.insertItem(5, _translate("Form", "原创作品排行榜"))
        self.typeBox.insertItem(6, _translate("Form", "受男性欢迎"))
        self.typeBox.insertItem(7, _translate("Form", "受女性欢迎"))
       

        self.pushButton.clicked.connect(self.clickLogin)
        self.pushButton_2.clicked.connect(self.clickBegin)
        self.commandLinkButton.clicked.connect(self.clickLink)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.spider = PixivSpider()
        self.urls = ["http://www.pixiv.net/search.php?word=%s", 
            "https://www.pixiv.net/ranking.php?mode=daily",
            "https://www.pixiv.net/ranking.php?mode=weekly",
            "https://www.pixiv.net/ranking.php?mode=monthly",
            "https://www.pixiv.net/ranking.php?mode=rookie",
            "https://www.pixiv.net/ranking.php?mode=original",
            "https://www.pixiv.net/ranking.php?mode=male",
            "https://www.pixiv.net/ranking.php?mode=female"]
        self.has_login = False
        self.is_crawling = False
        self.tag = ""

    def clickLogin(self):
        username = self.userEdit.text().strip()
        password = self.passwordEdit.text().strip()
        if self.spider.login(username, password):
            QMessageBox.information(self, "PixivSpider", "登录成功！", QMessageBox.Yes)
            _translate = QtCore.QCoreApplication.translate
            self.state_label.setText(_translate("Form", "状态：已登录"))
            self.has_login = True
        else:
            QMessageBox.information(self, "PixivSpider", "登录失败，请检查你的网络链接或用户名和密码", QMessageBox.Yes)

    def clickBegin(self):
        if self.is_crawling:
            return
        if not self.has_login:
            QMessageBox.information(self, "PixivSpider", "你还没有登录！", QMessageBox.Yes)
            return
        data = self.getInformation()
        if data == None:
            return
        self.spider.crawl(self.tag ,data)
        self.is_crawling = True
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate("Form", "状态：正在爬取..."))

    def clickLink(self):
        webbrowser.open("https://github.com/NeilKleistGao/PixivSpider")

    def getInformation(self):
        data = CrawlData()
        crawl_index = self.typeBox.currentIndex()
        url = self.urls[crawl_index]

        if crawl_index == 0:
            data.is_customize = True
            self.tag = self.tagEdit.text().strip()
            if self.tag == "":
                QMessageBox.information(self, "PixivSpider", "自定义爬取标签不能为空！", QMessageBox.Yes)
                return None
            else:
                url = url % self.tag
        else:
            self.tag = self.typeBox.currentText()
        crawl_level = 0
        if self.lv2Button.isChecked():
            crawl_level = 100
        elif self.lv3Button.isChecked():
            crawl_level = 500
        elif self.lv4Button.isChecked():
            crawl_level = 1000
        elif self.lv5Button.isChecked():
            crawl_level = 5000
        
        data.url = url
        data.lowest_starts = crawl_level
        return data

    def update(self):
        if self.is_crawling:
            schedule = self.spider.getSchedule()
            self.progressBar.setProperty("value", schedule)

            if self.spider.hasFinished():
                self.is_crawling = False
                QMessageBox.information(self, "PixivSpider", "爬取完成！", QMessageBox.Yes)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = mainWidget()
    widget.show()
    sys.exit(app.exec_())