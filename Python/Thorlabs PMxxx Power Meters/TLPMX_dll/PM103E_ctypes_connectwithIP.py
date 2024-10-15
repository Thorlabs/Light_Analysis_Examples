# Title: PM103E_ctypes_connectwithIP.py
# Created Date: 2024-10-15
# Last modified date: 2024-10-15
# Python Version: 3.11
# Thorlabs DLL version: Optical Power Monitor 6.2
# Uses the Thorlabs TLPMX_64.dll in order to communicate with the power meters and shows how to connect PM103E using the IP of the powermeter

from ctypes import *

# load the DLL- if your path is different, this may need to change.
lib = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll")

def main():
    sessionHandle = c_ulong(0)
    err=lib.TLPMX_init(b'TCPIP0::10.10.4.221::2000::SOCKET', 1, 0, byref(sessionHandle)) # change to IP of your PM103E
    if err!=0:
        message=create_string_buffer(256)
        lib.TLPMX_errorMessage(0,err,message)
        print(message.value) 
    else:
        print("device connected")

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