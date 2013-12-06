using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Messaging;
using Messaging = System.Messaging;

namespace MSMQSend
{
    class MSMQSend
    {
        static void Main(string[] args)
        {
            // XXX: add a usage message.
            // `.\private$\test`,
            // `FormatName:DIRECT=HTTP://localhost/msmq/private$/test`,
            // etc
            foreach (string arg in args)
            {
                Boolean isHTTP = false;

                // http://stackoverflow.com/questions/5559123/programmatically-add-private-queues-in-msmq
                if (arg.ToLower().IndexOf("FormatName:DIRECT=HTTP://") != -1)
                {
                    isHTTP = true;
                }

                if (!isHTTP && !MessageQueue.Exists(arg)) {
                    MessageQueue.Create(arg, true);
                }
                MessageQueue queue = new MessageQueue(arg);
                try
                {
                    Message msg = new Message();
                    msg.Body = "Hello, the time is: " + System.DateTime.Now;
                    msg.Label = "Test Message " + msg.Body.GetHashCode();
                    Console.Write("Will send message " + msg.Label + "  `" + msg.Body + "` to queue: " + arg + "\n");

                    if (!isHTTP && queue.Transactional)
                    {
                        // Send a single, transactional, internal message. See also:
                        // http://msdn.microsoft.com/en-us/library/3hyd9xby%28v=vs.110%29.aspx
                        queue.Send(msg, MessageQueueTransactionType.Single);
                    }
                    else
                    {
                        // Send to a non-transactional queue
                        queue.Send(msg);
                    }
                }
                finally
                {
                    queue.Close();
                }
            }
            Console.Write("Press enter to continue..");
            Console.Read();
        }
    }
}
