# 네트워크 관련 코드
import struct
import socket
import threading
import Network_Packet
import base64

class Client:
    # 생성자
    def __init__(self, ip, port):
        self.sock = None
        self.recv_del = None
        self.RThread = None
        self.ip = ip
        self.port = port
        self.in_running = True

    def open(self, fun):
        self.recv_del = fun
        try:
            # 소켓 생성
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 연결
            self.sock.connect((self.ip, self.port))

            # 수신 스레드 생성
            self.RThread = threading.Thread(target=self.recv_thread)
            self.RThread.daemon = True
            self.RThread.start()

            # 결과 반환
            return True
        except Exception as e:
            print(f"Error occurred while opening the client : {e}")
            return False

    def close(self):
        self.sock.close()
        self.in_running = False

    def recv_thread(self):
        try:
            data = b""                  # 초기값을 빈 바이트열로 설정
            while self.in_running:
                # 데이터 수신처리
                new_data = self.RecvData(data)
                if new_data is None:
                    # 새로 받은 데이터가 없으면 루프를 다시 실행
                    continue
                data = new_data

                msg = data.decode('utf-8').strip('\0')
                # sp1 = msg.split('@')
                # if sp1[0] == Network_Packet.Sendbyte_ACK:
                #     decoded_base = base64.b64decode(msg)
                #     msg = decoded_base.decode('utf-8')
                #     self.recv_del(msg)
                # else:

                print("recv_thread msg 통과")
                self.recv_del(msg)

        except Exception as e:
            print(e)
            self.close()

    # 데이터 송/수신
    def SendData(self, msg):
        buffer = msg.encode('utf-8')
        self.send_data(buffer)

    def send_data(self, data):
        try:
            total = 0  # 보낸크기
            size = len(data)  # 보낼크기
            left_data = size  # 남은크기

            # 1) 전송할 데이터의 크기 전달
            data_size = struct.pack('I', size)
            self.sock.send(data_size)

            # 2) 실제 데이터 전송
            while total < size:
                ret = self.sock.send(data[total:])
                total += ret
                left_data -= ret
        except Exception as e:
            print(e)

    def RecvData(self, data):
        try:
            total = 0
            size = 0
            left_data = 0

            # 1) 수신할 데이터 크기 알아내기
            data_size = self.sock.recv(4)
            size = struct.unpack('I', data_size)[0]
            left_data = size

            data = b''

            # 2) 실제 데이터 수신
            while total < size:
                recv_data = self.sock.recv(left_data)
                if not recv_data:
                    break
                data += recv_data
                total += len(recv_data)
                left_data -= len(recv_data)

            return data

        except Exception as e:
            print(e)
            return None