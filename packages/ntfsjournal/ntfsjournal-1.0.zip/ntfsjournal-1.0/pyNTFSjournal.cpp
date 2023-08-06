/************************************************************************
pyntfsjournal - NTFS USN journal reader for Python
Copyright (C) 2011  Lazar Laszlo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

http://pyntfsjournal.sourceforge.net/
mailto:laszlolazar@yahoo.com
************************************************************************/ 

#include "Python.h"
#include <windows.h>

#include "Python.h"

static PyObject *
getfunc(PyObject *self, PyObject *args)
{
	PyObject *ret = PyList_New(0);
	//PyObject *ob = Py_BuildValue("s", "hello");
	char *param;
	DWORD mask=USN_REASON_FILE_DELETE;
	char drive[MAX_PATH];

	HANDLE hVol;
   CHAR Buffer[0x4000];
   char fn[MAX_PATH];

   USN_JOURNAL_DATA JournalData;
   READ_USN_JOURNAL_DATA ReadData = {0, 0, FALSE, 0, 0};
   PUSN_RECORD UsnRecord;  

   DWORD dwBytes;
   DWORD dwRetBytes;

   int ok = PyArg_ParseTuple(args, "s|k", &param, &mask);

   if(ok!=1)
	   return Py_None;

   ReadData.ReasonMask = mask;

	strcpy_s(drive,MAX_PATH,"\\\\.\\");
	strcat_s(drive,MAX_PATH,param);
	strcat_s(drive,MAX_PATH,":");

   hVol = CreateFile( drive, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE,NULL,OPEN_EXISTING,0,NULL);

   if( hVol == INVALID_HANDLE_VALUE )
   {
	   return Py_None;
   }

   if( !DeviceIoControl( hVol, FSCTL_QUERY_USN_JOURNAL, NULL,0,&JournalData,sizeof(JournalData),&dwBytes,NULL) )
   {
      return Py_None;
   }

   ReadData.UsnJournalID = JournalData.UsnJournalID;


   while(1)
   {
      memset( Buffer, 0, sizeof(Buffer) );

      if( !DeviceIoControl( hVol, FSCTL_READ_USN_JOURNAL, &ReadData,sizeof(ReadData),&Buffer,sizeof(Buffer),&dwBytes,NULL) )
      {
         return Py_None;
      }

      dwRetBytes = dwBytes - sizeof(USN);

      // Find the first record
      UsnRecord = (PUSN_RECORD)(((PUCHAR)Buffer) + sizeof(USN));  

	  if(dwRetBytes<=0)
		  break;
      //printf( "****************************************\n");

      while( dwRetBytes > 0 )
      {
         //printf( "USN: %I64x\n", UsnRecord->Usn );
         //printf("File name: %.*S\n", UsnRecord->FileNameLength/2, UsnRecord->FileName );
		 WideCharToMultiByte(CP_ACP, 0, UsnRecord->FileName,UsnRecord->FileNameLength/2, fn,MAX_PATH,NULL,0);
		 fn[UsnRecord->FileNameLength/2]=0;
	
		 PyList_Append(ret,Py_BuildValue("{s:s,s:K,s:K,s:k,s:k,s:K}", "name",fn,
			 "timestamp",UsnRecord->TimeStamp.QuadPart,
			 "frn",UsnRecord->FileReferenceNumber,
			 "attr",UsnRecord->FileAttributes,
			 "reason",UsnRecord->Reason,
			 "pfrn",UsnRecord->ParentFileReferenceNumber));

         dwRetBytes -= UsnRecord->RecordLength;
		 
         // Find the next record
         UsnRecord = (PUSN_RECORD)(((PCHAR)UsnRecord) + UsnRecord->RecordLength); 
      }
      // Update starting USN for next call
      ReadData.StartUsn = *(USN *)&Buffer; 
   }
   CloseHandle(hVol);


	//PyList_Append(ret,ob);
	//PyList_Append(ret,ob);
	return ret;
}

static PyObject *
tsfunc(PyObject *self, PyObject *args)
{
	SYSTEMTIME st;
	LONGLONG ts;
   int ok = PyArg_ParseTuple(args, "K", &ts);
	if(ok!=1)
		return Py_None;
	FileTimeToSystemTime((FILETIME*)&ts, &st);
	SystemTimeToTzSpecificLocalTime(NULL, &st, &st);
	char str[256];
	sprintf_s(str,"%04i-%02i-%02i %02i:%02i:%02i.%i",st.wYear,st.wMonth,st.wDay,st.wHour,st.wMinute,st.wSecond,st.wMilliseconds);
	return Py_BuildValue("s",str);
}

static PyMethodDef ntfsjournal_methods[] = {
	{"get", getfunc, METH_VARARGS, "get(drive, [mask]) returns a list of journal records"},
	{"ts2str", tsfunc, METH_VARARGS, "ts2str(timestamp) returns timestamp as string"},
	{NULL, NULL}
};

PyMODINIT_FUNC
initntfsjournal(void)
{
	PyObject *ob =	Py_InitModule("ntfsjournal", ntfsjournal_methods,"NTFS journal reader by Lazar Laszlo");
	PyModule_AddIntConstant(ob,"USN_REASON_DATA_OVERWRITE",0x00000001);
	PyModule_AddIntConstant(ob,"USN_REASON_DATA_EXTEND",0x00000002);
	PyModule_AddIntConstant(ob,"USN_REASON_FILE_CREATE",0x00000100);
	PyModule_AddIntConstant(ob,"USN_REASON_FILE_DELETE",0x00000200);
	PyModule_AddIntConstant(ob,"USN_REASON_EA_CHANGE",0x00000400);
	PyModule_AddIntConstant(ob,"USN_REASON_SECURITY_CHANGE",0x00000800);
	PyModule_AddIntConstant(ob,"USN_REASON_RENAME_OLD_NAME",0x00001000);
	PyModule_AddIntConstant(ob,"USN_REASON_RENAME_NEW_NAME",0x00002000);
	PyModule_AddIntConstant(ob,"USN_REASON_HARD_LINK_CHANGE",0x00010000);
	PyModule_AddIntConstant(ob,"USN_REASON_CLOSE",0x80000000);
	PyModule_AddIntConstant(ob,"USN_REASON_ALL",0xFFFFFFFF);
} 
