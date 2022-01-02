from PyQt5.QtWidgets import *
import sys
from PyQt5 import uic
import os
import chromedriver_autoinstaller # pip install chromedriver-autoinstaller
from selenium import webdriver
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
import time
import random
import urllib.request as req

ui_file = "./instagram.ui"
class SeleniumWorker(QObject):
    login_progress_signal = pyqtSignal(int)
    login_success_signal = pyqtSignal(bool)
    search_progress_signal = pyqtSignal(int)
    content_signal = pyqtSignal(str)
    image_signal = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self, None)
        self.browser = webdriver.Chrome(chromedriver_autoinstaller.install())
        self.input_id = ""
        self.input_pw = ""
        self.keyword = ""
    def search(self):
        # 해시태그 검색
        self.search_progress_signal.emit(10)
        url = f"https://www.instagram.com/explore/tags/{self.keyword}/?hl=ko"
        self.search_progress_signal.emit(30)
        self.browser.get(url)
        self.search_progress_signal.emit(50)
        time.sleep(6)
        self.search_progress_signal.emit(70)
        # 첫번째 게시물 클릭
        first_photo = self.browser.find_element_by_css_selector("div._9AhH0")
        self.search_progress_signal.emit(90)
        first_photo.click()
        self.search_progress_signal.emit(95)
        time.sleep(5)
        self.search_progress_signal.emit(100)
        while True:
            like = self.browser.find_element_by_css_selector("section.ltpMr.Slqrh div.QBdPU.rrUvL svg._8-yf5")
            value = like.get_attribute("aria-label")
            next = self.browser.find_element_by_css_selector("div.l8mY4.feth3 > button.wpO6b")
            ### 크롤링 ###
            content = self.browser.find_element_by_css_selector("div.C4VMK > span")
            self.content_signal.emit(content.text)
            try:
                img = self.browser.find_element_by_css_selector("article.M9sTE.L_LMM.JyscU.ePUX4 div.KL4Bh > img")
                img_url = img.get_attribute("src")
            except:  # 게시물이 영상이라면?
                img = self.browser.find_element_by_css_selector("video.tWeCl")
                img_url = img.get_attribute("poster")
            self.image_signal.emit(img_url)
            if value == "좋아요":
                like.click()
                time.sleep(30)
                next.click()
                time.sleep(30)
                # time.sleep(3)
            else:
                next.click()
                time.sleep(30)
                # time.sleep(3)

    def login(self):
        self.login_progress_signal.emit(10)
        self.browser.get("https://www.instagram.com/accounts/login/")
        self.login_progress_signal.emit(20)
        time.sleep(3)
        self.login_progress_signal.emit(30)
        id = self.browser.find_element_by_name("username")
        self.login_progress_signal.emit(40)
        id.send_keys(self.input_id)  # 본인 계정 적어주세요.
        self.login_progress_signal.emit(50)
        pw = self.browser.find_element_by_name("password")
        self.login_progress_signal.emit(60)
        pw.send_keys(self.input_pw)  # 본인 계정 적어주세요.
        self.login_progress_signal.emit(70)
        button = self.browser.find_element_by_css_selector("div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB")
        self.login_progress_signal.emit(80)
        button.click()
        self.login_progress_signal.emit(90)
        time.sleep(5)
        self.login_progress_signal.emit(100)
        if self.browser.current_url == "https://www.instagram.com/accounts/login/":
            self.login_success_signal.emit(False)
        else:
            self.login_success_signal.emit(True)

class MainDialog(QDialog):
    login_signal = pyqtSignal()
    search_signal = pyqtSignal()
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)
        ### 쓰레드 할당 ###
        self.worker = SeleniumWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.start()
        ####################

        self.login_progressbar.setValue(0)
        self.search_progressbar.setValue(0)
        self.button_search.setEnabled(False)
        self.button_login.clicked.connect(self.login_button_clicked)
        self.login_signal.connect(self.worker.login)
        self.worker.login_progress_signal.connect(self.login_progressbar.setValue)
        self.worker.login_success_signal.connect(self.login_finish)
        self.button_search.clicked.connect(self.search_button_clicked)
        self.search_signal.connect(self.worker.search)
        self.worker.search_progress_signal.connect(self.search_progressbar.setValue)
        self.worker.content_signal.connect(self.show_content)
        self.worker.image_signal.connect(self.show_image)

    def show_image(self, img_url):
        data = req.urlopen(img_url).read()  # 이미지 데이터 받아오기
        pixmap = QPixmap()  # 이미지를 담을 수 있는 장바구니
        pixmap.loadFromData(data)  # 장바구니에 이미지를 넣음
        pixmap = pixmap.scaled(250, 250)
        self.img_label.setPixmap(pixmap)

    def show_content(self, content):
        self.text_label.clear()
        self.text_label.append(content)

    def search_button_clicked(self):
        self.button_search.setEnabled(False)
        self.search_status.setText("해시태그 검색 중...")
        keyword = self.input_search.text()
        self.worker.keyword = keyword
        self.search_signal.emit()



    def login_finish(self, data):
        if data == False:
            self.login_status.setText("로그인 실패! 다시 시도하세요.")
            self.button_login.setEnabled(True)
        else:
            self.login_status.setText("로그인 성공!")
            self.button_search.setEnabled(True)


    def login_button_clicked(self):
        self.button_login.setEnabled(False)
        user_id = self.input_id.text()
        user_pw = self.input_pw.text()
        self.worker.input_id = user_id
        self.worker.input_pw = user_pw
        self.login_signal.emit()




QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())