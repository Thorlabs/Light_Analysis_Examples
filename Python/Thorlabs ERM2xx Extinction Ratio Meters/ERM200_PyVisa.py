"""
ERM200_SCPI
Example Date of Creation: 2025-08-25
Example Date of Last Modification on Github: 2025-08-25
Version of Python: 3.13
Version of the Thorlabs SDK used: -
Tested with ERM210
==================
Example Description: The example shows how to use SCPI commands in Python with pyvisa
"""

import pyvisa
import time

def main():
    rm = None
    device = None
    try:
        #Opens a resource manager
        rm = pyvisa.ResourceManager()
        

        #Opens the connection to the device. The variable instr is the handle for the device.
        # !!! In the USB number the serial number (M01...) and PID (0x8032) needs to be changed to the one of the connected device.
        #Check with the Windows DEvice Manager
        instr = rm.open_resource('USB0::0x1313::0x8032::M01099532::INSTR')


        #print the device information
        print(instr.query("*IDN?"))
        
        result = instr.query("MEAS?")
        er, phi = result.split(",")
        print("Measured ER: ", er)
        print("Measured Phi: ", phi)

    finally:
        #Close device in any case
        if device is not None:
            try:
                device.close()
            except Exception:
                pass

        #Close resource manager in any case
        if rm is not None:
            try:
                instr.close()
            except Exception:
                pass

        #close out session
        rm.close()

    
    import sys
    print(sys.version)

if __name__ == "__main__":
    main()