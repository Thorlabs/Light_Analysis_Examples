"""
Example Thorlabs Power Meter Dual Channel Scope Mode Example
Example Date of Creation                            2024-03-15
Example Date of Last Modification on Github         2024-03-15
Version of Python                                   3.11.2
Version of the Thorlabs SDK used                    anyvisa0.3.0
==================
This examples shows how to configure, execute and fetch results of a dual channel power
scope measurement using SCPI commands and anyvisa. The code contains scope configuration for 
software and hardware triggered scope measurements. 
"""

from anyvisa import AnyVisa
import struct
import time
import sys
import matplotlib.pyplot as plt

def fetchBinaryTriplet(inst):
    """
    Sends SCPI request to device and parses binary triplet response
    
    Parameters
    ----------
    inst : anyvisa device 
        The device anyvisa object used for communication

    Returns
    -------
    list
        list of tripplets with timestamp followed by channel 0 and channel 1 measurements
    """    
    vals = inst.read_bytes(4096)
    length = struct.unpack('<I',  bytearray(vals[0     : 0 +  4]))[0]
    
    res = []
    i = 4
    while i < 12 * length:
        reltime  = struct.unpack('<I',  bytearray(vals[i     : i +  4]))[0]
        value0   = struct.unpack('<f',  bytearray(vals[i + 4 : i +  8]))[0]
        value1   = struct.unpack('<f',  bytearray(vals[i + 8 : i + 12]))[0]
        res.append([reltime, value0, value1])
        i += 12
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
        list of all tripplets with timestamp followed by channel 1 and channel 2 measurements
        
    Raises
    -------
    ValueError
        If there is no data to fetch
    """
    data = [] 
    inst.write("FETC:ARR? 0, 100")
    data.extend(fetchBinaryTriplet(inst))

    if len(data) > 0:
        for x in range (100, 10000, 100):
            inst.write(f"FETCh:ARRay? {x}, 100")
            data.extend(fetchBinaryTriplet(inst))
    else:
        raise ValueError("No data to fetch")
    return data

def plotData(data, chan0, chan1, hPos_t_us=None, triggerLevel=None, xLimit=10000):
    """
    Uses matplotlib to plot the channel measurement results
    
    Parameters
    ----------
    data : anyvisa device 
        The device anyvisa object used for communication
    
    chan0 : bool
        True to enable channel 0
        
    chan1 : bool
        True to enable channel 1
    
    hPos_t_us : uint
        horizontal position of trigger. Unit is microseconds.
        
    triggerLevel : float
        Scope trigger level in percent
        
    xLimit : uint
        Limit of X axis. Max and default is 10000. Unit is microseconds.
    """
    columns = list(zip(*data))
    if chan0:
        plt.plot(columns[0], columns[1], '-or')
    if chan1:
        plt.plot(columns[0], columns[2], '-ob')
    
    maxVal = 0
    minVal = 0
    if chan0 is not None and chan1 is not None:
        maxVal = max(max(columns[1]), max(columns[2]))
        minVal = min(min(columns[1]), min(columns[2]))
    elif chan0 is not None:
        maxVal = max(columns[1])
        minVal = min(columns[1])
    else:
        maxVal = max(columns[2])
        minVal = min(columns[2])
            
    if hPos_t_us is not None:
        plt.plot([hPos_t_us, hPos_t_us], [minVal, maxVal], 'g--') #trigger hpos
    if triggerLevel is not None:
        plt.plot([0,xLimit], [triggerLevel, triggerLevel], 'g--') #trigger threshold

    plt.title("Dual Channel Scope Measure Results")
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
    data : two dimensional array with tuples out of scope buffer
        entire scope buffer
    """
    startTime = data[0][0]
    for sample in data:       
        if sample[0] >= startTime:
            sample[0] = sample[0] - startTime
        else:
            sample[0] = 0xffffffff - startTime + sample[0]

def dualChannelSoftwareScope(inst, chan0, chan1, powerRange_W = 0.1, avg=1, xLim=None):
    """
        Configures, executes single or dual channel software triggered scope mode and visualize result in graph.
        
        Parameters
        ----------
        inst : anyvisa device 
            The device anyvisa object used for communication
        chan0 : bool
            Set to true to enable this channel. False when nothing connected or not relevant.
        chan1 : bool
            Set to true to enable this channel. False when nothing connected or not relevant.
        powerRange_W : float
            Manual measure range for the both or or both channels
        avg : uint
            Averaging of scope. Unit is samples. 1 results in 100 kSPS. 2 results in 50 kSPS.
        xLim : uint
            Limit range of graph X axis.
    """
    if not chan0 and not chan1:
        return
    
    print(">>dualChannel Software scope mode example.")
    print(inst.query('SYST:ERR?').strip())
 
    inst.write("ABOR") #Abort any previous measureument
    
    print(">>Prepare device for scope mode")
    if chan0:
        inst.write(f'SENS1:POW:RANG {powerRange_W}') # Disable autoranging and select fix range
    if chan1:
        inst.write(f'SENS2:POW:RANG {powerRange_W}') # Disable autoranging and select fix range
    print(inst.query('SYST:ERR?').strip())
    
    #Configure the single channels
    print(f">>Configure SW scope mode. Use avg: {avg}")
    if chan0:
        inst.write("CONF1:ARR:CHA")
    if chan1:
        inst.write("CONF2:ARR:CHA")
    #Configure the software triggered scope mode in general
    inst.write(f"CONF:ARR {avg}") 
    print(inst.query('SYST:ERR?').strip())
    
    #Now start the scope measurement. Starts right now.

    print(">>Start measurement")
    inst.write("INIT")
    print(inst.query('SYST:ERR?').strip())
     
    print(">>Wait for scope buffer to be filled")
    waitForTrigger(inst)

    #Now fetch all results from device buffer
    print(">>Fetch scope buffer results")
    data = fetchBinaryData(inst)
    
    print(">>Calculate delta t between scope samples")
    normalizeScopeSampleTime(data)
    
    #use time of last sample as limit of x axis when no other limit given as parameter
    if xLim is None:
        xLim = data[-1][0]

    #Abort any ongoing measureument
    inst.write("ABOR") 

    #Plot data finally
    print(f">>Plot scope data with x limit {xLim}")
    plotData(data, chan0, chan1, None, None, xLim)

