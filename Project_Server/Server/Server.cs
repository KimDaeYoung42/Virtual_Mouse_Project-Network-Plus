using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Server
{
    // Del 정의
    internal delegate void Recv_Del(Socket sock, string msg);
    class Server
    {
        // 대기 소켓
        private Socket server;

        private Recv_Del recv_del = null;

        public int Server_Port { get; private set; }

        // 통신 소켓
        private List<Socket> sockets = new List<Socket>();

        #region 생성자 및 초기화 함수

        public Server(int port)
        {
            Server_Port = port;
            Init();
        }

        private void Init()
        {
            try
            {
                server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

                IPEndPoint ipep = new IPEndPoint(IPAddress.Any, Server_Port);
                server.Bind(ipep);
                server.Listen(20);

                Console.WriteLine("서버 시작.... 클라이언트 접속 대기중");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Environment.Exit(0);
            }
        }

        #endregion

        #region 엔진부(반복 실행)
        public void Run(Recv_Del fun)
        {
            recv_del = fun;
            while (true)
            {
                try
                {
                    Socket client = server.Accept();
                    sockets.Add(client);

                    IPEndPoint ip = (IPEndPoint)client.RemoteEndPoint;
                    Console.WriteLine("{0}, {1} 접속", ip.Address, ip.Port);

                    Thread thread = new Thread(WorkThread);
                    thread.IsBackground = true;
                    thread.Start(client);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
        }

        public void WorkThread(object value)
        {
            Socket client = (Socket)value;

            try
            {
                byte[] data = null;
                while (true)
                {
                    string msg = string.Empty;
                    //문자열 수신
                    if (ReceiveData(client, ref data) == true)
                    {
                        msg = Encoding.Default.GetString(data).Trim('\0');
                        recv_del(client, msg);
                    }
                    else
                    {
                        Console.WriteLine("수신 데이터 없음");
                        throw new Exception("수신 오류");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                sockets.Remove(client);
                client.Close();
            }
        }
        #endregion

        #region 데이터 송/수 신부

        // 한개의 클라에만 송신
        public void SendData(Socket sock, string msg, int size)
        {
            // 문자열 전송
            byte[] bmsg = Encoding.Default.GetBytes(msg);
            SendData(sock, bmsg, size);
            int ret = sock.Send(bmsg, bmsg.Length, SocketFlags.None);
            Console.WriteLine("데이터 전송 : {0}byte\n", ret);
        }

        // 연결된 모든 클라에 송신
        public void SendAllData(Socket sock, string msg, int size)
        {
            foreach (Socket s in sockets)
            {
                SendData(s, msg, size);
            }
        }

        public void SendData(Socket sock, byte[] data, int _size)
        {
            try
            {
                int total = 0;          //보낸크기
                int size = _size;       //보낼크기
                int left_data = size;   //남은크기

                //전송할 데이터 크기 전달
                byte[] data_size = new byte[4];
                data_size = BitConverter.GetBytes(size);
                int ret = sock.Send(data_size);

                //실제 데이터 전송
                while (total < size)
                {
                    ret = sock.Send(data, total, left_data, SocketFlags.None);
                    total += ret;
                    left_data -= ret;
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        public bool ReceiveData(Socket sock, ref byte[] data)
        {
            try
            {
                int total = 0;
                int size = 0;
                int left_data = 0;

                //수신할 데이터 크기
                byte[] data_size = new byte[4];
                int ret = sock.Receive(data_size, 0, 4, SocketFlags.None);
                size = BitConverter.ToInt32(data_size, 0);
                left_data = size;

                data = new byte[size];

                // 실제 데이터 수신
                while (total < size)
                {
                    ret = sock.Receive(data, total, left_data, 0);
                    if (ret == 0)
                        break;
                    total += ret;
                    left_data -= ret;
                }
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                return false;
            }
        }
        #endregion
    }
}
