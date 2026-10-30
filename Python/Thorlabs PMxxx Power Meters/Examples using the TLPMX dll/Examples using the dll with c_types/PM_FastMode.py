"""
Example Thorlabs Power Meter Fast Measurement Mode
Example Date of Creation                            2026-08-24
Example Date of Last Modification on Github         2026-08-24
Version of Python                                   3.13
Version of the Thorlabs SDK used: Thorlabs Optical Parameter Monitor Version 7.0
==================
This examples shows how to access the Power Meter Fast Measurement data stream. 
For this example it is important to query the meter as fast as possible to reduce data loss propability.
The meter enqueues every millisecond 100 or 200 results and the fixed size queue length is limited to recent 10 ms of samples. 
The examplle acquires 5 ms of data and writes it to a csv file.
Only for PM103x and PM5020
"""
from ctypes import cdll, c_long, c_uint32, byref, create_string_buffer, c_bool,  c_float, sizeof, c_voidp
import time

TLPM_DEFAULT_CHANNEL = 1
TLPM_BUFFER_SIZE = 256

#load dll
if sizeof(c_voidp) == 4:
    dll_path = r"C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin\TLPMX_32.dll"
else:
    dll_path = r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll"

lib = cdll.LoadLibrary(dll_path)

def main():
    #find devices
    device_session = c_long(0)
    deviceCount = c_uint32()
    lib.TLPMX_findRsrc(device_session, byref(deviceCount))

    print("devices found: " + str(deviceCount.value))

    resource_name = create_string_buffer(TLPM_BUFFER_SIZE)

    lib.TLPMX_getRsrcName(device_session, c_uint32(0), resource_name)

    #connect to first powermeter
    lib.TLPMX_init(resource_name, c_bool(True), c_bool(False), byref(device_session))
    time.sleep(1)
    lib.TLPMX_setWavelength(device_session, c_float(500), TLPM_DEFAULT_CHANNEL)

    #configure device for fast measurement
    lib.TLPMX_resetFastArrayMeasurement(device_session, TLPM_DEFAULT_CHANNEL)
    lib.TLPMX_confPowerFastArrayMeasurement(device_session, TLPM_DEFAULT_CHANNEL)
 
    dataSize = 200 #Every millisecond the PM103 adds a list of up to 100 tuples (time, measurement) to the queue as a non-dividable package.
    timeStamps = (c_uint32 * dataSize)()
    data = (c_float * dataSize)() 

    returnSize = c_uint32(0)
    timestampsresult = [0]
    dataresult=[0]
    acquisitiontime = 5000 #in microseconds

    #aquire values
    while timestampsresult[-1]< acquisitiontime-10:
        #data will be acquired in packages of 100 or 200 samples, depending on the device. They can also have 0 samples if the queue is empty. 
        lib.TLPMX_getNextFastArrayMeasurementRelativeTime(
            device_session, byref(returnSize), timeStamps, data, TLPM_DEFAULT_CHANNEL)
        #print(f"Acquired {returnSize.value} samples")
        timestampsresult.extend(timeStamps[:returnSize.value])
        dataresult.extend(data[:returnSize.value])

    #write data to csv file
    with open("powerData.csv", "w") as txt_file:
        txt_file.write("TimeStamp [us],Power\n")
        for timestamp, measurement in zip(timestampsresult, dataresult):
            txt_file.write(str(timestamp) + "," + "{:.5e}".format(measurement) + "\n")
    print("Data written to powerData.csv")
 
    #close device
    lib.TLPMX_close(device_session)
    print('End program')

if __name__ == "__main__":
    main()