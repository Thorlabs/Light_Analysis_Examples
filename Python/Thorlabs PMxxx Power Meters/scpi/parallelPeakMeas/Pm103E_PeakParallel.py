"""
Example Thorlabs Power Meter Parallel Peak Measurement
Example Date of Creation: 2024-03-11
Version of Python: 3.11
Version of the Thorlabs SDK used: -                anyvisa0.3.0
==================
The example shows how to measure peaks of same experiment with multiple powermeters 
simulanioulsy and how to write results to a csv file.
"""
from anyvisa import AnyVisa
from enum import Enum
import sys
import time
from datetime import datetime

#List of states for state machine
class PM_PeakState(Enum):
    INIT = 0
    WAIT_FOR_PEAK = 1
    TRIGGERED = 2
    FETCHED_ALL = 3
    FETCHED_SOME = 4

def test_system_error(pm):
    """
    Reads one error out of device error queue. Result might be 0 
    and "No error" in case no error in queue.
    
    Parameters
    ----------
    pm : anyvisa device 
        The device anyvisa object used for communication

    Returns
    -------
    list
        first element error code followed by error description as string
    """
    resp = pm.auto_query("SYST:ERR?").strip()
    respClear = resp.replace('"','')

    tokens = respClear.split(',')
    tokens[0] = int(tokens[0])
    return tokens

def pm_write_assert_no_err(pm, cmd):
    """
    Sends command to device and check for error. In case
    of error exception is thrown
    
    Parameters
    ----------
    pm : anyvisa device 
        The device anyvisa object used for communication
    cmd : str
        Excecute this command and check error afterwards
    Raises
    ------
    Exception
        In case error found in qeueue
    """
    pm.write(cmd)
    errors = test_system_error(pm)
    if errors[0] != 0:
        raise Exception(f"Error configure {pm} with cmd: {cmd} results in error: '{errors[1]}'")

def configure_pm_peak_meas(pm):
    """
    Configure power meter for peak measurement
    
    Parameters
    ----------
    pm : anyvisa device 
        The device anyvisa object used for communication
    """

    #Rst and start with default parameters
    pm.write("*RST")
    time.sleep(0.2)
    #configure wavelength
    pm_write_assert_no_err(pm, "SENS:CORR:WAV 600")
    #configure range
    pm_write_assert_no_err(pm, "SENS:ENER:RANG 10e-3")
    #configure threshold
    pm_write_assert_no_err(pm, "SENS:PEAK 10")

