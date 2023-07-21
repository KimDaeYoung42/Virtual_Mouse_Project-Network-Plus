using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Threading;
using System.Net;

namespace Project_Client
{
    // Delegate 대리자
    internal delegate void Recv_Dell(string msg);

    class Client
    {
        private Socket sock;
        private Recv_Dell recv_del = null;
        public Thread Recv_Thread { get; private set; }

        public string Ip { get; private set; }
        public int Port { get; private set; }

        public Client(string ip, int port)
        {
            Ip = ip;
            Port = port;
        }


        #region 외부 접근 허용 메서드

        public bool Open(Recv_Dell fun)
        {
            recv_del = fun;
            try
            {
                //1. 소켓 생성
                sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

                //2. 연결
                IPEndPoint ipep = new IPEndPoint(IPAddress.Parse(Ip), Port);
                sock.Connect(ipep);

                //3. 수신 스레드 생성
                Recv_Thread = new Thread(RecvThread);
                Recv_Thread.IsBackground = true;
                Recv_Thread.Start();

                return true;
            }
            catch(Exception ex)
            {
                Console.WriteLine(ex.Message);
                return false;
            }
        }

        public void Close()
        {
            sock.Close();
            //스레드 강제종료
            Recv_Thread.Abort();
        }

        public void SendData(string msg, int size)
        {
            byte[] buffer = Encoding.Default.GetBytes(msg);
            SendData(sock, buffer, size);
        }
        #endregion

        #region 내부 메서드

        public void RecvThread()
        {
            byte[] data = null;
            while (true)
            {
                ReceiveData(sock, ref data);

                string msg = Encoding.Default.GetString(data).Trim('\0');

                recv_del(msg);
            }
        }

        #endregion

        #region 데이터 송수신

        private void SendData(Socket sock, byte[] data, int _size)
        {
            try
            {
                int total = 0;          //보낸크기
                int size = _size;       //보낼크기
                int left_data = size;   //남은크기

                //1. 전송할 데이터의 크기 전달
                byte[] data_size = new byte[4];
                data_size = BitConverter.GetBytes(size);
                int ret = sock.Send(data_size);

                //2. 실제 데이터 전송
                while(total < size)
                {
                    ret = sock.Send(data, total, left_data, SocketFlags.None);
                    total += ret;
                    left_data -= ret;
                }
            }
            catch(Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private bool ReceiveData(Socket sock, ref byte[] data)
        {
            try
            {
                int total = 0;          //받은 크기
                int size = 0;           //받을 크기
                int left_data = 0;      //남은 크기

                //수신할 데이터 크기
                byte[] data_size = new byte[4];
                int ret = sock.Receive(data_size, 0, 4, SocketFlags.None);
                size = BitConverter.ToInt32(data_size, 0);
                left_data = size;

                data = new byte[size];

                //실제 데이터 수신
                while(total < size)
                {
                    ret = sock.Receive(data, total, left_data, 0);
                    if (ret == 0)
                        break;
                    total += ret;
                    left_data -= ret;
                }
                return true;
            }
            catch(Exception ex)
            {
                Console.WriteLine(ex.Message);
                return false;
            }
        }

        #endregion
    }
}
