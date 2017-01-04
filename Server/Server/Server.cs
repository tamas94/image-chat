using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;

namespace Server
{
    class Server
    {
        private TcpListener server;
        private TcpClient client;
        private NetworkStream stream;

        private Dictionary<string, Client> users;
        private static Mutex mutex;

        private string ip;
        private int port;

        public Server(string ip, int port)
        {
            this.server = null;
            this.ip = ip;
            this.port = port;
            users = new Dictionary<string, Client>();
            mutex = new Mutex();
        }

        public void Start()
        {
            try
            {
                server = new TcpListener(IPAddress.Parse(ip), port);
                server.Start();
                Console.WriteLine("Server started.");
                return;
            }
            catch (Exception e)
            {
                Console.WriteLine("Exception: {0}", e);
            }
            server.Stop();
            throw new Exception("error");
        }

        public void Connect()
        {
            client = server.AcceptTcpClient();
            stream = client.GetStream();

            while (!stream.DataAvailable) ;

            byte[] bytes = new byte[client.Available];
            stream.Read(bytes, 0, bytes.Length);
            string data = Encoding.UTF8.GetString(bytes);
            Console.WriteLine(data);

            if (new Regex("^GET").IsMatch(data))
            {
                byte[] response = Encoding.UTF8.GetBytes("HTTP/1.1 101 Switching Protocols" + Environment.NewLine
                    + "Connection: Upgrade" + Environment.NewLine
                    + "Upgrade: websocket" + Environment.NewLine
                    + "Sec-WebSocket-Accept: " + Convert.ToBase64String(
                        SHA1.Create().ComputeHash(
                            Encoding.UTF8.GetBytes(
                                new Regex("Sec-WebSocket-Key: (.*)").Match(data).Groups[1].Value.Trim() + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
                            )
                        )
                    ) + Environment.NewLine
                    + Environment.NewLine);
                stream.Write(response, 0, response.Length);
                Console.WriteLine(Encoding.UTF8.GetString(response));
            }
        }

        public void NewClient(string id)
        {
            Client newclient = new Client(client, id, ref users, ref mutex, port);
        }

        public string Receive()
        {
            while (!stream.DataAvailable) ;

            byte[] bytes = new byte[client.Available];
            stream.Read(bytes, 0, bytes.Length);

            byte[] msg = new byte[bytes[1] - 128];
            byte[] key = new byte[4] { bytes[2], bytes[3], bytes[4], bytes[5] };
            for (int i = 0; i < bytes.Length - 6; i++)
            {
                msg[i] = (byte)(bytes[i + 6] ^ key[i % 4]);
            }
            string message = Encoding.UTF8.GetString(msg);

            return message;
        }

        public void Send(string message)
        {
            int size = message.Length;
            message = "" + (char)129 + (char)size + message;
            byte[] tosend = Encoding.UTF8.GetBytes(message);

            stream.Write(tosend, 1, message.Length);
        }
    }
}
