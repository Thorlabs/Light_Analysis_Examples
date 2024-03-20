/*
Thorlabs Power Meter Fast Measurement Mode
Example Date of Creation                        2024-03-20
Example Date of Last Modification on Github     2024-03-20
Version of C++ used for Testing and IDE         Visual Studio
Version of the Thorlabs SDK used.               TLPMx.dll 5.6.4847
==================
This example shows how to fetch the Thorlabs Power Meter Fast Measurement stream.
The fast measurement stream allows to aquire all sampling results at maximum speed.
*/

#include "TLPMX.h"
#include <iostream>

using namespace std;

int error_exit(ViSession instrHdl, ViStatus err)
{
    ViChar buf[TLPM_ERR_DESCR_BUFFER_SIZE];

    // Print error
    TLPMX_errorMessage (instrHdl, err, buf);
    cout << "ERROR 0x" << hex << err << " - " << buf;
    // Close instrument hande if open
    if(instrHdl != VI_NULL) 
        TLPMX_close(instrHdl);
    return EXIT_FAILURE;
}

int main(int argc, char* argv[])
{
    ViUInt32    deviceCount;
    //Search for power meters
    ViStatus err = TLPMX_findRsrc (VI_NULL, &deviceCount);
    if(VI_SUCCESS != err)
       return err;
    
    //Found a power meter?
    if(deviceCount == 0)
    {
        cout << "No power meter found" << endl;
        return EXIT_FAILURE;
    }

    //Get first device resource string
    static ViChar rsrcDescr[TLPM_BUFFER_SIZE];
    err = TLPMX_getRsrcName (VI_NULL, 0, rsrcDescr);
    if(VI_SUCCESS != err)
        return err;

    //Connect to device via resource string
    ViSession   instrHdl = VI_NULL;
    cout << "Opening session to '"<< rsrcDescr << "' ..." << endl << endl;
    if((err = TLPMX_init(rsrcDescr, VI_ON, VI_OFF, &instrHdl))) 
        return error_exit(instrHdl, err);

    cout << "Session opened" << endl;

    //Get and print power meter identification 
    ViChar vendor[TLPM_BUFFER_SIZE];
    ViChar name[TLPM_BUFFER_SIZE];
    ViChar sernr[TLPM_BUFFER_SIZE];
    ViChar revision[TLPM_BUFFER_SIZE];
    if((err = TLPMX_identificationQuery(instrHdl, vendor, name, sernr, revision)))
        return error_exit(instrHdl, err);

    cout << "Vendor: " << vendor << endl;
    cout << "Name: " << name << endl;
    cout << "S/N: " << sernr << endl;
    cout << "revision: " << revision << endl;

    //Get and print connected light sensor identification
    ViInt16 pType,pStype, pFlags;
    ViChar message[TLPM_BUFFER_SIZE];
    if((err = TLPMX_getSensorInfo(instrHdl, name, sernr, message, &pType, &pStype, &pFlags, 1)))
        return error_exit(instrHdl, err);

    cout << "Sensor Name: " << name << endl;
    cout << "Sensor S/N: " << sernr << endl;
    cout << "Sensor Message: " << message << endl;

    //Get and print connected light sensor identification
    ViUInt32 samplesCount;
    ViUInt32 timestamps[200] = {0};
    ViReal32 values[200] = {0};

#if !defined(FAST_STREAM_RAW_DATA)
    //Configure stream for power measurement. This will also flush the device stream buffer.
    if((err = TLPMX_confPowerFastArrayMeasurement(instrHdl, 1)))
        return error_exit(instrHdl, err);
    
    //Fetch fast array measurement results where delta t is already calculated in the driver. Use any
    //configure function to reset the start time base. 
    if((err = TLPMX_getNextFastArrayMeasurementRelativeTime(instrHdl, &samplesCount, timestamps, values, 1)))
        return error_exit(instrHdl, err);
    //Fetch more data. Do this as fast as possible. Device  buffers recent 10ms samples only!
    if((err = TLPMX_getNextFastArrayMeasurementRelativeTime(instrHdl, &samplesCount, timestamps, values, 1)))
        return error_exit(instrHdl, err);
#else
    //Configure stream for power measurement. This will also flush the device stream buffer.
    if((err = TLPMX_confPowerFastArrayMeasurement(instrHdl, 1)))
        return error_exit(instrHdl, err);

    //Fetch fast array measurement results with relative time stamps. 
    //Timestamps is a relative wrapping 32-bit microsecond counter. You have to calculate detla t between samples youreself.
    if((err = TLPMX_getNextFastArrayMeasurement(instrHdl, &samplesCount, timestamps, values, 1)))
        return error_exit(instrHdl, err);
    //Fetch more data. Do this as fast as possible. Device  buffers recent 10ms samples only!
    if((err = TLPMX_getNextFastArrayMeasurement(instrHdl, &samplesCount, timestamps, values, 1)))
        return error_exit(instrHdl, err);
#endif
    cout << "Closing session to " << rsrcDescr << endl;
    TLPMX_close (instrHdl);

    return 0;
}

