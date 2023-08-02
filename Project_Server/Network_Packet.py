from enum import Enum
# 네트워크 패킷 관련

# 데이터 송/수신 할 때 패킷을 어떻게 주고받을 것인가?
# 필요한 패킷
# 1. 로그인 ( 클라이언트가 서버에 접속했을 때 접속자명을 통지 )
# 2. 채팅
# 3. 파일 공유 ( 보내기 )
# 4. 화면 공유
class PacketTag(Enum):
    # Client -> Server
    Login = "LOGIN"
    Loginlist = "LOGINLIST"
    Logout = "LOGOUT"
    Shortmessage = "SHORTMESSAGE"
    Sendfile = "SENDFILE"
    Sendbyte = "SENDBYTE"

    # Server - > Client
    Login_ACK = "LOGIN_ACK"
    Loginlist_ACK = "LOGINLIST_ACK"
    Logout_ACK = "LOGOUT_ACK"
    Shortmessage_ACK = "SHORTMESSAGE_ACK"
    Sendfile_ACK = "SENDFILE_ACK"
    Sendbyte_ACK = "SENDBYTE_ACK"


# Client -> Server 전송 패킷 만드는 부분

class Packet:
    # 로그인 ( 서버에 접속시 접속자의 이름을 알림 )
    @staticmethod
    def LogIn(name):
        pack = ''

        pack += PacketTag.Login.value + '@'
        pack += name

        return pack


    # 로그아웃 ( 서버 연결 해제 )
    @staticmethod
    def LogOut(name, list):
        pack = ''

        pack += PacketTag.Logout.value + '@'
        pack += name

        return pack

    # 로그인 리스트
    @staticmethod
    def LogInList(list):
        pack = ''

        pack += PacketTag.Loginlist.value + '@'
        for name in list:
            pack += name + '#'

        return pack


    # 채팅 ( 메시지 전송, 이름과 메시지 )
    @staticmethod
    def ShortMessage(name, msg):
        pack = ''

        pack += PacketTag.Shortmessage.value + '@'
        pack += name + '#'
        pack += msg

        return pack


    # 파일 전송 ( 파일 이름과 파일의 크기 )
    @staticmethod
    def SendFile(filename, size):
        pack = ''

        pack += PacketTag.Sendfile.value + '@'
        pack += filename + '#'
        pack += size

        return pack


    # 화면 공유
    @staticmethod
    def SendByte(bytes):
        # bytes -> 문자열로 바꿔서 보내야 할듯?
        decoded_bytes = bytes.decode('utf-8', errors='ignore')
        pack = ''

        pack += PacketTag.Sendbyte.value + '@'
        pack += decoded_bytes

        return pack


        ###############################################################################################

    # Server -> Client 전송 패킷 만드는 부분
    @staticmethod
    def LogIn_ACK(name, list):
        pack = ''

        pack += PacketTag.Login_ACK.value + '@'
        pack += name + '#'
        for user in list:
            pack += user + '$'

        return pack

    @staticmethod
    def LogInList_ACK(list):
        pack = ''

        pack += PacketTag.Loginlist_ACK.value + '@'
        for name in list:
            pack += name + '#'

        return pack
    
    @staticmethod
    def LogOut_ACK(name, list):
        pack = ''

        pack += PacketTag.Logout_ACK.value + '@'
        pack += name + '#'
        for user in list:
            pack += user + '$'

        return pack

    @staticmethod
    def ShortMessage_ACK(name, msg):
        pack = ''

        pack += PacketTag.Shortmessage_ACK.value + '@'
        pack += name + '#'
        pack += msg

        return pack

    @staticmethod
    def SendFile_ACK(filename, size):
        pack = ''

        pack += PacketTag.Sendfile_ACK.value + '@'
        pack += filename + '#'
        pack += size

        return pack

    @staticmethod
    def SendByte_ACK(bytes):
        pack = ''

        decoded_bytes = bytes.decode('utf-8', errors='ignore')
        pack += PacketTag.Sendbyte_ACK.value + '@'
        pack += decoded_bytes

        return pack
