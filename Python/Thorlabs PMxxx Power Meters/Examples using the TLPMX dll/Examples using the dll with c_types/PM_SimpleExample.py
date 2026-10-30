"""
Example Title: PMxxx_ctypes
Example Date of Creation(YYYY-MM-DD): 2026-08-21
Example Date of Last Modification on Github: 2026-08-21
Python Version used for Testing: 3.13
Version of the Thorlabs SDK used: Thorlabs Optical Power Monitor Version 7.0
==================
Example Description: The example connects to the power meter, makes the wavelength setting and then reads and displays power value.
"""
from ctypes import * 

# load the DLL
lib = cdll.LoadLibrary(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll")

def main():
    # Get the number of connected powermeters
    deviceCount = c_uint32(0)
    lib.TLPMX_findRsrc(0,byref(deviceCount))
    print("Number of connected powermeters: " , str(deviceCount.value))

    # If at least one device is found, get the resource name of the first device and initialize it
    if deviceCount.value >= 1:
        resourceName = create_string_buffer(256)
        lib.TLPMX_getRsrcName(0, 0, resourceName)
        print("First powermeter found: " , resourceName.value.decode())

        # Initialize the device
        pmHandle = c_ulong(0)
        err=lib.TLPMX_init(resourceName, 1, 0, byref(pmHandle))
        # Check if initialization was successful
        if err== 0:
            print("device connected") 
        else: #if initialization fails, print the error message
            message=create_string_buffer(256)
            lib.TLPMX_errorMessage(0,err,message)
            print(message.value)

        # Set the wavelength to 532 nm
        lib.TLPMX_setWavelength(pmHandle, c_longdouble(532.0), 1)
  
        # Read the power
        power = c_longdouble(0)
        lib.TLPMX_measPower(pmHandle,byref(power),1)
        print("Power reading: " , str(power.value) )

        lib.TLPMX_close(pmHandle)


    else:
        print("No connected power meters were detected. Check connections and installed drivers.")



if __name__ == "__main__":
    main()
