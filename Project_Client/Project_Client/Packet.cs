using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project_Client
{
    internal class Packet
    {
        // Client -> Server 
        public const string Shortmessage = "SHORTMESSAGE";

        // Server -> Client
        public const string Shortmessage_ACK = "SHORTMESSAGE_ACK";

        public static string ShortMessage(string name, string msg)
        {
            string pack = string.Empty;

            pack += Shortmessage + "@";
            pack += name + "#";
            pack += msg;

            return pack;

        }
    }   
}
