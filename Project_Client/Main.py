# main.py : 프로그램 시작점.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget
from PyQt5.QtCore import Qt, QRect
from App import App_Control

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.app_window = App_Control()
#         self.app_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = app_window()
    window = App_Control()
    window.show()
    sys.exit(app.exec_())


__copyright__ = 'Copyright (C) HTML Team (Hand Tracking MotionCapture Lab) 2023 '
__version__ = '2023_07 '
__license__ = 'MIT License'
__developer__ = 'KimDaeYoung42, Woosss99, Su-hwanKim, minseok4266, ELUKA123'
__author_email__ = 'Representative : Hawkthema@gmail.com'
__url__ = 'https://github.com/KimDaeYoung42/Virtual_Mouse_Project'
