# App_Active.py : 메인 프로그램 관련 코드.

import os
import shutil
import sys
import io
import time

import socket
import threading
import tracemalloc

import pyautogui
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QPushButton, QFileDialog, QDesktopWidget, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap, QImage, QScreen
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PIL import Image

import base64
import zlib

import Network_Control
import Network_Packet
from Network_Control import Client
from App_Active_Screen import Active_Screen
from App_Help import Active_Help
import icon_toolbar

# tracemalloc 활성화
tracemalloc.start()

class Active_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi("UI_App_Active.ui", self)
        self.setWindowTitle("가상 인터페이스 프로그램 (일반 사용자용)")
        self.setGeometry(430, 100, 1180, 700)
        self.setMinimumSize(1180, 700)
        self.setMaximumSize(1180, 700)

        self.screen_window = Active_Screen()
        self.help_active = Active_Help()
        self.network_read_data()
        self.text_chat_view.append('안내 : 네트워크 접속하여야 여러 기능을 사용할 수 있습니다.')

        # 화면 최상단 (메뉴 표시줄)
        self.actionNetwork_Connect.triggered.connect(self.network_connect)
        self.actionNetwork_Disconnect.triggered.connect(self.network_disconnect)
        self.actionScreen_Sharing_Start.triggered.connect(self.sharing_start)
        self.actionScreen_Sharing_Stop.triggered.connect(self.sharing_stop)
        # self.actionRemote_Start_2.triggered.connect(self.remote_start)            # do not run in client
        # self.actionRemote_Stop_2.triggered.connect(self.remote_stop)              # do not run in client
        self.actionFile_Select.triggered.connect(self.select_file)
        self.actionFile_Sharing.triggered.connect(self.file_send)
        # self.actionFile_Receive.triggered.connect(self.file_download)             # auto
        self.actionHelp.triggered.connect(self.help_button)

        # 화면 상단 버튼 (도구 모음줄 / Toolbar)
        self.action_Network_ON.triggered.connect(self.network_connect)
        self.action_NetWork_OFF.triggered.connect(self.network_disconnect)
        self.actionsharing_on.triggered.connect(self.sharing_start)
        self.actionsharing_off.triggered.connect(self.sharing_stop)
        # self.actionreceive_on.triggered.connect(self.receive_start)                # auto
        # self.actionreceive_off.triggered.connect(self.receive_stop)                # auto
        # self.actionremote_setting.triggered.connect(self.remote_start)             # do not run in client
        self.actionfile_select.triggered.connect(self.select_file)
        self.actionfile_share.triggered.connect(self.file_send)
        # self.actionfile_recive.triggered.connect(self.file_download)               # auto
        self.actionhelp.triggered.connect(self.help_button)

        # 버튼 클릭 이벤트 연결 1
        self.push_chat_Button.clicked.connect(self.chatting_send)
        self.push_connect_Button.clicked.connect(self.network_connect)
        self.push_disconnect_Button.clicked.connect(self.network_disconnect)
        self.sharing_start_Button.clicked.connect(self.sharing_start)
        self.sharing_stop_Button.clicked.connect(self.sharing_stop)

        self.receive_screen_zoom.clicked.connect(self.screen_window.show)
        self.file_Button1.clicked.connect(self.select_file)
        self.file_Button2.clicked.connect(self.file_send)

        # 버튼 클릭 이벤트 연결 2
        self.text_chatting_insert.installEventFilter(self)
        # self.text_chatting_insert.returnPressed.connect(self.chatting_send)

        # 초기화
        self.nickname = ''
        self.myname = ''
        self.user_list = []
        self.network_connect_count = False
        self.net_open_connected = False
        self.chatting_count = False
        self.close_socket_text = False

        # 화면 캡처 관련
        self.timer = QTimer(self)
        self.sharing_started = False                        # 화면 공유 관련
        self.receive_started = False                        # 화면 수신 관련
        self.screen_dataset = None

        # 파일 전송 및 수신 관련
        self.file_widget_Item_add()
        self.file_name = None
        self.file_data = None
        self.select_file_path = None

        self.send_path = r"C:\Users\user\Desktop\file_send"  # 원본 파일 경로!
        self.recv_path = r"C:\Users\user\Desktop\file_recv"     # 복사될 파일 경로

    # 0.1 최근 사용한 네트워크 접속 정보 가져오기
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

    # 0.2 키보드 입력 관련 모듈
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and source is self.text_chatting_insert):
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                self.chatting_send()
                return True
        return super().eventFilter(source, event)

    # 1. 데이터 수신 파트
    def Recv_data(self, msg):
        if self.network_connect_count:
            try:
                self.network_connect_count = True
                print(f"서버로부터 수신 데이터 : {msg}")

                # 받은 패킷을 파싱
                sp1 = msg.split('@', 1)                 # ex) sp1[0] -> SENDBYTE_ACK // sp1[1] -> bytes

                # 패킷 파싱 -> 적절한 기능을 한다.

                # 1) 로그인 관련
                if sp1[0] == Network_Packet.Login_ACK:
                    sp2 = sp1[1].split('#')
                    self.text_chat_view.append(f"{sp2[0]}님께서 입장하였습니다.")
                    self.person_listWidget.clear()

                    sp3 = sp2[1].split('$')
                    for list_name in sp3:
                        self.person_listWidget.addItem(list_name)

                # 2) 로그아웃 관련
                elif sp1[0] == Network_Packet.Logout_ACK:
                    sp2 = sp1[1].split('#')
                    self.text_chat_view.append(f"{sp2[0]}님께서 퇴장하였습니다.")
                    self.person_listWidget.clear()

                    sp3 = sp2[1].split('$')
                    for list_name in sp3:
                        self.person_listWidget.addItem(list_name)

                # 3) 채팅 관련
                elif sp1[0] == Network_Packet.Shortmessage_ACK:
                    sp2 = sp1[1].split('#')
                    self.text_chat_view.append(f"{sp2[0]} : {sp2[1]}")

                # 4) 파일 데이터 수신
                elif sp1[0] == Network_Packet.Sendfile_ACK:
                    self.text_network_view.append("기능 : 서버로부터 파일 데이터를 수신하였습니다.")
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

                    sp2 = sp1[1].split('#')
                    file_recv_name = sp2[0]
                    file_recv_data = sp2[1]

                    self.text_network_view.append('기능 : 파일 데이터 다운로드 진행 중... (1)')
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                    time.sleep(5)                                                       # file_recv_data 데이터가 전부 받아올때까지 시간 대기
                    self.file_download(file_recv_name, file_recv_data)

                # 5) 화면 데이터 수신
                elif sp1[0] == Network_Packet.Sendbyte_ACK:
                    # print(sp1[1])
                    self.receive_started = True
                    self.text_network_view.append('기능 : 공유화면 데이터 수신하였습니다.')
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

                    try:
                        # 메인 화면
                        self.recv_sharing_thread1 = threading.Thread(target=self.Recv_Screen_Thread, args=(sp1[1],))
                        self.recv_sharing_thread1.daemon = True
                        self.recv_sharing_thread1.start()

                        # 확대 화면 UI 연결
                        self.recv_sharing_thread2 = threading.Thread(target=self.screen_window.Recv_Screen_Thread, args=(sp1[1],))
                        self.recv_sharing_thread2.daemon = True
                        self.recv_sharing_thread2.start()

                    except Exception as e:
                        self.text_chat_view.append("오류 : 공유화면 데이터 수신 실패하였습니다.")
                        self.text_network_view.append("오류 : 공유화면 데이터 수신 실패하였습니다.")
                        self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                        print(f"Error displaying image: {e}")

                # 6) 원격 화면 기능 (클라이언트)
                elif sp1[0] == Network_Packet.Request_Screen_ACK:
                    self.text_network_view.append("기능 : 서버로부터 모니터 화면 요청이 들어왔습니다.")
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                    # 내가 가진 이름과 요청받은 이름이 같을 경우 // 서버에게 화면 공유를 해야한다.
                    if self.myname == sp1[1]:
                        self.sharing_start()

                # 7) 화면 수신 종료 기능 (서버)
                elif sp1[0] == Network_Packet.Sendbytebreak_ACK:
                    self.text_network_view.append("기능 : 서버로부터의 공유화면이 종료되었습니다.")
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

                    # time.sleep(5)
                    self.sharing_started = False  # 화면 공유 관련
                    self.receive_started = False  # 화면 수신 관련

                    # self.recv_sharing_thread1.stop()
                    # self.recv_sharing_thread2.stop()
                    # self.recv_sharing_thread1.join()
                    # self.recv_sharing_thread2.join()

                    self.text_network_view.append("기능 : 정상적으로 공유 화면 수신 종료되었습니다.")
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

                # 8) 공유화면 전송 종료 기능 (클라이언트)
                elif sp1[0] == Network_Packet.Request_Screen_Stop_ACK:
                    self.text_network_view.append("기능 : 서버로부터의 공유화면이 종료되었습니다.")
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                    self.sharing_started = False  # 화면 공유 관련
                    self.receive_started = False  # 화면 수신 관련

                else:
                    self.text_network_view.append('에러 : 알 수 없는 데이터가 수신되었습니다.')
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                    print(f"서버로부터 수신한 알 수 없는 데이터 (1) : {msg}")

            except Exception as e:
                self.text_network_view.append('에러 : 알 수 없는 데이터 오류가 발생하였습니다.')
                self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                print(f"서버로부터 수신한 알 수 없는 데이터 (2) : {msg}")
                print("오류가 발생했습니다 : ", e)

        else:
            self.text_chat_view.append('에러 : 네트워크 접속에 실패하였습니다.')


    # 2. 네트워크 연결, 연결 해제 관련
    # 2.1 네트워크 연결 기능
    def network_connect(self):
        ip = self.text_serverip.toPlainText()
        port = int(self.text_port.toPlainText())
        self.nickname = self.text_nickname.toPlainText()

        if not self.network_connect_count:
            self.text_chat_view.clear()
            self.text_network_view.append('네트워크 : 네트워크 연결 중...')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
            try:
                # (1) Client생성 및 서버 연결
                self.client = Client(ip=ip, port=port)

                if self.client.open(self.Recv_data):
                    # (2) 서버 연결 성공시 - 관련 기능 활성화
                    self.chatting_count = True
                    self.network_connect_count = True
                    self.text_network_view.append('네트워크: 연결되었습니다.')
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                    self.text_chat_view.append('네트워크: 연결되었습니다.')

                    # (3) 로그인 패킷 생성 및 전송
                    pack = Network_Packet.LogIn(self.nickname)
                    self.client.SendData(pack)

                    self.myname = self.nickname

                else:
                    self.text_network_view.append('네트워크: 연결 실패했습니다.')
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                    self.text_chat_view.append('네트워크: 연결 실패했습니다.')

            except Exception as e:
                self.text_network_view.append('에러 : 네트워크 접속에 실패하였습니다.')
                self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                print("네트워크 접속 오류 : ", e)

        else:
            self.text_network_view.append('에러 : 이미 네트워크 접속되어 있습니다.')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

    # 2.2 네트워크 종료 기능
    def network_disconnect(self):
        if self.network_connect_count:
            # (1) 로그아웃 패킷 전송
            pack = Network_Packet.LogOut(self.nickname)
            self.client.SendData(pack)

            # (2) 로그아웃 진행
            time.sleep(3)
            self.network_connect_count = False
            self.chatting_count = False
            self.client.close()
            self.person_listWidget.clear()
            self.text_network_view.append('네트워크 : 연결 종료 되었습니다.')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
            self.text_chat_view.append('네트워크 : 연결 종료 되었습니다.')
        else:
            self.text_network_view.append('에러 : 이미 네트워크 종료되어 있습니다.')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

    # 2.3 소켓 비정상 감지시
    # def network_socket_close(self):
        #     print('network_socket_close 실행됨')
        # socket_run = Network_Control.Client.socket_close_text()
        # self.close_socket_text = socket_run

        # print(f"socket_run : {socket_run}")
        # if socket_run == False:
    #      self.network_disconnect()

    # 3. 채팅 관련
    def chatting_view(self):
        self.text_chat_view.append('채팅 뷰')

    # 3.1 채팅 전송 기능
    def chatting_send(self):
        if self.network_connect_count:
            self.text_network_view.append('기능 : 채팅 메시지를 서버에 전송했습니다.')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

            chatting_text = self.text_chatting_insert.toPlainText()

            # 로그인 패킷 생성 및 전송
            pack = Network_Packet.ShortMessage(self.nickname, chatting_text)
            self.client.SendData(pack)

            self.text_chatting_insert.clear()
        else:
            self.text_chat_view.append('오류 : 오프라인 상태 입니다.')


    # 4. 파일 기능 관련
    # 4.1 파일 선택
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 선택")

        # 파일 복사
        send_path = r"C:\Users\user\Desktop\file_send"
        shutil.copy(file_path, send_path)

        self.file_widget_Item_add()

    # 4.2 클라이언트 파일 리스트
    def file_widget_Item_add(self):
        self.file_list_widget.clear()
        path = r"C:\Users\user\Desktop\file_send"  # 원본 파일 경로!

        # 특정 경로에 있는 파일들을 가져와서 QListWidget에 추가
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                item = QListWidgetItem(filename)
                self.file_list_widget.addItem(item)

    # 4.3 파일 전송 기능
    def file_send(self):
        if self.network_connect_count:
            self.text_network_view.append('기능 : 파일전송 기능 선택')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
            send_file_path = r"C:\Users\user\Desktop\file_send"  # 원본 파일 경로!
            selected_file = self.file_list_widget.currentItem()

            if selected_file:
                file_send_name = selected_file.text()
                file_path = send_file_path + f'\{file_send_name}' ### 여기 코드가 문제 있음.

                if os.path.exists(file_path) and os.path.isfile(file_path):
                    # (1) 파일을 바이트로 변환하기
                    with open(file_path, 'rb') as file:       # 바이너리 읽기 모드 'rb'
                        file_data = file.read()

                    # (2) 바이트 데이터를 문자열로 변환하기
                    based_file_data = base64.b64encode(file_data)

                    file_send_name = os.path.basename(file_path)
                    # file_size = len(file_data)

                    # (3) 파일 패킷 생성 및 전송
                    pack = Network_Packet.SendFile(file_send_name, based_file_data)
                    self.client.SendData(pack)
                    self.text_network_view.append('기능 : 파일이 성공적으로 전달되었습니다.')
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

                else:
                    self.text_network_view.append('에러 : 전송할 파일의 경로가 없습니다')
                    self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
            else:
                self.text_network_view.append('에러 : 전송할 파일을 선택해주세요.')
                self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
        else:
            self.text_network_view.append('오류 : 오프라인 상태 입니다.')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

    # 4.4 파일 다운로드 (자동)
    def file_download(self, file_download_name, file_ddata):
        self.text_network_view.append('기능 : 전송받은 파일이 있습니다.')
        self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

        try:
            self.text_network_view.append('기능 : 파일을 download 파일에 저장 중...(2)')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
            download_path = r"C:\Users\user\Downloads\test"  # 파일 다운로드 경로

            # (1) 경로가 존재하지 않는 경우 디렉토리를 생성하고 빈 파일을 만듭니다.
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            # (2) 파일 확장자 분리
            dencode_filedata = base64.b64decode(file_ddata)

            # (3) 파일 저장
            save_path = os.path.join(download_path, file_download_name)

            with open(save_path, 'wb') as file:
                file.write(dencode_filedata)

            print(f"파일 수신 및 저장 성공: {file_download_name}")
            self.text_network_view.append(f"파일 수신 및 저장 성공: {file_download_name}")
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

            # self.file_widget_Item_add()

        except Exception as e:
            print(f"파일 수신 및 저장 중 오류 발생: {e}")


    # 5. 화면 공유 관련
    # 5.1 화면 공유 코드
    def screen_sharing_start(self):
        #if self.receive_started == False:          # false 명령어 불가
            print("화면공유 스레드 시작")

            while self.sharing_started:
                # (1) 모니터 화면 캡처
                screen_image = pyautogui.screenshot()

                # (2) 서버로 전송하기 위한 작업
                screen_data = screen_image.tobytes()
                compressed_data = zlib.compress(screen_data)
                length = len(screen_data)

                # (3) 화면 전송
                encoded_data = base64.b64encode(compressed_data)
                pack = Network_Packet.SendByte(encoded_data)
                self.client.SendData(pack)

                self.text_network_view.append("기능 : 화면공유 중...")
                self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

                # (4) 이미지를 PyQt5의 QImage로 변환 (이미지 크기를 640x360으로 조정)
                width, height = 640, 360
                resized_image = screen_image.resize((width, height), Image.ANTIALIAS)

                # (5) 화면 표시 파트
                qimage = QImage(resized_image.tobytes(), width, height, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                self.Webcam_label.setPixmap(pixmap)

                time.sleep(0.1)

                # (6) 화면 공유 종료
                if self.sharing_started == False:
                    break
        #else:
            #self.text_network_view.append("에러 : 이미 공유화면 수신하고 있어, 화면 공유를 할 수 없습니다.")
            #self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
    
    # 5.2 화면 공유 시작 기능
    def sharing_start(self):
        if self.network_connect_count:
            #if self.receive_started == False:
                self.text_network_view.append('기능 : 화면공유 시작하는 중...')
                self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                self.sharing_started = True

                # 화면 공유 코드
                sharing_thread = threading.Thread(target=self.screen_sharing_start)
                sharing_thread.daemon = True
                # self.threads.append(sharing_thread)
                sharing_thread.start()
            #else:
            #    self.text_network_view.append('오류 : 이미 공유화면 수신하고 있어, 화면 공유를 할 수 없습니다.')
            #   self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
        else:
            self.text_network_view.append('오류 : 오프라인 상태에서 화면 공유할 수 없습니다.')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

    # 5.3 화면 공유 종료 기능
    def sharing_stop(self):
        if self.network_connect_count:
            if self.sharing_started:
                self.text_network_view.append('기능 : 화면공유 종료하는 중...')
                self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
                # self.timer.stop()
                self.sharing_started = False
                self.receive_started = False

                # self.recv_sharing_thread1.stop()
                # self.recv_sharing_thread2.stop()
                # self.sharing_thread.stop()
                # self.sharing_thread.join()
                # self.Webcam_label.setPixmap(None)
                time.sleep(2)
                self.text_network_view.append('기능 : 화면공유 종료되었습니다.')
                self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

            else:
                self.text_network_view.append('오류 : 화면공유 기능하지 않고 있습니다.')
                self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
        else:
            self.text_network_view.append('오류 : 오프라인 상태 입니다.')
            self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

    # 5.4 공유 화면 수신 기능
    def Recv_Screen_Thread(self, img):
        while True:
            print("기능 : 화면 데이터 메시지222")
            self.receive_started = True

            # (1) 데이터 검증 작업
            if self.screen_dataset is None:
                # (2) dataset이 비어있는 경우, data를 바로 저장
                self.screen_dataset = img
                data_img = self.screen_dataset
                break
            else:
                # (3) img가 이전 데이터와 동일한 경우, 이전 데이터 삭제
                if img == self.screen_dataset:
                    self.screen_dataset = None
                    data_img = None
                    break

                else:
                    # (4) img가 이전 데이터와 다른 경우, data를 저장하고 이전 데이터 삭제
                    self.screen_dataset = img
                    data_img = self.screen_dataset

                    # (5) 실제 이미지 데이터 -> UI 출력 파트
                    data = data_img.encode('utf-8')
                    decoded_data = base64.b64decode(data)
                    img_data = zlib.decompress(decoded_data)

                    # (6) 데이터를 UI에 추가하거나 갱신
                    self.update_screen(img_data)
                    break

    # 5.5 공유 화면 수신 조정 기능
    def update_screen(self, img_data):
        # (1) Bytes 데이터를 -> PIL의 Image 타입으로 변환 작업
        screen_image = Image.frombytes("RGB", (1920, 1080), img_data)

        # (2) 이미지 크기를 640x360으로 조정
        width, height = 640, 360
        resized_image = screen_image.resize((width, height), Image.ANTIALIAS)

        # (3) 화면 표시 파트
        qimage = QImage(resized_image.tobytes(), width, height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.Webcam_label.setPixmap(pixmap)

    # 6. 원격 조정 기능 (* 클라이언트 비활성화 사항)
    # 6.1 원격조정 시작 기능
    def remote_start(self):
        self.text_network_view.append('기능 : 원격조정 시작하는 중...')
        self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

        # 원격 조정할 유저 선택
        selected_items = self.person_listWidget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            index = self.person_listWidget.indexFromItem(selected_item).row()
            print(self.nickname)
            print(selected_item)
            if selected_item == self.nickname:
                QtWidgets.QMessageBox.warning(self, "선택 오류", "자기 자신을 원격조정할 수 없습니다.")
            else:
                QtWidgets.QMessageBox.information(self, "선택 확인", f"{index + 1}번 유저를 선택했습니다.")
        else:
            QtWidgets.QMessageBox.warning(self, "선택 오류", "원격 조정할 유저를 선택해주세요.")

        self.text_network_view.append('에러 : 원격조정에 실패하였습니다.')
        self.text_network_view.moveCursor(self.text_network_view.textCursor().End)

    # 6.2 원격조정 종료 기능
    def remote_stop(self):
        self.text_network_view.append('기능 : 원격조정 종료하는 중...')
        self.text_network_view.moveCursor(self.text_network_view.textCursor().End)
        time.sleep(2)
        self.text_network_view.append('에러 : 원격조정 종료 실패하였습니다.')
        self.text_network_view.moveCursor(self.text_network_view.textCursor().End)


    # 7. 이외. help! 도움!
    def help_button(self):
        # self.app_text_view.append('App : Help!')
        self.help_active.show()


