using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;

namespace HTTPClient
{
    class HTTPClient
    {
        static void Main(string[] args)
        {
            WebClient client;
            string data, request_type, uri;
            byte[] response;

            if (args.Length == 0 || 2 < args.Length)
            {
                Console.WriteLine("usage: {0} URI [GET|PUT|POST]",
                    System.AppDomain.CurrentDomain.FriendlyName);
                Environment.Exit(1);
            }

            data = "";

            uri = args[0];

            if (args.Length == 2)
            {
                request_type = args[1];
            }
            else
            {
                request_type = "GET";
            }

            if (request_type == "PUT")
            {
                for (string line = Console.ReadLine(); line != null; line = Console.ReadLine())
                {
                    data += line;
                }

                if (data == "")
                {
                    Environment.Exit(0);
                }
            }

            client = new WebClient();

            //client.Headers.Add("Content-Type", "application/json");

            try
            {
                if (request_type == "PUT")
                {
                    response = client.UploadData(uri, request_type,
                        Encoding.Default.GetBytes(data));
                }
                else
                {
                    response = client.DownloadData(uri);
                }

                Console.WriteLine("{0}",
                    System.Text.Encoding.Default.GetString(response));

            }
            catch (Exception e)
            {
                Console.WriteLine("Failed to {0} request\n{1}", request_type,
                    e.ToString());
                Environment.Exit(1);
            }

        }
    }
}
