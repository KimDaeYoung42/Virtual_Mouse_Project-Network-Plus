using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Server
{
    internal static class Packet
    {
        // Client -> Server
        public const string Login = "LOGIN";
        public const string Logout = "LOGOUT";
        public const string Shortmessage = "SHORTMESSAGE";
        public const string Sendfile = "SENDFILE";
        public const string Sendbyte = "SENDBYTE";
        public const string Sendremote = "SENDREMOTE";

        // Server -> Client
        public const string Login_ACK = "LOGIN_ACK";
        public const string Logout_ACK = "LOGOUT_ACK"; 
        public const string Shortmessage_ACK = "SHORTMESSAGE_ACK";
        public const string Sendfile_ACK = "SENDFILE_ACK";
        public const string Sendbyte_ACK = "SENDBYTE_ACK";
        public const string Sendremote_ACK = "SENDREMOTE_ACK";

        //메시지(채팅)
        public static string LogIn_ACK(string name)
        {
            string packet = string.Empty;

            packet += Login_ACK + '@';

            packet += name;

            return packet;
        }

        public static string LogOut_ACK(string name)
        {
            string packet = string.Empty;

            packet += Logout_ACK + '@';

            packet += name;

            return packet;
        }


        public static string ShortMessage_ACK(string nickname, string msg)
        {
            string packet = string.Empty;

            packet += Shortmessage_ACK + '@';

            packet += nickname + '#';
            packet += msg;

            return packet;
        }

        //파일 보내기
        public static string SendFile_ACK(string filename, int size)
        {
            string packet = string.Empty;

            packet += Sendfile_ACK + '@';

            packet += filename + '#';
            packet += size;

            return packet;
        }

        //바이트 배열 보내기( 화면공유 )
        public static string SendByte_ACK(byte[] bytes)
        {
            string packet = string.Empty;

            packet += Sendbyte_ACK + '@';

            packet += bytes;

            return packet;
        }

        //원격 제어
        public static string SendRemote_ACK(byte[] bytes)
        {
            string packet = string.Empty;

            packet += Sendremote_ACK + '@';

            packet += bytes;

            return packet;
        }
    }
}