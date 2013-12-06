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
            const string direct_format = "formatname:direct";

            // XXX: add a usage message.
            // `.\private$\test`,
            // `FormatName=DIRECT=OS:localhost/private$/test`,
            // etc
            foreach (string arg in args) {
                // HTTP* can't pull; it can only push :/...
                Boolean isLocal =
                    arg.ToLower().IndexOf(".\\") == 0 ||
                    arg.ToLower().IndexOf(direct_format + "=os:.\\") == 0;
                Boolean isHTTP = !isLocal &&
                    arg.ToLower().IndexOf(direct_format + "=http") == 0;

                // :(..
                // http://blogs.msdn.com/b/johnbreakwell/archive/2008/06/09/msmq-over-http-is-a-push-only-technology.aspx
                if (isHTTP)
                {
                    Console.WriteLine("Can't read from HTTP queue :(..");
                    continue;
                }

                MessageQueue queue = new MessageQueue(arg);

                try
                {
                    if (isLocal) {
                        // This just peeks at the messages; see
                        // http://stackoverflow.com/questions/1228684/how-can-i-get-all-the-available-messages-on-a-msmq-queue
                        // for an alternative method that receives the message
                        // and plucks it off the queue.
                        foreach (Message msg in queue.GetAllMessages())
                        {
                            msg.Formatter =
                                new XmlMessageFormatter(new Type[1] { typeof(string) });

                            Console.WriteLine("Received message ({0}) with " +
                                              "payload: ({1}) from queue {2}",
                                              msg.Label, msg.Body, arg);
                        }
                    } else {
                        Console.WriteLine("XXX: implement non-GetAllMessages " +
                                          "method for peeking at queue");
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
