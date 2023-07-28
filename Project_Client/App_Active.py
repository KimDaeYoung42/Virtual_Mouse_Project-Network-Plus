# App_Active.py : 메인 프로그램 관련 코드.

import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt, QRect, pyqtSlot
from PyQt5.uic import loadUi

import socket
from Network_Control import Client
import Network_Packet

import threading
import pyautogui
import io
from PIL import Image
import zlib

from App_Help import Active_Help
import icon_toolbar  # 삭제 금지! 비활성화상태라도 활성화되어있음!


class Active_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # 임시 UI 구성
        loadUi("UI_App_Active.ui", self)
        self.setWindowTitle("가상 인터페이스 프로그램")
        self.setGeometry(430, 100, 1180, 700)
        self.setMinimumSize(1180, 700)

        self.help_active = Active_Help()
        # self.network_read_data()

        # 화면 최상단 (임시 / 수정 필요! )
        self.actionServer_Run.triggered.connect(self.network_view)  # x
        self.actionServer_Connect.triggered.connect(self.network_view)  # x
        self.actionScreen_Sharing_Start.triggered.connect(self.sharing_start)
        self.actionScreen_Sharing_Stop.triggered.connect(self.sharing_stop)
        self.actionScreen_Receive_Start.triggered.connect(self.receive_start)
        self.actionScreen_Receive_Stop.triggered.connect(self.receive_stop)
        self.actionRemote_Start.triggered.connect(self.remote_start)
        self.actionRemote_Stop.triggered.connect(self.remote_stop)
        self.actionFile_Report.triggered.connect(self.network_view)  # x
        self.actionFile_Sharing.triggered.connect(self.file_send)
        self.actionFile_Receive.triggered.connect(self.file_download)
        self.actionHelp.triggered.connect(self.help_button)

        # 화면 상단 버튼 (아이콘)
        self.actionNetwork_access.triggered.connect(self.network_view)
        self.actionsharing_on.triggered.connect(self.sharing_start)
        self.actionsharing_off.triggered.connect(self.sharing_stop)
        self.actionreceive_on.triggered.connect(self.receive_start)
        self.actionreceive_off.triggered.connect(self.receive_stop)
        self.actionremote_setting.triggered.connect(self.remote_start)
        self.actionfile_report.triggered.connect(self.network_view)
        self.actionfile_share.triggered.connect(self.file_send)
        self.actionfile_recive.triggered.connect(self.file_download)
        self.actionhelp.triggered.connect(self.help_button)

        # 버튼 클릭 이벤트 연결
        self.push_chat_Button.clicked.connect(self.chatting_send)
        self.push_connect_Button.clicked.connect(self.network_connect)
        self.push_disconnect_Button.clicked.connect(self.network_disconnect)
        self.file_send_Button.clicked.connect(self.file_send)
        self.file_download_Button.clicked.connect(self.file_download)

        # 임시 버튼 클릭 이벤트 연결
        self.sharing_start_Button.clicked.connect(self.sharing_start)
        self.sharing_stop_Button.clicked.connect(self.sharing_stop)
        self.receive_start_Button.clicked.connect(self.receive_start)
        self.receive_stop_Button.clicked.connect(self.receive_stop)
        self.remote_start_Button.clicked.connect(self.remote_start)
        self.remote_stop_Button.clicked.connect(self.remote_stop)

        # 네트워크 관련
        # self.network_box()
        self.network_read_data()

        # 초기화
        self.network_connect_count = False
        self.chatting_count = False

        # self.ip = ''
        # self.port = 0
        self.nickname = ''

        self.is_sharing = False
        self.screen_size = 0.7

        self.user_list = []

        #################################################################################################

    # 임시 0. Ip, Port, 접속자명 입력 및 연결&종료
    # 서버 Ip 박스 : text_serverip
    # Port 박스 : text_port
    # 접속자명 박스 : text_nickname
    # 연결 버튼 : push_connect_Button
    # 종료 버튼 : push_disconnect_Button

    # 0. 네트워크 - 편의성 기능 (미리 ip, port 저장된 값 불러오기)
    def network_read_data(self):
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

                print(self.text_serverip, self.text_port, self.text_nickname)

        except FileNotFoundError:
            pass

    def Recv_data(self, msg):
        if self.network_connect_count:
            self.text_network_view.append(f"서버로부터 수신 데이터 : {msg}")

            # 받은 패킷을 파싱
            sp1 = msg.split('@')

            # 패킷을 파싱하여 적절한 동작을 한다.
            # 기능별로 함수화 시킬것!
            if sp1[0] == Network_Packet.Login_ACK:
                self.text_chat_view.append(f"{sp1[1]}님께서 입장하였습니다.")

            elif sp1[0] == Network_Packet.Loginlist_ACK:
                self.user_list = []

            elif sp1[0] == Network_Packet.Logout_ACK:
                self.text_chat_view.append(f"{sp1[1]}님께서 퇴장하였습니다.")

            elif sp1[0] == Network_Packet.Shortmessage_ACK:
                sp2 = sp1[1].split('#')
                self.text_chat_view.append(f"{sp2[0]} : {sp2[1]}")

            # 파일 데이터 수신
            elif sp1[0] == Network_Packet.Sendfile_ACK:
                self.text_chat_view.append("Sendfile_ACK 메시지 수신")

            # 바이트배열 수신(화면공유 기능)
            elif sp1[0] == Network_Packet.Sendbyte_ACK:
                self.text_chat_view.append("Sendbyte_ACK 메시지 수신")      # 1초에 33번옴
                # 받은 bytes를 bitmap으로 변환 -> 화면에 출력
                bytes_data = sp1[1]     # str -> bytes로 변환
                data = bytes_data.encode('utf-8')
                ms = io.BytesIO(data)
                bitmap = Image.open(ms)
                self.Webcam_label.setPixmap(bitmap)

            # 원격 조정 데이터 수신?
            elif sp1[0] == Network_Packet.Sendremote_ACK:
                self.text_chat_view.append("Sendremote_ACK 메시지 수신")

            else:
                self.text_network_view.append('에러 : 알 수 없는 데이터가 수신되었습니다.')

        else:
            self.text_chat_view.append('에러 : 네트워크 Recv_data 접속에 실패하였습니다.')

    def network_connect(self):
        ip = self.text_serverip.toPlainText()
        port = int(self.text_port.toPlainText())
        self.nickname = self.text_nickname.toPlainText()

        if not self.network_connect_count:
            self.network_connect_count = True
            self.chatting_count = True
            self.text_network_view.append('네트워크 : 네트워크 연결되었습니다.')

            # Client생성 및 서버 연결
            self.client = Client(ip=ip, port=port)
            self.client.open(self.Recv_data)

            # 로그인 패킷 생성 및 전송
            pack = Network_Packet.LogIn(self.nickname)
            self.client.SendData(pack)

            # 로그인 리스트를 달라고 패킷을 보낸다
            # 스레드를 만들어서 N초에 한번씩 리스트를 갱신하도록한다.
            self.user_list_thread = threading.Thread(target=self.get_userlist)
            self.user_list_thread.daemon = True
            self.user_list_thread.start()

        else:
            self.text_network_view.append('에러 : 이미 네트워크 접속되어 있습니다.')

    def get_userlist(self):
        while True:
            pack = Network_Packet.LogInlist()
            self.client.SendData(pack)

            time.sleep(1)


    def network_disconnect(self):
        if self.network_connect_count:

            # 로그아웃 패킷 전송
            pack = Network_Packet.LogOut(self.nickname)
            self.client.SendData(pack)

            # 로그아웃 진행
            time.sleep(3)
            self.network_connect_count = False
            self.chatting_count = False
            self.client.close()
            self.text_network_view.append('네트워크 : 네트워크 연결 종료 되었습니다.')
        else:
            self.text_network_view.append('에러 : 이미 네트워크 종료되어 있습니다.')

    # 공통 0. 네트워크 이벤트뷰
    # self.text_network_view.append('네트워크 이벤트뷰 테스트')
    def network_view(self):
        self.text_network_view.append('네트워크 이벤트뷰 테스트')

    # 0. 채팅 관련
    def chatting_view(self):
        self.text_chat_view.append('채팅 뷰')

    def chatting_send(self):
        if self.network_connect_count:
            self.text_network_view.append('채팅 메시지를 서버에 전송했습니다.')

            chatting_text = self.text_chatting_insert.toPlainText()

            # 로그인 패킷 생성 및 전송
            pack = Network_Packet.ShortMessage(self.nickname, chatting_text)
            self.client.SendData(pack)

            # 채팅 전송 버튼은 : push_chat_Button
            # 채팅 전송 버튼 옆 박스 : text_chatting_insert
        else:
            self.text_chat_view.append('오류 : 오프라인 상태 입니다.')

    # 1. 화면 그룹
    # 화면 표현 박스 : Webcam_label
    # 화면공유 시작 버튼 (임시 / 추후 제스처로 변경!) : sharing_start_Button
    def sharing_start(self):
        self.text_network_view.append('기능 : 화면공유 시작하는 중...')

        self.is_sharing = True

        # 화면공유 스레드를 생성 --> 스레드 내부에서 화면공유 패킷을 보냄
        # 화면공유 --> 화면의 bitmap 데이터를 byte배열로 전환해서 패킷을 보냄
        thread = threading.Thread(target=self.capture_Thread)
        thread.daemon = True
        thread.start()

    def capture_Thread(self):
        while self.is_sharing:
            image = pyautogui.screenshot()
            image = image.resize((int(image.size[0]*(self.screen_size)), int(image.size[1] * (self.screen_size))))
            data = image.tobytes()
            data = zlib.compress(data)
            # 2. 패킷 구성
            pack = Network_Packet.SendByte(data)
            # 3 전송
            self.client.SendData(pack)

            time.sleep(0.03)        # 1초에 33

    # 화면공유 종료 버튼 (임시 / 추후 제스처로 변경!) : sharing_stop_Button
    def sharing_stop(self):
        self.text_network_view.append('기능 : 화면공유 종료하는 중...')
        self.is_sharing = False

    # 공유화면 수신 버튼 (임시) : receive_start_Button
    def receive_start(self):
        self.text_network_view.append('기능 : 공유화면 수신 시작하는 중...')

    # 공유화면 종료 버튼 (임시) : receive_stop_Button
    def receive_stop(self):
        self.text_network_view.append('기능 : 공유화면 종료하는 중...')

        # 2. 접속자 리스트뷰 그룹

    # 접속자 리스트뷰 : person_listView
    def person_list(self):
        self.person_listView.append('접속자 리스트 뷰')

    # 원격조정 시작 버튼 : remote_start_Button
    def remote_start(self):
        self.text_network_view.append('기능 : 원격조정 시작하는 중...')

    # 원격조정 종료 버튼 : remote_stop_Button
    def remote_stop(self):
        self.text_network_view.append('기능 : 원격조정 종료하는 중...')

    # 3. 파일 리스트뷰 그룹
    # 파일 리스트뷰 : file_listView
    def file_list(self):
        self.file_listView.append('파일 리스트 뷰')

    # 파일 전송 : file_send_Button
    def file_send(self):
        self.text_network_view.append('기능 : 파일전송 기능 선택')

    # 파일 다운로드 : file_download_Button
    def file_download(self):
        self.text_network_view.append('기능 : 파일다운로드 기능 선택')

    # 이외. help! 도움!
    def help_button(self):
        # self.app_text_view.append('App : Help!')
        self.help_active.show()
