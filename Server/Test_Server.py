import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QListWidget, QTextEdit
import socket
import threading
import struct
import base64
from enum import Enum

class Win_Main(QMainWindow):
    class PacketTag(Enum):
        # Client -> Server
        LOGIN = "LOGIN"
        LOGOUT = "LOGOUT"
        SHORTMESSAGE = "SHORTMESSAGE"
        SENDBYTE = "SENDBYTE"

        # Server -> Client
        LOGIN_ACK = "LOGIN_ACK"
        LOGOUT_ACK = "LOGOUT_ACK"
        SHORTMESSAGE_ACK = "SHORTMESSAGE_ACK"
        SENDBYTE_ACK = "SENDBYTE_ACK"

    def __init__(self):
        super().__init__()

        self.server = Server(9000)
        self.user_list = []

        self.init_ui()
        self.run_server()

    def init_ui(self):
        self.setWindowTitle("가상 인터페이스 서버")
        self.setGeometry(100, 100, 640, 480)

        self.user_listWidget = QListWidget(self)
        self.user_listWidget.setGeometry(10, 10, 200, 460)

        self.text_receive_view = QTextEdit(self)
        self.text_receive_view.setGeometry(220, 10, 400, 230)

        self.text_transmit_view = QTextEdit(self)
        self.text_transmit_view.setGeometry(220, 250, 400, 220)

    def server_recv_data(self, sock, msg):
        tag, data = msg.split('@', 1)

        if not tag == self.PacketTag.SENDBYTE:
            print(f'수신 메시지 : {msg}')

        elif tag == self.PacketTag.SENDBYTE:
            print(f'수신 메시지 : {tag}@bytes')

        
        if tag == self.PacketTag.LOGIN.value:
            self.ret = Control.login_ack(data, self.server)
            self.user_list.append(data)
            self.update_user_list()

        elif tag == self.PacketTag.LOGOUT.value:
            self.ret = Control.logout_ack(data, self.server)
            self.user_list.remove(data)
            self.update_user_list()

        elif tag == self.PacketTag.SHORTMESSAGE.value:
            name, msg = data.split('#', 1)
            self.ret = Control.short_message_ack(name, msg, self.server)

        elif tag == self.PacketTag.SENDBYTE.value:
            self.ret = Control.send_bytes_ack(data, self.server)
            tag, data = self.ret.split('@', 1)
            self.ret = tag + '@bytes'

        print(f'송신 메시지 : {self.ret}')

    def update_user_list(self):
        self.user_listWidget.clear()
        self.user_listWidget.addItems(self.user_list)

    def run_server(self):
        self.server.run(self.server_recv_data)


