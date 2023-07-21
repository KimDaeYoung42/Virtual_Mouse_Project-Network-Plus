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
        //private Control con = Control.Instance;
        Client client = new Client("127.0.0.1", 9000);

        public UI_Login()
        {
            InitializeComponent();
        }

        #region 버튼 핸들러 
        
        // 서버 연결 버튼
        private void btn_open_Click(object sender, EventArgs e)
        {
            
        }

        private void btn_close_Click(object sender, EventArgs e)
        {
            //con.Close();

            //btn_close.Enabled = false;
            //btn_open.Enabled = true;
        }

        #endregion
    }
}
