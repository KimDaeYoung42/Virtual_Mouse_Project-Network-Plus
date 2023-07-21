using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Project_Client
{
    public partial class UI_Client_Main : Form
    {
        private Control con = Control.Instance;

        public UI_Client_Main()
        {
            InitializeComponent();
        }

        #region 버튼 핸들러
        private void btn_send_Click(object sender, EventArgs e)
        {
            con.SendData(txt_nickname.Text, txt_msgsend.Text);
        }
        #endregion 

        #region 컨트롤에서 전달되는 메시지 수신
        public void MsgPrint(string nickname, string msg)
        {
            string temp = string.Format("{0} : {1}({2})\r\n", nickname, msg, DateTime.Now.ToLongTimeString());

            txt_msgview.AppendText(temp);
        }

        #endregion
    }
}