def main():
    #Amount of PM require for experiment
    pmExperimentSize = 3

    #Search for powermeters
    devicesList = []
    devicesList = AnyVisa.FindResources("?*")
    sorted(devicesList)

    devCnt = len(devicesList)
    print(f"Info: Found {devCnt} devices")
    for dev in devicesList:
        print("\t- "+str(dev))

    #test if we found all PM for experiment
    if devCnt < pmExperimentSize:
        print(f"Error: Require at least {pmExperimentSize} powermeters for this program")
        sys.exit(-1)

    pms = []
    state = PM_PeakState.INIT
    fetchRes = [None] * devCnt #Crate an array with None for every device
    fetchRepCnt = 0
    sampleTime = None
    recordCounter = 1

    try:
        #establish connection to all found devices
        for pmToOpen in devicesList:
            pmToOpen.open()
            pms.append(pmToOpen)
            
        #Configure devices parameters for experiment
        for pm in pms:
            configure_pm_peak_meas(pm)

        #prepare the peak measurement
        for pm in pms:
            pm.write("CONF:ENER")
            err = test_system_error(pm)
            if err[0] != 0:
                raise Exception("Failed to configure energy measurement")

        #generate unique file name using date and time
        startDateTime = datetime.now()
        filename = f"pmExp_{startDateTime:%Y_%m_%d_%H_%M_%S}.csv"
        print("Info: Log to file: "+filename)

        with open(filename, "w") as fp:
            #Write meta information about experiment to file
            fp.write(f"DateTime,{startDateTime:%Y-%m-%d %H:%M:%S}\n")
            fp.write(f"Power meters,{devCnt}\n")
            for x in range(devCnt):
                fp.write(f"Meter {x}, {pms[x]}\n")
                sensInfo = pms[x].query("SYST:SENS:IDN?").strip()
                #delete all " in response. Split into array on ,
                sensInfos = sensInfo.replace('"','').split(",")
                #Print sensor info Name, Serial and CalDate
                fp.write(f"Sensor {x}, {sensInfos[0]},{sensInfos[1]},{sensInfos[2]}\n")

            #Separate header and record with an additional empty line
            fp.write("\n")

            #Write record columns description header line
            fp.write("[Counter, Time")
            for x in range(devCnt):
                fp.write(f", Meter {x}")
            fp.write("]\n")
            
            print("Info: Start experiment. Use CTRL+C to terminate execution")
            #Read as long as required
            while True:
                #Initate a new measurement state
                if state == PM_PeakState.INIT:
                    for pm in pms:
                        pm.write("ABOR")
                        pm.write("INIT")
                        err = test_system_error(pm)
                        if err[0] != 0:
                            raise Exception("Failed to initiate energy measurement")
                    state = PM_PeakState.WAIT_FOR_PEAK

                #Wait for trigger state
                elif state == PM_PeakState.WAIT_FOR_PEAK:
                    #Now wait for first PM detecting a peak
                    for pm in pms:
                        fetchState = int(pm.query("FETC:STAT?"))
                        if fetchState > 0: #Data read to fetch?
                            fetchRepCnt = 0
                            fetchRes = [None] * devCnt
                            sampleTime = datetime.now()
                            print("Info: Powermeter triggered")
                            state = PM_PeakState.TRIGGERED
                            break
                    
                    if state == PM_PeakState.WAIT_FOR_PEAK:
                        time.sleep(0.01) #Sleep for 10 ms and try again

                #Triggered State. At least one PM received a Peak
                elif state == PM_PeakState.TRIGGERED:
                    #Try to fetch peak measure result of all PM
                    for x in range(devCnt):
                        #Fetched result for this meter already?
                        if fetchRes[x] is None:
                            #Test if meter has data to fetch
                            fetchState = int(pms[x].query("FETC:STAT?"))
                            if fetchState > 0: #Data read to fetch?
                                fetchRes[x] = float(pms[x].query("FETC?"))
                        
                        #Test if peak data is still pending?
                        if None in fetchRes:
                            fetchRepCnt += 1
                            #Timeout on fetching results?
                            if fetchRepCnt > 10:
                                #Abort any ongoing measurement
                                for x in range(devCnt):
                                    if fetchRes[x] is None:
                                        pms[x].write("ABOR")
                                state = PM_PeakState.FETCHED_SOME #We fetched only some results
                            else:
                                time.sleep(0.01) #Sleep for 10 ms and try again
                        else:
                            state = PM_PeakState.FETCHED_ALL #We fetched all res

                #Data fetched state. Received peak on all PM
                elif state == PM_PeakState.FETCHED_ALL:
                    fp.write(f"{recordCounter},{sampleTime:%H:%M:%S%z}")
                    for res in fetchRes:
                        fp.write(f", {res}")
                    fp.write("\n")
                    recordCounter += 1
                    state = PM_PeakState.INIT
                    print("Info: Peak recorded by all PM")

                #Data fetched state. Only some PM fetched peak result
                elif state == PM_PeakState.FETCHED_SOME:
                    fp.write(f"{recordCounter},{sampleTime:%H:%M:%S%z}")
                    devFound = 0
                    for res in fetchRes:
                        if res is None:
                            fp.write(",           ")
                        else:
                            fp.write(f", {res}")
                            devFound += 1
                    fp.write("\n")
                    recordCounter += 1
                    state = PM_PeakState.INIT
                    print(f"Warning: Peak recorded only by {devFound} PM")
    
    #Catch keyboard exception CTRL + C to abort program execution
    except KeyboardInterrupt:
        #Try to abort all ongoing measurements on the meters on exit of application
        for dev in devicesList:
            try:
                dev.write("ABOR")
            except Exception:
                pass

    #Ensure all resources are released in case of success or error
    finally:
        #Close all powermeters
        for pm in pms:
            try: #Do not handle any exception during close
                pm.close()
            except Exception:
                pass
        #Finally release resource handler
        AnyVisa.ReleaseSystem()
    
    print(f"Info: Terminate execution after {recordCounter-1} records")
    
if __name__ == "__main__":
    main()
