using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project_Client
{
    internal class Control
    {   
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

        private TCP_Client client = null;
        private UI_Client_Main ui_client_main = null;

        public void ThisForm(UI_Client_Main ui_client_main1)
        {
            ui_client_main = ui_client_main1; 
        }

        #region Form1에서 호출하는 메서드
        public void Open(string ip, int port)
        {

            client = new TCP_Client("127.0.0.1", 9000);
            // client = new TCP_Client(ip, port);
            client.RecvFunc = RecvMessage;
        }

        public void Close()
        {
            client.Close();
        }

        public void SendData(string nickname, string msg)
        {
            string packet = Packet.ShortMessage(nickname, msg);

            client.Send(packet);
        }
        #endregion

        #region Network에서 호출하는 메서드
        public void RecvMessage(string packet)
        {
            string[] sp1 = packet.Split('@');
            if (sp1[0] == Packet.Pack_Shortmessage)
            {
                string[] sp2 = sp1[1].Split('#');

                // form에 출력
                ui_client_main.MsgPrint(sp2[0], sp2[1]);
            }
        }
        #endregion

    }
}
