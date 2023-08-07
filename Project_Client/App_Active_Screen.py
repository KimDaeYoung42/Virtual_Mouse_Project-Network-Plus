# App_Active_Screen.py : 공유 화면 확대 코드

import base64
import time
import zlib
from PIL import Image
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class Active_Screen(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi("UI_App_Screen.ui", self)
        self.setMinimumSize(1620, 950)
        self.setMaximumSize(1620, 950)

        self.dataset = None
        # self.img_data = None

    # 1. 공유화면 수신 스레드
    def Recv_Screen_Thread(self, img):
        while True:
            print("기능 : 화면 데이터 메시지222")
            self.receive_started = True

            # (1) 데이터 검증 작업
            if self.dataset is None:
                # (2) dataset이 비어있는 경우, data를 바로 저장
                self.dataset = img
                data_img = self.dataset
                break

            else:
                # (3) img가 이전 데이터와 동일한 경우, 이전 데이터 삭제
                if img == self.dataset:
                    self.dataset = None
                    data_img = None
                    break

                else:
                    # (4) img가 이전 데이터와 다른 경우, data를 저장하고 이전 데이터 삭제
                    self.dataset = img
                    data_img = self.dataset

                    # (5) 실제 이미지 데이터 -> UI 출력 파트
                    data = data_img.encode('utf-8')
                    decoded_data = base64.b64decode(data)
                    img_data = zlib.decompress(decoded_data)

                    # (6) 데이터를 UI에 추가하거나 갱신
                    self.update_screen(img_data)
                    break

            # time.sleep(3)

    # 2. 공유화면 표현 기능
    def update_screen(self, img_data):
        # (1) Bytes 데이터를 -> PIL의 Image 타입으로 변환 작업
        screen_image = Image.frombytes("RGB", (1920, 1080), img_data)

        # (2) 이미지 크기를 1600 x 900으로 조정
        width, height = 1600, 900
        resized_image = screen_image.resize((width, height), Image.ANTIALIAS)

        # (3) 이미지를 PyQt5의 QImage로 변환
        qimage = QImage(resized_image.tobytes(), width, height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        # (4) QLabel에 이미지를 표시
        self.Screen_label.setPixmap(pixmap)



