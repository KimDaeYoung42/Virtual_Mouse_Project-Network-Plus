using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace Server
{
    internal class Program
    {
        private Server server = new Server(9000);

        public Program()
        {
            Control.Instance.SendServer(server);
        }

        // 수신 메시지 파싱 ( 서버 )
        public void Server_RecvData(Socket sock, string msg)
        {
            Console.WriteLine("수신 메시지 : " + msg);
            // msg == "LOGIN@woohyun"
            
            string[] sp1 = msg.Split('@');
            // sp1[0] = "LOGIN", sp1[1] = "woohyun"
            if (sp1[0].Equals(Packet.Login))
            {
                string name = sp1[1];
                Control.Instance.Login(sock, name);
            }
            else if (sp1[0].Equals(Packet.Shortmessage))
            {
                string[] sp2 = sp1[1].Split('#');
                Control.Instance.ShortMessage(sock, sp2[0], sp2[1]);
            }
            else if (sp1[0].Equals(Packet.Sendfile))
            {
                string[] sp2 = sp1[1].Split('#');
                Control.Instance.SendFile(sock, sp2[0], int.Parse(sp2[1]));
            }
            else if (sp1[0].Equals(Packet.Sendbyte))
            {
                // sp1[1] 의 바이트 배열을 보낸다.
                byte[] bytes = Encoding.UTF8.GetBytes(sp1[1]);
                Control.Instance.ScreenShare(sock, bytes);
            }
            else if (sp1[0].Equals(Packet.Sendremote))
            {
                byte[] bytes = Encoding.UTF8.GetBytes(sp1[1]);
                Control.Instance.RemoteControl(sock, bytes);
            }
        }

        public void Run()
        {
            server.Run(Server_RecvData);
        }
        static void Main(string[] args)
        {
            new Program().Run();
        }
    }
}
