# App.py : 메인 프로그램.
import sys
from tkinter import messagebox

import psutil
import subprocess
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QCursor
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QDesktopServices

from App_Active import Active_Window
# from App_Gesture import Active_Webcam
from App_Help import Active_Help

import autopy
import icon_toolbar                                 # 삭제 금지! 비활성화상태라도 활성화되어있음!
import pyautogui

#################
# 화면 크기 설정
screen_size = autopy.screen.size()                  # print(screen_size) 1920, 1080 <- 모니터 1대만 사용시 기준
screen_size_x, screen_size_y = screen_size
#################

class App_Control(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI_App.ui", self)
        self.setWindowTitle("가상 인터페이스 프로그램")
        self.setGeometry(100, 100, 320, 330)
        self.setMinimumSize(320, 330)
        self.setMaximumSize(320, 330)

        # 인스턴스 생성
        self.app_window = Active_Window()
        # self.app_webcam = Active_Webcam()
        self.help_active = Active_Help()

        # 초기화 (프로그램 중복실행 방지)
        self.app_start_count = 0

        # 버튼 클릭 이벤트 연결
        self.push_user_Button.clicked.connect(self.start_user)
        self.Button_Exit.clicked.connect(self.stop_program)

        # self.Button_Network_Start.clicked.connect(self.start_network)
        # self.Button_Network_Stop.clicked.connect(self.stop_network)
        # self.Button_Server_Open.clicked.connect(self.open_server)

        # 최상단 UI 버튼 이벤트 연결
        self.actionWindow_Capture.triggered.connect(self.capture_tool)
        self.actionNotepad.triggered.connect(self.notepad_tool)

        self.actionNaver_Map.triggered.connect(self.open_naver_button)
        self.actionDaum_Map.triggered.connect(self.open_daum_button)
        self.actionGoogle_Map.triggered.connect(self.open_google_button)

        self.actionProgram_Close_2.triggered.connect(self.stop_program)

        # 상단 UI 버튼 이벤트 연결
        self.action_Capture.triggered.connect(self.capture_tool)
        self.action_Notepad.triggered.connect(self.notepad_tool)
        self.action_help.triggered.connect(self.help_button)

    # 사용자 버튼 클릭시
    def start_user(self):
        # self.net_connect_box()
        if self.app_start_count == 0:
            self.app_start_count += 1
            self.app_window.show()
            # 추후 ip 연결 동기화 작업
        else:
            self.show_error()

    # 오류 메시지 - 경고창
    def show_error(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("네트워크 오류")
        msg_box.setText("이미 네트워크 접속 중이거나 다중 네트워크 접속 시도 오류입니다.")
        msg_box.setInformativeText("프로그램을 다시 실행시켜주세요")
        msg_box.exec_()

    # 종료 UI 버튼
    def stop_program(self):
        # self.app_text_view.append('App : 프로그램이 종료됩니다')
        QApplication.quit()

    # 상단 UI - toolbar 버튼
    def capture_tool(self):
        # self.app_text_view.append('App : 캡처 기능이 활성화됩니다.')
        capture_tool_path = "C:\windows\system32\SnippingTool.exe"

        capture_process = QProcess(self)
        capture_process.startDetached(capture_tool_path)

    def notepad_tool(self):
        # self.app_text_view.append('App : 메모장 기능이 활성화됩니다.')
        notepad_tool_path = "notepad.exe"

        notepad_process = QProcess(self)
        notepad_process.startDetached(notepad_tool_path)

    def help_button(self):
        # self.app_text_view.append('App : Help!')
        self.help_active.show()

    # Map 버튼
    def open_naver_button(self):
        webbrowser.open('https://map.naver.com/', new=2)

    def open_daum_button(self):
        webbrowser.open('https://map.kakao.com/', new=2)

    def open_google_button(self):
        webbrowser.open('https://www.google.co.kr/maps/', new=2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App_Control()
    window.show()
    sys.exit(app.exec_())
