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
            foreach (string arg in args)
            {
                MessageQueue queue = new MessageQueue(arg);
                try
                {
                    Message msg = new Message();
                    msg.Body = "Hello, the time is: " + System.DateTime.Now;
                    msg.Label = "Test Message " + msg.Body.GetHashCode();
                    Console.Write("Will send message " + msg.Label + "  `" + msg.Body + "` to queue: " + arg + "\n");
                    if (queue.Transactional)
                        queue.Send(msg, MessageQueueTransactionType.Single);
                    else
                        queue.Send(msg);
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
