"""
Example Title: PMxxx using ctypes - Python 3.py
Example Date of Creation(YYYY-MM-DD): 2023-02-07
Example Date of Last Modification on Github: 2023-02-07
Version of Python used for Testing and IDE: 3.10.0
Version of the Thorlabs SDK used: Thorlabs Optical Power Meter Version 6.0
==================
Example Description: It connects to the power meter, makes the necessary settings and then reads and displays power values.
"""

from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from TLPMX import TLPMX
import time

from TLPMX import TLPM_DEFAULT_CHANNEL

# Find connected power meter devices.
tlPM = TLPMX()
deviceCount = c_uint32()
tlPM.findRsrc(byref(deviceCount))

print("Number of found devices: " + str(deviceCount.value))
print("")

resourceName = create_string_buffer(1024)

for i in range(0, deviceCount.value):
    tlPM.getRsrcName(c_int(i), resourceName)
    print("Resource name of device", i, ":", c_char_p(resourceName.raw).value)
print("")
tlPM.close()

# Connect to last device.
tlPM = TLPMX()
tlPM.open(resourceName, c_bool(True), c_bool(True))

message = create_string_buffer(1024)
tlPM.getCalibrationMsg(message,TLPM_DEFAULT_CHANNEL)
print("Connected to device", i)
print("Last calibration date: ",c_char_p(message.raw).value)
print("")

time.sleep(2)

# Set wavelength in nm.
wavelength = c_double(532.5)
tlPM.setWavelength(wavelength,TLPM_DEFAULT_CHANNEL)

# Enable auto-range mode.
# 0 -> auto-range disabled
# 1 -> auto-range enabled
tlPM.setPowerAutoRange(c_int16(1),TLPM_DEFAULT_CHANNEL)

# Set power unit to Watt.
# 0 -> Watt
# 1 -> dBm
tlPM.setPowerUnit(c_int16(0),TLPM_DEFAULT_CHANNEL)

# Take power measurements and save results to arrays.
power_measurements = []
times = []
count = 0
while count < 5:
    power =  c_double()
    tlPM.measPower(byref(power),TLPM_DEFAULT_CHANNEL)
    power_measurements.append(power.value)
    times.append(datetime.now())
    print(times[count], ":", power_measurements[count], "W")
    count+=1
    time.sleep(1)
print("")

# Close power meter connection.
tlPM.close()
print('End program')
