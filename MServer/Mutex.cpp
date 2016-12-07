#include "Mutex.h"

Mutex::Mutex() {
	m_cReaders = 0;
	InitializeCriticalSection(&m_csWrite);
	InitializeCriticalSection(&m_csReaderCount);
	m_hevReadersCleared = CreateEvent(NULL, TRUE, TRUE, NULL);
}

Mutex::~Mutex() {
	WaitForSingleObject(m_hevReadersCleared, INFINITE);
	CloseHandle(m_hevReadersCleared);
	DeleteCriticalSection(&m_csWrite);
	DeleteCriticalSection(&m_csReaderCount);
}

void Mutex::EnterReader() {
	EnterCriticalSection(&m_csWrite);
	EnterCriticalSection(&m_csReaderCount);
	if (++m_cReaders == 1)
		ResetEvent(m_hevReadersCleared);
	LeaveCriticalSection(&m_csReaderCount);
	LeaveCriticalSection(&m_csWrite);
}

void Mutex::LeaveReader() {
	EnterCriticalSection(&m_csReaderCount);
	if (--m_cReaders == 0)
		SetEvent(m_hevReadersCleared);
	LeaveCriticalSection(&m_csReaderCount);
}

void Mutex::EnterWriter() {
	EnterCriticalSection(&m_csWrite);
	WaitForSingleObject(m_hevReadersCleared, INFINITE);
}

void Mutex::LeaveWriter() {
	LeaveCriticalSection(&m_csWrite);
}
