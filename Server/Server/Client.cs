using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Server
{
    class Client
    {
        private TcpClient client;
        private NetworkStream stream;
        
        private Dictionary<string, Client> users;
        Mutex mutex;

        private string id;
        private int port;

        public Client(TcpClient client, string id, ref Dictionary<string, Client> users, ref Mutex mutex, int port)
        {
            this.client = client;
            this.stream = client.GetStream();
            this.users = users;
            this.mutex = mutex;
            this.id = id;
            this.port = port;

            Thread thread = new Thread(Listen);
            thread.Start();
        }

        public void Listen()
        {
            string message, to;
            string[] array;
            int code = 0;

            mutex.WaitOne();
            foreach (var user in users) {
                user.Value.Send("5 " + id);
            }
            users[id] = this;
            mutex.ReleaseMutex();

            bool exit = false;
            while (true)
            {
                if (exit) break;

                message = Receive();

                Console.WriteLine(message);
                Console.Read();

                array = message.Split(new char[] { ' ' }, 3);

                try
                {
                    code = int.Parse(array[0]);
                }
                catch
                {
                    break;
                }
                to = array[1];

                switch (code)
                {
                    case 0:
                        if (port != 10011) break;
                        Send(OnlineUsers());
                        break;
                    case 1:
                        mutex.WaitOne();
                        users[to].Send("1 " + id + " " + array[2]);
                        mutex.ReleaseMutex();
                        break;
                    case 2:
                    case 3:
                    case 4:
                        if (port != 10011) break;
                        mutex.WaitOne();
                        users[to].Send(code + " " + id);
                        mutex.ReleaseMutex();
                        break;
                    case 6:
                        exit = true;
                        break;
                }
            }

            if (port != 10011) return;
            mutex.WaitOne();
            users.Remove(id);
            foreach (var user in users)
            {
                user.Value.Send("6 " + id);
            }
            mutex.ReleaseMutex();
        }

        public string Receive()
        {
            while (!stream.DataAvailable) ;

            byte[] bytes = new byte[client.Available];
            stream.Read(bytes, 0, bytes.Length);

            int size = -1;
            int offset = 2;
            if (bytes[1] - 128 < 126)
            {
                Console.WriteLine("a");
                size = bytes[1] - 128;
            }
            else if (bytes[1] - 128 == 126)
            {
                Console.WriteLine("b");
                size = (bytes[2] << 8) | bytes[3];
                offset += 2;
            }
            else
            {
                Console.WriteLine("c");
                size = ((bytes[7] << 16) | bytes[8] << 8) | bytes[9];
                offset += 8;
            }

            byte[] msg = new byte[size];
            byte[] key = new byte[4] { bytes[offset], bytes[offset + 1], bytes[offset + 2], bytes[offset + 3] };
            for (int i = 0; i < bytes.Length - 4 - offset; i++)
            {
                msg[i] = (byte)(bytes[i + 4 + offset] ^ key[i % 4]);
            }
            Console.Write("hossz: " + msg.Length);
            Console.Write("\n");
            string message = Encoding.UTF8.GetString(msg);

            return message;
        }

        public void Send(string message)
        {
            char[] c = new char[9];
            int size = message.Length;
            if (size < 126)
            {
                message = "" + (char)129 + (char)size + message;
            }
            else if (size == 126)
            {
                c[1] = (char)(size >> 8);
                c[2] = (char)((size << 8) >> 8);
                message = "" + (char)129 + c[1] + c[2] + message;
            }
            else
            {
                c[1] = (char)(0);
                c[2] = (char)(0);
                c[3] = (char)(0);
                c[4] = (char)(0);
                c[5] = (char)(0);
                c[6] = (char)(size >> 16);
                c[7] = (char)((size << 16) >> 24);
                c[8] = (char)((size << 24) >> 24);
                message = "" + (char)129 + c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[8] + message;
            }

            byte[] tosend = Encoding.Unicode.GetBytes(message);
            byte[] good = new byte[tosend.Length / 2];

            for (int i = 0; i < tosend.Length / 2; i++)
            {
                good[i] = tosend[2 * i];
            }

            stream.Write(good, 0, tosend.Length / 2);
        }

        public string OnlineUsers()
        {
            string users = "0 ";

            mutex.WaitOne();
            foreach (var user in this.users)
            {
                users += (user.Key) + " ";
            }
            mutex.ReleaseMutex();

            users = users.Substring(0, users.Length - 1);
            return users;
        }
    }
}
