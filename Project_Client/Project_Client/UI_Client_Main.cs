using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Project_Client
{
    public partial class UI_Client_Main : Form
    {
        
        public string Ip { get; private set; }
        public int Port { get; private set; }

        Client client;
        public UI_Client_Main()
        {
            InitializeComponent();
        }

        #region 버튼 핸들러
        // 메시지 전송 버튼 클릭
        private void btn_send_Click(object sender, EventArgs e)
        {
            // 메시지 전송 패킷을 서버에 보낸다.
            string name = textBox4.Text;
            string msg = txt_msgsend.Text;

            // 패킷 구성
            string packet = Packet.ShortMessage(name, msg);

            // 전송
            client.SendData(packet, packet.Length);

        }
        #endregion

        #region 네트워크
        public void Client_RecvData(string msg)
        {
            //이벤트 로그뷰에 수신 메시지 입력
            string recv_msg = string.Format("수신 메시지 : {0}", msg);
            textBox1.AppendText(recv_msg);

            string[] sp1 = msg.Split('@');

            //메시지 파싱
            if (sp1[0].Equals(Packet.Shortmessage_ACK))
            {
                string[] sp2 = sp1[1].Split('#');
                PrintMessage(sp2[0], sp2[1]);
            }
        }

        #endregion

        #region 패킷 파싱후 응답(메서드)

        // 메시지 수신
        private void PrintMessage(string nickname, string msg)
        {
            string temp = string.Format("{0} : {1}({2})\r\n", nickname, msg, DateTime.Now.ToLongTimeString());

            txt_msgview.AppendText(temp);
        }

        #endregion

        #region 서버 연결 / 해제
        // 서버 연결
        private void button1_Click(object sender, EventArgs e)
        {
            Ip = textBox2.Text;
            Port = int.Parse(textBox3.Text);
            string name = textBox4.Text;

            client = new Client(Ip, Port);

            // 서버 연결
            if (client.Open(Client_RecvData) == false)
            {
                Environment.Exit(0);
                return;
            }

            // 누가 접속했는지 확인 필요
        }
        #endregion

        // 연결 해제
        private void button5_Click(object sender, EventArgs e)
        {
            // 누가 접속을 해제했는지 확인 필요

            client.Close();
        }
    }
}
