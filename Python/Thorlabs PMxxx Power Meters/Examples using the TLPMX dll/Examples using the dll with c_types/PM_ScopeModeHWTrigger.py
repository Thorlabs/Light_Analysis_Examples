"""
Example Thorlabs Scope HW Trigger
Example Date of Creation                            2026-08-24
Example Date of Last Modification on Github         2026-08-24
Version of Python                                   3.13
Version of the Thorlabs SDK used: Thorlabs Optical Parameter Monitor Version 7.0
==================
The Scope Mode provides an oscilloscope-like measurement method. 
The Scope Mode is meant to provide a highly resolved snapshot of a signal.
After a trigger signal, 10000 samples are acquired and stored in the internal buffer.
This examples shows how use the hardware trigger.
Two different types of hardware trigger are supported: 1. Incoming signal on the detector 2. TTL input 
Powermeters PM5020, PM100D3, PM6x and PM103/PM103E support the hardware trigger.
"""

import time
from ctypes import c_int16, c_uint16, cdll, c_float, c_long, c_uint32, c_double, byref, create_string_buffer, c_bool, c_int, c_float, sizeof, c_voidp
import time
import matplotlib.pyplot as plt

TLPM_DEFAULT_CHANNEL = 1
TLPM_BUFFER_SIZE = 256

def main():
    #load dll
    if sizeof(c_voidp) == 4:
        dll_path = r"C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin\TLPMX_32.dll"
    else:
        dll_path = r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll"
    lib = cdll.LoadLibrary(dll_path)

    #find devices
    deviceHandle = c_long(0)
    deviceCount = c_uint32()
    lib.TLPMX_findRsrc(deviceHandle, byref(deviceCount))
    print("devices found: " + str(deviceCount.value))
    resource_name = create_string_buffer(TLPM_BUFFER_SIZE)
    lib.TLPMX_getRsrcName(deviceHandle, c_uint32(0), resource_name)

    #Connect to first powermeter
    res=lib.TLPMX_init(resource_name, c_bool(True), c_bool(False), byref(deviceHandle))
    if res==0: 
        print(resource_name.value ," connected  " )
    time.sleep(1)

    #Set to CW mode, turn off autorange, and set input filter state to high bandwidth. 
    lib.TLPMX_setFreqMode(deviceHandle, c_uint16(0), c_uint16(TLPM_DEFAULT_CHANNEL)) 
    #auto range must be set to false before finding the range and trigger level.
    lib.TLPMX_setCurrentAutoRange(deviceHandle, c_bool(False), TLPM_DEFAULT_CHANNEL)
    #Input filter state must be set to high bandwidth before finding the range and trigger level.
    lib.TLPMX_setInputFilterState(deviceHandle, c_bool(False), TLPM_DEFAULT_CHANNEL)

    time.sleep(1)

    #If a pulse train is measured, and the trigger source is the incoming light, the range and trigger level have to be set. 
    #The peak detector can be used to find the range and trigger level.
    lib.TLPMX_setFreqMode(deviceHandle, c_uint16(1), c_uint16(TLPM_DEFAULT_CHANNEL))
    lib.TLPMX_startPeakDetector(deviceHandle, TLPM_DEFAULT_CHANNEL)
    isRunning = c_bool(True)
    while isRunning.value:
        time.sleep(1)
        lib.TLPMX_isPeakDetectorRunning(deviceHandle, byref(isRunning), TLPM_DEFAULT_CHANNEL)
    lib.TLPMX_setFreqMode(deviceHandle, c_uint16(0), c_uint16(TLPM_DEFAULT_CHANNEL))
    powerrange = c_double()
    lib.TLPMX_getPowerRange(deviceHandle, c_int16(0), byref(powerrange), TLPM_DEFAULT_CHANNEL)
    print("Power range: " + str(powerrange.value))
    threshold = c_double()
    lib.TLPMX_getPeakThreshold(deviceHandle, c_int16(0), byref(threshold), TLPM_DEFAULT_CHANNEL)#peak detection threshold in percent of range
    print("Trigger level: " + str(threshold.value))    



    #Configure device for current measurement sequence with hardware trigger
    trgSource = c_uint32(1)
    """     external trigger source:
    PM5020: 1(default) signal of channel 1, 2 signal of channel 2, 3 signal of front AUX, 4 signal of rear trigger.
    PM100D3: 1(default) signal of channel 1, 2 for DIO1
    PM6x: 1(default) signal of channel 1, 2 for DIO1
    PM103/PM103E: 1(default) """
    averaging = c_uint32(1)
    horPos = c_uint32(0) #trigger horizontal position
    lib.TLPMX_confCurrentMeasurementSequenceHWTrigger(deviceHandle, trgSource, averaging, horPos, TLPM_DEFAULT_CHANNEL) 

    #Start measurement with hardware trigger
    triggerForced = c_bool(True)
    autoTriggerDelay = c_uint16(0)
    lib.TLPMX_startMeasurementSequence(deviceHandle, autoTriggerDelay, byref(triggerForced))

    #Retrieve the scope measurement results out of the device internal buffer.
    baseTime = c_int(10)
    dataSize = baseTime.value * 100
    timeStamps = (c_float * dataSize)()
    data = (c_float * dataSize)() 
    lib.TLPMX_getMeasurementSequence(deviceHandle, baseTime, timeStamps, data, None)


    #Plot the results
    plt.figure()
    plt.plot(timeStamps, data)
    plt.title("Scope Measurement with Hardware Trigger")
    plt.xlabel("Time (ms)")
    plt.ylabel("Current (A)")
    plt.grid(True)
    plt.show()

    
    lib.TLPMX_close(deviceHandle)
    print('End program')

if __name__ == "__main__":
    main()
