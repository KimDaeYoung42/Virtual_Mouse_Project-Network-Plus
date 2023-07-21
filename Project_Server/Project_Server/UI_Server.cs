using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Project_Server
{
    public partial class UI_Server : Form
    {
        private const int port = 9000;

        private Server server;
        public UI_Server()
        {
            InitializeComponent();

            server = new Server(port);
        }


        #region 패킷 파싱

        public void Server_RecvData(Socket sock, string msg)
        {

            //메시지 파싱
            string[] sp1 = msg.Split('@');

            if (sp1[0].Equals(Packet.Shortmessage))
            {
                string[] sp2 = sp1[1].Split('#');
                Msg_Send(sock, sp2[0], sp2[1]);
                Msg_Log(sp2[0], sp2[1]);
            }
        }


        #endregion

        #region 패킷 응답 메서드 (로그출력 및 패킷 전송)

        public void Msg_Log(string name, string msg)
        {
            string temp = string.Format("{0} : {1} ({2})\r\n", name, msg, DateTime.Now.ToLongTimeString());
            textbox_logview.AppendText(temp);
        }

        public void Msg_Send(Socket sock, string nickname, string msg)
        {
            //1. 수신 데이터처리
            string pack = Packet.ShortMessage_ACK(nickname, msg);

            //2. 패킷 전송
            server.SendAllData(sock, pack, pack.Length);

        }
        #endregion

    }
}
