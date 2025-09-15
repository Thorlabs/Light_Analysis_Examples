"""
Thorlabs_VM_example_02
Example Date of Creation: 2025-08-22
Example Date of Last Modification on Github: 2025-08-22
Version of Python: 3.13.7
Version of the Thorlabs SDK used: OPM 6.5, TLWAVE_32.dll
Version of Platform Firmware: 0.9.12
Version of Interferometer Firmware: 0.58
==================
Example Description: Read the wavelength from Thorlabs WM20X Wavelength Meter using TLWAVE dll (USB/TCP)
"""
import time
from PyTLWAVE import TLWAVE

discover = True

wavemeter = None

if discover:
    # Here we try to find wavemeters using USB
    wavemetersession = TLWAVE()

    deviceCount = wavemetersession.findRsrc()
    print("devices found: " + str(deviceCount))

    resourceNames = []
    for i in range(deviceCount):
        localName = wavemetersession.getRsrcName(i)
        print(localName)
        resourceNames.append(localName)
    
    wavemetersession.close()

    wavemeter = TLWAVE(resourceNames[0])
else:
    # Here is an example of connecting to using ethernet to a specific ip
    wavemeter = TLWAVE(b"TCPIP0::192.168.55.6::2000::SOCKET", False)

def waitfornewdata():
    """Wait for new data flag (9th bit) in status register"""
    newdata = False
    newstatus = False
    while not newdata:
        wavemeter.writeRaw("STAT:OPER:COND?\n")
        value, numbytes = wavemeter.readRaw(1024)
        try:
            reg_value = int(value)
            if reg_value is not None:
                if (reg_value & 512) == 512:  # Checking the 9th bit
                    newdata = True
                if (reg_value & 1024) == 1024:  # Checking the 10th bit
                    newstatus = True
        except Exception as e:
            print(f"Error parsing response: {e}, got: '{value}'")
        
        if not newdata:
            time.sleep(0.1)
        if newstatus:
            wavemeter.writeRaw("SENS:STAT:COND?\n")
            rawValue, numbytes = wavemeter.readRaw(1024)
            statuscode = int(rawValue)
            print(f"New status: {statuscode}")
            newstatus = False



for i in range(1000):
    # Loop and print the wavelength continuously
    wavemeter.writeRaw("FETC:WAV?\n")
    rawValue, numbytes = wavemeter.readRaw(1024)
    wavelength = float(rawValue)
    print(f"{wavelength} nm(vac)")
    waitfornewdata()

wavemeter.close()

