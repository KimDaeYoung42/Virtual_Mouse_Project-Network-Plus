using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project_Client
{
    internal class Packet
    {
        public const string Pack_Shortmessage = "P_SHORTMESSAGE"; 

        public static string ShortMessage(string name, string msg)
        {
            string pack = string.Empty;

            pack += Pack_Shortmessage + "@";
            pack += name + "#";
            pack += msg;

            return pack;

        }
    }   
}
