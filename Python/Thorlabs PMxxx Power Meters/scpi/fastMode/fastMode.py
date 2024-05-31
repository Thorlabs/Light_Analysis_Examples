"""
Example Thorlabs Power Meter Fast Measurement Mode
Example Date of Creation                            2024-03-15
Example Date of Last Modification on Github         2024-03-15
Version of Python                                   3.11.2
Version of the Thorlabs SDK used                    anyvisa0.3.0
==================
This examples shows how to access the Power Meter Fast Measurement data stream. For this
example it is important to query the Meter as fast as possible to reduce data loss propability.
The meter enqueues every millisecond up to 100 results and the fixed size queue length is limited
to recent 10 ms of samples. 
"""

from anyvisa import AnyVisa
import sys
from datetime import datetime
import struct

def parseFastModeBinaryPM103(inst):
    """
    Parses PM103 tuple response
    
    Parameters
    ----------
    inst : anyvisa device 
        The device anyvisa object used for communication
    
    Returns
    -------
    list
        list of tuples with relative timestamp followed by measurement value
    """
    bytes = inst.read_bytes(4096)
    byteCnt = len(bytes) - 1

    i = 0
    
    #Device response length is 0 bytes long
    if chr(bytes[0]) == '0':
        return []
    
    #Find , in response before parsing binary data
    for byte in bytes:
        byte = chr(byte)
        i+=1
        if byte == ',':
            break

    res = []
    #Parse binary tuple data
    while i < byteCnt:
        reltime = struct.unpack('<I', bytearray(bytes[i:i+4]))[0]
        value   = struct.unpack('<f', bytearray(bytes[i+4:i+ 8]))[0]
        res.append([reltime, value])
        i += 8
    return res

def parseFastModeBinary(dev):
    """
    Parses binary tuple response
    
    Parameters
    ----------
    dev : anyvisa device 
        The device anyvisa object used for communication
    
    Returns
    -------
    list
        list of tuples with timestamp followed by channel measurement
    """
    vals = dev.read_bytes(4)
    length = struct.unpack('<I', bytearray(vals[0:0+4]))[0]
    vals = dev.read_bytes(8 * length)
    res = []
    i = 0
    while i < 8 * length:
        reltime = struct.unpack('<I', bytearray(vals[i:i+4]))[0]
        value1   = struct.unpack('<f', bytearray(vals[i+4:i+8]))[0]
        res.append([reltime, value1])
        i += 8; 
    return res
    
def calcRelTime(t0, tn):
    """
    Calculated time delta with 32 bit wrapp around special case
    
    Parameters
    ----------
    t0 : uint 
        start time of fast record
    tn : uint 
        actual time to calculate delta for
        
    Returns
    -------
    uint
        time delta in microseconds
    """
    if tn > t0:
        return tn - t0
    return 0xffffffff - t0 + tn

def main():
    devices = []
    devices = AnyVisa.FindResources("?*")

    print("Found devices")
    print(devices)
    print()
    
    #test if we found at least one meter
    if not devices:
        print("Require at least one powermeter for this demo")
        sys.exit(-1)
    
    #Open device 0 out of find list for communication
    with devices[0] as pm:
        #Print meter and sensor information
        print("PM: ", pm.auto_query('*IDN?').strip())
        print("Sensor: ",pm.auto_query('SYST:SENS:IDN?').strip())

        #configure fast measure stream of channel 1 for power measurement    
        pm.write('ACQ1:FAST:POW')
        pm.write('ACQ1:FAST:RESET')

        res = []
        #Read as fast as possible and store in RAM
        while (len(res) < 1000):
            pm.write('ACQ1:FAST:FETC?')
            res.extend(parseFastModeBinary(pm))       # Use for PM5020 and newer pm
            #res.extend(parseFastModeBinaryPM103(pm)) # Use for PM103 and PM103E

        #Create a unique file name based on date and time
        startDateTime = datetime.now()
        filename = f'pmFastMeas_{startDateTime:%Y_%m_%d_%H_%M_%S}.csv'
        print("Info: Log to file: "+filename)

        #open file for writting
        with open(filename, "w") as fp:
            t0 = res[0][0]
            #Iterate all samples and store in file
            for sample in res:
                fp.write(f"{calcRelTime(t0, sample[0])}, {sample[1]}\n")
                
        print(f"Info: Add sum of {len(res)} samples to file")
        
        
if __name__ == '__main__':
    main()