# -*- coding: utf-8 -*-

from anyvisa import AnyVisa
import struct
import time
import sys
import matplotlib.pyplot as plt

def fetchBinaryTuplePM103(inst):
    length = 0
    lenStr = ""
    res = []
    while length == 0:
        byte = inst.read_bytes(1)
        if byte == 0:
            return res
        if byte == b',':
            length = int(lenStr)
        else:
            lenStr = lenStr + chr(byte[0])

    vals = inst.read_bytes(8 * length)
    i = 0
    while i < 8 * length:
        reltime = struct.unpack('<I', bytearray(vals[i:i+4]))[0]
        value   = struct.unpack('<f', bytearray(vals[i+4:i+ 8]))[0]
        res.append([reltime, value])
        i += 8
    return res

def fetchBinaryData(inst):
    data = [] 
    inst.write("FETC:ARR? 0, 100")
    data.extend(fetchBinaryTuplePM103(inst))

    if len(data) > 0:
        for x in range (100, 10000, 100):
            inst.write(f"FETC:ARR? {x}, 100")
            data.extend(fetchBinaryTuplePM103(inst))
    else:
        raise ValueError("No data to fetch")
    return data

def plotData(data, hPos_t_us=None, triggerLevel=None, xLimit=10000):
    columns = list(zip(*data))
    plt.plot(columns[0], columns[1], '-or')
    
    maxVal = 0
    minVal = 0
    maxVal = max(columns[1])
    minVal = min(columns[1])
            
    if hPos_t_us is not None:
        plt.plot([hPos_t_us, hPos_t_us], [minVal, maxVal], 'g--') #trigger hpos
    if triggerLevel is not None:
        plt.plot([0,xLimit], [triggerLevel, triggerLevel], 'g--') #trigger threshold

    plt.title("PM103 Scope Measure Results")
    plt.ylabel('Power [W]')
    plt.xlabel('Time [us]')
    plt.xlim([0, xLimit])
    plt.show()
    
def waitForTrigger(inst, timeout=50):
    timeoutCnt = 0
    while True:
        state = int(inst.query("FETC:STAT?").strip())
        if state == 0: # dataReadyToFetch bit
            time.sleep(0.1)
            timeoutCnt = timeoutCnt + 1
        else:
            break; 
        if timeoutCnt > timeout:
            inst.write("ABOR") #Abort measureument
            sys.exit("Waiting for trigger timed out")

def normalizeScopeSampleTime(data):
    startTime = data[0][0]
    for sample in data:       
        if sample[0] >= startTime:
            sample[0] = sample[0] - startTime
        else:
            sample[0] = 0xffffffff - startTime + sample[0]

def pm60_SoftwareScope(inst, powerRange_W = 0.1, avg=1, xLim=None):
    print(">>PM103 Software scope mode example.")
    print(inst.query('SYST:ERR?').strip())

    inst.write("ABOR") #Abort any previous measureument

    print(">>Prepare device for scope mode")
    inst.write(f'SENS:POW:RANG {powerRange_W}')    # Disable autoranging and select fix range
    inst.write('SENS:FREQ:MODE CW')                # Select CW mode. In Peak mode scope is not available
    inst.write('INP:FILT 0')                       # Disable bandwidth limitation
    print(inst.query('SYST:ERR?').strip())         

    print(f">>Configure software triggered scope mode. Use avg: {avg}")
    inst.write("CONF:ARR "+str(avg)) 
    print(inst.query('SYST:ERR?').strip())

    print(">>Start measurement")
    inst.write("INIT")
    print(inst.query('SYST:ERR?').strip())

    print(">>Wait for scope buffer to be filled")
    waitForTrigger(inst)

    print(">>Fetch scope buffer results")
    data = fetchBinaryData(inst)

    print(">>Calculate delta t between scope samples")
    normalizeScopeSampleTime(data)
    
    #use time of last sample as xLimit
    if xLim is None:
        xLim = data[-1][0]

    inst.write("ABOR") #Abort any previous measureument

    print(f">>Plot scope data with x limit {xLim}")
    plotData(data, None, None, xLim)


def pm60_HardwareScope(inst, powerRange_W = 0.1, peakThresPerc = 40, trigSrc=1, avg=1, hPos = 0, xLim=None):
    print(">>PM60 Hardware scope mode example.")
    print(inst.query('SYST:ERR?').strip())

    inst.write("ABOR") #Abort any previous measureument

    print(">>Prepare device for scope mode")
    inst.write('SENS:POW:RANG '+str(powerRange_W)) # Disable autoranging and select fix range
    print(inst.query('SYST:ERR?').strip())
    inst.write('SENS:PEAK '+str(peakThresPerc)) # Set threshold for peak detection in percent.
    print(inst.query('SYST:ERR?').strip())
    print(f"Range: {powerRange_W}, Thresh:{peakThresPerc}")
    
    print(">>Configure scope mode. Use avg: "+str(avg))
    inst.write("CONF:ARR:CHA")
    inst.write(f"CONF{trigSrc}:ARR:HWT {avg}, {hPos}") 
    print(inst.query('SYST:ERR?').strip())

    print(">>Configure IO output pin")
    inst.write("SOUR:DIG:PIN2:FUNC OALT")
    print(inst.query('SYST:ERR?').strip())

    print(">>Start measurement")
    inst.write("INIT")
    print(inst.query('SYST:ERR?').strip())

    print(">>Wait for scope buffer to be filled")
    waitForTrigger(inst)

    print(">>Fetch scope buffer results")
    data = fetchBinaryData(inst)
    print("Start of raw scope data")
    print(data[:5])

    print(">>Calculate delta t between scope samples")
    normalizeScopeSampleTime(data)
    print("Start of data with normalized time")
    print(data[:5])

    #use time of last sample as xLimit
    if xLim is None:
        xLim = data[-1][0]

    inst.write("ABOR") #Abort any previous measureument


    print(">>Plot scope data with x limit "+str(xLim))
    plotData(data, None, None, xLim)

def main():

    devicesList = AnyVisa.FindResources("USB?*::INSTR")

    if not devicesList:
        print("Did not find a single instrument for scope mode")
        sys.exit(1)

    with devicesList[0] as pm:
        #pm60_SoftwareScope(inst, powerRange_W = 0.1, avg=1, xLim=None)
        pm60_SoftwareScope(pm, 0.01)
        #pm60_HardwareScope(inst, powerRange_W = 0.1, peakThresPerc = 40, trigSrc=1, avg=1, hPos = 0, xLim=None):
        #pm60_HardwareScope(pm, 0.004, 40, 2, 1, 100, 20000)


if __name__ == '__main__':
    main()