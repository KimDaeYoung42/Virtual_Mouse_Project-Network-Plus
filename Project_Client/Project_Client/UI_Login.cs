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
    public partial class UI_Login : Form
    {
        private Control con = Control.Instance;

        public UI_Login()
        {
            InitializeComponent();

            txt_ip.Text = "127.0.0.1";
            txt_port.Text = 9000.ToString();
        }

        #region 버튼 핸들러 
        private void btn_open_Click(object sender, EventArgs e)
        {
            con.Open(txt_ip.Text, int.Parse(txt_port.Text));

            btn_open.Enabled = false;
            btn_close.Enabled = true;
        }

        private void btn_close_Click(object sender, EventArgs e)
        {
            con.Close();

            btn_close.Enabled = false;
            btn_open.Enabled = true;
        }

        #endregion
    }
}
