# Network_Packet.py : 네트워크 패킷 관련

# Client -> Server
Login = "LOGIN"
Loginlist = "LOGINLIST"
Logout = "LOGOUT"
Shortmessage = "SHORTMESSAGE"
Sendfile = "SENDFILE"
Sendbyte = "SENDBYTE"
Sendremote = "SENDREMOTE"
Request_Screen = "REQUEST_SCREEN"

# Server - > Client
Login_ACK = "LOGIN_ACK"
Loginlist_ACK = "LOGINLIST_ACK"
Logout_ACK = "LOGOUT_ACK"
Shortmessage_ACK = "SHORTMESSAGE_ACK"
Sendfile_ACK = "SENDFILE_ACK"
Sendbyte_ACK = "SENDBYTE_ACK"
Sendbytebreak_ACK = "SENDBYTEBREAK_ACK"
Sendremote_ACK = "SENDREMOTE_ACK"
Request_Screen_ACK = "REQUEST_SCREEN_ACK"
Request_Screen_Stop_ACK = "REQUEST_SCREEN_STOP_ACK"


# Client -> Server 전송 패킷 만드는 부분

# 로그인 ( 서버에 접속시 접속자의 이름을 알림 )
def LogIn(name):
    pack = ''

    pack += Login + '@'
    pack += name

    return pack


# 로그아웃 ( 서버 연결 해제 )
def LogOut(name):
    pack = ''

    pack += Logout + '@'
    pack += name

    return pack

# 로그인 리스트
def LogInList(list):
    pack = ''

    pack += Loginlist_ACK + '@'
    for name in list:
        pack += name + '#'

    return pack


# 채팅 ( 메시지 전송, 이름과 메시지 )
def ShortMessage(name, msg):
    pack = ''

    pack += Shortmessage + '@'
    pack += name + '#'
    pack += msg

    return pack


# 파일 전송 ( 파일 이름과 파일의 크기 )
def SendFile(filename, filedata):
    pack = ''

    decode_filedata = filedata.decode('utf-8', errors='ignore')
    pack += Sendfile + '@'
    pack += filename + '#'
    pack += decode_filedata

    return pack


# 화면 공유
def SendByte(bytes):
    # bytes -> 문자열로 바꿔서 보내야 할듯?
    pack = ''

    decoded_bytes = bytes.decode('utf-8', errors='ignore')
    pack += Sendbyte + '@'
    pack += decoded_bytes

    return pack


# 원격 제어 ( 입력된 키 인식을 byte배열로 전환해서 전송 )
def SendRomte(bytes):
    pack = ''

    pack += Sendremote + '@'
    pack += bytes

    return pack

# def Request_Screen():





###############################################################################################

# Server -> Client 전송 패킷 만드는 부분
def LogIn_ACK(list):
    pack = ''

    pack += Login_ACK + '@'
    # pack += name
    for name in list:
        pack += name + '$'

    return pack

def LogOut_ACK(list):
    pack = ''

    pack += Logout_ACK + '@'
    # pack += name
    for name in list:
        pack += name + '$'

    return pack


def LogInList_ACK(list):
    pack = ''

    pack += Loginlist_ACK + '@'
    for name in list:
        pack += name + '#'

# user1, user2, user3

    # Loginlist_ACK@user1#user2#user3#

    return pack



def ShortMessage_ACK(name, msg):
    pack = ''

    pack += Shortmessage_ACK + '@'
    pack += name + '#'
    pack += msg

    return pack


def SendFile_ACK(filename, filedata):
    pack = ''

    decode_filedata = filedata.decode('utf-8', errors='ignore')
    pack += Sendfile + '@'
    pack += filename + '#'
    pack += decode_filedata

    return pack

def SendByte_ACK(bytes):
    pack = ''

    pack += Sendbyte_ACK + '@'
    pack + bytes

    return pack


def SendRemote_ACK(bytes):
    pack = ''

    pack += Sendremote_ACK + '@'
    pack += bytes

    return pack