#include <iostream>
#include <string>
#include "Server.h"

using namespace std;

void main() {
	Server *server;
	string username;

	server = new Server(10011);
	cout << "Server started.\n";

	server->Start();
	cout << "Waiting for clients to connect.\n\n";

	while (true) {
		if (!server->Connect()) continue;
		cout << "Client connecing... '";

		username = server->Receive();
		if (username == "0") {
			cout << "username recv error.\n";
			continue;
		}

		cout << username << "' connected.\n";
		server->NewClient(username);
	}
}