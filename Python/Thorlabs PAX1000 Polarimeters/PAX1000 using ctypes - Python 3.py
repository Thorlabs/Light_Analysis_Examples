"""
Example Title: PAX1000 using ctypes - Python 3.py
Example Date of Creation(YYYY-MM-DD): 2022-08-25
Example Date of Last Modification on Github: 2022-08-25
Version of Python used for Testing and IDE: 3.10.0
Version of the Thorlabs SDK used: PAX1000 Software Version 1.2
==================
Example Description: This example shows how to scan the available PAX1000, connect the PAX1000, make necessary settings 
and get the azimuth and ellipticity value. 
"""

import os
import time
import ctypes
from ctypes import *

# Load DLL library
lib = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPAX_64.dll")

# Detect and initialize PAX1000 device
instrumentHandle = c_ulong()
IDQuery = True
resetDevice = False
resource = c_char_p(b"")
deviceCount = c_int()

# Check how many PAX1000 are connected
lib.TLPAX_findRsrc(instrumentHandle, byref(deviceCount))
if deviceCount.value < 1 :
    print("No PAX1000 device found.")
    exit()
else:
    print(deviceCount.value, "PAX1000 device(s) found.")
    print("")

# Connect to the first available PAX1000
lib.TLPAX_getRsrcName(instrumentHandle, 0, resource)
if (0 == lib.TLPAX_init(resource.value, IDQuery, resetDevice, byref(instrumentHandle))):
    print("Connection to first PAX1000 initialized.")
else:
    print("Error with initialization.")
    exit()
print("")

# Short break to make sure the device is correctly initialized
time.sleep(2)

# Make settings
lib.TLPAX_setMeasurementMode(instrumentHandle, 9)
lib.TLPAX_setWavelength(instrumentHandle, c_double(633e-9))
lib.TLPAX_setBasicScanRate(instrumentHandle, c_double(60))

# Check settings
wavelength = c_double()
lib.TLPAX_getWavelength(instrumentHandle, byref(wavelength))
print("Set wavelength [nm]: ", wavelength.value*1e9)
mode = c_int()
lib.TLPAX_getMeasurementMode(instrumentHandle, byref(mode))
print("Set mode: ", mode.value)
scanrate = c_double()
lib.TLPAX_getBasicScanRate(instrumentHandle, byref(scanrate))
print("Set scanrate: ", scanrate.value)
print("")

# Short break
time.sleep(5)

# Take 5 measurements and output values
for x in range (5):
    revolutionCounter = c_int()
    scanID = c_int()
    lib.TLPAX_getLatestScan(instrumentHandle, byref(scanID))

    print("Measurement", (x+1))
    azimuth = c_double()
    ellipticity = c_double()
    lib.TLPAX_getPolarization(instrumentHandle, scanID.value, byref(azimuth), byref(ellipticity))
    print("Azimuth [rad]: ", azimuth.value)
    print("Ellipticity [rad]: ", ellipticity.value)
    print("")

    lib.TLPAX_releaseScan(instrumentHandle, scanID)
    time.sleep(0.5)

# Close
lib.TLPAX_close(instrumentHandle)
print("Connection to PAX1000 closed.")
