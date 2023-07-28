# 프로그램 시작지점

import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow
from Server import Server
from Control import Control

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI_Server_Test.ui", self)  # UI 파일을 현재 클래스와 연결

        self.server = Server(9000)
        Control().SendServer(self.server)


        # UI 입력
        # 이미지 입력 : Webcam_label3
        # 접속자 리스트뷰 : text_user_view.append('')
        # 수신 리스트뷰 : text_receive_view.append('')
        # 송신 리스트뷰 : text_transmit_view.append('')
        
        self.Run()


    def Server_RecvData(self, msg):
        print(f'수신메시지 : {msg}')

    
    def Run(self):
        self.server.Run(self.Server_RecvData)
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

