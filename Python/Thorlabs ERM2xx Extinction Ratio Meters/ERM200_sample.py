import os
import time
from ctypes import * 

lib = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLERM200_64.dll")

#Find resources
erm_handle=c_int(0)
deviceCount=c_int()

lib.TLERM200_findRsrc(erm_handle, byref(deviceCount))
if deviceCount.value < 1 :
    print("No ERM200 device found.")
    exit()
else:
    print(deviceCount.value, "ERM200 device(s) found.")
    print("")

#Get device information
modelName=create_string_buffer(1024)
serialNumber=create_string_buffer(1024)
manufacturer=create_string_buffer(1024)
available=c_bool()
lib.TLERM200_getRsrcInfo(erm_handle,c_int(0),modelName, serialNumber, manufacturer,byref(available))
print(modelName.value.decode('utf_8'), serialNumber.value.decode('utf_8'),manufacturer.value.decode('utf_8'),"\n") 

# Connect to the first available ERM200
resource = c_char_p(b"")
IDQuery = True
resetDevice = False
lib.TLERM200_getRsrcName(erm_handle, 0, resource)
if (0 == lib.TLERM200_init(resource.value, IDQuery, resetDevice, byref(erm_handle))):
    print("Connection ERM200 initialized.")
else:
    print("Error with initialization.")
    exit()
print("")

# Short break to make sure the device is correctly initialized
time.sleep(2)

# Make settings
lib.TLERM200_setPowerUnit(erm_handle,0)#set power unit to Watt
lib.TLERM200_setWavelength(erm_handle,c_ushort(632))#set wavelength to 632 nm
wavelength=c_ushort(0)
lib.TLERM200_getWavelength(erm_handle,byref(wavelength))
print("Wavelength set to ",wavelength.value,"nm\n")

# Make measurement
ER=c_double()
phi=c_double()
lib.TLERM200_getMeasurement(erm_handle,byref(ER),byref(phi))
print("ER=",ER.value,"dB     \nphi=",phi.value,"°")
power=c_double()
lib.TLERM200_getPower(erm_handle,byref(power))
print("Power=",power.value,"W\n")

# Close connection
lib.TLERM200_close(erm_handle)
print("Connection closed")


