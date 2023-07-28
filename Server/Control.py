from Server import Server

class Control:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Control, cls).__new__(cls)
            cls._instance.Init()
        return cls._instance
    
    def Init(self):
        self.users = []
        self.server = Server()
    

    
    def SendServer(self, port):
        self.server = Server(port)

    # 수신 데이터 처리 및 응답 메서드