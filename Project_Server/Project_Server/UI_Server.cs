using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Project_Server
{
    public partial class UI_Server : Form
    {
        Control con = Control.Instance;

        public UI_Server()
        {
            InitializeComponent();

            textbox_ip.Text = "";
            textbox_port.Text = "9000";

            con.thisForm(this);

            btn_close.Enabled = false;
        }
                                                
        #region 시작 & 종료 버튼 핸들러 
        // 서버 실행 (데이터, [네트워크], UI)
        private void btn_open_Click(object sender, EventArgs e)
        {
            con.ServerStart(int.Parse(textbox_port.Text));
            
            btn_open.Enabled = false; 
            btn_close.Enabled = true;
        }

        // 서버 종료
        private void btn_close_Click(object sender, EventArgs e)
        {
            con.ServerStop();

            btn_open.Enabled = true;
            btn_close.Enabled = false;
        }
        #endregion 

        #region 로그 & 메시지 출력
        public void LogPrint(string msg)
        {
            string temp = string.Format("{0} ({1})\r\n", msg, DateTime.Now.ToLongTimeString());
            textbox_logview.AppendText(temp);
        }

        public void MsgPrint(string nickname, string msg)
        {
            string temp = string.Format("{0} : {1} ({2})\r\n", nickname, msg, DateTime.Now.ToLongTimeString());

            list_conview.Items.Add(temp);   
        }
        #endregion




    }
}
