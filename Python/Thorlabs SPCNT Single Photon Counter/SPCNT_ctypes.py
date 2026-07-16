"""
Example Title: SPCNT ctypes 
Example Date of Creation(YYYY-MM-DD): 2026-05-20
Example Date of Last Modification on Github: 2026-05-20
Version of Python used for Testing and IDE: 3.13
Version of the Thorlabs SDK used: OPM 7.0
==================
Example Description: This example shows how to scan the available SPCNT, connect the SPCNT, make necessary settings 
and get the frequency value. 
"""

from ctypes import *

# Load DLL library
lib = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLSPCNT_64.dll")

# Detect and initialize SPCNT device
instrumentHandle = c_ulong()
IDQuery = True
resetDevice = False
resource = c_char_p(b"")
deviceCount = c_int()

# Check how many SPCNT are connected
lib.TLSPCNT_findRsrc(instrumentHandle, byref(deviceCount))
if deviceCount.value < 1 :
    print("No SPCNT device found.")
    exit()
else:
    print(deviceCount.value, "SPCNT device(s) found.")
    print("")

# Connect to the first available SPCNT
lib.TLSPCNT_getRsrcName(instrumentHandle, 0, resource)
if (0 == lib.TLSPCNT_init(resource.value, IDQuery, resetDevice, byref(instrumentHandle))):
    print("Connection to", resource.value.decode(),"established.")
else:
    print("Error with initialization.")
    exit()
print("")

binWidth = c_uint32()
lib.TLSPCNT_setBinWidth(instrumentHandle, 20)  
lib.TLSPCNT_getBinWidth(instrumentHandle, byref(binWidth))
print("Bin width set to", binWidth.value, "ms.")    

lib.TLSPCNT_setDeadtime(instrumentHandle,  0)
deadTime = c_uint32()   
lib.TLSPCNT_getDeadtime(instrumentHandle, byref(deadTime))
print("Dead time set to", deadTime.value, "ms.")

#wait until frequency value is present 
registerValue = c_uint16()
lib.TLSPCNT_readRegister(instrumentHandle, 4, byref(registerValue))#Operation Condition Register
while (registerValue.value & 512) == 0:#register value 512 means "Frequency to fetch"
    lib.TLSPCNT_readRegister(instrumentHandle, 4, byref(registerValue))
    
frequency, minValue, maxValue, averageValue = c_double(), c_double(), c_double(), c_double()
lib.TLSPCNT_getFrequency(instrumentHandle, byref(frequency), byref(minValue), byref(maxValue), byref(averageValue))
print("Frequency:", frequency.value, "Hz")

lib.TLSPCNT_close(instrumentHandle)
print("Connection closed.")