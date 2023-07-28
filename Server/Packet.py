# 패킷 

# Client -> Server 

Login = "LOGIN"
Loginlist = "LOGINLIST"
Logout = "LOGOUT"
Shortmessage = "SHORTMESSAGE"
Sendfile = "SENDFILE"
Sendbyte = "SENDBYTE"

# Server -> Client

Login_ACK = "LOGIN_ACK"
Loginlist_ACK = "LOGINLIST_ACK"
Logout_ACK = "LOGOUT_ACK"
Shortmessage_ACK = "SHORTMESSAGE_ACK"
Sendfile_ACK = "SENDFILE_ACK"
Sendbyte_ACK = "SENDBYTE_ACK"

def LogIn_ACK(name):
    pack = ''

    pack += Login_ACK + '@'
    pack += name

    return pack

def LogInList_ACK(user_list):
    pack = ''

    pack += Loginlist_ACK + '@'
    for user in user_list:
        pack += user + '#'

    return pack

def LogOut_ACK(name):
    pack = ''

    pack += Logout_ACK + '@'
    pack += name

    return pack

def ShortMessage_ACK(name, msg):
    pack = ''

    pack += Shortmessage_ACK + '@'
    pack += name + '#'
    pack += msg

    return pack

def FileSend_ACK(filename, size):
    pack = ''

    pack += Sendfile_ACK + '@'
    pack += filename + '#'
    pack += size

    return pack

def BytesSend_ACK(bytes):
    pack = ''

    decoded_bytes = bytes.decode('eur-kr')
    
    pack += Sendbyte_ACK + '@'
    pack += decoded_bytes

    return pack