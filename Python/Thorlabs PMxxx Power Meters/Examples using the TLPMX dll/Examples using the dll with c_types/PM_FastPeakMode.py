"""
Example Thorlabs Power Meter Fast Measurement Mode
Example Date of Creation:                            2026-08-24
Example Date of Last Modification on Github:         2026-08-24
Version of Python:                                   3.13
Version of the Thorlabs SDK used: Thorlabs Optical Parameter Monitor Version 7.0
==================
For pulse repetition rates faster than 1 kHz, fast measurement mode can be used to acquire peak power values. 
The device is configured to acquire a specified number of peaks, and the acquired data is then written to a CSV file.
The fast mode is available for PM103x and PM5020.
"""
from ctypes import c_double, c_int16, cdll, c_long, c_uint32, byref, create_string_buffer, c_bool, c_int, c_float, sizeof, c_voidp
import time

TLPM_DEFAULT_CHANNEL = 1
TLPM_BUFFER_SIZE = 256

#load dll
if sizeof(c_voidp) == 4:
    dll_path = r"C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin\TLPMX_32.dll"
else:
    dll_path = r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll"

lib = cdll.LoadLibrary(dll_path)

#find devices
device_session = c_long(0)
deviceCount = c_uint32()
lib.TLPMX_findRsrc(device_session, byref(deviceCount))

print("devices found: " + str(deviceCount.value))

#connect to first powermeter
resource_name = create_string_buffer(TLPM_BUFFER_SIZE)
lib.TLPMX_getRsrcName(device_session, c_uint32(0), resource_name)
res=lib.TLPMX_init(resource_name, c_bool(True), c_bool(False), byref(device_session))
if res==0: 
    print("Connected  " )
time.sleep(1)

#general settings
lib.TLPMX_setWavelength(device_session, c_float(500), TLPM_DEFAULT_CHANNEL)
lib.TLPMX_setPowerRange(device_session, c_double(0.05), TLPM_DEFAULT_CHANNEL)
powerRange = c_double()
lib.TLPMX_getPowerRange(device_session, c_int16(0), byref(powerRange), TLPM_DEFAULT_CHANNEL)
print("Power range: " + str(powerRange.value))

#configure device for fast measurement
lib.TLPMX_confPowerFastArrayMeasurement(device_session, TLPM_DEFAULT_CHANNEL)
lib.TLPMX_setFreqMode(device_session, c_int(1), TLPM_DEFAULT_CHANNEL) #Set to peak mode

#configure device for peak measurement
lib.TLPMX_setPeakThreshold(device_session, c_double(10), TLPM_DEFAULT_CHANNEL)#percentage of the power range, 10% of 0.05W = 0.005W
lib.TLPMX_setPeakFilter(device_session, c_int(1), TLPM_DEFAULT_CHANNEL)#	Valid valus for this parameter are 0 = NONE, 1 = OVER
#Use OVER if the signal measured is a rectangular signal.
#If it is a sinus or triangle signal use NONE.


dataSize = 40 # number of peaks expected in 1 ms
timeStamps = (c_uint32 * dataSize)()
data = (c_float * dataSize)() 

numberOfPeaks = c_uint32(100)#totalnumber of peaks you want to measure
returnSize = c_uint32(0)#number of peaks in one array measurement, this value is returned by the function TLPMX_getNextFastArrayMeasurementRelativeTime
timestampsresult = []
dataresult=[]

lib.TLPMX_resetFastArrayMeasurement(device_session, TLPM_DEFAULT_CHANNEL)
#start measurement
while len(dataresult) < numberOfPeaks.value:
    lib.TLPMX_getNextFastArrayMeasurementRelativeTime(
        device_session, byref(returnSize), timeStamps, data, TLPM_DEFAULT_CHANNEL)
    #print(f"Acquired {returnSize.value} samples")

    timestampsresult.extend(timeStamps[:returnSize.value])
    dataresult.extend(data[:returnSize.value])

#write data to csv file
with open("PowerPeaksData.csv", "w") as txt_file:
    txt_file.write("TimeStamp [us],Power\n")
    for timestamp, measurement in zip(timestampsresult, dataresult):
        txt_file.write(str(timestamp) + "," + "{:.5e}".format(measurement) + "\n")
 
#close device
lib.TLPMX_close(device_session)
print('End program')
