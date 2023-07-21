using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project_Server
{
    internal class Control
    {
        private TCP_Listener server = null;
        private UI_Server ui_server = null;

        #region 싱글톤
        public static Control Instance { get; set; }

        static Control()
        {
            Instance = new Control();
        }

        private Control()
        {

        }
        #endregion

        public void thisForm(UI_Server ui_server1)
        {   
            ui_server = ui_server1; 
        }

        #region 네트워크

        // 메시지 수신부
        public string RecvMessage(string packet)
        {
            string[] sp1 = packet.Split('@');
            if (sp1[0] == Packet.Pack_Shortmessage)
            {
                // 수신 처리
                string[] sp2 = sp1[1].Split('#');

                ui_server.MsgPrint(sp2[0], sp2[1]);

                // 송신 생성
                string pack = Packet.ShortMessage(sp2[0], sp2[1]);
                return pack;
            }
            return string.Empty;
        }

        // 로그메시지 수신부(서버 시작/종료, 클라이언트 연결/해제)
        public void LogMessage(string msg)
        {
            ui_server.LogPrint(msg);
        }

        public void ServerStart(int port)
        {   
            server = new TCP_Listener(port);  // TCP 9000번 포트 열기
            server.Recvfunc = RecvMessage;
            server.Logfunc = LogMessage;
            server.Start();
            server.Run();
        }

        public void ServerStop()
        {
            server.Close();
        }
        #endregion
    }
}
