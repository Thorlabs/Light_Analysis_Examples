"""
Example Thorlabs Power Meter Singlel Channel Scope Mode Example
Example Date of Creation                            2024-03-15
Example Date of Last Modification on Github         2024-03-15
Version of Python                                   3.11.2
Version of the Thorlabs SDK used                    anyvisa0.3.0
==================
This examples shows how to configure, execute and fetch results of scope measurement on single channel
power meters (Except PM103) using SCPI commands and anyvisa. The code contains scope configuration for 
software and hardware triggered scope measurements.
"""

from anyvisa import AnyVisa
import struct
import time
import sys
import matplotlib.pyplot as plt

def fetchBinaryTuple(inst):
    """
    Sends SCPI request to device and parses binary tuple response
    
    Parameters
    ----------
    inst : anyvisa device 
        The device anyvisa object used for communication

    Returns
    -------
    list
        list of tuples with relative timestamp followed by measurement value
    """    
    vals = inst.read_bytes(4096)
    length = struct.unpack('<I',  bytearray(vals[0     : 0 +  4]))[0]
    
    res = []
    i = 4
    while i < 8 * length:
        reltime  = struct.unpack('<I',  bytearray(vals[i     : i +  4]))[0]
        value   = struct.unpack('<f',  bytearray(vals[i + 4 : i +  8]))[0]
        res.append([reltime, value])
        i += 8
    return res

def fetchBinaryData(inst):
    """
    Fetches the entire device scope buffer
    
    Parameters
    ----------
    inst : anyvisa device 
        The device anyvisa object used for communication
    
    Returns
    -------
    list
        list of all tuples with relative timestamp followed by power measurement

    Raises
    -------
    ValueError
        In case there is no data to fetch
    """
    data = [] 
    inst.write("FETC:ARR? 0, 100")
    data.extend(fetchBinaryTuple(inst))

    if len(data) > 0:
        for x in range (100, 10000, 100):
            inst.write(f"FETC:ARR? {x}, 100")
            data.extend(fetchBinaryTuple(inst))
    else:
        raise ValueError("No data to fetch")
    return data

def plotData(data, hPos_t_us=None, triggerLevel=None, xLimit=10000):
    """
    Uses matplotlib to plot the channel measurement results
    
    Parameters
    ----------
    data : anyvisa device 
        The device anyvisa object used for communication
    
    hPos_t_us : uint
        horizontal position of trigger. Unit is microseconds. None for SW trigger.
        
    triggerLevel : float. None for SW trigger.
        Scope trigger level in percent
        
    xLimit : uint
        Limit of X axis. Max and default is 10000. Unit is microseconds.
    """
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

    plt.title("Single Channel Scope Measure Results")
    plt.ylabel('Power [W]')
    plt.xlabel('Time [us]')
    plt.xlim([0, xLimit])
    plt.show()
    
def waitForTrigger(inst, timeout=50):
    """
    Wait for scope buffer beeing filled completey or raise timeout
    
    Parameters
    ----------
    inst : anyvisa device 
        The device anyvisa object used for communication
    timeout : uint
        timeout in 100ms steps

    Raises
    -------
    TimeoutError
        If scope buffer is not filled in time. 
    """
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
            raise TimeoutError("Waiting for trigger timed out")

def normalizeScopeSampleTime(data):
    """
    Updates relative time stamps and calculated time delta considering 32bit wrapp around

    Parameters
    ----------
    data : two dimensional array 
        entire scope buffer with tuples out of scope buffer
    """
    startTime = data[0][0]
    for sample in data:       
        if sample[0] >= startTime:
            sample[0] = sample[0] - startTime
        else:
            sample[0] = 0xffffffff - startTime + sample[0]

