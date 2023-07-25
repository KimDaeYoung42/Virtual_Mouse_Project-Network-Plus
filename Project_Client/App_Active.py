# App_Active.py : 메인 프로그램 관련 코드.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget
from PyQt5.QtCore import Qt, QRect, pyqtSlot
from PyQt5.uic import loadUi
import socket

import Network_Control
import Network_Packet


import icon_toolbar                                 # 삭제 금지! 비활성화상태라도 활성화되어있음!

class Active_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 임시 UI 구성
        loadUi("UI_App_Active.ui", self)  # 추후 UI 파일 제작 후 적용하기.
        self.setWindowTitle("가상 인터페이스 프로그램")
        self.setGeometry(430, 100, 1180, 700)


        # 화면 최상단 (임시 / 수정 필요! )
        self.actionServer_Run.triggered.connect(self.network_view)
        self.actionServer_Connect.triggered.connect(self.network_view)
        self.actionScreen_Sharing_Start.triggered.connect(self.network_view)
        self.actionScreen_Sharing_Stop.triggered.connect(self.network_view)
        self.actionScreen_Receive_Start.triggered.connect(self.network_view)
        self.actionScreen_Receive_Stop.triggered.connect(self.network_view)
        self.actionRemote_Start.triggered.connect(self.network_view)
        self.actionRemote_Stop.triggered.connect(self.network_view)
        self.actionFile_Report.triggered.connect(self.network_view)
        self.actionFile_Sharing.triggered.connect(self.network_view)
        self.actionFile_Receive.triggered.connect(self.network_view)
        self.actionHelp.triggered.connect(self.network_view)

        # 화면 상단 버튼 (아이콘)
        self.actionNetwork_access.triggered.connect(self.network_view)
        self.actionsharing_on.triggered.connect(self.network_view)
        self.actionsharing_off.triggered.connect(self.network_view)
        self.actionreceive_on.triggered.connect(self.network_view)
        self.actionreceive_off.triggered.connect(self.network_view)
        self.actionremote_setting.triggered.connect(self.network_view)
        self.actionfile_report.triggered.connect(self.network_view)
        self.actionfile_share.triggered.connect(self.network_view)
        self.actionfile_recive.triggered.connect(self.network_view)
        self.actionhelp.triggered.connect(self.network_view)

        # 네트워크 관련
        # self.network_box()
        self.network_read_data()

    #################################################################################################

    # 임시 0. Ip, Port, 접속자명 입력 및 연결&종료
    # 서버 Ip 박스 : text_serverip
    # Port 박스 : text_port
    # 접속자명 박스 : text_nickname
    # 연결 버튼 : push_connect_Button
    # 종료 버튼 : push_disconnect_Button
    def network_box(self):
        self.text_serverip.setReadOnly(True)  # 읽기 전용으로 설정
        self.text_port.setReadOnly(True)
        self.text_nickname.setReadOnly(True)
        # self.network_read_data()

    def network_read_data(self):
        # 파일에서 데이터 읽기
        try:
            with open("network_data.txt", "r") as file:
                lines = file.readlines()
                num_lines = len(lines)

                if num_lines >= 1:
                    self.text_serverip.setPlainText(lines[0].strip())

                if num_lines >= 2:
                    self.text_port.setPlainText(lines[1].strip())

                if num_lines >= 3:
                    self.text_nickname.setPlainText(lines[2].strip())
        except FileNotFoundError:
            pass

    # ui에 입력한 ip, port, nickname 정보를 가지고 서버 연결하는 코드 작성 필요함!
    def network_connect(self):
        ip = self.text_serverip()
        port = self.text_port()
        nickname = self.text_nickname()

        # 입력한 정보로 서버 연결
        Network_Control.Connect(sock=self.sock, ip=ip, port=port)

        # 패킷 만들기
        packet = Network_Packet.LogIn(name=nickname)

        # 패킷 전송

    # 공통 0. 네트워크 이벤트뷰
    # self.text_network_view.append('네트워크 이벤트뷰 테스트')
    def network_view(self):
        self.text_network_view.append('네트워크 이벤트뷰 테스트')

    # 0. 채팅 관련
    def chatting_view(self):
        self.text_chat_view.append('채팅 테스트')

    def chatting_send(self):
        self.text_chat_view.append('채팅 테스트')
        # 채팅 전송 버튼은 : push_chat_Button
        # 채팅 전송 버튼 옆 박스 : text_chatting_insert

    # 1. 화면 그룹
    # 화면 표현 박스 : Webcam_label
    # 화면공유 시작 버튼 (임시 / 추후 제스처로 변경!) : sharing_start_Button
    # 화면공유 종료 버튼 (임시 / 추후 제스처로 변경!) : sharing_stop_Button
    # 공유화면 수신 버튼 (임시) : receive_start_Button
    # 공유화면 종료 버튼 (임시) : receive_stop_Button


    # 2. 접속자 리스트뷰 그룹
    # 접속자 리스트뷰 : person_listView
    # 원격조정 시작 버튼 : remote_start_Button
    # 원격조정 종료 버튼 : remote_stop_Button


    # 3. 파일 리스트뷰 그룹
    # 파일 리스트뷰 : file_listView
    # 파일 전송 : file_send_Button
    # 파일 다운로드 : file_download_Button







