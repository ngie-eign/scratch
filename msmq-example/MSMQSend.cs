using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
//using System.Text.RegularExpressions;
using System.Messaging;
using Messaging = System.Messaging;

namespace MSMQSend
{
    class MSMQSend
    {
        static void Main(string[] args)
        {
            MessageQueueTransaction transaction;
            const string direct_format = "formatname:direct";

            // XXX: add a usage message.
            // `.\private$\test`,
            // `FormatName:DIRECT=HTTP://localhost/msmq/private$/test`,
            // etc
            foreach (string arg in args)
            {
                // Best guesses for the magic tables in the MSDN docs for
                // Local, Remote, etc.
                //Boolean isDirect = Regex.IsMatch(arg, "^" + Regex.Escape(direct_format) + "=");
                Boolean isLocalNoDirectFormat =
                    arg.ToLower().IndexOf(".\\") == 0;
                Boolean isLocal = isLocalNoDirectFormat ||
                    arg.ToLower().IndexOf(direct_format + "=os:.\\") == 0;

                // Create a private queue if it's being created on the local
                // machine.
                // http://stackoverflow.com/questions/5559123/programmatically-add-private-queues-in-msmq
                if (isLocalNoDirectFormat && !MessageQueue.Exists(arg))
                {
                    MessageQueue.Create(arg, true);
                }

                MessageQueue queue = new MessageQueue(arg);
                // Only local queues can be Transactional.
                // http://msdn.microsoft.com/en-us/library/system.messaging.messagequeue.transactional%28v=vs.110%29.aspx
                Boolean isTransactional = isLocal && queue.Transactional;

                if (isTransactional)
                {
                    transaction = new MessageQueueTransaction();
                }
                else
                {
                    transaction = null;
                }

                // Use reliable messaging (i.e. store message on disk).
                queue.DefaultPropertiesToSend.Recoverable = true;

                try
                {
                    Message msg = new Message();

                    msg.Body = "Hello, the time is: " + System.DateTime.Now;
                    msg.Label = "Test Message " + msg.Body.GetHashCode();

                    Console.WriteLine("Will send {0}transactional message " +
                                      "({1}) with payload ({2}) to queue {3}",
                                      (isTransactional ? "" : "non-"),
                                      msg.Label, msg.Body, arg);

                    // Send a transactional message. See also:
                    // http://msdn.microsoft.com/en-us/library/3hyd9xby%28v=vs.110%29.aspx
                    // http://msdn.microsoft.com/en-us/library/ms978430.aspx
                    if (isTransactional)
                    {
                        transaction.Begin();
                        try
                        {
                            queue.Send(msg, transaction);
                            transaction.Commit();
                        }
                        catch
                        {
                            transaction.Abort();
                            throw;
                        }
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
