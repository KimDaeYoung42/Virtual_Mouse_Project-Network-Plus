# App_Gesture.py : 마우스, 키보드 기능 코드 1번.

import sys
import subprocess
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QCursor
from tensorflow.keras.models import load_model

import cv2
import mediapipe as mp
import math
from HandTrackingModule import HandDetector
from Mouse_Module import MouseFunction
import Network_Packet

import autopy
import pyautogui
import time
import pygetwindow as gw
import numpy as np
import threading
import socket

#################
# 모니터 화면 크기 설정
screen_size = autopy.screen.size()                  # print(screen_size) 1920, 1080 <- 모니터 1대만 사용시 기준
screen_size_x, screen_size_y = screen_size

# 윈도우 확대 축소 기능 - 원래 윈도우 사이즈를 위한 변수들.
# window_original_width = None
# window_original_height = None

#################

class Active_Webcam(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 관련
        loadUi("UI_App_WebCam.ui", self)      # UI 파일 로드
        self.setWindowTitle("가상 인터페이스 프로그램")
        self.setGeometry(100, 440, 950, 420)
        self.setMinimumSize(950, 420)

        # 웹캠 관련
        # self.cap = None                                                     # 웹캠 객체
        self.is_running = True                                             # 웹캠 실행 여부 flag

        self.hand_detector = HandDetector()                                 # 인스턴스 생성.
        self.text_view.append('웹캠 실행 중...')

        # 초기화
        self.start_time = 0
        self.active_stop = False                                            # 마우스 행동 해제 (False : 비활성화 / True : 활성화)
        self.hand_detect_count = 0

        # 초기화 - 클릭, 더블클릭, 스크롤, 드래그 관련
        self.Lclick_count = 0
        self.LDclick_count = 0
        self.Rclick_count = 0
        self.RDclick_count = 0
        self.Scroll_count = 0
        self.Drag_count = 0
        self.Fuck_count = 0
        self.Good_count = 0

        self.Window_zoom = 0
        self.Keyboard_count = 0

        # 드래그 관련 초기화
        self.dragging = False                                               # 드래그 상태 플래그
        self.start_drag_pos = None                                          # 드래그 시작 좌표

        # Webcam에 대한 스레드 생성
        self.thread = threading.Thread(target=self.update_frame)
        self.thread.daemon = True
        self.thread.start()

        self.server = None
        self.recv_del = None
        self.sockets = []

        self.port = 9000

        self.Init()

        self.Run(self.Server_RecvData)

        # 서버 인스턴스 생성
        # self.server = Server()

        # self.Run()

    def update_frame(self):

        cap = cv2.VideoCapture(0)                                      # 웹캠 번호 (0은 기본 웹캠)
        seq = []
        action_seq = []
        model = load_model('models/model.h5')
        actions = ['none', 'move', 'click', 'ok']

        while self.is_running:
            ret, frame = cap.read()                                        # 웹캠 프레임 읽기
            
            frame = cv2.flip(frame, 1)                                      # 웹캠 좌우 반전
            frame = self.hand_detector.find_hands(frame)
            left_lm_list = []
            right_lm_list = []
            lm_list, label = self.hand_detector.find_positions(frame)
            action = self.hand_detector.action_estimation(frame, seq, action_seq, model, actions)
            # action --> 제스쳐에 대한 액션 ex) 'Move' 등 이 들어간다.

            if lm_list:
                print(label)

                # action에 따라 self.SendData(sock, msg, size)


            # 프레임 화면에 출력
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_img)
            self.Webcam_label.setPixmap(q_pixmap)

    def Init(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind('0.0.0.0'. server_port)
        self.server.listen(20)

        print('서버 시작...... 클라이언트 접속 대기중')    

    def Run(self, fun):
        self.recv_del = fun
        while True:
            try:
                client_socket, client_address = self.server.accept()
                self.sockets.append(client_socket)
                
                ip, port = client_address
                print(f"{ip}, {port} 접속")

                thread = threading.Thread(self, target=self.WorkThread)
                thread.daemon = True
                thread.start()

            except Exception as e:
                print(e)

    def WorkThread(self, clinet_socket):
        try:
            while True:
                data = clinet_socket.recv(1024)
                if not data:
                    break
                msg = data.decode().strip('\0')
                self.recv_del(clinet_socket, msg)
        except Exception as e:
            print(e)
            self.sockets.remove(clinet_socket)
            clinet_socket.close()

    # 데이터 송/수신 
    def SandData(self, sock, msg):
        bmsg = msg.encode('utf-8')
        self.Send_Data(sock, bmsg)
        ret = sock.Send(bmsg)
        print(f'데이터 전송 : {ret}byte')

    def SendAllData(self, msg):
        for s in self.sockets:
            self.SandData(s, msg)

    def Send_Data(self, sock, data):
        try:
            size = len(data)  # 보낼 크기

            # 전송할 데이터 크기 전달
            data_size = size.to_bytes(4, byteorder='big')
            ret = sock.send(data_size)

            # 실제 데이터 전송
            total = 0
            left_data = size
            while total < size:
                ret = sock.send(data[total:])
                total += ret
                left_data -= ret

        except Exception as e:
            print(e)
            

    def ReceiveData(self, sock):
        try:
            # 수신할 데이터 크기
            data_size = sock.recv(4)
            size = int.from_bytes(data_size, byteorder='big')
            left_data = size

            data = bytearray()

            # 실제 데이터 수신
            while left_data > 0:
                chunk = sock.recv(left_data)
                if not chunk:
                    break
                data += chunk
                left_data -= len(chunk)

            return data if len(data) == size else None
        except Exception as ex:
            print(ex)
    
    # 수신 메시지 파싱(서버)
    # 클라이언트로 부터 받은 메시지를 파싱해서 동작 ( 메시지를 가공해서 클라이언트로 보냄 )
    def Server_RecvData(self, msg):
        print(f'수신 메시지 : {msg}')

        sp1 = msg.split('@')
        if sp1[0] == Network_Packet.Login:
            self.Login(sp1[1])
        elif sp1[0] == Network_Packet.Logout:
            self.Logout(sp1[1])
        elif sp1[0] == Network_Packet.Shortmessage:
            sp2 = sp1[1].split('#')
            self.ShortMessage(sp2[0], sp2[1])
        elif sp1[0] == Network_Packet.Sendfile:
            sp2 = sp1[1].split('#')
            self.SendFile(sp2[0], sp2[1])
        elif sp1[0] == Network_Packet.Sendremote:
            self.RemoteControl(sp1[1])

    # 수신 처리 및 응답
    def Login(self, name):
        # 1. 수신 데이터 처리
        print(f'로그인 정보 : {name}')

        # 2. 응답패킷 생성 및 전송
        pack = Network_Packet.LogIn_ACK(name)
        self.SendAllData(pack)

    def Logout(self, name):
        # 1. 수신 데이터 처리
        print(f'로그아웃 정보 : {name}')

        # 2. 응답패킷 생성 및 전송
        pack = Network_Packet.LogOut_ACK(name)
        self.SendAllData(pack)

    def ShortMessage(self, name, msg):
        print(f'메시지 전송, {name} : {msg}')

        pack = Network_Packet.ShortMessage_ACK(name, msg)
        self.SendAllData(pack)

    def SendFile(self, filename, size):
        print(f'파일 전송 :  {filename}, {size}byte')

        pack = Network_Packet.SendFile_ACK(filename, size)
        self.SendAllData(pack)

    def RemoteControl(self, bytes):
        print('원격 제어')

        pack = Network_Packet.SendRemote_ACK(bytes)
        self.SendAllData(pack)
        


    ### 마우스 기능 파트 (MouseModule.py에서 핸들 주고받아옴) ###
    ## 공통 기능 / 양손 제스처 ##
    # 0. 행동 해제 이벤트
    def active_stop(self):
        self.text_view.append('기능 : 행동 해제 이벤트 감지')

    # 1.1 / 2.1 마우스 이동 이벤트
    def mouse_MoveEvent(self, event, screen_size):
        MouseFunction.handle_mouse_move(self, event, screen_size)

    ## 1. 왼손 제스처 기준 ##
    # 1.2 마우스 좌클릭 관련 (1번 좌클릭 / 좌 프레스(계속 누르는) )
    def mouse_Left_ClickEvent(self):
        self.text_view.append('기능 : 마우스 좌클릭 이벤트 감지')
        MouseFunction.handle_left_mouse_click(self)

    # 1.3 마우스 좌 더블클릭 이벤트 (2번 좌클릭)
    def mouse_Left_DoubleClickEvent(self):
        MouseFunction.handle_left_mouse_doubleclick(self)
        self.text_view.append('기능 : 마우스 더블클릭 이벤트 감지')

    # 1.4 마우스 좌클릭 후 드래그 / 드래그 and 드롭 이벤트
    def mouse_Left_drag(self):
        MouseFunction.handle_left_mouse_drag(self)
        self.text_view.append('기능 : 마우스 드래그 이벤트 감지')

    # 1.5 마우스 스크롤 확대 및 축소 이벤트
    def mouse_scroll_event(self, event):
        MouseFunction.handle_mouse_scroll(self, event)
        self.text_view.append('기능 : 마우스 스크롤 이벤트 감지')

    # 1.5.1 화면 스크롤 - 확대 동작 수행
    def mouse_zoom_in(self, event):
        MouseFunction.handle_mouse_zoom_in(self, event)
        self.text_view.append('기능 : 마우스 확대 이벤트 감지')

    # 1.5.2 화면 스크롤 - 축소 동작 수행
    def mouse_zoom_out(self, event):
        MouseFunction.handle_mouse_zoom_out(self, event)
        self.text_view.append('기능 : 마우스 축소 이벤트 감지')

    ## 2. 오른손 제스처 기준 ##
    # 2.2 마우스 우클릭 이벤트 (1번 우클릭 / 우 프레스 (계속 누르는) )
    def mouse_Right_ClickEnvet(self):
        MouseFunction.handle_right_mouse_click(self)
        self.text_view.append('기능 : 마우스 우클릭 이벤트 감지')

    # 2.3 윈도우 창 확대 축소 이벤트


    # 2.4 키보드 기능 화상키보드 켜기 (새끼손가락만)
    def keyboard_on_Event(self):
        keyboard_process = subprocess.Popen('osk.exe', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.text_view.append('기능 : 키보드 실행 이벤트 감지')
        # 화상 키보드 선행설정 - 옵션 - 화상키보드 사용방식 중 가리켜서 입력 3초 기준
        # notepad_process = subprocess.Popen('notepad.exe', shell=True)

        if MouseFunction.active_stop:
            keyboard_process.terminate()    # 화상 키보드 종료
            return

    def keyboard_off_Event(self):
        self.text_view.append('기능 : 키보드 종료 이벤트 감지')
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'osk.exe':
                pid = proc.info['pid']
                # 프로세스 종료
                psutil.Process(pid).kill()
                break