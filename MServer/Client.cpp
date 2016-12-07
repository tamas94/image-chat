#include <iostream>
#include <string>
#include <sstream>
#include <iterator>
#include "Client.h"

using namespace std;

Client::Client(SOCKET socket, string name, USERS &users, Mutex &mutex) :
		users(users), mutex(mutex) {
	this->socket = socket;
	this->name = name;

	this->thread = std::thread(&Client::run, this);
}

void Client::run(void) {
	int received = 0;

	this->Send(OnlineUsers());

	mutex.EnterReader();
	for (auto user : users)
		(user.second)->Send("1 " + name);
	mutex.LeaveReader();

	mutex.EnterWriter();
	users[name] = this;
	mutex.LeaveWriter();

	while (true) {
		string message = Receive(received);
		if (message == "0") {
			cout << name << " - disconnected.\n";
			break;
		}
		else if (message == "-1") {
			cout << name << " - connection lost.\n";
			break;
		}

		string to, msg;
		istringstream iss(message);
		getline(iss, to, ' ');
		msg = message.substr(iss.tellg());

		mutex.EnterReader();
		users[to]->Send("3 " + name + " " + msg);
		mutex.LeaveReader();
	}

	mutex.EnterWriter();
	users.erase(name);
	mutex.LeaveWriter();

	mutex.EnterReader();
	for (auto user : users)
		(user.second)->Send("2 " + name);
	mutex.LeaveReader();

	closesocket(socket);
	delete this;
}

void Client::Send(string message) {
	int sent, total = 0, size = message.size() + 2;
	int b1 = (message.size() << 8) >> 8;
	int b2 = message.size() >> 8;
	message = char(b2) + message;
	message = char(b1) + message;
	auto msg = message.c_str();

	do {
		sent = send(socket, msg + total, size - total, 0);
		if (sent > 0)
			total += sent;
		else if (sent == SOCKET_ERROR) {
			cout << name << " - error sending.\n";
			break;
		}
	} while (total < size);
}

string Client::Receive(int& received) {
	int size, rec;

	do {
		rec = recv(socket, buffer + received, 4096, 0);
		if (rec == 0)
			return "0";
		else if (rec == -1)
			return "-1";
		received += rec;
	} while (received - 2 < buffer[0] | buffer[1] << 8);

	size = buffer[0] | buffer[1] << 8;
	string message(buffer + 2, size);

	if (size == received - 2) {
		received = 0;
		memset(buffer, 0, sizeof(buffer));
	}
	else {
		received = received - size - 2;
		strncpy_s(buffer, strlen(buffer), buffer + size + 2, strlen(buffer));
	}
	return message;
}

string Client::OnlineUsers() {
	string users = "0 ";

	mutex.EnterReader();
	for (auto user : this->users) {
		users += (user.first) + " ";
	}
	mutex.LeaveReader();

	users.pop_back();
	return users;
}

Client::~Client() {
	this->thread.join();
}