using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;

namespace JSonToXml
{
    class Program
    {
        static void Main(string[] args)
        {
            string jsonDoc = "";
            for (string line = Console.ReadLine(); line != null; line = Console.ReadLine())
            {
                jsonDoc += line;
            }
            if (jsonDoc != "")
            {
                Console.WriteLine(JsonConvert.DeserializeXmlNode(jsonDoc).OuterXml);
            }
        }
    }
}
