"""
Example Thorlabs Power Meter Scope Mode with SW Trigger
Example Date of Creation                            2026-08-24
Example Date of Last Modification on Github         2026-08-24
Version of Python                                   3.13
==================
This examples shows how to use the scope mode with software trigger.
The Scope Mode provides an oscilloscope-like measurement method. 
It is designed to provide a highly resolved snapshot of a signal.
With software trigger, acquisition starts immediately, regardless of hardware trigger or incoming pulses.
The scope mode is configured to acquire 100 ms of data at a sample rate of 100 kHz. Data is shown in a plot. 
Only for PM103x, PM100D3 and PM5020
"""

from ctypes import byref, c_char_p, c_float, c_int, c_int16, c_long, c_uint16, c_uint32, cdll, create_string_buffer,sizeof,c_voidp
import time
import matplotlib.pyplot as plt

TLPM_DEFAULT_CHANNEL = 1

#load dll
if sizeof(c_voidp) == 4:
    dll_path = r"C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin\TLPMX_32.dll"
else:
    dll_path = r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll"

lib = cdll.LoadLibrary(dll_path)

deviceHandle = c_long(0)
deviceCount = c_uint32()
lib.TLPMX_findRsrc(deviceHandle, byref(deviceCount))

print("devices found: " + str(deviceCount.value))

resourceName = create_string_buffer(1024)

for i in range(0, deviceCount.value):
	lib.TLPMX_getRsrcName(deviceHandle, c_uint32(i), resourceName)
	print(c_char_p(resourceName.raw).value)
	break

lib.TLPMX_close(deviceHandle)

#Connect to first powermeter
lib.TLPMX_init(resourceName, c_int16(1), c_int16(0), byref(deviceHandle))

#Set to CW mode 
lib.TLPMX_setFreqMode(deviceHandle, c_uint16(0), c_uint16(TLPM_DEFAULT_CHANNEL))

#For pulsed signals, autorange does not work. Instead, the Peak Detector can be used. 
#Alternatively the range can be set manually.
lib.TLPMX_setCurrentAutoRange(deviceHandle, c_int16(0), c_uint16(TLPM_DEFAULT_CHANNEL))
lib.TLPMX_setInputFilterState(deviceHandle, c_int16(0), c_uint16(TLPM_DEFAULT_CHANNEL))# set to high bandwidth
lib.TLPMX_setFreqMode(deviceHandle, c_uint16(1), c_uint16(TLPM_DEFAULT_CHANNEL))#set to peak mode
#Start autoset
lib.TLPMX_startPeakDetector(deviceHandle, c_uint16(TLPM_DEFAULT_CHANNEL))
isRunning = c_int16(1)
while isRunning.value:
      lib.TLPMX_isPeakDetectorRunning(deviceHandle, byref(isRunning), c_uint16(TLPM_DEFAULT_CHANNEL))
      time.sleep(1)
lib.TLPMX_setFreqMode(deviceHandle, c_uint16(0), c_uint16(TLPM_DEFAULT_CHANNEL))
#End autoset

#Configure scope mode measurement
averaging = c_uint32(1) 
lib.TLPMX_confCurrentMeasurementSequence(deviceHandle, averaging, c_uint16(TLPM_DEFAULT_CHANNEL))

#Start measurement 
triggerForced = c_int16()
autoTriggerDelay = c_uint16(0)
lib.TLPMX_startMeasurementSequence(deviceHandle, c_uint32(autoTriggerDelay.value), byref(triggerForced))
# triggerForced is alway 0 in software trigger mode

#Get the measurement data
baseTime = c_int(10)
dataSize = baseTime.value * 100
timeStamps = (c_float * dataSize)()
currentData = (c_float * dataSize)()
lib.TLPMX_getMeasurementSequence(deviceHandle, c_uint32(baseTime.value), timeStamps, currentData, None)

#Plot the results
plt.figure()
plt.plot(timeStamps, currentData)
plt.title("Scope Measurement with Software Trigger")
plt.xlabel("Time (ms)")
plt.ylabel("Current (A)")
plt.grid(True)
plt.show()
 
lib.TLPMX_close(deviceHandle)
print('End program')
