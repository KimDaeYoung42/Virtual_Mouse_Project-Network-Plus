# App_Gesture.py : 마우스, 키보드 기능 코드 1번.

import os
import sys
import subprocess
import psutil
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QLineEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QCursor
from tensorflow.keras.models import load_model 

import cv2
import mediapipe as mp
import math
from HandTrackingModule import HandDetector
from Mouse_Module import MouseFunction
from Server_Control import Server, Control
from Network_Packet import PacketTag, Packet
from Recv_Screen import Active_Screen

import autopy
import icon_toolbar 
import icon_gesture
import pyautogui
import time
import pygetwindow as gw
import numpy as np
import threading
import zlib
import socket
import base64
import shutil

class Active_Webcam(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 관련
        loadUi("UI_App_WebCam (Network_Mode) (1).ui", self)      # UI 파일 로드
        self.setWindowTitle("가상 인터페이스 프로그램 (제어자 전용)")  
        # self.setGeometry(100, 440, 1500, 820)
        self.setMinimumSize(1500, 820)

        # 웹캠 관련
        # self.cap = None                                                     # 웹캠 객체
        self.is_running = True                                             # 웹캠 실행 여부 flag
        
        self.hand_detector = HandDetector()
        self.recv_screen = Active_Screen()
    
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

        self.file_send_count = 0
        self.screen_share_count = 0
        self.request_screen_count = 0

        self.user_list = []
        self.click_elapse_time = 0
        self.click_start_time = 0

        # Default 제스쳐
        self.actions = ['Click', 'Zoom', 'None', 'Move', 'DClick', 'Keyboard', 'Server', 'Share', 'Request', 'File']
        self.action = ''

        # 디볼트 스크롤에 아이템 추가하기
        self.listWidget1_1.addItem("Click")
        self.listWidget1_2.addItem("Click")
        self.listWidget1_3.addItem("Zoom")
        self.listWidget1_4.addItem("Zoom")

        # 선택 스크롤에 기능 선택
        Scroll_items = ['None', 'Move', 'DClick', 'Keyboard', 'Server', 'Share', 'Request', 'File', '기능미정']

        # comboBox들을 리스트로 저장
        comboboxes = [self.comboBox2_1, self.comboBox2_2, self.comboBox2_3, self.comboBox2_4, self.comboBox2_5, self.comboBox2_6, self.comboBox2_7, self.comboBox2_8]

        for index, Scroll_item in enumerate(Scroll_items):
            # 각각의 comboBox에 아이템 추가
            if index < len(comboboxes):
                comboboxes[index].addItem(Scroll_item)


        for Scroll_item in Scroll_items:
            self.comboBox2_1.addItem(Scroll_item)
            self.comboBox2_2.addItem(Scroll_item)
            self.comboBox2_3.addItem(Scroll_item)
            self.comboBox2_4.addItem(Scroll_item)
            self.comboBox2_5.addItem(Scroll_item)
            self.comboBox2_6.addItem(Scroll_item)
            self.comboBox2_7.addItem(Scroll_item)
            self.comboBox2_8.addItem(Scroll_item)

        # 드래그 관련 초기화
        self.dragging = False                                               # 드래그 상태 플래그
        self.start_drag_pos = None                                          # 드래그 시작 좌표

        # 채팅 전송 버튼
        self.push_chat_Button.clicked.connect(self.short_message)
        self.text_chatting1.installEventFilter(self)
        
        # 서버 시작/종료 버튼
        self.is_connected = False
        self.push_start_Button1.clicked.connect(self.start_server)
        self.push_stop_Button1.clicked.connect(self.stop_server)
        
        # 웹캠 시작/종료 버튼
        self.push_webcam_start_button.clicked.connect(self.start_cam)
        self.push_webcam_stop_button.clicked.connect(self.stop_cam)

        # 화면공유 시작/종료 버튼
        self.sharing_start_Button.clicked.connect(self.screen_sharing_start)
        self.sharing_stop_Button.clicked.connect(self.screen_sharing_stop)

        # 모니터 화면 크기 설정
        self.screen_size = autopy.screen.size()                  # print(screen_size) 1920, 1080 <- 모니터 1대만 사용시 기준
        self.screen_size_x, self.screen_size_y = self.screen_size
        
        # 파일 선택/전송 버튼
        self.file_select_Button.clicked.connect(self.select_file)
        self.file_send_Button.clicked.connect(self.file_send)

        # 파일 리스트 위젯 초기화 ( Downloads 폴더의 모든 파일들을 위젯에 추가 )
        self.file_widget_Item_add()

        # 공유받을 화면 버튼
        self.user_screen_recive.clicked.connect(self.request_screen)

        # 제스쳐 기능 맵핑 버튼
        self.gesture_pushbutton.clicked.connect(self.gesture_update)

        self.server_thread = None
        
        self.user_list = []

    # self.actions에 값을 입력받아야 함.
    def gesture_update(self):
        # 디폴트 입력
        self.actions.clear()
        self.actions.append('Click')
        self.actions.append('Zoom') 

        # 입력받은 값을 순서대로 self.actions 리스트에 넣는다.
        self.actions.append(self.comboBox2_1.currentText())
        self.actions.append(self.comboBox2_2.currentText())
        self.actions.append(self.comboBox2_3.currentText())
        self.actions.append(self.comboBox2_4.currentText())
        self.actions.append(self.comboBox2_5.currentText())
        self.actions.append(self.comboBox2_6.currentText())
        self.actions.append(self.comboBox2_7.currentText())
        self.actions.append(self.comboBox2_8.currentText())

        print(self.actions)

    def update_frame(self):

        cap = cv2.VideoCapture(0)                                      # 웹캠 번호 (0은 기본 웹캠)
        seq = []
        action_seq = []
        model = load_model('models/model.h5')

        #   디폴트 제스쳐   가위    엄지검지   주먹    보     약지소지  검지중지약지  엄지소지  검지소지  검지오른쪽   소지
        # self.actions = ['Click', 'Zoom', 'None', 'Move', 'DClick', 'Keyboard', 'Server', 'Share', 'Request', 'File']

        while self.is_running:
            ret, frame = cap.read()                                        # 웹캠 프레임 읽기

            click_start_time = 0
            
            frame = cv2.flip(frame, 1)                                      # 웹캠 좌우 반전
            frame = self.hand_detector.find_hands(frame)
            lm_list, label = self.hand_detector.find_positions(frame)
            self.action = self.hand_detector.action_estimation(frame, seq, action_seq, model, self.actions)

            if lm_list:
                print(label)

                # 엄지와 검지의 거리를 측정해야함.
                thumb_tip = lm_list[4]
                index_tip = lm_list[8]
                middle_tip = lm_list[12]
                thumb_index_distance = math.sqrt((thumb_tip[1] - index_tip[1]) ** 2 + (thumb_tip[2] - index_tip[2]) ** 2)
                index_middle_distance = math.sqrt((index_tip[1] - middle_tip[1]) ** 2 + (index_tip[2] - middle_tip[2]) ** 2)

                print(index_middle_distance)


                # 행동해제
                if self.action == 'None':
                    start_time = time.time()
                    elapse_time = time.time() - start_time
                    if elapse_time > 3:
                        self.active_stop()
                        elapse_time = 0
                        self.Lclick_count = 0  # 클릭 횟수 초기화
                        self.LDclick_count = 0
                        self.Scroll_count = 0
                        self.Drag_count = 0
                        self.file_send_count = 0
                        self.Window_zoom = 0
                        self.dragging = False

                # 마우스 움직임
                if self.action == 'Move':
                    self.mouse_MoveEvent(event=lm_list, screen_size=pyautogui.size())
                    self.Lclick_count = 0      # 클릭 횟수 초기화
                    self.LDclick_count = 0
                    self.Scroll_count = 0
                    self.Drag_count = 0
                    self.file_send_count = 0
                    self.Window_zoom = 0
                    self.dragging = False

                # 더블클릭
                if self.action == 'DClick':
                    if self.LDclick_count == 0:
                        self.LDclick_count += 1  # 클릭 횟수 증가
                        self.mouse_Left_DoubleClickEvent()
                        self.text_view.append('기능 : 더블클릭')
                    else:
                        self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")


                # 마우스 클릭
                if self.action == 'Click':
                    if label == 'left':
                        # 우클릭
                        if self.Rclick_count == 0:
                            self.Rclick_count += 1  # 클릭 횟수 증가
                            self.mouse_Right_ClickEnvet()
                            self.text_view.append('기능 : 우클릭')
                        else:
                            self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")
                    elif label == 'right':
                        # 좌클릭
                        if self.Lclick_count == 0:
                            self.click_start_time = time.time()
                            self.Lclick_count += 1  # 클릭 횟수 증가
                            self.mouse_Left_ClickEvent()
                            self.text_view.append('기능 : 좌클릭')
                        else:
                            self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")

                    self.click_elapse_time = time.time() - self.click_start_time
                    print(self.click_elapse_time)
                    # 3초 이상 지속시 드래그 다운 and index_middle_distance 가 x 이상 ( 손가락이 떨어졋을 때 드래그 업)
                    if label == 'right' and self.click_elapse_time >= 3 and index_middle_distance < 30:
                        # 드래그 다운
                        if not self.dragging:
                            pyautogui.mouseDown(button='left')
                            self.text_view.append("드래그 기능 : 좌클릭 상태")
                            self.dragging = True

                        if index_middle_distance < 30:
                            # 마우스 커서 이동
                            self.text_view.append("드래그 기능 : 드래그 중")
                            self.mouse_MoveEvent(event=lm_list, screen_size=pyautogui.size())
                        elif index_middle_distance > 30 and self.dragging:
                            self.text_view.append("드래그 기능 : 드래그 해제 상태")
                            pyautogui.mouseUp(button='left')
                            self.dragging = False  # 드래그 상태 플래그 해제
                            self.click_elapse_time = 0 


                # 0 ~ 25 축소,  And  100 이상시 확대 

                if self.action == 'Zoom':
                    # label == left -> 윈도우창 확대 or 축소 --> 엄지,검지의 거리를 측정
                    if label == 'left':
                        if thumb_index_distance > 100 and self.Window_zoom == 0:
                            self.Window_zoom += 1
                            self.text_view.append('기능 : 윈도우 확대 이벤트 발생')

                            # 현재 포커스 하는 윈도우의 창을 최대화 한다.

                            # 원래의 윈도우 창 크기 저장.
                            window = gw.getActiveWindow()

                            # 윈도우의 크기 재설정 ( 최대화 )
                            window.maximize()

                        elif thumb_index_distance < 25 and self.Window_zoom == 0:
                            self.Window_zoom += 1
                            self.text_view.append('기능 : 윈도우 축소 이벤트 발생')

                            # 현재 포커스 하는 윈도우의 크기를 600 * 400으로 재설정

                            # 원래의 윈도우 창 크기 저장.
                            window = gw.getActiveWindow()

                            # 600 * 400 으로 크기 재설정
                            window.resize(600, 400)

                        else:
                            self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")

                    # label == right -> 스크롤 올리기 or 내리기
                    elif label == 'right':
                        if self.Scroll_count == 0 and 100 < thumb_index_distance:
                            self.text_view.append("기능 : 스크롤 확대 이벤트 감지")
                            pyautogui.scroll(20)
                        elif self.Scroll_count == 0 and thumb_index_distance < 25:
                            self.text_view.append("기능 : 스크롤 축소 이벤트 감지")
                            pyautogui.scroll(-20)
                        elif not self.Scroll_count == 0:
                            self.text_view.append("기능 : 스크롤 이벤트 정지")
                            self.text_view.append("손가락을 펼치고 다시 제스처 취해야 기능 가능")                    

                # 키보드 키기 / 끄기 
                if self.action == 'Keyboard':
                    if label == 'right':
                        if self.Keyboard_count == 0:
                            self.text_view.append("기능 : 키보드 실행")
                            self.Keyboard_count += 1
                            self.keyboard_on_Event()
            
                    elif label == 'left':
                        if not self.Keyboard_count == 0:
                            self.text_view.append("기능 : 키보드 종료")
                            self.Keyboard_count = 0
                            self.keyboard_off_Event()

                # 서버 연결 / 해제 
                if self.action == 'Server':
                    if label == 'right' and not self.is_connected:
                        self.text_view.append("기능 : 서버 연결")
                        self.start_server()
                        
                    # elif label == 'left' and self.is_connected:
                    #     self.text_view.append("기능 : 서버 연결 해제")
                    #     self.stop_server()
                
                # 화면 공유 시작 / 해제 
                if self.action == 'Share':
                    if self.is_connected:
                        if label == 'right' and self.screen_share_count == 0:
                            self.text_view.append("기능 : 화면 공유 시작")
                            self.screen_sharing_start()
                        elif label == 'left' and self.screen_share_count == 1:
                            self.text_view.append("기능 : 화면 공유 종료")
                            self.screen_sharing_stop()
                    elif not self.is_connected:
                        self.text_view.append("서버 연결이 되어있지 않습니다.")

                # 파일 전송 
                if self.action == 'File':
                    if self.is_connected and self.file_send_count == 0:
                        self.text_view.append('기능 : 파일 전송')
                        self.file_send()
                        self.file_send_count += 1
                    elif not self.is_connected:
                        self.text_view.append('서버 연결이 되어있지 않습니다.')
                
                # 화면 공유 요청 ( 서버 -> 클라 )
                if self.action == 'Request':
                    if self.is_connected and self.request_screen_count == 0:
                        self.request_screen()
                        self.text_view.append('기능 : 화면공유 요청')
                        self.request_screen_count += 1
                    elif not self.is_connected:
                        self.text_view.append('서버 연결이 되어있지 않습니다.')

            # 손 인식하지 않았을 시
            else:
                if self.hand_detect_count == 0:
                    self.hand_detect_count += 1
                    self.text_view.append('손이 인식되지 않았습니다')


            # 프레임 화면에 출력
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_img)
            self.Webcam_label2.setPixmap(q_pixmap)



    # 웹캠 시작/종료 버튼 클릭시
    def start_cam(self):
        
        thread = threading.Thread(target=self.update_frame)
        thread.daemon = True
        thread.start()

        if thread.is_alive:
            self.text_view.append('웹캠 실행 중...')

    def stop_cam(self):
        self.is_running = False

    # 서버 연결 / 해제
    def start_server(self):
        if self.is_connected:
            self.text_network_view1.append("서버가 이미 실행 중입니다.")
            return
        
        self.is_connected = True
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()

    def run_server(self):
        self.server = Server(9000)
        
        self.run_server2()


    def run_server2(self):
        self.user_list.append('admin')
        self.user_list_view()
        
        self.text_network_view1.append('서버 시작.... 클라이언트 접속 대기중')
        self.server.run(self.server_recv_data)
        

    # 클라 -> 서버 메시지 수신했을 때
    def server_recv_data(self, sock, msg):
        tag, data = msg.split('@', 1)

        if tag == PacketTag.Login.value:
            self.text_network_view1.append(f'수신 메시지 : {msg}')
            self.user_list.append(data)
            self.user_list_view()
            self.ret = Control.login_ack(data, self.user_list, self.server)
            self.text_network_view1.append(f'송신 메시지 : {self.ret}') 
            
        elif tag == PacketTag.Logout.value:
            self.text_network_view1.append(f'수신 메시지 : {msg}')
            self.user_list.remove(data)
            self.user_list_view()
            self.ret = Control.logout_ack(data, self.user_list, self.server)
            self.text_network_view1.append(f'송신 메시지 : {self.ret}') 
            
        elif tag == PacketTag.Shortmessage.value:
            self.text_network_view1.append(f'수신 메시지 : {msg}')
            name, msg = data.split('#', 1)
            self.text_chat_view1.append(f'{name} : {msg}')
            self.ret = Control.short_message_ack(name, msg, self.server)
            self.text_network_view1.append(f'송신 메시지 : {self.ret}') 

        elif tag == PacketTag.Sendbyte.value:
            self.text_network_view1.append(f'수신 메시지 : {tag}@bytes')

            recv_screen_thread = threading.Thread(target=self.recv_screen.Recv_Screen_Thread, args=(data,))
            recv_screen_thread.daemon = True
            recv_screen_thread.start()
        
        elif tag == PacketTag.Sendfile.value:
            filename, file_data = data.split('#', 1) 
            self.text_network_view1.append(f'수신 메시지 : {tag}@{filename}')

            time.sleep(5)
            self.recv_file(filename, file_data)

            # 받은 파일을 다시 클라들에게 보낼까....?
            # encoded_filedata = file_data.encode('utf-8')
            # self.ret = Control.send_file_ack(filename, encoded_filedata, self.server)


        else:
            self.text_network_view1.append(f'모르는 메시지 수신')

    def stop_server(self):
        self.text_network_view1.append('서버가 종료됩니다.')
        self.is_connected = False
        
    # 채팅 전송버튼
    def short_message(self):
        name = 'admin'
        msg = self.text_chatting1.toPlainText()
        self.text_chat_view1.append(f'{name} : {msg}')

        ret = Control.short_message_ack(name, msg, self.server)
        # 전송 이후 메시지 입력창 초기화
        self.text_chatting1.clear()

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and source is self.text_chatting1):
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                self.short_message()
                return True
        return super().eventFilter(source, event)
    
    # 접속자 리스트 갱신
    def user_list_view(self):
        self.person_listWidget1.clear()
        for user in self.user_list:
            self.person_listWidget1.addItem(user)

    def screen_sharing_start(self):
        self.screen_share_count += 1
        sharing_thread = threading.Thread(target=self.screen_sharing_thread)
        sharing_thread.daemon = True
        sharing_thread.start()

    def screen_sharing_thread(self):
        self.text_network_view1.append('화면 공유 시작')
        while self.screen_share_count == 1:

            # 모니터 화면 캡쳐
            image = pyautogui.screenshot()

            # 서버로 전송하기 위한 작업
            data = image.tobytes()
            compress_data = zlib.compress(data)
            length = len(data)

            # 화면 전송
            encoded_data = base64.b64encode(compress_data)
            pack = Packet.SendByte_ACK(encoded_data)
            self.server.send_all_data(pack)
            self.text_network_view1.append('화면공유중')

            time.sleep(0.1)

    def screen_sharing_stop(self):
        if self.screen_share_count == 1:
            self.screen_share_count = 0
            self.text_network_view1.append('화면공유 종료')
        else:
            self.text_network_view1.append('화면 공유중이 아닙니다.')

    # 화면 공유 요청
    def request_screen(self):
        # 공유받을 화면을 띄움
        self.recv_screen.show()
        
        # 만약 유저 리스트 위젯에서 선택을 안했다면...? ------- 2번째 사람의 이름으로 한다
        if not self.person_listWidget1.currentItem():
            item = self.person_listWidget1.item(1)
            name = item.text()
        # 유저 리스트 위젯에서 선택된 이름을 가져온다.
        else:
            item = self.person_listWidget1.currentItem()
            name = item.text()

        print(name)

        # 그 이름을 클라이언트에게 보낸다.
        ret = Control.request_screen_ack(name, self.server)

    # 파일 선택
    def select_file(self): 
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 선택")
        # 선택된 파일을 지정된 폴더 ( C:\Users\user\Desktop\다운로드 )에 이동 시키기
        Download_path = r'C:\Users\user\Desktop\다운로드'

        # 0. 경로가 존재하지 않을 경우 폴더 생성
        if not os.path.exists(Download_path):
            os.makedirs(Download_path)

        # file_path -> 파일을 Download_path에 복사시킴
        shutil.copy(file_path, Download_path)
        
        # 파일 리스트뷰 로드
        self.file_widget_Item_add()


    # 파일 받았을 때
    def recv_file(self, file_name, file_data):
        try:
            download_path = r'C:\Users\user\Desktop\다운로드'  # 파일 다운로드 경로

            # 0. 경로가 존재하지 않을 경우 폴더 생성
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            # 1. base64 디코딩
            decoded_filedata = base64.b64decode(file_data)

            # 2. 파일 저장
            save_path = os.path.join(download_path, file_name)

            with open(save_path, 'wb') as file:
                file.write(decoded_filedata)

            self.text_network_view1.append(f'{file_name} 저장 성공')

            # 3. 받은 파일을 파일 리스트 위젯의 아이템에 넣기
            self.file_widget_Item_add()

        except Exception as e:
            print(f'파일 수신중 오류 발생 : {e}')
        
    # 파일 보낼 때
    def file_send(self):
        if self.is_connected:
            self.text_network_view1.append('파일 전송')
            send_file_path = r'C:\Users\user\Desktop\다운로드'
            selected_file = self.file_listView1.currentItem()

            if selected_file:
                file_name = selected_file.text()
                file_path = send_file_path + f'\{file_name}'

                if os.path.exists(file_path) and os.path.isfile(file_path):
                    # 1. 파일을 바이트로 변환하기
                    with open(file_path, 'rb') as file:
                        file_data = file.read()

                    # 2. 바이트 데이터를 문자열로 변환하기
                    based_file_data = base64.b64encode(file_data)

                    file_name = os.path.basename(file_path)

                    # 파일 패킷 생성 및 전송
                    pack = Packet.SendFile_ACK(file_name, based_file_data)
                    self.server.send_all_data(pack)

                    # 전송 로그
                    tag, data = pack.split('@', 1)
                    filename, filedata = data.split('#', 1)

                    self.text_network_view1.append(f'송신 메시지 : {tag}@{filename}')
                
                else:
                    self.text_network_view1.append('파일 경로가 없습니다.')
            else:
                self.text_network_view1.append('전송할 파일을 선택해 주세요.')
        else:
            self.text_network_view1.append('서버를 시작해 주세요.')

    # 프로그램이 시작 되었을 때 다운로드 폴더의 파일들이 위젯에 들어감
    def file_widget_Item_add(self):
        self.file_listView1.clear()

        path = r'C:\Users\user\Desktop\다운로드'

        # 0. 경로가 존재하지 않을 경우 폴더 생성
        if not os.path.exists(path):
            os.makedirs(path)

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                item = QListWidgetItem(filename)
                self.file_listView1.addItem(item)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Active_Webcam()
    window.show()
    sys.exit(app.exec_())