class Server:
    def __init__(self, port):
        self.recv_del = None
        self.server = None
        self.sockets = []
        self.server_port = port
        self.init_server()

    def init_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ipep = ('0.0.0.0', self.server_port)
            self.server.bind(ipep)
            self.server.listen(20)
            print("서버 시작.... 클라이언트 접속 대기중")

        except Exception as e:
            print(e)
            sys.exit(0)

    def run(self, fun):
        self.recv_del = fun
        while True:
            try:
                client, addr = self.server.accept()
                self.sockets.append(client)
                print(f'{addr[0]}, {addr[1]} 접속')
                self.thread = threading.Thread(target=self.work_thread, args=(client,))
                self.thread.daemon = True
                self.thread.start()

            except Exception as e:
                print(e)

    def work_thread(self, client):
        try:
            while True:
                data = b''
                msg_data = self.receive_data(client)
                if not msg_data:
                    break
                # print(msg_data) # b'SENDBYTE@bytes'
                msg = msg_data.decode('utf-8').strip('\0')
                # print(msg)  # SENDBYTE@bytes
                # msg[0] -> Sendbyte, msg[1] -> bytes () base64로 인코딩된
                # bytes = msg.split('@')
                # bytes[0] -> SENDBYTE, bytes[1] -> bytes
                # 만약 이미지 데이터 -> 바이트배열로 변환한 값을 받았다면 base64로 디코딩을 먼저 하고 utf-8로 디코딩 한다.
                # if bytes[0] == Packet.send_byte:
                #     decoded_base = base64.b64decode(msg_data)
                #     data = decoded_base.decode('utf-8')
                #     self.recv_del(client, data)    
                # 일반적인 데이터를 받았을 때.
                self.recv_del(client, msg)

        except Exception as e:
            print(e)
            self.sockets.remove(client)
            client.close()

    def send_data(self, sock, msg):
        bmsg = msg.encode('utf-8')
        self.send_data_with_size(sock, bmsg)

    def send_data_with_size(self, sock, data):
        size = len(data)
        data_size = struct.pack('I', size)
        sock.send(data_size)

        total_sent = 0
        while total_sent < size:
            sent = sock.send(data[total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent += sent

    def send_all_data(self, msg):
        for s in self.sockets:
            self.send_data(s, msg)

    def receive_data(self, sock):
        data_size = sock.recv(4)
        size = struct.unpack('I', data_size)[0]
        data = b''

        while len(data) < size:
            recv_data = sock.recv(size - len(data))
            if not recv_data:
                break
            data += recv_data

        return data if len(data) == size else None


class Control:
    # Client -> Server
    @staticmethod
    def login(name, server):
        pack = Packet.login(name)
        server.send_all_data(pack)
        return pack

    @staticmethod
    def logout(name, server):
        pack = Packet.logout(name)
        server.send_all_data(pack)
        return pack

    @staticmethod
    def short_message(name, msg, server):
        pack = Packet.short_message(name, msg)
        server.send_all_data(pack)
        return pack

    @staticmethod
    def send_bytes(bytes_data, server):
        pack = Packet.send_byte(bytes_data)
        server.send_all_data(pack)
        return pack
    
    # Server -> Client
    @staticmethod
    def login_ack(name, server):
        pack = Packet.login_ack(name)
        server.send_all_data(pack)
        return pack
    
    @staticmethod
    def logout_ack(name, server):
        pack = Packet.logout_ack(name)
        server.send_all_data(pack)
        return pack
    @staticmethod
    def short_message_ack(name, msg, server):
        pack = Packet.short_message_ack(name, msg)
        server.send_all_data(pack)
        return pack

    @staticmethod
    def send_bytes_ack(bytes_data, server):
        # bytes_data -> 문자열
        pack = Packet.send_byte_ack(bytes_data)
        # pack => SENDBYTE_ACK@bytes, bytes -> not 'str'
        # encoded_data = base64.b64encode(pack)   
        server.send_all_data(pack)
        return pack


class Packet:
    # Client -> Server
    @staticmethod
    def login(name):
        return f"{Win_Main.PacketTag.LOGIN.value}@{name}"


    @staticmethod
    def logout(name):
        return f"{Win_Main.PacketTag.LOGOUT.value}@{name}"


    @staticmethod
    def short_message(name, msg):
        return f"{Win_Main.PacketTag.SHORTMESSAGE.value}@{name}#{msg}"

    @staticmethod
    def send_byte(bytes_data):
        return f"{Win_Main.PacketTag.SENDBYTE.value}@{bytes_data}"
    
    # Server -> client
    @staticmethod
    def login_ack(name):
        return f"{Win_Main.PacketTag.LOGIN_ACK.value}@{name}"
    
    @staticmethod
    def logout_ack(name):
        return f"{Win_Main.PacketTag.LOGOUT_ACK.value}@{name}"
    
    @staticmethod
    def short_message_ack(name, msg):
        return f"{Win_Main.PacketTag.SHORTMESSAGE_ACK.value}@{name}#{msg}"

    @staticmethod
    def send_byte_ack(bytes_data):
        return f"{Win_Main.PacketTag.SENDBYTE_ACK.value}@{bytes_data}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Win_Main()
    window.show()
    sys.exit(app.exec_())
