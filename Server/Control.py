
import Packet


# 수신 메시지에 대한 처리
def Login(name, server):

    # 응답패킷 생성 및 전송
    pack = Packet.LogIn_ACK(name)
    server.SendAllData(pack, len(pack))

    return pack

def Logout(name, server):

    # 응답패킷 생성 및 전송
    pack = Packet.LogOut_ACK(name)
    server.SendAllData(pack, len(pack))

    return pack

def Shortmessage(name, msg, server):
    # 응답패킷 생성 및 전송
    pack = Packet.ShortMessage_ACK(name, msg)
    server.SendAllData(pack, len(pack))

    return pack

def Sendbytes(bytes, server):
     # 응답패킷 생성 및 전송
    pack = Packet.BytesSend_ACK(bytes)
    server.SendAllData(pack, len(pack))

    return pack