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
from Server_Control import Server, Control
from Network_Packet import PacketTag, Packet


import autopy
import pyautogui
import time
import pygetwindow as gw
import numpy as np
import threading
import zlib
import socket
import base64

class ServerProxy:
    def __init__(self, port):
        self.server = Server(port)

    def send_all_data(self, msg):
        self.server.send_all_data(msg)

class Active_Webcam(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 관련
        loadUi("UI_App_WebCam (Network_Mode).ui", self)      # UI 파일 로드
        self.setWindowTitle("가상 인터페이스 프로그램")
        # self.setGeometry(100, 440, 1500, 820)
        self.setMinimumSize(1500, 820)

        # 웹캠 관련
        # self.cap = None                                                     # 웹캠 객체
        self.is_running = True                                             # 웹캠 실행 여부 flag
        
    
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

        self.user_list = []

        # 실행할 스레드 수
        self.num_thread = 2

        # 스레드 객체를 저장할 리스트
        self.threads = []

        # 드래그 관련 초기화
        self.dragging = False                                               # 드래그 상태 플래그
        self.start_drag_pos = None                                          # 드래그 시작 좌표


        # 화면 공유 플래그
        self.is_sharing = True

        # 채팅 전송 버튼
        self.push_chat_Button.clicked.connect(self.short_message)
        
        # 서버 시작/종료 버튼 
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
        
        self.server_thread = None
        
        self.user_list = []


    def update_frame(self):

        cap = cv2.VideoCapture(0)                                      # 웹캠 번호 (0은 기본 웹캠)
        seq = []
        action_seq = []
        model = load_model('models/model.h5')
        # 필요한 action ---- 주먹, 다핌, 검지중지, 엄지검지, 엄지중지, 엄지소지만, 소지만 ---- 7개
        actions = ['rock', 'paper', 'scissors', 'thumb_index', 'thumb_middle', 'thumb_pinky', 'pinky']

        while self.is_running:
            ret, frame = cap.read()                                        # 웹캠 프레임 읽기

            click_start_time = 0
            
            frame = cv2.flip(frame, 1)                                      # 웹캠 좌우 반전
            frame = self.hand_detector.find_hands(frame)
            lm_list, label = self.hand_detector.find_positions(frame)
            action = self.hand_detector.action_estimation(frame, seq, action_seq, model, actions)

            if lm_list:
                print(label)

                # 엄지와 검지의 거리를 측정해야함.
                thumb_tip = lm_list[4]
                index_tip = lm_list[8]
                middle_tip = lm_list[12]
                thumb_index_distance = math.sqrt((thumb_tip[1] - index_tip[1]) ** 2 + (thumb_tip[2] - index_tip[2]) ** 2)
                index_middle_distance = math.sqrt((index_tip[1] - middle_tip[1]) ** 2 + (index_tip[2] - middle_tip[2]) ** 2)

                # print(index_middle_distance)


                # 행동해제 --> action == rock
                if action == 'rock':
                    start_time = time.time()
                    elapse_time = time.time() - start_time
                    if elapse_time > 3:
                        self.active_stop()
                        elapse_time = 0
                        self.Lclick_count = 0  # 클릭 횟수 초기화
                        self.LDclick_count = 0
                        self.Scroll_count = 0
                        self.Drag_count = 0

                # 마우스 움직임 --> action == paper
                if action == 'paper':
                    # 검지와 중지가 붙어있지 않음
                    if index_middle_distance > 60:
                        self.mouse_MoveEvent(event=lm_list, screen_size=pyautogui.size())
                        self.Lclick_count = 0      # 클릭 횟수 초기화
                        self.LDclick_count = 0
                        self.Scroll_count = 0
                        self.Drag_count = 0
                    # 검지와 중지가 붙음 --> 더블클릭
                    elif index_middle_distance < 60:
                        if self.LDclick_count == 0:
                            self.LDclick_count += 1  # 클릭 횟수 증가
                            # self.mouse_Left_DoubleClickEvent()
                            # self.text_view.append('기능 : 더블클릭')
                        else:
                            self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")


                # 마우스 클릭 --> action == scissors
                if action == 'scissors':
                    if label == 'left':
                        # 우클릭
                        if self.Rclick_count == 0 and index_middle_distance < 60:
                            self.Rclick_count += 1  # 클릭 횟수 증가
                            # self.mouse_Right_ClickEnvet()
                            # self.text_view.append('기능 : 우클릭')
                        else:
                            self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")
                    elif label == 'right':
                        # 좌클릭
                        if self.Lclick_count == 0 and index_middle_distance < 60:
                            click_start_time = time.time()
                            self.Lclick_count += 1  # 클릭 횟수 증가
                            # self.mouse_Left_ClickEvent()
                            # self.text_view.append('기능 : 좌클릭')
                        else:
                            self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")

                    click_elapse_time = time.time() - click_start_time
                    # 1초 이상 지속시 드래그 다운 and thumb_index_distance 가 x 이상 ( 손가락이 떨어졋을 때 드래그 업)
                    if label == 'right' and click_elapse_time >= 1:
                        # 드래그 다운
                        if not self.dragging:
                            # pyautogui.mouseDown(button='left')
                            # self.text_view.append("드래그 기능 : 좌클릭 상태")
                            self.dragging = True

                        if index_middle_distance < 60:
                            # 마우스 커서 이동
                            self.text_view.append("드래그 기능 : 드래그 중")
                            # self.mouse_MoveEvent(event=lm_list, screen_size=pyautogui.size())
                        elif index_middle_distance > 60 and self.dragging:
                            # self.text_view.append("드래그 기능 : 드래그 해제 상태")
                            # pyautogui.mouseUp(button='left')
                            self.dragging = False  # 드래그 상태 플래그 해제
                            click_elapse_time = 0

                window_original_width = 0
                window_original_height = 0

                x = 16
                y = 9

                if action == 'thumb_index':
                    # label == left -> 윈도우창 확대 or 축소 --> 엄지,검지의 거리를 측정 150 이상일 때 확대 150 이하일 때 축소
                    if label == 'left':
                        if thumb_index_distance > 150 and self.Window_zoom == 0:
                            self.Window_zoom += 1
                            # self.text_view.append('기능 : 윈도우 확대 이벤트 발생')

                            # 원래의 윈도우 창 크기 저장.
                            # window = gw.getActiveWindow()               

                            # # 현재 활성화 윈도우 창 상태정보 가져오기
                            # window_original_width, window_original_height = window.width, window.height

                            # # 윈도우의 크기 재설정 ( 확대 )
                            # if self.screen_size_x > window_original_width and self.screen_size_y > window_original_height:
                            #     window.resize(window_original_width + x, window_original_height + y)
                            # elif self.screen_size_x > window_original_width and self.screen_size_y < window_original_height:
                            #     window.resize(window_original_width + x, window_original_height)
                            # elif self.screen_size_x < window_original_width and self.screen_size_y > window_original_height:
                            #     window.resize(window_original_width, window_original_height + y)

                        elif thumb_index_distance > 150 and self.Window_zoom == 0:
                            self.Window_zoom += 1
                            # self.text_view.append('기능 : 윈도우 축소 이벤트 발생')

                            # 원래의 윈도우 창 크기 저장.
                            # window = gw.getActiveWindow()

                            # # 현재 활성화 윈도우 창 상태정보 가져오기
                            # window_original_width, window_original_height = window.width, window.height

                            # # 윈도우의 크기 재설정 ( 축소 )
                            # if window_original_width > 300 and window_original_height > 300:
                            #     window.resize(window_original_width - x, window_original_height - y)
                            # elif window_original_width < 300 and window_original_height > 300:
                            #     window.resize(window_original_width, window_original_height - y)
                            # elif window_original_width > 300 and window_original_height < 300:
                            #     window.resize(window_original_width - x, window_original_height)

                        else:
                            self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")

                    # label == right -> 스크롤 올리기 or 내리기 --> 거리를 측정 150이상 -> 올리기, 150이하 -> 내리기
                    elif label == 'right':
                        if self.Scroll_count == 0 and 200 < thumb_index_distance < 300:
                            # self.text_view.append("기능 : 스크롤 확대 이벤트 감지")
                            # pyautogui.scroll(-20)
                            self.Scroll_count += 1
                        elif self.Scroll_count == 0 and 0 < thumb_index_distance < 100:
                            # self.text_view.append("기능 : 스크롤 축소 이벤트 감지")
                            # pyautogui.scroll(20)
                            self.Scroll_count += 1
                        elif not self.Scroll_count == 0:
                            self.text_view.append("기능 : 스크롤 이벤트 정지")
                            # self.text_view.append("손가락을 펼치고 다시 제스처 취해야 기능 가능")                    

                # 키보드 키기 / 끄기    action == pinky
                if action == 'pinky':
                    # labal == right -> 키기
                    if label == 'right':
                        if self.Keyboard_count == 0:
                            # self.text_view.append("기능 : 키보드 실행")
                            self.Keyboard_count += 1
                            # self.keyboard_on_Event()
            
                    # label == left -> 끄기
                    elif label == 'left':
                        if not self.Keyboard_count == 0:
                            # self.text_view.append("기능 : 키보드 종료")
                            self.Keyboard_count = 0
                            # self.keyboard_off_Event()

                # 서버 연결 / 해제      action == thumb_middle
                if action == 'thumb_middle':
                    # label == right -> 연결
                    if label == 'right' and not self.is_connected:
                        self.text_view.append("기능 : 서버 연결")
                        self.network_connect()
                        # Active_Window.network_connect(Active_Window)
                        self.is_connected = True
                    # label == left -> 해제
                    elif label == 'left' and self.is_connected:
                        self.text_view.append("기능 : 서버 연결 해제")
                        self.network_disconnect()
                        # Active_Window.network_disconnect(Active_Window)
                        self.is_connected = False
                
                # 화면 공유 시작 / 해제     action == thumb_ring
                if action == 'thumb_pinky':
                    if self.is_connected:
                        # label == right -> 시작
                        if label == 'right' and not self.is_sharing:
                            self.text_view.append("기능 : 화면 공유 시작")
                            self.is_sharing = True
                            sharing_thread = threading.Thread(target=self.screen_sharing_start)
                            self.threads.append(sharing_thread)
                            # self.sharing_thread.daemon = True
                            sharing_thread.start()
                        elif label == 'left' and self.is_sharing:
                            self.text_view.append("기능 : 화면 공유 종료")
                            self.is_sharing = False
                    elif not self.is_connected:
                        self.text_view.append("서버 연결이 되어있지 않습니다.")

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
        self.threads.append(thread)
        # self.thread.daemon = True
        thread.start()

        if thread.is_alive:
            self.text_view.append('웹캠 실행 중...')

    def stop_cam(self):
        self.is_running = False

    # 서버 연결 / 해제
    def start_server(self):
        if self.server_thread and self.server_thread.is_alive():
            self.text_network_view1.append("서버가 이미 실행 중입니다.")
            return

        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def run_server(self):
        self.server = Server(9000)
        
        self.run_server2()


    def run_server2(self):
        self.user_list.append('admin')
        self.user_list_view()
        
        self.text_network_view1.append('서버 시작.... 클라이언트 접속 대기중')
        self.server.run(self.server_recv_data)
        
        

    def server_recv_data(self, sock, msg):
        tag, data = msg.split('@', 1)

        if tag == PacketTag.Login.value:
            self.text_network_view1.append(f'수신 메시지 : {msg}')
            self.ret = Control.login_ack(data, self.server)
            self.user_list.append(data)
            self.user_list_view()

        elif tag == PacketTag.Logout.value:
            self.text_network_view1.append(f'수신 메시지 : {msg}')
            self.ret = Control.logout_ack(data, self.server)
            self.user_list.remove(data)
            self.user_list_view()

        elif tag == PacketTag.Shortmessage.value:
            self.text_network_view1.append(f'수신 메시지 : {msg}')
            name, msg = data.split('#', 1)
            self.text_chat_view1.append(f'{name} : {msg}')
            self.ret = Control.short_message_ack(name, msg, self.server)

        elif tag == PacketTag.Sendbyte.value:
            self.text_network_view1.append(f'수신 메시지 : {tag}@bytes')
            self.ret = Control.send_bytes_ack(data, self.server)
            tag, data = self.ret.split('@', 1)
            self.ret = tag + '@bytes'

        self.text_network_view1.append(f'송신 메시지 : {self.ret}')    


    def stop_server(self):
        self.text_network_view1('서버가 종료됩니다.')
        
    # 채팅 전송버튼
    def short_message(self):
        name = 'admin'
        msg = self.text_chatting1.toPlainText()
        self.text_chat_view1.append(f'{name} : {msg}')

        self.ret = Control.short_message_ack(name, msg, self.server)
        self.text_network_view1(f'송신 메시지 : {self.ret}')
    
    # 접속자 리스트
    def user_list_view(self):
        self.person_listWidget1.clear()
        for user in self.user_list:
            self.person_listWidget1.addItem(user)

    def screen_sharing_start(self):
        self.is_sharing = True
        sharing_thread = threading.Thread(target=self.screen_sharing_thread)
        sharing_thread.daemon = True
        sharing_thread.start()

    def screen_sharing_thread(self):
        self.text_network_view1.append('화면 공유 시작')
        while self.is_sharing:

            # 모니터 화면 캡쳐
            image = pyautogui.screenshot()

            # 서버로 전송하기 위한 작업
            data = image.tobytes()
            data = zlib.compress(data)
            length = len(data)

            # 화면 전송
            encoded_data = base64.b64encode(data)
            pack = Packet.SendByte_ACK(encoded_data)
            self.server.send_all_data(pack)

            time.sleep(0.1)

    def screen_sharing_stop(self):
        self.is_sharing = False

    def file_send(self):
        print('파일전송')


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