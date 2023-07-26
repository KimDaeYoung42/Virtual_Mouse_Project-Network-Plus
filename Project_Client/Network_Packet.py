# 네트워크 패킷 관련

# 데이터 송/수신 할 때 패킷을 어떻게 주고받을 것인가?
# 필요한 패킷
# 1. 로그인 ( 클라이언트가 서버에 접속했을 때 접속자명을 통지 )
# 2. 채팅
# 3. 파일 공유 ( 보내기 )
# 4. 화면 공유

# Client -> Server
Login = "LOGIN"
Shortmessage = "SHORTMESSAGE"
Sendfile = "SENDFILE"
Sendbyte = "SENDBYTE"
Sendremote = "SENDREMOTE"

# Server - > Client
Login_ACK = "LOGIN_ACK"
Shortmessage_ACK = "SHORTMESSAGE_ACK"
Sendfile_ACK = "SENDFILE_ACK"
Sendbyte_ACK = "SENDBYTE_ACK"
Sendremote_ACK = "SENDREMOTE_ACK"

# Client -> Server 전송 패킷 만드는 부분

# 로그인 ( 서버에 접속시 접속자의 이름을 알림 )
def LogIn(self, name):
    self.pack = ''

    self.pack += Login + '@'
    self.pack += name

    return self.pack

# 채팅 ( 메시지 전송, 이름과 메시지 )
def ShortMessage(self, name, msg):
    self.pack = ''

    self.pack += ShortMessage + '@'
    self.pack += name + '#'
    self.pack += msg

    return self.pack

# 파일 전송 ( 파일 이름과 파일의 크기 )
def SendFile(self, filename, size):
    self.pack = ''

    self.pack += SendFile + '@'
    self.pack += filename + '#'
    self.pack += size

    return self.pack

# 화면 공유 ( 클라의 화면 BitMap을 byte배열로 전환해서 전송 )
def SendByte(self, bytes):
    self.pack = ''

    self.pack += Sendbyte + '@'
    self.pack += bytes

    return self.pack

# 원격 제어 ( 입력된 키 인식을 byte배열로 전환해서 전송 )
def SendRomte(self, bytes):
    self.pack = ''

    self.pack += Sendremote + '@'
    self.pack += bytes

    return self.pack
