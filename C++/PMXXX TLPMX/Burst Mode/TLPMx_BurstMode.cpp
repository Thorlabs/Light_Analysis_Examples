/*
Thorlabs Power Meter Burst Measurement Mode
Example Date of Creation                        2024-03-20
Example Date of Last Modification on Github     2024-03-20
Version of C++ used for Testing and IDE         Visual Studio
Version of the Thorlabs SDK used.               TLPMx.dll 5.6.4847
==================
This example shows how to configure and fetch a Thorlabs Power Meter for Burst Measurement mode.
In Burst mode the meter stores a sequence of measurements in an device internal memory for every
trigger condition. Once the measurement is complete you can fetch the results. 
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
    if(instrHdl != nullptr) 
        TLPMX_close(instrHdl);
    return EXIT_FAILURE;
}

int main(int argc, char* argv[])
{
    static ViUInt32 timestamps[15000] = {0};
#if !defined(IS_DUAL_CHANNEL_TL_PM)
    static ViReal32 values[15000] = {0};
#else
    static ViReal32 values1[15000] = {0};
    static ViReal32 values2[15000] = {0};
#endif
    ViUInt32    deviceCount;
    //Search for power meters
    ViStatus err = TLPMX_findRsrc (nullptr, &deviceCount);
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
    err = TLPMX_getRsrcName (nullptr, 0, rsrcDescr);
    if(VI_SUCCESS != err)
        return err;

    //Connect to device via resource string
    ViSession   instrHdl = nullptr;
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
    
    //Configure photodiode measurement for burst mode
    //================================================
    //Select CW measurement mode
    if((res = TLPMX_setFreqMode(instrHdl, TLPM_FREQ_MODE_CW, 1)))
        return error_exit(instrHdl, err);
 
   //Disable bandwidth limitation
    if((res = TLPMX_setInputFilterState(instrHdl, VI_FALSE, 1)))
        return error_exit(instrHdl, err);
    
    //Select manual range in Watt and disables auto ranging
    if((res = TLPMX_setPowerRange(instrHdl, 0.005, 1))) ///TODO: Adjust to your experiment
        return error_exit(instrHdl, err);

    //Set trigger threshold level in percent
    if((res = TLPMX_setPeakThreshold(instrHdl, 30, 1))) ///TODO: Adjust to your experiment
        return error_exit(instrHdl, err);
        
#if defined(IS_DUAL_CHANNEL_TL_PM)
    //Select CW measurement mode
    if((res = TLPMX_setFreqMode(instrHdl, TLPM_FREQ_MODE_CW, 2)))
        return error_exit(instrHdl, err);
 
   //Disable bandwidth limitation
    if((res = TLPMX_setInputFilterState(instrHdl, VI_FALSE, 2)))
        return error_exit(instrHdl, err);
    
    //Select manual range in Watt and disables auto ranging
    if((res = TLPMX_setPowerRange(instrHdl, 0.005, 2))) ///TODO: Adjust to your experiment
        return error_exit(instrHdl, err);

    //Set trigger threshold level in percent
    if((res = TLPMX_setPeakThreshold(instrHdl, 30, 2))) ///TODO: Adjust to your experiment
        return error_exit(instrHdl, err);
#endif

    //Configure burst measurement
    //================================================
    //Configure channel for burst power measurement
    if((err = TLPMX_confBurstArrayMeasPowerChannel(instrHdl,1)))
        return error_exit(instrHdl, err);
    
#if defined(IS_DUAL_CHANNEL_TL_PM)
    //Select CW measurement mode
    if((err = TLPMX_confBurstArrayMeasPowerChannel(instrHdl,2)))
        return error_exit(instrHdl, err);
#endif   
    constexpr ViUInt32 trigScr = 1;     //Select trigger source. 1 is for channel 1. For other trigger sources refer to SCPI command documentation.
    constexpr ViUInt32 initDelay = 0;   //Initial delay after trigger before measurement burst starts. Unit is XXX. 
    constexpr ViUInt32 burstCount = 10; //Amount of samples stored in buffer for every trigger. 
    constexpr ViUInt32 averaging = 2;   //Unit is samples. So if PM samples at 100 kHz, avg = 2 results in a sample rate of 50 kHz. 
    if((err = TLPMX_confBurstArrayMeasTrigger(instrHdl, trigScr, initDelay, burstCount, averaging)))
        return error_exit(instrHdl, err);
    
    //Burst measurement
    //================================================
    //Start the burst measurement mode. Now trigger is armed. 
    if((err = TLPMX_startBurstArrayMeasurement(instrHdl)))
        return error_exit(instrHdl, err);
    
    //OPTIONAL: For example! Simulate a trigger. Hardware trigger would also cause burst measurement
    if((err = TLPMX_writeRaw(instrHdl, "TRIGer:ARRay:FORCe")))
        return error_exit(instrHdl, err);
    
    //Aborts burst measurement and returns amount of samples in device buffer
    ViUInt32 samplesCount;
    if((err = TLPMX_getBurstArraySamplesCount(instrHdl, &samplesCount)))
        return error_exit(instrHdl, err);

#if !defined(IS_DUAL_CHANNEL_TL_PM)
    //Fetch burst measurement results out of buffer
    if((err = TLPMX_getBurstArraySamples(instrHdl, 0, samplesCount, timestamps, values, nullptr)))
        return error_exit(instrHdl, err);
#else
    //Fetch burst measurement results out of buffer
    if((err = TLPMX_getBurstArraySamples(instrHdl, 0, samplesCount, timestamps, values1, values2)))
        return error_exit(instrHdl, err);
#endif

    cout << "Closing session to " << rsrcDescr << endl;
    TLPMX_close (instrHdl);

    return 0;
}

