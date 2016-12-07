#pragma once

#pragma comment(lib, "Ws2_32.lib")
#pragma warning(disable:4996)
#define _WINSOCK_DEPRECATED_NO_WARNINGS

#include <stdio.h>
#include <iostream>
#include <string>
#include <unordered_map>
#include "winsock2.h"
#include "Client.h"

class Server {
	typedef std::unordered_map<std::string, Client*> USERS;
private:
	WSADATA wsaData;
	sockaddr_in service;
	Mutex *mutex;
	USERS users;
public:
	SOCKET ListenSocket, AcceptSocket;
	Server(int);
	void Start();
	void Stop();
	bool Connect();
	void NewClient(std::string name);
	bool Send(std::string);
	std::string Receive();
};