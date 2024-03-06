"""
PMxxx_SCPI
Example Date of Creation: 2023-10-09
Example Date of Last Modification on Github: 2023-10-09
Version of Python: 3.11
Version of the Thorlabs SDK used: -
==================
Example Description: The example shows how to use SCPI commands in Python
"""

#Import the PyVISA and time library to Python.
import pyvisa
import time

def main():

    #Opens a resource manager
    rm = pyvisa.ResourceManager()

    #Opens the connection to the device. The variable instr is the handle for the device.
    # !!! In the USB number the serial number (P00...) and PID (0x8078) needs to be changed to the one of the connected device.
    #Check with the Windows DEvice Manager
    instr = rm.open_resource('USB0::0x1313::0x8078::P0007837::INSTR')
    #turn on auto-ranging
    instr.write("SENS:RANGE:AUTO ON")
    #set wavelength setting, so the correct calibration point is used
    instr.write("SENS:CORR:WAV 1310")
    #set units to Watts
    instr.write("SENS:POW:UNIT W")
    #set averaging to 1000 points
    instr.write("SENS:AVER:1000")

    #read the power
    print (instr.query("MEAS:POW?"))


    print(instr.query("SYST:SENS:IDN?"))

    #close out session
    rm.close()

if __name__ == "__main__":
    main()
