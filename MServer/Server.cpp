#include <iostream>
#include <string>
#include <sstream>
#include "Client.h"
#include "Server.h"

using namespace std;

Server::Server(int Port) {
	mutex = new Mutex();

	service.sin_family = AF_INET;
	service.sin_addr.s_addr = INADDR_ANY;
	service.sin_port = htons(Port);

	AcceptSocket = INVALID_SOCKET;
	ListenSocket = INVALID_SOCKET;
}

void Server::Start() {
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != NO_ERROR) {
		cout << "Error at WSAStartup().\n";
		Stop();
	}

	ListenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (ListenSocket == INVALID_SOCKET) {
		cout << "Error at socket(): " + WSAGetLastError() << endl;
		Stop();
	}

	if (::bind(ListenSocket, (SOCKADDR*)&service, sizeof(service)) == SOCKET_ERROR) {
		cout << "bind() failed.\n";
		Stop();
	}

	if (listen(ListenSocket, SOMAXCONN) == SOCKET_ERROR) {
		cout << "Error listening on socket.\n";
		Stop();
	}
}

bool Server::Connect() {
	AcceptSocket = accept(ListenSocket, NULL, NULL);
	if (AcceptSocket == INVALID_SOCKET) {
		cout << "Accept failed: " + WSAGetLastError() << endl;
		return false;
	}
	return true;
}

void Server::NewClient(string name) {
	Client *thread = new Client(AcceptSocket, name, users, *mutex);
}

string Server::Receive() {
	char buffer[1024];
	int received = 0;
	int size, rec;
	do {
		rec = recv(AcceptSocket, buffer + received, 1024, 0);
		if (rec < 1)
			return "0";
		received += rec;
	} while (received - 1 < buffer[0]);

	size = buffer[0];
	string message(buffer + 1, size);

	return message;
}

void Server::Stop() {
	delete mutex;

	closesocket(ListenSocket);
	closesocket(AcceptSocket);
	WSACleanup();

	exit(0);
}