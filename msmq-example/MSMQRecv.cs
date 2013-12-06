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
            // XXX: add a usage message.
            // `.\private$\test`,
            // `FormatName=DIRECT=HTTP://localhost/msmq/private$/test`,
            // etc
            foreach (string arg in args) {
                MessageQueue queue = new MessageQueue(arg);
                try
                {
                    // This just peeks at the messages; see
                    // http://stackoverflow.com/questions/1228684/how-can-i-get-all-the-available-messages-on-a-msmq-queue
                    // for an alternative method that receives the message
                    // and plucks it off the queue.
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
