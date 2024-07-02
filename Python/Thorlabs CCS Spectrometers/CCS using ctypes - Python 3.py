# -*- coding: utf-8 -*-
"""
Example of C Libraries for CCS Spectrometers in Python with CTypes

"""
import os
import time
import matplotlib.pyplot as plt
from ctypes import *

os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")
lib = cdll.LoadLibrary("TLCCS_64.dll")

ccs_handle=c_int(0)

#documentation: C:\Program Files\IVI Foundation\VISA\Win64\TLCCS\Manual

#Start Scan- Resource name will need to be adjusted
#windows device manager -> NI-VISA USB Device -> Spectrometer -> Properties -> Details -> Device Instance ID
lib.tlccs_init(b"USB0::0x1313::0x8089::M00245773::RAW", 1, 1, byref(ccs_handle))   

#set integration time in  seconds, ranging from 1e-5 to 6e1
integration_time=c_double(10.0e-3)
lib.tlccs_setIntegrationTime(ccs_handle, integration_time)


#start scan
lib.tlccs_startScan(ccs_handle)

wavelengths=(c_double*3648)()

lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))

#retrieve data
data_array=(c_double*3648)()
lib.tlccs_getScanData(ccs_handle, byref(data_array))

#plot data
plt.plot(wavelengths, data_array)
plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity [a.u.]")
plt.grid(True)
plt.show()

#close
lib.tlccs_close (ccs_handle)


