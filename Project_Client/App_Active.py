# App_Active.py : 메인 프로그램 관련 코드.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt, QRect, pyqtSlot
from PyQt5.uic import loadUi

import socket
from Network_Control import Client
import Network_Packet

from App_Help import Active_Help
import icon_toolbar                                 # 삭제 금지! 비활성화상태라도 활성화되어있음!


class Active_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.ip = ''
        # self.port = 0
        # self.nickname = ''

        # 임시 UI 구성
        loadUi("UI_App_Active.ui", self)
        self.setWindowTitle("가상 인터페이스 프로그램")
        self.setGeometry(430, 100, 1180, 700)
        self.setMinimumSize(1180, 700)

        self.help_active = Active_Help()
        #self.network_read_data()

        # 화면 최상단 (임시 / 수정 필요! )
        self.actionServer_Run.triggered.connect(self.network_view)                  # x
        self.actionServer_Connect.triggered.connect(self.network_view)              # x
        self.actionScreen_Sharing_Start.triggered.connect(self.sharing_start)
        self.actionScreen_Sharing_Stop.triggered.connect(self.sharing_stop)
        self.actionScreen_Receive_Start.triggered.connect(self.receive_start)
        self.actionScreen_Receive_Stop.triggered.connect(self.receive_stop)
        self.actionRemote_Start.triggered.connect(self.remote_start)
        self.actionRemote_Stop.triggered.connect(self.remote_stop)
        self.actionFile_Report.triggered.connect(self.network_view)                 # x
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
        # self.network_read_data()

        # 초기화
        # self.network_connect_count = 0

    #################################################################################################

    # 임시 0. Ip, Port, 접속자명 입력 및 연결&종료
    # 서버 Ip 박스 : text_serverip
    # Port 박스 : text_port
    # 접속자명 박스 : text_nickname
    # 연결 버튼 : push_connect_Button
    # 종료 버튼 : push_disconnect_Button

    # def network_box(self):
    #     self.text_serverip.setReadOnly(True)  # 읽기 전용으로 설정
    #     self.text_port.setReadOnly(True)
    #     self.text_nickname.setReadOnly(True)
    #     # self.network_read_data()

    def network_read_data(self):
        # 파일에서 데이터 읽기 (기존 디볼트 ip : 127.0.0.1와 port : 9000 값 불러오는 것임)
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
        # if not self.network_connect_count == 0:
            self.text_chat_view.append('네트워크 Recv_data 접속 진행 중...')
            self.text_network_view.append(f"수신 메시지 : {msg}")

            # 받은 패킷을 파싱
            sp1 = self.RecvData.split('@')

            # 패킷을 파싱하여 적절한 동작을 한다.
            # 기능별로 함수화 시킬것!
            if sp1[0] == Network_Packet.Shortmessage_ACK:
                sp2 = sp1[1].split('#')
                chat = sp2[0] + ' : ' + sp2[1]
                self.text_chat_view.append(chat)
            elif sp1[0] == Network_Packet.Login_ACK:
                self.myname = sp1[1]
                self.users.append(sp1[1])

        #else:
        #    self.text_chat_view.append('네트워크 Recv_data 접속에 실패하였습니다.')

    # ui에 입력한 ip, port, nickname 정보를 가지고 서버 연결하는 코드 작성 필요함!
    def network_read_ui_data(self):
        self.ip = self.text_serverip.toPlainText()
        self.port = self.text_port.toPlainText()
        self.nickname = self.text_nickname.toPlainText()

    def network_connect(self):
        self.network_read_ui_data()

        print("text1에 적혀있는 글자:", self.ip)
        print("text2에 적혀있는 글자:", self.port)
        print("text3에 적혀있는 글자:", self.nickname)

        # ip = self.ip
        # port = self.port
        # nickname = self.nickname

        ip = '10.101.224.36'
        port = 9000
        nickname = 'test1'
        # self.network_read_ui_data()
        # ip = self.text_serverip.toPlainText()
        # port = self.text_port.toPlainText()
        # nickname = self.text_nickname.toPlainText()

        #if self.network_connect_count == 0:
        #self.network_connect_count += 1
        self.text_network_view.append('네트워크 : 네트워크 연결 중...')
        # combined_text = f"네트워크 연결 : {self.ip} {self.port} {self.nickname}"
        # self.text_edit4.append(combined_text)

        # Client생성 및 서버 연결
        self.client = Client(ip=ip, port=port)
        self.client.open(self.Recv_data)

        # 로그인 패킷 생성 및 전송
        pack = Network_Packet.LogIn(nickname)
        self.client.SendData(pack)

        #else:
        #    self.text_network_view.append('네트워크 : 이미 네트워크 접속되어 있습니다.')

    def network_disconnect(self):
        self.text_network_view.append('네트워크 : 네트워크 연결 종료 중...')
        # self.network_connect_count = 0


    # 공통 0. 네트워크 이벤트뷰
    # self.text_network_view.append('네트워크 이벤트뷰 테스트')
    def network_view(self):
        self.text_network_view.append('네트워크 이벤트뷰 테스트')

    # 0. 채팅 관련
    def chatting_view(self):
        self.text_chat_view.append('채팅 뷰')

    def chatting_send(self):
        self.text_chat_view.append('채팅 테스트')
        # 채팅 전송 버튼은 : push_chat_Button
        # 채팅 전송 버튼 옆 박스 : text_chatting_insert


    # def chatting_send(self):
    #     sp1 = "테스트"
    #     self.text_chat_view.append(sp1 + '채팅 테스트')
    #     # 채팅 전송 버튼은 : push_chat_Button
    #     # 채팅 전송 버튼 옆 박스 : text_chatting_insert

    # 1. 화면 그룹
    # 화면 표현 박스 : Webcam_label
    # 화면공유 시작 버튼 (임시 / 추후 제스처로 변경!) : sharing_start_Button
    def sharing_start(self):
        self.text_network_view.append('기능 : 화면공유 시작하는 중...')
        # 화면 공유 조건 코드 작성필요!

    # 화면공유 종료 버튼 (임시 / 추후 제스처로 변경!) : sharing_stop_Button
    def sharing_stop(self):
        self.text_network_view.append('기능 : 화면공유 종료하는 중...')


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


