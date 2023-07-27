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

import autopy
import pyautogui
import time
import pygetwindow as gw
import numpy as np
import threading

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

        # 스레드를 생성해서 그 스레드 안에서 update_frame이 돌아가게끔 하면 어떨까?
        
        self.thread = threading.Thread(target=self.update_frame)
        self.thread.daemon = True
        self.thread.start()

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
                

            # # 손가락 각도 계산
            # joint_list = [[3, 0, 5], [4, 3, 2], [8, 7, 6], [12, 11, 10], [16, 15, 14], [20, 19, 18]]
            # finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
            # left_finger_angles = []
            # right_finger_angles = []

            # # 각 손가락의 상태 ( True == 펴짐, False == 안펴짐)
            # left_thumb_state    = False     # 엄지
            # left_index_state    = False     # 검지
            # left_middle_state   = False     # 중지
            # left_ring_state     = False     # 약지
            # left_pinky_state    = False     # 소지

            # right_thumb_state   = False     # 엄지
            # right_index_state   = False     # 검지
            # right_middle_state  = False     # 중지
            # right_ring_state    = False     # 약지
            # right_pinky_state   = False     # 소지

            # 1. 왼손 제스처 기준
            # if left_lm_list and not right_lm_list:
            #     # 손가락 각도 계산
            #     for i, joint in enumerate(joint_list):
            #         a = np.array([left_lm_list[joint[0]][1], left_lm_list[joint[0]][2]])  # 첫번째 좌표
            #         b = np.array([left_lm_list[joint[1]][1], left_lm_list[joint[1]][2]])  # 두번째 좌표
            #         c = np.array([left_lm_list[joint[2]][1], left_lm_list[joint[2]][2]])  # 세번째 좌표

            #         radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            #         left_angle = np.abs(radians * 180.0 / np.pi)

            #         if left_angle > 180.0:
            #             left_angle = 360 - left_angle

            #         left_finger_angles.append(left_angle)

            #     for i, finger_name in enumerate(finger_names):
            #         left_angle = left_finger_angles[i]  # 손가락별 관절 각도

            #         # print(f'{finger_name}: {left_angle} degrees')

            #     # 0 ~ 5번까지 6개의 각도가 나온다.
            #     # 0 번 - 엄지가 접힌경우 ----- 10 이하, 평상시 - 약 30 ~ 40, 1번 - 엄지손가락이 구부러진 정도, 2 ~ 5번 - 검지부터 소지까지 접히는 각도
            #     # print(left_finger_angles[0])

            #     if left_finger_angles[0] > 10:
            #         left_thumb_state = True
            #     else:
            #         left_thumb_state = False

            #     left_thumb_state = left_lm_list[4][2] < left_lm_list[3][2] < left_lm_list[2][2] < left_lm_list[1][2]
            #     left_index_state = left_lm_list[8][2] < left_lm_list[7][2] < left_lm_list[6][2] < left_lm_list[5][2]
            #     left_middle_state = left_lm_list[12][2] < left_lm_list[11][2] < left_lm_list[10][2] < left_lm_list[9][2]
            #     left_ring_state = left_lm_list[16][2] < left_lm_list[15][2] < left_lm_list[14][2] < left_lm_list[13][2]
            #     left_pinky_state = left_lm_list[20][2] < left_lm_list[19][2] < left_lm_list[18][2] < left_lm_list[17][2]
            #     # print(left_thumb_state, left_index_state, left_middle_state, left_ring_state, left_pinky_state)      # 손가락 펴짐상태 출력

            #     # print(left_lm_list)
            #     left_thumb_tip = left_lm_list[4]
            #     left_index_tip = left_lm_list[8]
            #     left_middle_tip = left_lm_list[12]
            #     left_ring_tip = left_lm_list[16]
            #     left_pinty_tip = left_lm_list[20]

            #     # 손가락 거리 기준.
            #     left_index_middle_distance = math.sqrt((left_index_tip[1] - left_middle_tip[1]) ** 2 + (left_index_tip[2] - left_middle_tip[2]) ** 2)
            #     # print(left_index_middle_distance)

            #     # 1.0 왼손 행동 해제 (손 모양이 주먹일 경우)
            #     if not left_pinky_state and not left_ring_state and not left_middle_state and not left_index_state and not left_thumb_state:
            #         self.start_time = time.time()
            #         elapse_time = time.time() - self.start_time
            #         if elapse_time > 3:
            #             self.active_stop()
            #             elapse_time = 0
            #             self.Lclick_count = 0  # 클릭 횟수 초기화
            #             self.LDclick_count = 0
            #             self.Scroll_count = 0
            #             self.Drag_count = 0

            #     # 1.1 마우스 이동 이벤트 (모든 손가락이 핀 상태)
            #     if left_pinky_state and left_ring_state and left_middle_state and left_index_state and left_thumb_state:
            #         self.mouse_MoveEvent(event=left_lm_list, screen_size=pyautogui.size())
            #         self.Lclick_count = 0      # 클릭 횟수 초기화
            #         self.LDclick_count = 0
            #         self.Scroll_count = 0
            #         self.Drag_count = 0

            #     # 1.2 마우스 좌클릭 이벤트 (검지와 중지만 핀 상태 및 두 손가락의 거리 조건)
            #     if not left_pinky_state and not left_ring_state and left_middle_state and left_index_state and left_index_middle_distance < 25:
            #         if self.Lclick_count == 0:
            #             self.Lclick_count += 1  # 클릭 횟수 증가
            #             self.mouse_Left_ClickEvent()
            #         else:
            #             self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")

            #         # self.text_view.append(f"기능: {self.click_count}번째 왼클릭")

            #     # 1.3 마우스 좌 더블클릭 이벤트 (검지와 중지, 약지만 핀 상태 및 검지~중지 손가락의 거리 조건 / 제스처 손가락 피기에 어려움)
            #     if not left_pinky_state and left_ring_state and left_middle_state and left_index_state and left_index_middle_distance < 25:
            #         if self.LDclick_count == 0:
            #             self.LDclick_count += 1  # 클릭 횟수 증가
            #             self.mouse_Left_DoubleClickEvent()
            #         else:
            #             self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")

            #     # 1.4 마우스 좌클릭 후 드래그 (검지와 중지, 소지만 핀 상태 및 검지~중지 손가락의 거리 조건 / 제스처 손가락 피기에 어려움)
            #     if left_pinky_state and not left_ring_state and left_middle_state and left_index_state :
            #         # drag_elapse_time = time.time() - self.start_time                              # 드래그 시간 제한
            #         # if drag_elapse_time > 1 and left_index_middle_distance < 25:
            #         if left_index_middle_distance < 25:
            #             if not self.dragging:
            #                 self.text_view.append("드래그 기능 : 좌클릭 상태")
            #                 pyautogui.mouseDown(button='left')                                      # 좌클릭 누르기
            #                 self.dragging = True                                                    # 드래그 상태 플래그 설정
            #                 self.start_drag_pos = pyautogui.position()                              # 드래그 시작 좌표 저장
            #             else:
            #                 # current_pos = pyautogui.position()
            #                 # drag_distance = abs(current_pos[0] - self.start_drag_pos[0]) + abs(current_pos[1] - self.start_drag_pos[1])
            #                 # if drag_distance < 10 :
            #                 self.text_view.append("드래그 기능 : 드래그 중")
            #                 self.mouse_MoveEvent(event=left_lm_list, screen_size=pyautogui.size())  # 마우스 이동
            #         elif left_index_middle_distance >= 25:
            #             if self.dragging:
            #                 self.text_view.append("드래그 기능 : 드래그 해제 상태")
            #                 pyautogui.mouseUp(button='left')  # 좌클릭 놓기
            #                 self.dragging = False  # 드래그 상태 플래그 해제
            #             # drag_elapse_time = 0

            #     # 1.5 마우스 스크롤 확대 및 축소 이벤트 (엄지와 검지만 핀 상태, 엄지~검지 거리 조건)
            #     left_thumb_index_distance = math.sqrt((left_thumb_tip[1] - left_index_tip[1]) ** 2 + (left_thumb_tip[2] - left_index_tip[2]) ** 2)
            #     #print(left_thumb_index_distance)

            #     if not left_pinky_state and not left_ring_state and not left_middle_state and left_index_state and left_thumb_state:
            #         # if self.Scroll_count == 0:
            #         if 80 < left_thumb_index_distance < 120:
            #             self.text_view.append("기능 : 스크롤 확대 이벤트 감지")
            #             pyautogui.scroll(-20)
            #             # self.Scroll_count += 1
            #         elif 0 < left_thumb_index_distance < 40 :
            #             self.text_view.append("기능 : 스크롤 축소 이벤트 감지")
            #             pyautogui.scroll(20)
            #             # self.Scroll_count += 1
            #         else:
            #             self.text_view.append("기능 : 스크롤 이벤트 정지")
            #             # self.text_view.append("손가락을 펼치고 다시 제스처 취해야 기능 가능")

            # # 2. 오른손 제스처 기준
            # elif right_lm_list and not left_lm_list:
            #     # 손가락 각도 계산
            #     for i, joint in enumerate(joint_list):
            #         a = np.array([right_lm_list[joint[0]][1], right_lm_list[joint[0]][2]])  # 첫번째 좌표
            #         b = np.array([right_lm_list[joint[1]][1], right_lm_list[joint[1]][2]])  # 두번째 좌표
            #         c = np.array([right_lm_list[joint[2]][1], right_lm_list[joint[2]][2]])  # 세번째 좌표

            #         radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            #         right_angle = np.abs(radians * 180.0 / np.pi)

            #         if right_angle > 180.0:
            #             right_angle = 360 - right_angle

            #         right_finger_angles.append(right_angle)

            #     for i, finger_name in enumerate(finger_names):
            #         right_angle = right_finger_angles[i]                                    # 손가락별 관절 각도

            #         # print(f'{finger_name}: {right_angle} degrees')

            #     # 0 ~ 5번까지 6개의 각도가 나온다.
            #     # 0 번 - 엄지가 접힌경우 ----- 10 이하, 평상시 - 약 30 ~ 40, 1번 - 엄지손가락이 구부러진 정도, 2 ~ 5번 - 검지부터 소지까지 접히는 각도
            #     # print(right_finger_angles[0])

            #     if right_finger_angles[0] > 10:
            #         right_thumb_state = True
            #     else:
            #         right_thumb_state = False

            #     right_thumb_state = right_lm_list[4][2] < right_lm_list[3][2] < right_lm_list[2][2] < right_lm_list[1][2]
            #     right_index_state = right_lm_list[8][2] < right_lm_list[7][2] < right_lm_list[6][2] < right_lm_list[5][2]
            #     right_middle_state = right_lm_list[12][2] < right_lm_list[11][2] < right_lm_list[10][2] < right_lm_list[9][2]
            #     right_ring_state = right_lm_list[16][2] < right_lm_list[15][2] < right_lm_list[14][2] < right_lm_list[13][2]
            #     right_pinky_state = right_lm_list[20][2] < right_lm_list[19][2] < right_lm_list[18][2] < right_lm_list[17][2]
            #     # print(right_thumb_state, right_index_state, right_middle_state, right_ring_state, right_pinky_state)      # 손가락 펴짐상태 출력

            #     # print(right_lm_list)
            #     right_thumb_tip = right_lm_list[4]
            #     right_index_tip = right_lm_list[8]
            #     right_middle_tip = right_lm_list[12]
            #     right_ring_tip = right_lm_list[16]
            #     right_pinky_tip = right_lm_list[20]

            #     # (오른손)검지와 중지 사이의 거리 계산.
            #     right_index_middle_distance = math.sqrt((right_index_tip[1] - right_middle_tip[1]) ** 2 + (right_index_tip[2] - right_middle_tip[2]) ** 2)
            #     # print(right_index_middle_distance)

            #     # 2.0 오른손 행동 해제 (손 모양이 주먹일 경우)
            #     if not right_pinky_state and not right_ring_state and not right_middle_state and not right_index_state and not right_thumb_state:
            #         self.start_time = time.time()
            #         elapse_time = time.time() - self.start_time
            #         if elapse_time > 3:
            #             self.active_stop()
            #             elapse_time = 0
            #             self.Rclick_count = 0  # 클릭 횟수 초기화
            #             self.Window_zoom = 0
            #             self.Fuck_count = 0
            #             self.Good_count = 0
            #             self.Keyboard_count = 0

            #     # 2.1 마우스 움직임 이벤트 (모든 손가락이 핀 상태)
            #     if right_thumb_state and right_index_state and right_middle_state and right_ring_state and right_pinky_state:
            #         self.mouse_MoveEvent(event=right_lm_list, screen_size=pyautogui.size())
            #         self.Rclick_count = 0       # 클릭 횟수 초기화
            #         self.Window_zoom = 0
            #         self.Fuck_count = 0
            #         self.Good_count = 0
            #         self.Keyboard_count = 0

            #     # 2.2 마우스 우클릭 이벤트 (검지와 중지만 핀 상태 및 두 손가락의 거리 조건)
            #     if not right_pinky_state and not right_ring_state and right_middle_state and right_index_state and right_index_middle_distance < 25:
            #         if self.Rclick_count == 0:
            #             self.Rclick_count += 1  # 클릭 횟수 증가
            #             self.mouse_Right_ClickEnvet()
            #         else:
            #             self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")

            #     # 2.3 윈도우 창 확대 축소 이벤트
            #     window_original_width = None
            #     window_original_height = None

            #     # (오른손)엄지와 검지 사이의 거리 계산.
            #     distance_bz = math.sqrt((right_thumb_tip[1] - right_index_tip[1]) ** 2 + (right_thumb_tip[2] - right_index_tip[2]) ** 2)

            #     # 검지, 중지, 소지만 펴고 / 검지와 중지 사이의 거리가 30 이상일 경우 윈도우 확대.
            #     if right_pinky_state and not right_ring_state and right_middle_state and right_index_state:
            #     # if not right_pinky_state and not right_ring_state and not right_middle_state and right_index_state and right_thumb_state:
            #         if right_index_middle_distance >= 30 and self.Window_zoom == 0:
            #             self.Window_zoom += 1
            #             self.text_view.append('기능 : 윈도우 확대 이벤트 발생')

            #             # 원래의 윈도우 창 크기 저장.
            #             window = gw.getActiveWindow()               # 현재 활성화 윈도우 창 상태정보 가져오기
            #             window_original_width, window_original_height = window.width, window.height
            #             window.resize(window_original_width, window_original_height)

            #             window.maximize()   # 윈도우 최대화

            #         # 검지와 중지 사이의 거리가 30 미만일 경우 윈도우 축소.
            #         elif right_index_middle_distance < 30 and self.Window_zoom == 0:
            #             self.Window_zoom += 1
            #             self.text_view.append('기능 : 윈도우 축소 이벤트 발생')

            #             window = gw.getActiveWindow()

            #             # 윈도우의 사이즈를 원래 크기로 재설정.
            #             window = gw.getActiveWindow()
            #             window.resizeTo(window_original_width, window_original_height)

            #         else:
            #             self.text_view.append("오류 : 손 펼친 뒤 다시 제스처 취해야 합니다.")

            #     # 2.4 키보드 기능 화상키보드 켜기 (새끼손가락만 펴기)
            #     if right_pinky_state and not right_index_state and not right_middle_state and not right_ring_state:
            #        if self.Keyboard_count == 0:
            #            self.Keyboard_count += 1
            #            self.keyboard_on_Event()
            #        # else:
            #        #     self.Keyboard_count = 0    # 문제 있음 <- 손을 피지도 않았는데도 Keyboard_count가 바로 0으로 되어버림 (타 제스처엔 두 손가락 거리 기준이 있지만 이 코드는 없어서 오류, 기준 마련해야)
            #        #     self.keyboard_off_Event()


            #     # 3. 이외 기능
            #     # 3.1 이스터에그 - 뻐큐! (오른손 기준)
            #     if not right_pinky_state and not right_ring_state and right_middle_state and not right_index_state and not right_thumb_state:
            #         if self.Fuck_count == 0:
            #             self.Fuck_count += 1  # 클릭 횟수 증가
            #             self.text_view.append('기능 : 뻐큐 금지!')

            #     # 3.2 이스터에그 - 굿! (오른손 기준)
            #     if not right_pinky_state and not right_ring_state and not right_middle_state and not right_index_state and right_thumb_state:
            #         if self.Good_count == 0:
            #             self.Good_count += 1  # 클릭 횟수 증가
            #             self.text_view.append('기능 : 굿 감사합니다')


            # # 4. 양손 인식시 ~ (양손 기반 제스처 없음.)
            # elif left_lm_list and right_lm_list:
            #     self.text_view.append('임시 양손 인식')

            # # 5. 손 인식하지 않았을 시
            # else:
            #     if self.hand_detect_count == 0:
            #         self.hand_detect_count += 1
            #         self.text_view.append('손이 인식되지 않았습니다')


            # 프레임 화면에 출력
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_img)
            self.Webcam_label.setPixmap(q_pixmap)



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