def singleChannelSoftwareScope(inst, powerRange_W = 0.1, avg=1, xLim=None):
    """
        Configures, executes single channel software triggered scope mode and visualize result in graph.
        
        Parameters
        ----------
        inst : anyvisa device 
            The device anyvisa object used for communication
        powerRange_W : float
            Manual measure range for the both or or both channels
        avg : uint
            Averaging of scope. Unit is samples. 1 results in 100 kSPS. 2 results in 50 kSPS.
        xLim : uint
            Limit range of graph X axis. Use None to show all data.
    """
    print(">>singleChannelSoftware scope mode example.")
    print(inst.query('SYST:ERR?').strip())

    inst.write("ABOR") #Abort any previous measureument

    print(">>Prepare device for scope mode")
    inst.write(f'SENS:POW:RANG {powerRange_W}')    # Disable autoranging and select fix range
    inst.write('SENS:FREQ:MODE CW')                # Select CW mode. In Peak mode scope is not available
    inst.write('INP:FILT 0')                       # Disable bandwidth limitation
    print(inst.query('SYST:ERR?').strip())         

    print(f">>Configure SW triggered scope mode. Use avg: {avg}")
    inst.write("CONF:ARR:CHA")
    inst.write(f"CONF:ARR {avg}") 
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


def singleChannelHardwareScope(inst, powerRange_W = 0.1, peakThresPerc = 40, trigSrc=1, avg=1, hPos = 0, xLim=None):
    """
        Configures, executes hardware triggered scope mode and visualize result in graph.
        
        Parameters
        ----------
        inst : anyvisa device 
            The device anyvisa object used for communication
        powerRange_W : float
            Manual measure range for the both or or both channels
        peakThresPerc : float
            Trigger signal threshold in percent of measurement range. Only relevant when trigSrc is 1 or 2. 
        trigSrc : uint
            hardware trigger source. For closer details read SCPI command CONF:ARR:HWT dokumentation of device.
        avg : uint
            Averaging of scope. Unit is samples. 1 results in 100 kSPS. 2 results in 50 kSPS.
        hPos : uint
            Horizontal position of trigger. Unit is samples.
        xLim : uint
            Limit range of graph X axis. Use None to show all data.
    """
    print(">>singleChannelHardware scope mode example.")
    print(inst.query('SYST:ERR?').strip())

    inst.write("ABOR") #Abort any previous measureument

    print(">>Prepare device for hardware triggered scope mode")
    inst.write(f'SENS:POW:RANG {powerRange_W}')    # Disable autoranging and select fix range
    inst.write('SENS:FREQ:MODE CW')                # Select CW mode. In Peak mode scope is not available
    inst.write('INP:FILT 0')                       # Disable bandwidth limitation
    print(inst.query('SYST:ERR?').strip())
    
    print(f"Range: {powerRange_W}, Thresh:{peakThresPerc}")

    print(f">>Configure HW scope mode. Use avg: {avg}")
    inst.write("CONF:ARR:CHA")
    inst.write(f"CONF{trigSrc}:ARR:HWT {avg}, {hPos}") 
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

    #convert threshold to power value for graph 
    triggerThreshold_W = None
    if trigSrc == 1:
        range = float(inst.query('SENS:POW:RANG?'))
        triggerThreshold_W = range * peakThresPerc / 100
    
    #convert hpos from samples to time domain
    hPos_t_us = hPos * 10 * avg 
    
    #Plot data finally
    print(f">>Plot scope data with x limit {xLim}")
    plotData(data, hPos_t_us, triggerThreshold_W, xLim)

def main():
    devicesList = AnyVisa.FindResources("USB?*::INSTR")

    if not devicesList:
        print("Did not find a single instrument for scope mode")
        sys.exit(1)
    
    #Open device 0 out of find list for communication
    with devicesList[0] as pm:
        #singleChannelSoftwareScope(inst, powerRange_W = 0.1, avg=1, xLim=None)
        #singleChannelSoftwareScope(pm, 0.01)
        #singleChannelHardwareScope(inst, powerRange_W = 0.1, peakThresPerc = 40, trigSrc=1, avg=1, hPos = 0, xLim=None):
        singleChannelHardwareScope(pm, 0.000150, 20, 1, 1, 50, 6000)


if __name__ == '__main__':
    main()