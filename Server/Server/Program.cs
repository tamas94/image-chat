using System;
using System.Text;

namespace Server
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Port: ");
            string input = Console.ReadLine();
            int port = int.Parse(input);


            try
            {
                Server server = new Server("192.168.43.205", port);
                server.Start();

                while (true)
                {
                    server.Connect();
                    string id = server.Receive();
                    Console.WriteLine(id + " connected.");
                    server.NewClient(id);
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("Exception: {0}", e);
            }


            Console.WriteLine("\nHit enter to exit...");
            Console.Read();
        }
    }
}
