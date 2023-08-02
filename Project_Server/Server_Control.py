import socket
import threading
import sys
import struct

from Network_Packet import Packet

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
                msg = msg_data.decode('utf-8').strip('\0')
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
        pack = Packet.LogIn(name)
        server.send_all_data(pack)
        return pack

    @staticmethod
    def logout(name, server):
        pack = Packet.LogOut(name)
        server.send_all_data(pack)
        return pack

    @staticmethod
    def ShortMessage(name, msg, server):
        pack = Packet.ShortMessage(name, msg)
        server.send_all_data(pack)
        return pack

    @staticmethod
    def SendByte(bytes_data, server):
        pack = Packet.SendByte(bytes_data)
        server.send_all_data(pack)
        return pack
    
    # Server -> Client
    @staticmethod
    def login_ack(name, list, server):
        pack = Packet.LogIn_ACK(name, list)
        server.send_all_data(pack)
        return pack
    
    @ staticmethod
    def loginlist_ack(list, server):
        pack = Packet.LogInList_ACK(list)
        server.send_all_data(pack)
        return pack
    
    @staticmethod
    def logout_ack(name, list, server):
        pack = Packet.LogOut_ACK(name, list)
        server.send_all_data(pack)
        return pack
    @staticmethod
    def short_message_ack(name, msg, server):
        pack = Packet.ShortMessage_ACK(name, msg)
        server.send_all_data(pack)
        return pack

    @staticmethod
    def send_bytes_ack(bytes_data, server):
        # bytes_data -> 문자열
        pack = Packet.SendByte_ACK(bytes_data)
        # pack => SENDBYTE_ACK@bytes, bytes -> not 'str'
        # encoded_data = base64.b64encode(pack)   
        server.send_all_data(pack)
        return pack