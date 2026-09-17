"""
Example Thorlabs Power Meter Write Read Raw
Example Date of Creation                            2026-08-24
Example Date of Last Modification on Github         2026-08-24
Version of Python                                   3.13
Version of the Thorlabs SDK used: Thorlabs Optical Parameter Monitor Version 7.0
==================
This examples shows how to send SCPI commands when using the TLPMX dll. 
The example sends the *IDN? command to the device and reads the response.
"""

from ctypes import cdll,c_long, c_uint32,byref,create_string_buffer,c_char_p,c_int,c_int16, sizeof, c_voidp
import time

def main():

    #load dll
    if sizeof(c_voidp) == 4:
        dll_path = r"C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin\TLPMX_32.dll"
    else:
        dll_path = r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll"

    lib = cdll.LoadLibrary(dll_path)

    #find devices
    deviceCount = c_long(0)
    deviceHandle = c_long(0)
    lib.TLPMX_findRsrc(deviceHandle, byref(deviceCount))
    print("devices found: " + str(deviceCount.value))

    resourceName = create_string_buffer(1024)
    lib.TLPMX_getRsrcName(deviceHandle, c_int(0), resourceName)

    #initialize device
    lib.TLPMX_init(resourceName, c_int16(1), c_int16(0), byref(deviceHandle))

    time.sleep(1) 

    #send *IDN? command and read response
    lib.TLPMX_writeRaw(deviceHandle, c_char_p("*IDN?".encode('utf-8')))
    response = create_string_buffer(1024)
    retCount = c_uint32()
    lib.TLPMX_readRaw(deviceHandle, response, 1024, byref(retCount))
    print("Response from *IDN? command: " + str(c_char_p(response.raw).value))

    #close device
    lib.TLPMX_close(deviceHandle)
    print('End program')

if __name__ == "__main__":
    main()