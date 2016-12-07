#pragma once

#include <stdio.h>
#include <unordered_map>
#include "winsock2.h"
#include "Mutex.h"
#include <thread>

class Client {
	typedef std::unordered_map<std::string, Client*> USERS;
private:
	char buffer[65536];
	SOCKET socket;
	std::string name;
	Mutex &mutex;
	USERS &users;
	std::thread thread;
public:
	Client(SOCKET, std::string, USERS&, Mutex&);
	~Client();
	void run();
	void Send(std::string);
	std::string Receive(int&);
	std::string OnlineUsers();
};