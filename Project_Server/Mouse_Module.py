# MouseModule.py : 마우스, 키보드 기능의 상세 코드

import cv2
import math
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QCursor

import autopy
import pyautogui
from HandTrackingModule import HandDetector

class MouseFunction:
    def __init__(self):
        self.screen_size = autopy.screen.size()
        self.screen_size_x, self.screen_size_y = self.screen_size

    active_stop = False  # 임시

    ## 공통 기능 / 양손 제스처 ##
    # 1.1 / 2.1 마우스 이동 이벤트
    def handle_mouse_move(self, event, screen_size):
        if MouseFunction.active_stop:
            return

        size_x, size_y = screen_size
        # cursor_pos = event.pos()
        cursor_x = int(event[9][1] * size_x / 620)          # x좌표 스케일링
        cursor_y = int(event[9][2] * size_y / 360)          # y좌표 스케일링
        cursor_x = min(size_x - 1, max(0, cursor_x))        # x좌표 제한
        cursor_y = min(size_y - 1, max(0, cursor_y))        # y좌표 제한
        cursor = QCursor()
        # QCursor.setPos(cursor_x, cursor_y)
        self.cursor().setPos(cursor_x, cursor_y)

    ## 1. 왼손 제스처 기준 ##
    # 1.2 마우스 좌클릭 관련 (1번 좌클릭 / 좌 프레스(계속 누르는) )
    def handle_left_mouse_click(self):
        # if MouseFunction.active_stop:
        #    return

        # 클릭 이벤트 다수 입력 방지 - 시간초 제한?
        pyautogui.click()  # 파일 선택 혹은 웹 브라우저 창 선택 등의 동작 수행

    # 1.3 마우스 좌 더블클릭 이벤트 (2번 좌클릭)
    def handle_left_mouse_doubleclick(self):
        # if MouseFunction.active_stop:
        #    return

        pyautogui.doubleClick()

    # 1.4 마우스 좌클릭 후 드래그 / 드래그 and 드롭 이벤트
    def handle_left_mouse_drag(self):
        # if MouseFunction.active_stop:
        #    return

        pyautogui.mouseDown()       # 좌클릭 이벤트 발생
        pyautogui.dragTo()          # 드래그 이벤트
        pyautogui.mouseUp()         # 클릭 해제 이벤트

    # 구) 마우스 좌클릭 후 끌어서 놓기 이벤트 (파일 이동 / 클릭 앤 무브 )
    # - 구) 마우스 좌클릭 후 드래그 이벤트 동일해서 코드 삭제 하기
    # def handle_left_mouse_dragandmove(self):
    #     # if MouseFunction.active_stop:
    #     #    return
    #
    #     pyautogui.mouseDown()               # 클릭 이벤트 발생
    #     pyautogui.moveTo()                  # 드래그 시작 위치로 이동
    #     pyautogui.dragTo(duration=1)        # 드래그 동작 수행
    #     pyautogui.mouseUp()                 # 클릭 해제 이벤트

    # 1.5 마우스 스크롤 확대 및 축소 이벤트
    def handle_mouse_scroll(self, event):
        if MouseFunction.active_stop:
            return

        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom_in()
        elif delta < 0:
            self.zoom_out()

    # 1.5.1 화면 스크롤 - 확대 동작 수행
    def handle_mouse_zoom_in(self, event):
        if MouseFunction.active_stop:
            return

        current_width = self.Webcam_label.width()
        current_height = self.Webcam_label.height()
        self.Webcam_label.resize(current_width + 10, current_height + 10)

    # 1.5.2 화면 스크롤 - 축소 동작 수행
    def handle_mouse_zoom_out(self, event):
        if MouseFunction.active_stop:
            return

        current_width = self.Webcam_label.width()
        current_height = self.Webcam_label.height()
        self.Webcam_label.resize(current_width + 10, current_height + 10)

    ## 2. 오른손 제스처 기준 ##
    # 2.2 마우스 우클릭 이벤트 (1번 우클릭 / 우 프레스 (계속 누르는) )
    def handle_right_mouse_click(self):
        pyautogui.rightClick()

    # 2.3 윈도우 창 확대 축소 이벤트

    # 2.4 키보드 기능 화상키보드 켜기 (새끼손가락만)





