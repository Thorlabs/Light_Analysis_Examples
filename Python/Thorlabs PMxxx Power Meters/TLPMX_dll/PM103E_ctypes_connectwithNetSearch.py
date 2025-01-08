# Title: PM103E_ctypes_connectwithNetSearch.py
# Created Date: 2024-10-15
# Last modified date: 2024-10-15
# Python Version: 3.11
# Thorlabs DLL version: Optical Power Monitor 6.2
# Uses the Thorlabs TLPMX_64.dll in order to communicate with the power meters and shows how to find the PM103E setting a network mask

from ctypes import *

# load the DLL- if your path is different, this may need to change.
lib = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll")

def main():
    # Make settings for ethernet
    lib.TLPMX_setEnableNetSearch (0, 1)
    err=lib.TLPMX_setNetSearchMask(0,b'10.10.5.57 / 255.255.240.0') #choose apprpriate net mask
    if err!=0:
        message=create_string_buffer(256)
        lib.TLPMX_errorMessage(0,err,message)
        print(message.value) 

    # find out if there are devices connected
    deviceCount = c_ulong()
    lib.TLPMX_findRsrc(0, byref(deviceCount))

    # if there are devices connected, get name of the first device
    if deviceCount.value >= 1:
        meterName = create_string_buffer(256)
        lib.TLPMX_getRsrcName(0, 0, meterName)
        print( meterName.value)

        # Initialize the device
        sessionHandle = c_ulong(0)
        res=lib.TLPMX_init(meterName, 1, 0, byref(sessionHandle))
        if res== 0: print("device connected") 
    else:
        print("No connected power meters were detected. Check connections and installed drivers.")

    # Set Wavelength (given in nm)
    lib.TLPMX_setWavelength(sessionHandle, c_double(1064.0), 1);
    # Set Averaging count
    lib.TLPMX_setAvgCnt(sessionHandle, c_ushort(1000), 1)
    # Set Unit- below sets to Watts
    lib.TLPMX_setPowerUnit(sessionHandle, 0, 1)
    # Measure Power
    power = c_longdouble()
    lib.TLPMX_measPower(sessionHandle, byref(power), 1)
    print('Power: ' + str(power.value) + " W")

    # close
    lib.TLPMX_close(sessionHandle)

if __name__ == "__main__":  
    main()