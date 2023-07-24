# App.py : 메인 프로그램.

import sys
import psutil
import subprocess
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap, QCursor
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QDesktopServices

from App_Active import Active_Webcam
# from Network_Con import Active_Network
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
        loadUi("UI_App_Main.ui", self)  # UI 파일 로드
        self.setWindowTitle("가상 인터페이스 프로그램 (개발 0724버전)")
        self.setGeometry(100, 100, 440, 300)

        # 인스턴스 생성
        self.app_active = Active_Webcam()           # 인스턴스 생성.
        self.help_active = Active_Help()

        # 초기화 (프로그램 중복실행 방지)
        self.cap_count = 0
        self.network_count = 0
        self.server_count = 0

        # 버튼 클릭 이벤트 연결
        self.Button_WebCam_Start.clicked.connect(self.start_webcam)
        self.Button_WebCam_Stop.clicked.connect(self.stop_webcam)
        # self.Button_Network_Start.clicked.connect(self.start_network)
        # self.Button_Network_Stop.clicked.connect(self.stop_network)
        # self.Button_Server_Open.clicked.connect(self.open_server)
        self.Button_Exit.clicked.connect(self.stop_program)

        # 상단 UI 버튼 이벤트 연결
        self.action_WebCam_Start.triggered.connect(self.start_webcam)
        self.action_WebCam_Stop.triggered.connect(self.stop_webcam)
        # self.action_NetWork_ON.triggered.connect(self.start_network)
        # self.action_NetWork_OFF.triggered.connect(self.stop_network)

        self.action_Capture.triggered.connect(self.capture_tool)
        self.action_Notepad.triggered.connect(self.notepad_tool)
        self.action_help.triggered.connect(self.help_button)

        # 최상단 UI 버튼 이벤트 연결
        self.actionWindow_Capture.triggered.connect(self.capture_tool)
        self.actionNotepad.triggered.connect(self.notepad_tool)

        self.actionNaver_Map.triggered.connect(self.open_naver_button)
        self.actionDaum_Map.triggered.connect(self.open_daum_button)
        self.actionGoogle_Map.triggered.connect(self.open_google_button)

        self.actionProgram_Close_2.triggered.connect(self.stop_program)

    # 웹캠 UI 버튼
    def start_webcam(self):
        if self.cap_count == 0:
            self.cap_count += 1
            self.app_text_view.append('App : 웹캠 실행 준비 완료')
            self.app_active.show()
            self.app_text_view.append('App : 웹캠이 실행됩니다')
            self.app_active.active_webcam()
        else:
            self.app_text_view.append('App : 웹캠이 이미 실행되고 있습니다.')

    def stop_webcam(self):
        if not self.cap_count == 0:
            self.cap_count = 0
            self.app_text_view.append('App : 웹캠 종료 중...')
            self.app_text_view.append('App : 웹캠이 종료됩니다')

            self.app_active.close()
        else:
            self.app_text_view.append('App : 웹캠이 이미 종료되었습니다.')

    # 네트워크 UI 버튼
    # def start_network(self):
    #     if self.network_count == 0:
    #         self.network_count += 1
    #         self.app_text_view.append('App : 네트워크 실행 준비 완료')
    #
    #         # 임시로 캡처 툴 켜지게 함 (추후 네트워크 클라이언트.exe로 이름 변경하기!)
    #         network_start_path = "C:\windows\system32\SnippingTool.exe"
    #         network_process = QProcess(self)
    #         network_process.startDetached(network_start_path)
    #
    #         self.app_text_view.append('App : 네트워크 기능이 실행됩니다.')
    #     else:
    #         self.app_text_view.append('App : 네트워크 기능이 이미 실행 중입니다.')
    #
    # def stop_network(self):
    #     if not self.network_count == 0:
    #         self.network_count = 0
    #         self.app_text_view.append('App : 네트워크 기능이 종료됩니다.')
    #         # 임시로 캡처 툴 꺼지게 함 (추후 네트워크 클라이언트.exe로 이름 변경하기!)
    #         for proc in psutil.process_iter(['pid', 'name']):
    #             if proc.info['name'] == 'SnippingTool.exe':
    #                 pid = proc.info['pid']
    #                 # 프로세스 종료
    #                 psutil.Process(pid).kill()
    #                 break
    #     else:
    #         self.app_text_view.append('App : 네트워크 기능이 이미 종료되었습니다.')

    # def open_server(self):
    #     if self.server_count == 0:
    #         self.server_count += 1
    #         self.app_text_view.append('App : 서버가 구동됩니다.')
    #     else:
    #         self.app_text_view.append('App : 서버가 이미 구동되었거나 오류가 발생하였습니다.')

    # 종료 UI 버튼
    def stop_program(self):
        self.app_text_view.append('App : 프로그램이 종료됩니다')
        QApplication.quit()

    # 상단 UI - toolbar 버튼
    def capture_tool(self):
        self.app_text_view.append('App : 캡처 기능이 활성화됩니다.')
        capture_tool_path = "C:\windows\system32\SnippingTool.exe"

        capture_process = QProcess(self)
        capture_process.startDetached(capture_tool_path)

    def notepad_tool(self):
        self.app_text_view.append('App : 메모장 기능이 활성화됩니다.')
        notepad_tool_path = "notepad.exe"

        notepad_process = QProcess(self)
        notepad_process.startDetached(notepad_tool_path)

    def help_button(self):
        self.app_text_view.append('App : Help!')
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

