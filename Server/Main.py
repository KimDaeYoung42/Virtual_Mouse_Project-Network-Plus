# 프로그램 시작지점

import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow
from Server import Server
import Packet
import Control

from PIL import Image
import io

class Main(QMainWindow):
    # 생성자
    def __init__(self):
        super().__init__()
        loadUi("UI_Server_Test.ui", self)  # UI 파일을 현재 클래스와 연결

        self.server = Server(9000)

        self.user_list = []

        # UI 입력
        # 이미지 입력 : Webcam_label3
        # 접속자 리스트뷰 : text_user_view.append('')
        # 수신 리스트뷰 : text_receive_view.append('')
        # 송신 리스트뷰 : text_transmit_view.append('')
        
        self.Run()


    def Server_RecvData(self, sock, msg):
        
        # 1. 수신 데이터 처리
        self.text_receive_view.append(f'수신 메시지 : {msg}')

        # 2. 수신 메시지 파싱처리
        sp1 = msg.split('@')

        # 3. 수신 메시지에 대한 적절한 동작
        if sp1[0] == Packet.Login:
            ret = Control.Login(sp1[1], self.server)
            self.user_list.append(sp1[1])
        elif sp1[0] == Packet.Logout:
            ret = Control.Logout(sp1[1], self.server)
            self.user_list.remove(sp1[1])
        elif sp1[0] == Packet.Shortmessage:
            sp2 = sp1[1].split('#')
            ret = Control.Shortmessage(sp2[0], sp2[1], self.server)
        elif sp1[0] == Packet.Sendbyte:
            self.ByteToImage(sp1[1])
            ret = Control.Sendbytes(sp1[1], self.server)
        
        # 접속자 리스트뷰 
        if self.user_list:
            self.text_user_view.clear()

            for user in self.user_list:
                self.text_user_view.append(user)

        # 송신 메시지 로그
        if ret:
            self.text_transmit_view.append(f'송신 메시지 : {ret}')
    
    def Run(self):
        self.server.Run(self.Server_RecvData)

    # 받은 byte배열을 이미지로 변환해서 Webcam_label3에 출력
    def ByteToImage(self, data):
        # data -> 현재 문자열 상태 ( 인코딩 필요 )
        byte_array = data.encode('utf-8')

        # 바이트 배열을 바이트 스트림으로 변환
        byte_stream = io.BytesIO(byte_array)
    
        # 바이트 스트림으로부터 이미지 열기
        image = Image.open(byte_stream)

        # 이미지 표시 Webcam_label3


 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

