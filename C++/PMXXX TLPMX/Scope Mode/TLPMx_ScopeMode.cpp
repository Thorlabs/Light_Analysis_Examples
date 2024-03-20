/*
Thorlabs Power Meter Scope Measurement Mode
Example Date of Creation                        2024-03-20
Example Date of Last Modification on Github     2024-03-20
Version of C++ used for Testing and IDE         Visual Studio
Version of the Thorlabs SDK used.               TLPMx.dll 5.6.4847
==================
This example shows how to configure and fetch a Thorlabs Power Meter for Software or Hardware 
triggered Scope Measurement mode. In Scope mode the meter behaves like an oscilloscope and
stores a fixed amount of samples within the device after a softwar or hardware trigger condition.
Once the sequence is complete you can fetch the results.
*/

#include "TLPMX.h"
#include <iostream>

using namespace std;

static ViUInt32 timestamps[10000] = {0};
#if !defined(IS_DUAL_CHANNEL_TL_PM)
static ViReal32 values[10000] = {0};
#else
static ViReal32 values1[10000] = {0};
static ViReal32 values2[10000] = {0};
#endif

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

int softwareTriggeredScopeMeasurement(ViSession instrHdl)
{
    ViStatus err;

    //Configure software triggered scope measurement
    //================================================
    //Configure channel for scope power measurement
    constexpr ViUInt32 averaging = 2;
    if((err = TLPMX_confPowerMeasurementSequenceHWTrigger(instrHdl, averaging, 1)))
        return err;
    
#if defined(IS_DUAL_CHANNEL_TL_PM)
    //Configure channel for scope power measurement
    if((err = TLPMX_confPowerMeasurementSequenceHWTrigger(instrHdl, averaging, 2)))
        return err;
#endif   
    
    //scope measurement
    //================================================
    //Start the scope measurement mode. 
    ViBoolean wasForcedTrigger;
    if((err = TLPMX_startMeasurementSequence(instrHdl, 0, nullptr)))
        return err;


#if !defined(IS_DUAL_CHANNEL_TL_PM)
    //Fetch scope measurement results out of buffer
    if((err = TLPMX_getMeasurementSequence(instrHdl, 10000, timestamps, values, nullptr)))
        return err;
#else
    //Fetch scope measurement results out of buffer
    if((err = TLPMX_getMeasurementSequence(instrHdl, 10000, timestamps, values1, values2)))
        return err;
#endif
    return VI_SUCCESS;
}

int hardwareTriggeredScopeMeasurement(ViSession instrHdl)
{
    ViStatus err;
    
    //Configure hardware triggered scope measurement
    //================================================
    //Configure channel for scope power measurement
    constexpr ViUInt32 trigSrc = 1;
    constexpr ViUInt32 baseTime = 2;
    constexpr ViUInt32 hPos = 2;
    if((err = TLPMX_confPowerMeasurementSequenceHWTrigger(instrHdl, trigSrc, baseTime, hPos, 1)))
        return err;
    
#if defined(IS_DUAL_CHANNEL_TL_PM)
    //Configure channel for scope power measurement
    if((err = TLPMX_confPowerMeasurementSequenceHWTrigger(instrHdl, trigSrc, baseTime, hPos, 2)))
        return err;
#endif   
    
    //scope measurement
    //================================================
    //Start the scope measurement mode. Now trigger is armed. 
    ViBoolean wasForcedTrigger;
    if((err = TLPMX_startMeasurementSequence(instrHdl, 0, nullptr)))
        return err;


#if !defined(IS_DUAL_CHANNEL_TL_PM)
    //Fetch scope measurement results out of buffer
    if((err = TLPMX_getMeasurementSequenceHWTrigger(instrHdl, 10000, timestamps, values, nullptr)))
        return err;
#else
    //Fetch scope measurement results out of buffer
    if((err = TLPMX_getMeasurementSequenceHWTrigger(instrHdl, 10000, timestamps, values1, values2)))
        return err;
#endif
    return VI_SUCCESS;
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
    
    if((res = softwareTriggeredScopeMeasurement(instrHdl)))
        return error_exit(instrHdl, err);
    //if((res = hardwareTriggeredScopeMeasurement(instrHdl)))
    //    return error_exit(instrHdl, err);

    cout << "Closing session to " << rsrcDescr << endl;
    TLPMX_close (instrHdl);

    return 0;
}