def dualChannelHardwareScope(inst, chan0, chan1, powerRange_W = 0.1, peakThresPerc = 40, trigSrc=1, avg=1, hPos = 0, xLim=None):
    """
        Configures, executes single or dual channel hardware triggered scope mode and visualize result in graph.
        
        Parameters
        ----------
        inst : anyvisa device 
            The device anyvisa object used for communication
        chan0 : bool
            Set to true to enable this channel. False when nothing connected or not relevant.
        chan1 : bool
            Set to true to enable this channel. False when nothing connected or not relevant.
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
            Limit range of graph X axis.

    """
    if not chan0 and not chan1:
        return
    
    print(">>dualChannel Hardware scope mode example.")
    print(inst.query('SYST:ERR?').strip())
 
    inst.write("ABOR") #Abort any previous measureument
    
    print(">>Prepare device for scope mode")
    if chan0:
        inst.write(f'SENS1:POW:RANG {powerRange_W}')    # Disable autoranging and select fix range
        inst.write('SENS1:FREQ:MODE CW')                # Select CW mode. In Peak mode scope is not available
        inst.write('INP1:FILT 0')                       # Disable bandwidth limitation
        time.sleep(0.1)
    if chan1:
        inst.write(f'SENS2:POW:RANG {powerRange_W}')    # Disable autoranging and select fix range
        inst.write('SENS2:FREQ:MODE CW')                # Select CW mode. In Peak mode scope is not available
        inst.write('INP2:FILT 0')                       # Disable bandwidth limitation
        time.sleep(0.1)
    
    print(inst.query('SYST:ERR?').strip())
    
    #configure threshold for channel 1 or channel 2 trigger source
    if trigSrc == 1:
        inst.write('SENS1:PEAK 30')
    elif trigSrc == 2:
        inst.write('SENS2:PEAK 30')
    
    #Configure the single channels
    print(f">>Configure Hw scope mode. Use avg: {avg}")
    if chan0:
        inst.write("CONF1:ARR:CHA")
    if chan1:
        inst.write("CONF2:ARR:CHA")
    #Configure the hardware triggered scope mode in general
    inst.write(f"CONF{trigSrc}:ARR:HWT {avg}, {hPos}")
    print(inst.query('SYST:ERR?').strip())
    
    #Now start the scope measurement and arm trigger source
    print(">>Start measurement")
    inst.write("INIT")
    print(inst.query('SYST:ERR?').strip())
    
    #Wait until scope buffer is filled after trigger. Might cause Exception for timeout.
    print(">>Wait for scope buffer to be filled")
    waitForTrigger(inst)
    
    #Force trigger when required manually by software
    #print(inst.query('TRIGer:ARRay:FORCe').strip())
    
    #Now fetch all results from device buffer
    print(">>Fetch scope buffer results")
    data = fetchBinaryData(inst)
    
    #Convert relative time stamps to delta t
    print(">>Calculate delta t between scope samples")
    normalizeScopeSampleTime(data)

    #use time of last sample as limit of x axis when no other limit given as parameter
    if xLim is None:
        xLim = data[-1][0]
        
    #Abort any ongoing measureument
    inst.write("ABOR") 
    
    #convert threshold to power value for graph 
    triggerThreshold_W = None
    if trigSrc == 1 or trigSrc == 2:
        range = float(inst.query('SENS:POW:RANG?'))
        triggerThreshold_W = range * peakThresPerc / 100
    
    #convert hpos from samples to time domain
    hPos_t_us = hPos * 10 * avg 
    
    #Plot data finally
    print(f">>Plot scope data with x limit {xLim}")
    plotData(data, chan0, chan1, hPos_t_us, triggerThreshold_W, xLim)
    
def main():

    devicesList = AnyVisa.FindResources("USB?*::INSTR")

    print("Found devices")
    print(devicesList)
    print()
    
    #test if we found at least one meter
    if not devicesList:
        print("Require at least one powermeter for this demo")
        sys.exit(-1)
    
    #Open device 0 out of find list for communication
    with devicesList[0] as pm:
        print(pm, pm.lib())
        #dualChannelSoftwareScope(pm, True, True, 0.00006, 4, 10000)
        dualChannelHardwareScope(inst, chan0, chan1, powerRange_W = 0.1, peakThresPerc = 40, trigSrc=1, avg=1, hPos = 0, xLim=None)
        #dualChannelHardwareScope(pm, True, True, 0.00006, 40, 1, 1, 50, 6000)
        
if __name__ == '__main__':
    main()