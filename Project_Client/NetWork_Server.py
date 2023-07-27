import socket
import threading


class Server:
    def __init__(self):
        
        self.server = None
        self.recv_del = None
        self.sockets = []

        self.port = 9000

        self.Init()

        # UI 만들어서 서버 로그 

    def Init(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind('0.0.0.0'. server_port)
        self.server.listen(20)

        print('서버 시작...... 클라이언트 접속 대기중')    

    def Run(self, fun):
        self.recv_del = fun
        while True:
            try:
                client_socket, client_address = self.server.accept()
                self.sockets.append(client_socket)
                
                ip, port = client_address
                print(f"{ip}, {port} 접속")

                thread = threading.Thread(self, target=self.WorkThread)
                thread.daemon = True
                thread.start()

            except Exception as e:
                print(e)

    def WorkThread(self, clinet_socket):
        try:
            while True:
                data = clinet_socket.recv(1024)
                if not data:
                    break
                msg = data.decode().strip('\0')
                self.recv_del(clinet_socket, msg)
        except Exception as e:
            print(e)
            self.sockets.remove(clinet_socket)
            clinet_socket.close()

    # 데이터 송/수신 
    def SandData(self, sock, msg, size):
        bmsg = msg.encode('utf-8')
        self.Send_Data(sock, bmsg, size)
        ret = sock.Send(bmsg)
        print(f'데이터 전송 : {ret}byte')

    def SendAllData(self, sock, msg, size):
        for s in self.sockets:
            self.SendData(s, msg, size)

    def Send_Data(self, sock, data):
        try:
            size = len(data)  # 보낼 크기

            # 전송할 데이터 크기 전달
            data_size = size.to_bytes(4, byteorder='big')
            ret = sock.send(data_size)

            # 실제 데이터 전송
            total = 0
            left_data = size
            while total < size:
                ret = sock.send(data[total:])
                total += ret
                left_data -= ret

        except Exception as e:
            print(e)
            

    def ReceiveData(self, sock):
        try:
            # 수신할 데이터 크기
            data_size = sock.recv(4)
            size = int.from_bytes(data_size, byteorder='big')
            left_data = size

            data = bytearray()

            # 실제 데이터 수신
            while left_data > 0:
                chunk = sock.recv(left_data)
                if not chunk:
                    break
                data += chunk
                left_data -= len(chunk)

            return data if len(data) == size else None
        except Exception as ex:
            print(ex)

    

    

    


    