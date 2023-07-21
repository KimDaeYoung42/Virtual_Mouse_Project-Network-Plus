using System;
using System.Windows.Forms;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Net;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Project_Server
{
    public delegate string RecvFunc(string packet);
    public delegate void LogFunc(string msg);  
    /// <summary>
    /// 대기 소켓을 관리하는 클래스
    /// </summary>

    internal class TCP_Listener
    {   
        #region 델리게이트 레퍼런스 필드
        public RecvFunc Recvfunc { get; set; }
        public LogFunc Logfunc { get; set; }
        #endregion

        public int Port { get; private set; }
        public Socket Server { get; private set; }
        public Thread thread { get; private set; }

        private LinkedList<TCP_Client> tcpclients = new LinkedList<TCP_Client>();

        public TCP_Listener(int port)
        {
            Port = port;
        }

        public void Start()
        {
            Server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            IPEndPoint ipep = new IPEndPoint(IPAddress.Any, Port);
            Server.Bind(ipep);
            Server.Listen(20);
        }

        #region 서버 동작(Run -> WorkThread[AcceptTcpClient] -> 반복적인 RecvThread 생성)
        public void Run()
        {
            thread = new Thread(WorkThread);
            thread.IsBackground = true;
            thread.Start();
            Logfunc("서버 시작. . .");
        }

        // Thread함수 <- 여기서 접속하였는지 문제가 발생하는 중  
        private void WorkThread()
        {
            try
            {
                while (true)
                {
                    // 1.접속
                    TCP_Client client = AcceptTcpClient();
                    string temp = string.Format("[접속 ({0} : {1})]", client.RemoteIP, client.RemotePort);
                    MessageBox.Show(temp); // 테스트용 
                    Logfunc(temp);

                    // 2.저장
                    tcpclients.AddLast(client);

                    // 3.통신 스레드 생성
                    Thread th = new Thread(RecvThread);
                    th.IsBackground = true;
                    th.Start(client);
                }
            }
            catch (Exception)
            {

            }
        }

        private void RecvThread(object value)
        {
            TCP_Client sock = (TCP_Client)value;

            try
            {
                while (true)
                {
                    string msg = String.Empty;
                    int ret = sock.Recv(out msg);   // 수신한 문자열이 있으면 화면에 출력
                    if (ret == -1)
                        throw new Exception("클라이언트 종료");

                    string packet = Recvfunc(msg);

                    SendAll(packet);
                    //sock.Send(packet);
                }
            }
            catch (Exception ex)
            {
                //Console.WriteLine("수신 에러 : {0}", ex.Message);

                string temp = string.Format("[접속 종료 ({0}:{1})]", sock.RemoteIP, sock.RemotePort);
                MessageBox.Show(temp);  // 테스트용 
                Logfunc(temp);

                tcpclients.Remove(sock);
                sock.Close();
            }
        }

        private TCP_Client AcceptTcpClient()
        {
            Socket client = Server.Accept();  // 클라이언트 접속 대기

            TCP_Client tcpclient = new TCP_Client(client);

            return tcpclient;
        }
        #endregion

        #region 전체 전송   
        public void SendAll(string msg)
        {
            foreach (TCP_Client client in tcpclients)
            {
                client.Send(msg);
            }
        }
        #endregion 

        public void Close()
        {
            Server.Close();
            Logfunc("서버 종료. . .");
        }

    }
}
