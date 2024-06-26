//Example Date of Creation(YYYY - MM - DD) 2024 - 02 - 01
//Example Date of Last Modification on Github 2024 - 02 - 01
//Version of C++ used for Testing and IDE: C++ 14, Visual Studio 2022
//Version of the NI-VISA Driver used: 24.0
//Example Description: This example shows some of the functionality of PMXXX series power meter with SCPI commands.

#include "stdlib.h"
#include "stdio.h"
#include "iostream"
#include "visa.h"

using namespace std;
void SaveMultiRsrcName(ViChar rsrcNameMatrix[10][256], ViChar * rsrcName, int deviceNumber);

int main()
{
	ViStatus status = 0;
	ViSession defaultRM = 0, instr = 0;
	ViFindList rsrcList = 0;
	ViUInt32 count = 0;
	ViChar rsrcName[256];
	ViByte buffer[255];
	ViUInt32 returnCount = 0;

	//Open the default resource manager
	status = viOpenDefaultRM(&defaultRM);
	if (status < VI_SUCCESS)
	{
		printf("Can't initialize VISA\n");
		return -1;
	}
	
	//find the VISA resource devices which resource name starts with "USB0::0x1313" and ends with "INSTR"
	ViConstString rsrcFormat = "USB0::0x1313?*INSTR";
	viFindRsrc(defaultRM, rsrcFormat, &rsrcList, &count, rsrcName);
	
	if (count == 0)
	{
		printf("No Device Found!");
		return -1;
	}
	//Connect the only device
	else if (count == 1)
	{
		status = viOpen(defaultRM, rsrcName, VI_NULL, VI_NULL, &instr);
		if (status < VI_SUCCESS)
		{
			printf("Can not connect to %s\n", rsrcName);
			return -1;
		}
		printf("%s Connected.\n", rsrcName);
	}
	//Select one device to connect if there's more than one device.
	else if (count > 1)
	{
		ViChar rsrcNameMatrix[10][256];//Ten devices can be recorded in maximum, the length of resource name is 256 in maximum.
		int deviceNumber = 0;
		printf("Enter the number to select the device you want to connect.\n");

		//Display the first device
		SaveMultiRsrcName(rsrcNameMatrix, rsrcName, 0);
		printf("0. %s\n", rsrcNameMatrix[0]);

		//Display the remaining devices
		for (int i = 1; i < count; i++)
		{
			viFindNext(rsrcList, rsrcName);
			SaveMultiRsrcName(rsrcNameMatrix, rsrcName, i);
			printf("%d. %s\n", i, rsrcNameMatrix[i]);
		}

		//Select the device;
		cin >> deviceNumber;

		//Connect the selected device
		status = viOpen(defaultRM, rsrcNameMatrix[deviceNumber], VI_NULL, VI_NULL, &instr);
		if (status < VI_SUCCESS)
		{
			printf("Can not connect to %s\n", rsrcNameMatrix[deviceNumber]);
			return -1;
		}
		printf("%s Connected.\n", rsrcNameMatrix[deviceNumber]);
	}

	//Set the answer timeout
	viSetAttribute(instr, VI_ATTR_TMO_VALUE, 5000);

	//Enable the terminal character
	viSetAttribute(instr, VI_ATTR_TERMCHAR_EN, VI_TRUE);
	viSetAttribute(instr, VI_ATTR_TERMCHAR, '\n');

	//Read ID string
	viPrintf(instr, "*IDN?\n");
	viRead(instr, buffer, sizeof(buffer), &returnCount);
	printf("%.*s\n", returnCount,buffer);
	
	//Set Wavelength (unit: nm)
	int wavelength = 800;
	float wavelengthRead = 0;
	returnCount = 100;
	viPrintf(instr, "SENSE:CORRECTION:WAVELENGTH %d\n", wavelength);
	viQueryf(instr, "SENSE:CORRECTION:WAVELENGTH?\n", "%f", &wavelengthRead);
	if (wavelengthRead == wavelength)
	{
		printf("The wavelength is set to %f nm\n", wavelengthRead);
	}
	else
	{
		printf("Fail to set the wavelength.\n");
	}

	//Set the average rate
	int average = 500;
	int averageRead = 0;
	viPrintf(instr, "SENSE:AVERAGE %d\n", average);
	viQueryf(instr, "SENSE:AVERAGE?\n", "%d", &averageRead);
	if (averageRead == average)
	{
		printf("The average rate is set to %d\n", averageRead);
	}
	else
	{
		printf("Fail to set the average rate.\n");
	}

	//Read the power
	int sampleNum = 10;
	float power = 0;
	for (int i = 0; i < sampleNum; i++)
	{
		viQueryf(instr, "MEASURE:POWER?\n", "%f", &power);
		printf("The power is %f W\n", power);
	}
	
	//Disconnect the device
	viClose(instr);
	viClose(defaultRM);
	printf("Program finishes.\n");
	
}

void SaveMultiRsrcName(ViChar rsrcNameMatrix[10][256], ViChar* rsrcName, int deviceNumber)
{
	for (int j = 0; j < 256; j++)
	{
		rsrcNameMatrix[deviceNumber][j] = * (rsrcName+j);
	}
}

