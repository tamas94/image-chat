#pragma once

#include "windows.h"

class Mutex {
private:
	CRITICAL_SECTION m_csWrite;
	CRITICAL_SECTION m_csReaderCount;
	long m_cReaders;
	HANDLE m_hevReadersCleared;
public:
	Mutex();
	~Mutex();
	void EnterReader();
	void LeaveReader();
	void EnterWriter();
	void LeaveWriter();
};