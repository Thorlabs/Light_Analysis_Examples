from anyvisa import AnyVisa
import sys
from datetime import datetime
import struct

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
            res.extend(parseFastModeBinary(pm))

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