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
            string[] sp1 = msg.Split('@');

            if (sp1[0].Equals(Packet.Shortmessage))
            {
                string[] sp2 = sp1[1].Split('#');
                Control.Instance.ShortMessage(sock, sp2[0], sp2[1]);
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
