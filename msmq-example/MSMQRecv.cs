using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Messaging;
using Messaging = System.Messaging;

namespace MSMQRecv
{
    class MSMQRecv
    {
        static void Main(string[] args)
        {
            foreach (string arg in args) {
                MessageQueue queue = new MessageQueue(arg);
                try
                {
                    foreach (Message msg in queue.GetAllMessages())
                    {
                        msg.Formatter = new XmlMessageFormatter(new Type[1] { typeof(string) });
                        Console.Write("Received message (" + msg.Label + ") with payload: `" + msg.Body + "` from queue " + arg + "\n");
                    }
                } finally {
                    queue.Close();
                }
            }
            Console.Write("Press enter to continue..");
            Console.Read();
        }
    }
}
