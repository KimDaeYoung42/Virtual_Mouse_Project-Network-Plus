import socket
import sys
import threading


class Server:
    def __init__(self, port):
        self.recv_del = None
        self.server = None
        self.sockets = []

        self.port = port

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
        while True:
            try:
                data = None
                if self.ReceiveData(client, data):
                    msg = data.decode("utf-8").strip('\0')
                    self.recv_del(client, msg)
                else:
                    print("수신 데이터 없음")
                    raise Exception("수신 오류")

            except Exception as ex:
                print(ex)
                self.sockets.remove(client)
                client.close()
                break

    # 데이터 송신
    def SendData(self, sock, msg, size):
        bmsg = msg.encode("utf-8")
        self.SendDataBytes(sock, bmsg, size)

    def SendDataBytes(self, sock, data, size):
        try:
            total = 0
            left_data = size
            data_size = size.to_bytes(4, byteorder="little")
            ret = sock.send(data_size)
            while total < size:
                ret = sock.send(data[total:])
                total += ret
                left_data -= ret

        except Exception as ex:
            print(ex)

    def SendAllData(self, msg, size):
        bmsg = msg.encode("utf-8")
        for s in self.sockets:
            self.SendDataBytes(s, bmsg, size)

    # 데이터 수신
    def ReceiveData(self, sock, data):
        try:
            data_size = sock.recv(4)
            size = int.from_bytes(data_size, byteorder="little")
            data = bytearray(size)
            total = 0
            left_data = size
            while total < size:
                ret = sock.recv(left_data)
                if not ret:
                    break
                data[total:total+len(ret)] = ret
                total += len(ret)
                left_data -= len(ret)
            return True

        except Exception as ex:
            print(ex)
            return False