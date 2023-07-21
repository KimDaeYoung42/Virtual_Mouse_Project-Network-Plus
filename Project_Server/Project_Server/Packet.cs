using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project_Server
{
    internal static class Packet
    {
        // Client -> Server
        public const string Shortmessage = "SHORTMESSAGE";

        // Server -> Client
        public const string Shortmessage_ACK = "SHORTMESSAGE_ACK";

        public static string ShortMessage_ACK(string nickname, string msg)
        {
            string packet = string.Empty;

            packet += Shortmessage_ACK + "@";

            packet += nickname + "#";
            packet += msg;

            return packet;
        }
    }
}
