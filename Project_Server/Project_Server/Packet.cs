using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project_Server
{
    internal static class Packet
    {
        public const string Pack_Shortmessage = "P_SHORTMESSAGE";

        public static string ShortMessage(string nickname, string msg)
        {
            string packet = string.Empty;

            packet += Pack_Shortmessage + "@";

            packet += nickname + "#";
            packet += msg;

            return packet;
        }
    }
}
