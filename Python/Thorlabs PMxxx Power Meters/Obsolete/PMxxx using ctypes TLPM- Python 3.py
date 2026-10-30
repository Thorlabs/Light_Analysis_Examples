from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from TLPM import TLPM
import time


# Find connected power meter devices.
tlPM = TLPM()
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
tlPM = TLPM()
tlPM.open(resourceName, c_bool(True), c_bool(True))

message = create_string_buffer(1024)
tlPM.getCalibrationMsg(message)
print("Connected to device", i)
print("Last calibration date: ",c_char_p(message.raw).value)
print("")

time.sleep(2)

# Set wavelength in nm.
wavelength = c_double(532.5)
tlPM.setWavelength(wavelength)

# Enable auto-range mode.
# 0 -> auto-range disabled
# 1 -> auto-range enabled
tlPM.setPowerAutoRange(c_int16(1))

# Set power unit to Watt.
# 0 -> Watt
# 1 -> dBm
tlPM.setPowerUnit(c_int16(0))

# Take power measurements and save results to arrays.
power_measurements = []
times = []
count = 0
while count < 5:
    power =  c_double()
    tlPM.measPower(byref(power))
    power_measurements.append(power.value)
    times.append(datetime.now())
    print(times[count], ":", power_measurements[count], "W")
    count+=1
    time.sleep(1)
print("")

# Close power meter connection.
tlPM.close()
print('End program')