// Powermeter Simple Example.cpp : Diese Datei enthält die Funktion "main". Hier beginnt und endet die Ausführung des Programms.
//
/*
Thorlabs Power Meter Burst Measurement Mode
Example Date of Creation                        2024-12-17
Example Date of Last Modification on Github     2024-12-17
Version of C++ used for Testing and IDE         Visual Studio
Version of the Thorlabs SDK used.               TLPMX_64.dll 5.6.4983.666
==================
This example shows how to connect to a powermeter via USB or ethernet and displas a measurement value
*/

#include "TLPMX.h"
#include <iostream>

int error_exit(ViSession instrHdl, ViStatus err)
{
    ViChar buf[TLPM_ERR_DESCR_BUFFER_SIZE];

    // Print error
    TLPMX_errorMessage(instrHdl, err, buf);
    std::cout << "ERROR 0x" << err << " - " << buf;
    // Close instrument hande if open
    if (instrHdl != VI_NULL)
        TLPMX_close(instrHdl);
    return EXIT_FAILURE;
}

int main()
{
    //Uncomment and adapt the following two lines if you are using a powermeter via ethernet
    //TLPMX_setEnableNetSearch(0, 1);
    //TLPMX_setNetSearchMask(0, (ViString)"10.10.4.25 / 255.255.240.0");

    
    ViUInt32 deviceCount;
    ViStatus err = TLPMX_findRsrc(VI_NULL, &deviceCount);

    //Found a power meter?
    if (deviceCount == 0)
    {
        std::cout << "No power meter found" << std::endl;
        return EXIT_FAILURE;
    }

    //Get first device resource string
    static ViChar rsrcDescr[TLPM_BUFFER_SIZE];
    err = TLPMX_getRsrcName(VI_NULL, 0, rsrcDescr);
    if (VI_SUCCESS != err)
        return err;

    //Connect to device via resource string
    ViSession   instrHdl = VI_NULL;
    std::cout << "Opening session to '" << rsrcDescr << "' ..." << std::endl << std::endl;
    if ((err = TLPMX_init(rsrcDescr, VI_ON, VI_OFF, &instrHdl)))
        return error_exit(instrHdl, err);

    std::cout << "Session opened" << std::endl;

    //Get and print power meter identification 
    ViChar vendor[TLPM_BUFFER_SIZE];
    ViChar name[TLPM_BUFFER_SIZE];
    ViChar sernr[TLPM_BUFFER_SIZE];
    ViChar revision[TLPM_BUFFER_SIZE];
    if ((err = TLPMX_identificationQuery(instrHdl, vendor, name, sernr, revision)))
        return error_exit(instrHdl, err);

    std::cout << "Vendor: " << vendor << std::endl;
    std::cout << "Name: " << name << std::endl;
    std::cout << "S/N: " << sernr << std::endl;
    std::cout << "revision: " << revision << std::endl;

    //Get and print connected light sensor identification
    ViInt16 pType, pStype, pFlags;
    ViChar message[TLPM_BUFFER_SIZE];
    if ((err = TLPMX_getSensorInfo(instrHdl, name, sernr, message, &pType, &pStype, &pFlags, 1)))
        return error_exit(instrHdl, err);

    std::cout << "Sensor Name: " << name << std::endl;
    std::cout << "Sensor S/N: " << sernr << std::endl;
    std::cout << "Sensor Message: " << message << std::endl;

    ViReal64 power;
    err = TLPMX_measPower(instrHdl, &power,1);
    std::cout << std::endl;
    std::cout << "Power: " << power << std::endl;
    std::cout <<  std::endl;

    std::cout << "Closing session to " << rsrcDescr << std::endl;
    TLPMX_close(instrHdl);

    return 0;

}

