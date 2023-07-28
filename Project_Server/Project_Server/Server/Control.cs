using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace Server
{
    internal class Control
    {
        #region 싱글톤

        private Control()
        {

        }

        public static Control Instance { get; private set; }

        static Control()
        {
            Instance = new Control();
        }

        #endregion

        private Server server;

        public void SendServer(Server socket)
        {
            server = socket;
        }

        #region 수신 데이터 처리 및 응답 (메서드)
        public void Login(Socket sock, string name)
        {
            //1. 수신 데이터 처리
            Console.WriteLine("로그인 정보, {0}", name);

            //2. 응답패킷 생성 및 전송
            string pack = Packet.LogIn_ACK(name);
            server.SendAllData(sock, pack, pack.Length);
        }

        public void Logout(Socket sock, string name)
        {
            //1. 수신 데이터 처리
            Console.WriteLine("로그아웃 정보, {0}", name);

            //2. 응답패킷 생성 및 전송
            string pack = Packet.LogOut_ACK(name); 
            server.SendAllData(sock, pack, pack.Length);
        }

        public void ShortMessage(Socket sock, string name, string msg)
        {
            //1. 수신 데이터 처리
            Console.WriteLine("메시지 전송, {0} : {1}", name, msg);

            //2. 응답패킷 생성 및 전송
            string pack = Packet.ShortMessage_ACK(name, msg);
            server.SendAllData(sock, pack, pack.Length);
        }

        public void SendFile(Socket sock, string filename, int size)
        {
            //1. 수신 데이터 처리
            Console.WriteLine("파일 전송, {0} : {1}", filename, size);

            //2. 응답패킷 생성 및 전송
            string pack = Packet.SendFile_ACK(filename, size);
            server.SendAllData(sock, pack, pack.Length);
        }

        public void ScreenShare(Socket sock, byte[] bytes)
        {
            //1. 수신 데이터 처리
            Console.WriteLine("화면 공유, {0}", bytes);

            //2. 응답패킷 생성 및 전송
            string pack = Packet.SendByte_ACK(bytes);
            server.SendAllData(sock, pack, pack.Length);
        }

        public void RemoteControl(Socket sock, byte[] bytes)
        {
            //1. 수신 데이터 처리
            Console.WriteLine("원격 제어, {0}", bytes);

            //2. 응답패킷 생성 및 전송
            string pack = Packet.SendRemote_ACK(bytes);
            server.SendAllData(sock, pack, pack.Length);
        }

        #endregion

    }
}
