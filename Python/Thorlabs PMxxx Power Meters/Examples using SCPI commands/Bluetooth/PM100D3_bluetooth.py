"""
PM100D3_bluetooth.py
Example Date of Creation: 2026-04-08
Example Date of Last Modification on Github: 2026-04-08
Version of Python: 3.13
Version of the Thorlabs SDK used: -
==================
Example Description: The example shows how to connect a powermeter with Bluetooth and acquire a measurement. 
tested with PM61A, PM100D3
"""

from anyvisa import AnyVisa 

def main():


    #find devices
    devicesList = AnyVisa.FindResources("BTHLE?*")

    numberOfDevices = len(devicesList)
    for i in range(numberOfDevices):
        print(f"Device {i}: {devicesList[i]}")
    
    if numberOfDevices >1:
        chooseDevice = int(input(f"Choose device (0-{numberOfDevices-1}): "))
    elif numberOfDevices == 1:
        chooseDevice = 0
        
    with devicesList[chooseDevice] as instr:   
        
        try:
            #print the device information
            print(instr.query("SYST:SENS:IDN?"))

            #read the power
            print("measurement value:", instr.query("MEAS:POW?"))
        
        except Exception as e:
            print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()