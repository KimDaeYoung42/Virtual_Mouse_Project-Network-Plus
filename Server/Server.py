import socket
import sys
import threading
import struct


class Server:
    def __init__(self, port):
        self.recv_del = None
        self.server = None
        self.sockets = []

        self.Server_port = port
        self.Init()


    def Init(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            ipep = ('0.0.0.0', self.port)
            self.server.bind(ipep)
            self.server.listen(20)

            print("서버 시작.... 클라이언트 접속 대기중")

        except Exception as e:
            print(e)
            sys.exit(0)

    def Run(self, fun):
        self.recv_del = fun
        while True:
            try:
                client, addr = self.server.accept()
                self.sockets.append(client)

                print(f'{addr[0]}, {addr[1]} 접속')

                self.thread = threading.Thread(target=self.WorkThread, args=(client,))
                self.thread.daemon = True
                self.thread.start()

            except Exception as e:
                print(e)

    def WorkThread(self, client):
        try:
            data = b''
            while True:
                msg = ''
                if self.ReceiveData(client, data):
                    msg = data.decode('utf-8').strip('\0')
                    self.recv_del(client, msg)
                else:
                    print("수신 데이터 없음")
                    raise Exception("수신 오류")
        except Exception as e:
            print(e)
            self.sockets.remove(client)
            client.close()


    # 데이터 송신 ( 나에게 데이터를 보낸 클라이언트만 )
    def SendData(self, sock, msg, size):
        bmsg = msg.encode("utf-8")
        self.Send_Data(sock, bmsg, size)
        ret = sock.Send(bmsg, len(bmsg), 0)
        print(f'데이터 전송 : {ret}byte')
        
    # 연결된 모든 클라이언트에 데이터 송신
    def SendAllData(self, msg, size):
        for s in self.sockets:
            self.SendData(s, msg, size)

    def Send_Data(self, sock, data, _size):
        try:
            total = 0           # 보낸크기
            size = _size        # 보낼크기
            left_data = size    # 남은크기

            # 전송할 데이터 크기 전달
            data_size = struct.pack('I', size)
            sock.send(data_size)

            while total < size:
                ret = sock.send(data[total:], left_data)
                total += ret
                left_data -= ret

        except Exception as e:
            print(e)

    # 데이터 수신
    def ReceiveData(self, sock, data):
        try:
            total = 0       # 받을 크기
            size = 0        # 받은 크기
            left_data = 0   # 남은 크기

            data_size = sock.recv(4)
            size = struct.unpack('I', data_size)[0]
            left_data = size

            data = b''

            while total < size:
                recv = sock.recv(left_data)
                if not recv:
                    break
                data += recv
                total += len(recv)
                left_data -= len(recv)

            return data

        except Exception as ex:
            print(ex)
            return None