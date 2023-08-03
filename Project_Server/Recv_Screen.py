# 공유 화면 확대 코드

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
        self.dataset = None

        loadUi("UI_App_Screen.ui", self)

    def Recv_Screen_Thread(self, img):
        while True:

            # 데이터 검증작업
            if self.dataset is None:
                self.dataset = img
                data_img = self.dataset
                break
            else:
                # img 가 이전 데이터와 동일한 경우, 이전 데이터 삭제
                if img == self.dataset:
                    self.dataset = None
                    data_img = None
                    break
                # img가 이전 데이터와 다른 경우, data를 저장하고 이전 데이터 삭제
                else:
                    self.dataset = img
                    data_img = self.dataset

                    # 실제 이미지 데이터 -> UI 출력 파트
                    data = img.encode('utf-8')
                    decoded_data = base64.b64decode(data)
                    img_data = zlib.decompress(decoded_data)

                    # 데이터를 UI에 추가하거나 갱신
                    self.update_screen(img_data)
                    break


    def update_screen(self, img_data):
        # Bytes 데이터를 -> PIL의 Image 타입으로 변환 작업
        screen_image = Image.frombytes("RGB", (1920, 1080), img_data)

        # 이미지 크기를 1600 x 900으로 조정
        width, height = 1600, 900
        resized_image = screen_image.resize((width, height), Image.ANTIALIAS)

        # 이미지를 PyQt5의 QImage로 변환
        qimage = QImage(resized_image.tobytes(), width, height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        # QLabel에 이미지를 표시
        self.Screen_label.setPixmap(pixmap)