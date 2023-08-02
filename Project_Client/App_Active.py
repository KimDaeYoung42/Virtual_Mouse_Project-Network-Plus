# App_Active.py : 메인 프로그램 관련 코드.
import base64
import sys
import os
import time
import zlib
import io

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QPushButton, QFileDialog, QDesktopWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QScreen
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PIL import Image

import socket
import threading
import pyautogui
from Network_Control import Client
import Network_Packet

from App_Help import Active_Help
import icon_toolbar                                 # 삭제 금지! 비활성화상태라도 활성화되어있음!


class Active_Window(QMainWindow):
    def __init__(self):
        super().__init__()

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
        self.actionFile_Sharing.triggered.connect(self.select_file)
        self.actionFile_Receive.triggered.connect(self.file_send)
        self.actionHelp.triggered.connect(self.help_button)

        # 화면 상단 버튼 (아이콘)
        self.actionNetwork_access.triggered.connect(self.network_view)
        self.actionsharing_on.triggered.connect(self.sharing_start)
        self.actionsharing_off.triggered.connect(self.sharing_stop)
        self.actionreceive_on.triggered.connect(self.receive_start)
        self.actionreceive_off.triggered.connect(self.receive_stop)
        self.actionremote_setting.triggered.connect(self.remote_start)
        self.actionfile_report.triggered.connect(self.network_view)
        self.actionfile_share.triggered.connect(self.select_file)
        self.actionfile_recive.triggered.connect(self.file_send)
        self.actionhelp.triggered.connect(self.help_button)

        # 버튼 클릭 이벤트 연결
        self.push_chat_Button.clicked.connect(self.chatting_send)
        self.push_connect_Button.clicked.connect(self.network_connect)
        self.push_disconnect_Button.clicked.connect(self.network_disconnect)
        self.file_Button1.clicked.connect(self.select_file)
        self.file_Button2.clicked.connect(self.file_send)

        # 임시 버튼 클릭 이벤트 연결
        self.sharing_start_Button.clicked.connect(self.sharing_start)
        self.sharing_stop_Button.clicked.connect(self.sharing_stop)
        self.receive_start_Button.clicked.connect(self.receive_start)
        self.receive_stop_Button.clicked.connect(self.receive_stop)
        # self.remote_start_Button.clicked.connect(self.remote_start)
        # self.remote_stop_Button.clicked.connect(self.remote_stop)

        # 네트워크 관련
        # self.network_box()
        self.network_read_data()

        # 초기화
        self.nickname = ''
        self.user_list = []
        self.network_connect_count = False
        self.chatting_count = False

        # 화면 캡처 관련 (임시)
        self.timer = QTimer(self)
        self.sharing_started = False                        # 화면 공유 관련
        self.receive_started = False                        # 화면 수신 관련

        # 파일 전송 및 수신 관련 (추후 파일 경로 변경!)
        self.send_path = r"C:\Users\user\Desktop\file_send"  # 원본 파일 경로!
        self.recv_path = r"C:\Users\user\Desktop\file_recv"     # 복사될 파일 경로
        os.chmod(self.recv_path, 0o777)
        # self.file_list()



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
            sp1 = msg.split('@', 1)
            # sp1[0] -> SENDBYTE_ACK
            # sp1[1] -> bytes

            # 패킷을 파싱하여 적절한 동작을 한다.
            # 기능별로 함수화 시킬것!
            if sp1[0] == Network_Packet.Login_ACK:
                sp2 = sp1[1].split('#')
                self.text_chat_view.append(f"{sp2[0]}님께서 입장하였습니다.")
                self.person_listWidget.clear()

                sp3 = sp2[1].split('$')
                for list_name in sp3:
                    self.person_listWidget.addItem(list_name)
                # item = QtWidgets.QListWidgetItem(sp1[1])    # 로그인 한 유저 표시
                # self.person_listView.addItem(item)
                # self.person_listWidget.addItem(sp1[1])

            elif sp1[0] == Network_Packet.Logout_ACK:
                sp2 = sp1[1].split('#')
                self.text_chat_view.append(f"{sp2[0]}님께서 퇴장하였습니다.")
                self.person_listWidget.clear()

                sp3 = sp2[1].split('$')
                for list_name in sp3:
                    self.person_listWidget.addItem(list_name)

            elif sp1[0] == Network_Packet.Shortmessage_ACK:
                sp2 = sp1[1].split('#')
                self.text_chat_view.append(f"{sp2[0]} : {sp2[1]}")

            # 파일 데이터 수신
            elif sp1[0] == Network_Packet.Sendfile_ACK:
                self.text_chat_view.append("Sendfile_ACK 메시지 수신")


            # 화면 데이터 수신
            elif sp1[0] == Network_Packet.Sendbyte_ACK:
                print(sp1[1])
                self.receive_started = True
                self.text_chat_view.append("기능 : 화면 데이터 메시지 수신")

                # 이미지 데이터를 QPixmap으로 변환하여 QLabel에 표시
                try:
                    recv_sharing_thread = threading.Thread(target=self.Recv_Screen_Thread, args=(sp1[1],))
                    recv_sharing_thread.daemon = True
                    recv_sharing_thread.start()


                except Exception as e:
                    self.text_chat_view.append("데이터 : base64 디코딩 실패하였습니다. ")
                    print(f"Error displaying image: {e}")
                    # 오류 처리를 원하면 여기에 해당하는 코드를 작성하세요.
                    self.text_chat_view.append("에러 : 알 수 없는 화면1 데이터 수신")

            # 원격 조정 데이터 수신?
            elif sp1[0] == Network_Packet.Sendremote_ACK:
                self.text_chat_view.append("Sendremote_ACK 메시지 수신")


            else:
                self.text_network_view.append('에러 : 알 수 없는 데이터2가 수신되었습니다.')
                self.text_network_view.append('에러 : 아마 이미지 데이터가 수신된 듯 합니다.')


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

            # 로그인 리스트 패킷
            # pack = Network_Packet.Loginlist()
            # self.client.SendData(pack)

        else:
            self.text_network_view.append('에러 : 이미 네트워크 접속되어 있습니다.')

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
            self.person_listWidget.clear()
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
    # 화면공유 시작 버튼 (임시 / 추후 제스처로 변경!)
    def screen_sharing_start(self):
        self.text_network_view.append("화면공유 스레드 시작")
        while True:
            print('화면공유')

            # 모니터 화면 캡처
            screen_image = pyautogui.screenshot()

            # PIL의 Image 타입으로 변환 작업 <- 서버 전송 후 수신에서 처리할까 테스트
            # screen_image = Image.frombytes("RGB", screen_image.size, screen_image.tobytes())

            # 서버로 전송하기 위한 작업
            screen_data = screen_image.tobytes()
            compressed_data = zlib.compress(screen_data)
            length = len(screen_data)

            # 화면 전송
            encoded_data = base64.b64encode(compressed_data)
            pack = Network_Packet.SendByte(encoded_data)
            self.client.SendData(pack)
            # self.client.send_data(pack)     # utf-8 변환 안하고 전송 작업

            # 화면 표시
            # 이미지를 PyQt5의 QImage로 변환
            # qimage = QImage(screen_image.tobytes(), screen_image.size[0], screen_image.size[1], QImage.Format_RGB888)
            # pixmap = QPixmap.fromImage(qimage)
            # self.Webcam_label.setPixmap(pixmap)

            time.sleep(0.3)

    def sharing_start(self):
        if self.network_connect_count:
            self.text_network_view.append('기능 : 화면공유 시작하는 중...')
            self.sharing_started = True

            # 화면 공유 코드
            sharing_thread = threading.Thread(target=self.screen_sharing_start)
            sharing_thread.daemon = True
            # self.threads.append(sharing_thread)
            sharing_thread.start()
        else:
            self.text_network_view.append('오류 : 오프라인 상태에서 화면공유할 수 없습니다.')

    # 화면공유 종료 버튼 (임시 / 추후 제스처로 변경!) : sharing_stop_Button
    def sharing_stop(self):
        if self.network_connect_count:
            if self.sharing_started:
                self.text_network_view.append('기능 : 화면공유 종료하는 중...')
                self.sharing_started = False
                self.timer.stop()

                time.sleep(2)
                self.text_network_view.append('에러 : 화면공유 종료 실패하였습니다.')
                self.text_network_view.append('에러 : 화면공유 기능 중단 되었습니다.')
            else:
                self.text_network_view.append('오류 : 화면공유 기능하지 않고 있습니다.')
        else:
            self.text_network_view.append('오류 : 오프라인 상태 입니다.')

    def Recv_Screen_Thread(self, img):
        while True:
            self.text_chat_view.append("기능 : 화면 데이터 메시지222")

            ## 실제 이미지 데이터 -> UI 출력 파트
            # img -> 문자열 인코딩-> bytes -> 압축 풀면 이미지 데이터가 나온다 화면에 띄운다
            data = img.encode('utf-8')
            decoded_data = base64.b64decode(data)
            img_data = zlib.decompress(decoded_data)

            # decoded_data = base64.b64decode(img)  # 이미지 데이터를 bytes로 변환/ 여기서 예외 발생시 예외 코드로 빠짐
            # recv_image_data = zlib.decompress(decoded_data)

            self.text_chat_view.append("데이터 : base64 디코딩 및 압축 해제 성공하였습니다. ")

            # Bytes 데이터를 -> PIL의 Image 타입으로 변환 작업
            # screen_image = Image.frombytes("RGB", (1920, 1080), recv_image_data)
            screen_image = Image.frombytes("RGB", (1920, 1080), img_data)

            # 이미지 크기를 640x360으로 조정
            width, height = 640, 360
            resized_image = screen_image.resize((width, height), Image.ANTIALIAS)

            # 화면 표시 파트
            # qimage = QImage(screen_image.tobytes(), screen_image.size[0], screen_image.size[1], QImage.Format_RGB888)
            qimage = QImage(resized_image.tobytes(), width, height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.Webcam_label.setPixmap(pixmap)

            time.sleep(0.2)


    # 공유화면 수신 버튼 (임시) : receive_start_Button
    def receive_start(self):
        if self.network_connect_count:
            if self.sharing_started == False:
                self.receive_started = True
                self.text_network_view.append('기능 : 공유화면 수신 시작하는 중...')

                # 공유화면 수신 관련 코드 작성
                # 임시
                self.text_network_view.append('오류 : 공유화면 데이터를 받지 못했습니다.')
                self.text_network_view.append('에러 : 공유화면 수신 실패하였습니다.')

            else:
                self.text_network_view.append('오류 : 현재 화면공유하고 있습니다.')
        else:
            self.text_network_view.append('오류 : 오프라인 상태 입니다.')

    # 공유화면 종료 버튼 (임시) : receive_stop_Button
    def receive_stop(self):
        if self.receive_started:
            self.receive_started = False
            self.text_network_view.append('기능 : 공유화면 종료하는 중...')
        else:
            self.text_network_view.append('오류 : 이미 공유화면을 수신하고 있지 않습니다.')



    # 2. 접속자 리스트뷰 그룹
    # 접속자 리스트뷰 : person_listView
    def person_list(self):
        self.person_listView.append('접속자 리스트 뷰')

    # 원격조정 시작 버튼 : remote_start_Button
    def remote_start(self):
        self.text_network_view.append('기능 : 원격조정 시작하는 중...')

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

    # 원격조정 종료 버튼 : remote_stop_Button
    def remote_stop(self):
        self.text_network_view.append('기능 : 원격조정 종료하는 중...')
        time.sleep(2)
        self.text_network_view.append('에러 : 원격조정 종료 실패하였습니다.')


    # 3. 파일 리스트뷰 그룹
    # 파일 선택
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 선택")
        if file_path:
            self.file_list_widget.addItem(file_path)

    # 클라이언트 파일 현황
    # def file_list(self):
    #     if os.path.exists(self.send_path) and os.path.isdir(self.send_path):
    #         file_path = os.listdir(self.send_path)
    #         self.file_listView.addItems(file_path)
    #     else:
    #         self.text_network_view.append('에러 : 파일을 불러올 수 없습니다.')

    # 파일 전송 : file_send_Button
    def file_send(self):
        # file_path = r"C:\Users\user\Desktop\file_send"     # 원본 파일 경로!

        if self.network_connect_count:
            self.text_network_view.append('기능 : 파일전송 기능 선택')
            selected_file = self.file_list_widget.currentItem()

            if selected_file:
                file_path = selected_file.text()

                if os.path.exists(file_path) and os.path.isfile(file_path):
                    # 1. 파일을 바이트로 변환하기
                    with open(file_path, 'rb') as file:       # 바이너리 읽기 모드 'rb'
                        file_data = file.read()

                    # 2. 바이트 데이터를 문자열로 변환하기
                    file_data_base64 = base64.b64encode(file_data)

                    file_name = os.path.basename(file_path)
                    file_size = len(file_data)

                    # 파일 패킷 생성 및 전송
                    pack = Network_Packet.SendFile(file_name, file_data_base64, file_size)
                    self.client.SendData(pack)

                else:
                    self.text_network_view.append('에러 : 전송할 파일의 경로가 없습니다 (바탕화면 file_send 파일 X)')
            else:
                self.text_network_view.append('에러 : 전송할 파일을 선택해주세요.')
        else:
            self.text_network_view.append('오류 : 오프라인 상태 입니다.')

    # 파일 다운로드 : file_download_Button
    def file_download(self):
        self.text_network_view.append('기능 : 파일다운로드 기능 선택')
        time.sleep(2)
        self.text_network_view.append('에러 : 파일다운로드 실패하였습니다.')


    # 이외. help! 도움!
    def help_button(self):
        # self.app_text_view.append('App : Help!')
        self.help_active.show()


