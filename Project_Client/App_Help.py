# 도움말 관련 .py

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class Active_Help(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI_Help_Introduction.ui", self)  # UI 파일 로드
        self.setWindowTitle("Introduction")
        # self.setGeometry(570, 130, 970, 615)

