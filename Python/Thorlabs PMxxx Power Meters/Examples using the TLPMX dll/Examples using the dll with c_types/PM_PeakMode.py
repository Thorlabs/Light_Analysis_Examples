"""
Example Thorlabs Power Meter Peak Mode
Example Date of Creation:                            2026-08-24
Example Date of Last Modification on Github:         2026-08-24
Version of Python:                                   3.13
Version of the Thorlabs SDK used: Thorlabs Optical Parameter Monitor Version 7.0
==================
For pulse repetition rates well below 1 kHz, slow peak measurement mode can be used to acquire peak power values. 
The device is configured to acquire a specified number of peaks, and the acquired data is then written to the output.
The peak mode is available for PM100D2, PM100D3, PM103x and PM5020.
"""

#from datetime import datetime
from ctypes import c_char_p, c_uint16, cdll,c_long, c_uint32,byref,create_string_buffer,c_bool,c_int16,c_double, sizeof, c_voidp
import sys
import time
	
TLPM_DEFAULT_CHANNEL = 1
TLPM_BUFFER_SIZE = 256

def main():
	#load dll
	if sizeof(c_voidp) == 4:
		dll_path = r"C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin\TLPMX_32.dll"
	else:
		dll_path = r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll"
	lib = cdll.LoadLibrary(dll_path)

	#find devices
	deviceHandle = c_long(0)
	deviceCount = c_uint32()
	lib.TLPMX_findRsrc(deviceHandle, byref(deviceCount))
	print("devices found: " + str(deviceCount.value))
	resource_name = create_string_buffer(TLPM_BUFFER_SIZE)
	lib.TLPMX_getRsrcName(deviceHandle, c_uint32(0), resource_name)

	#Connect to first powermeter
	res=lib.TLPMX_init(resource_name, c_bool(True), c_bool(False), byref(deviceHandle))
	if res==0: 
		print(resource_name.value ," connected  " )
	else:
		print("Error connecting to device")
		sys.exit(1)
			
	time.sleep(1)

	#use the peak detector to find the range and trigger level.
	lib.TLPMX_setFreqMode(deviceHandle, c_uint16(1), c_uint16(TLPM_DEFAULT_CHANNEL))
	lib.TLPMX_startPeakDetector(deviceHandle, TLPM_DEFAULT_CHANNEL)
	isRunning = c_bool(True)
	while isRunning.value:
		time.sleep(1)
		lib.TLPMX_isPeakDetectorRunning(deviceHandle, byref(isRunning), TLPM_DEFAULT_CHANNEL)
	powerrange = c_double()
	lib.TLPMX_getPowerRange(deviceHandle, c_int16(0), byref(powerrange), TLPM_DEFAULT_CHANNEL)
	print("Power range: " + str(powerrange.value))
	threshold = c_double()
	lib.TLPMX_getPeakThreshold(deviceHandle, c_int16(0), byref(threshold), TLPM_DEFAULT_CHANNEL)#peak detection threshold in percent of range
	print("Trigger level: " + str(threshold.value)+" % of range") 
	#Instead of using the peak detector, range and threshold can also be set manually using the following commands:TLPMX_setPowerRange(),TLPMX_setPeakThreshold

	#Acquire 10 peaks and read the values. The device will wait for a trigger event, and then acquire the specified number of peaks.
	#SCPI commands are used instead of TLPMX_measCurrent() to avoid a timeout error if no peak is detected. 
	# This way it is possible to check if a measurement is available before reading the value.
	count = 0
	response = create_string_buffer(256)
	regValue = c_int16()
	retValue = c_uint32()
	while count < 10: 
		lib.TLPMX_writeRaw(deviceHandle, c_char_p("ABORT".encode('utf-8')))
		lib.TLPMX_writeRaw(deviceHandle, c_char_p("CONF:CURR".encode('utf-8')))
		lib.TLPMX_writeRaw(deviceHandle, c_char_p("INIT".encode('utf-8')))
		#Check if measurement is available with register value. This avoids a timeout error if no peak is detected. 
		#After a timeout the device will cancel the measurement after 10 seconds. Any incoming command in this time will interrupt USB connection.
		waiting=1
		while waiting==1:
			lib.TLPMX_readRegister(deviceHandle, c_uint16(4), byref(regValue))
			if (regValue.value & 512) != 0:
				waiting=0
				lib.TLPMX_writeRaw(deviceHandle, c_char_p("FETC?".encode('utf-8')))

		lib.TLPMX_readRaw(deviceHandle, response, c_uint32(256), byref(retValue))#read the measurement value
		print(c_char_p(response.raw).value.decode('utf-8'))
		count+=1

	lib.TLPMX_setFreqMode(deviceHandle, c_uint16(0), TLPM_DEFAULT_CHANNEL)

	lib.TLPMX_close(deviceHandle)
	print('End program')

if __name__ == "__main__":
	main()