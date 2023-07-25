# 네트워크 관련 코드
import struct

# 1. 네트워크 연결하는 부분
def Connect(sock, ip, port):
    # 서버에 연결
    sock.connect((ip, port))

    return True

# 2. 데이터 송신 부분 ( 클라 -> 서버 )
def SendData(sock, msg):
    # 1. 전송할 데이터의 크기 전송
    data_size = struct.pack('I', len(msg))
    sock.send(data_size)

    # 2. 실제 데이터 전송
    sock.send(msg.encode('utf-8'))

# 3. 데이터 수신 부분 ( 서버 -> 클라 )
def RecvData(sock):
    # 3. 데이터 크기 수신
    data_size = sock.recv(4)
    data_size = struct.unpack('I', data_size)[0]

    # 4. 실제 데이터 수신
    recv_data = b""
    while len(recv_data) < data_size:
        chunk = sock.recv(min(data_size - len(recv_data), 1024))
        if not chunk:
            break
        recv_data += chunk

    print(recv_data.decode('utf-8'))

    return recv_data.decode('utf-8')