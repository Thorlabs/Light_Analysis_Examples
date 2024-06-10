# -*- coding: utf-8 -*-
"""
Example of C Libraries for CCS Spectrometers in Python with CTypes

The example uses the driver file TLCCS_32/64.dll. A documentation of the functions in these files can be found here:

C:\Program Files\IVI Foundation\VISA\Win64\TLCCS\Manual

"""

import os
import time
import matplotlib.pyplot as plt
import math
from ctypes import *

#os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")
lib = cdll.LoadLibrary("TLCCS_64.dll")

#For the initialization the resource name needs to be changed to the name of the connected device.
#The resource name has this format: USB0::0x1313::<product ID>::<serial number>::RAW
#
#Product IDs are:
# 0x8081   // CCS100 Compact Spectrometer
# 0x8083   // CCS125 Special Spectrometer 
# 0x8085   // CCS150 UV Spectrometer 
# 0x8087   // CCS175 NIR Spectrometer 
# 0x8089   // CCS200 UV-NIR Spectrometer
#
#The serial number is printed on the CCS spectrometer.
#
#E.g.: "USB0::0x1313::0x8089::M00428858::RAW" for a CCS200 with serial number M00428858

ccs_handle=c_int(0)
lib.tlccs_init(b"USB0::0x1313::0x8089::M00428858::RAW", 1, 1, byref(ccs_handle))   

#Ask the user to enter the integration time.
integration_time=c_double(0)
try:
    #For convenience the integration time is entered here in ms.
    #But please note that tlccs_setIntegrationTime has seconds as input, hence the factor of 0.001.
    integration_time = c_double(0.001 * float(input("Please enter the integration time of the spectrometer in ms (allowed range is 0.01 - 60000 ms): ")))
    if  integration_time.value < 1e-5:
        print("Entered integration time is too small. Integration time will be set to 0.01 ms.")
        integration_time = c_double(1e-5)     
    elif integration_time.value > 6e1:
        print("Entered integration time is too high. Integration time will be set to 60000 ms.")
        integration_time = c_double(6e1)
except:
    print("Error: Incorrect input. Please do not use letters, only use numbers.")
    print("Code will be stopped.")
    exit()

#Set integration time in  seconds, ranging from 1e-5 to 6e1
lib.tlccs_setIntegrationTime(ccs_handle, integration_time)

#Reference measurement
input("Press ENTER to start measurement of reference spectrum.")
lib.tlccs_startScan(ccs_handle)
data_array_ref=(c_double*3648)()
status = c_int(0)

while (status.value & 0x0010) == 0:
    lib.tlccs_getDeviceStatus(ccs_handle, byref(status))

lib.tlccs_getScanData(ccs_handle, byref(data_array_ref))
print("Reference spectrum recorded.")
print()

#Measurement with sample
input("Press ENTER to start measurement of spectrum with sample.")
lib.tlccs_startScan(ccs_handle)
data_array_sample=(c_double*3648)()
status = c_int(0)

while (status.value & 0x0010) == 0:
    lib.tlccs_getDeviceStatus(ccs_handle, byref(status))

lib.tlccs_getScanData(ccs_handle, byref(data_array_sample))
print("Spectrum with sample recorded.")
print()

#Get the wavelength array.
#
#Each cell in the wavelength array corresponds to a cell in the data arrays.
#E.g. wavelength[5] is the wavelength for the scan data in data_array_sample[5]
wavelengths=(c_double*3648)()
lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))

#Calculate the absorption and optical density of the sample.
#
#Formulas:
# Absorption[%] = ((Reference Spectrum - Sample Spectrum) / Reference Spectrum) * 100
# Optical density = - log_10 (Transmission) =~ - log_10 (1- Absorption)
#
#try and except is necessary to prevent errors due to impossible mathematical operations.
data_array_absorption=(c_double*3648)()
data_array_OD=(c_double*3648)()
for i in range(3648):
    try:
        data_array_absorption[i] = ((data_array_ref[i] - data_array_sample[i])/data_array_ref[i])*100
        data_array_OD[i] = - math.log10(1 - (data_array_absorption[i]/100))
    except:
        data_array_absorption[i] = 0
        data_array_OD[i] = 0

#Create plots of the spectra. Matplotlib is used to create the plots.
#See this website for further information: https://matplotlib.org/stable/index.html#        
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig.subplots_adjust(hspace=2)

ax1.set_title('Reference Spectrum')
ax1.plot(wavelengths, data_array_ref)
ax1.set_xlabel('Wavelength [nm]')
ax1.set_ylabel('Intensity [a.u.]')
ax1.set_ylim(-0.1, 1.1)
ax1.grid(True)

ax2.set_title('Spectrum with sample')
ax2.plot(wavelengths, data_array_sample)
ax2.set_xlabel('Wavelength [nm]')
ax2.set_ylabel('Intensity [a.u.]')
ax2.set_ylim(-0.1, 1.1)
ax2.grid(True)

ax3.set_title('Absorption')
ax3.plot(wavelengths, data_array_absorption)
ax3.set_xlabel('Wavelength [nm]')
ax3.set_ylabel('Absorption [%]')
ax3.set_ylim(-10, 110)
ax3.grid(True)

ax4.set_title('Optical density')
ax4.plot(wavelengths, data_array_OD)
ax4.set_xlabel('Wavelength [nm]')
ax4.set_ylabel('Optical density')
ax4.grid(True)


fig.suptitle('Absorption Measurement')

plt.show()

#Closing the connection to the spectrometer.
lib.tlccs_close (ccs_handle)
