from datetime import datetime
from ctypes import *
from TLPMX import TLPMX
import numpy as np
import time

from TLPMX import TLPM_SENSOR_CHANNEL1,TLPM_SENSOR_CHANNEL2,TLPM_ATTR_SET_VAL, TLPM_ATTR_MAX_VAL, TLPM_ATTR_MIN_VAL

tlPM = TLPMX()

#available choices for normalization function
class _NormIndex(object):
    @property
    def CH1(self):
        return 'CH1'
    @property
    def CH2(self):
        return 'CH2'
    @property
    def NONE(self):
        return 'NONE'

#setting parameters here
#set the wavelength for channel 1 and channel 2 respectively. the unit is [nm]
setWavelengthCH1 = 500
setWavelengthCH2 = 800

#set the power or energy range for channel 1 and channel 2 respectively, the unit is [W] or [J]
setRangeCH1 = 0.000001
setRangeCH2 = 0.00001

#set if the auto power range is enabled.
#auto range isn't available for energy sensors
setPowerAutoRangeCH1 = True
setPowerAutoRangeCH2 = False

#set the baseLine for channel 1 and channel 2 respectively. 
#The BaseLine should be in a range from 0 to 1. It's a coefficient and will be multiplied to the current power or energy range.
#only the power or energy values which are larger than [baseLine*setRange] will be recorded.
setBaseLineCH1 = 0
setBaseLineCH2 = 0.1

#set the data point and the sampling interval
#the sampling interval will fail to work if the pulse period is longer than sampling interval for energy sensors
#the unit of sampling interval is [s].
setSampleNumber = 10
setInterval = 1

#set if the normalized power or energy is displayed
#NormIndex.CH1 : (CH2 value) / (CH1 value)
#NormIndex.CH2 : (CH1 value) / (CH2 value)
#NormIndex.NONE : not calculate the normalized power or energy
#this function is available only when two power sensors or two energy sensors are connected
NormIndex = _NormIndex()
normCH = NormIndex.NONE

###################################################################################################
def main():

    modelName,sensorType1,sensorType2 = ConnectDevice()

    if modelName == 0:
        tlPM.close()
        return
    
    #single channel console
    if modelName.value != c_char_p(b'PM5020')._objects: 
        #no sensor
        if sensorType1.value == c_char_p(b'')._objects: 
            print("No Sensor")
       
        #power sensor
        elif sensorType1.value != c_char_p(b'\x03')._objects: 
            SetWavelength(setWavelengthCH1,TLPM_SENSOR_CHANNEL1)
            SetRange("power",setRangeCH1,setPowerAutoRangeCH1,TLPM_SENSOR_CHANNEL1)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('power',float)]))
            for i in range(setSampleNumber):
                #only when the power or energy value is successfully fetched and is larger than baseline, it will be displayed
                value[i] = GetValue("power",TLPM_SENSOR_CHANNEL1)
                if value[i][0] != "":
                    print("{time:} CH1:{power:} W".format(time = value[i][0],power = value[i][1]))
                time.sleep(setInterval)

        #energy sensor
        elif sensorType1.value == c_char_p(b'\x03')._objects: 
            SetWavelength(setWavelengthCH1,TLPM_SENSOR_CHANNEL1)
            SetRange("energy",setRangeCH1,False,TLPM_SENSOR_CHANNEL1)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('energy',float)]))
            for i in range(setSampleNumber):
                #only when the power or energy value is successfully fetched and is larger than baseline, it will be displayed
                value[i] = GetValue("energy",TLPM_SENSOR_CHANNEL1)
                if value[i][0] != "":
                    print("{time:} CH1:{energy:} J".format(time = value[i][0],energy = value[i][1]))
                time.sleep(setInterval)

    else: #PM5020
        #CH1:no sensor CH2:no sensor
        if sensorType1.value == c_char_p(b'')._objects and sensorType2.value == c_char_p(b'')._objects: 
            print("No Sensor")
        
        #CH1:no sensor CH2:power sensor
        elif sensorType1.value == c_char_p(b'')._objects and sensorType2.value != c_char_p(b'\x03')._objects:
            SetWavelength(setWavelengthCH2,TLPM_SENSOR_CHANNEL2)
            SetRange("power",setRangeCH2,setPowerAutoRangeCH2,TLPM_SENSOR_CHANNEL2)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('power',float)]))
            for i in range(setSampleNumber):
                #only when the power or energy value is successfully fetched and is larger than baseline, it will be displayed
                value[i] = GetValue("power",TLPM_SENSOR_CHANNEL2)
                if value[i][0] != "":
                    print("{time:} CH2:{power:} W".format(time = value[i][0],power = value[i][1]))
                time.sleep(setInterval)
        
        #CH1:no sensor CH2:energy sensor
        elif sensorType1.value == c_char_p(b'')._objects and sensorType2.value == c_char_p(b'\x03')._objects:
            SetWavelength(setWavelengthCH2,TLPM_SENSOR_CHANNEL2)
            SetRange("energy",setRangeCH2,False,TLPM_SENSOR_CHANNEL2)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('energy',float)]))
            for i in range(setSampleNumber):
                #only when the power or energy value is successfully fetched and is larger than baseline, it will be displayed
                value[i] = GetValue("energy",TLPM_SENSOR_CHANNEL2)
                if value[i][0] != "":
                    print("{time:} CH2:{energy:} J".format(time = value[i][0],energy = value[i][1]))
                time.sleep(setInterval)
        
        #CH1:power sensor CH2:no sensor
        elif sensorType1.value != c_char_p(b'\x03')._objects and sensorType2.value == c_char_p(b'')._objects:
            SetWavelength(setWavelengthCH1,TLPM_SENSOR_CHANNEL1)
            SetRange("power",setRangeCH1,setPowerAutoRangeCH1,TLPM_SENSOR_CHANNEL1)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('power',float)]))
            for i in range(setSampleNumber):
                #only when the power or energy value is successfully fetched and is larger than baseline, it will be displayed
                value[i] = GetValue("power",TLPM_SENSOR_CHANNEL1)
                if value[i][0] != "":
                    print("{time:} CH1:{power:} W".format(time = value[i][0],power = value[i][1]))
                time.sleep(setInterval)
        
        #CH1:power sensor CH2:power sensor
        elif sensorType1.value != c_char_p(b'\x03')._objects and sensorType2.value != c_char_p(b'\x03')._objects:
            SetWavelength(setWavelengthCH1,TLPM_SENSOR_CHANNEL1)
            SetWavelength(setWavelengthCH2,TLPM_SENSOR_CHANNEL2)
            SetRange("power",setRangeCH1,setPowerAutoRangeCH1,TLPM_SENSOR_CHANNEL1)
            SetRange("power",setRangeCH2,setPowerAutoRangeCH2,TLPM_SENSOR_CHANNEL2)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('power1',float),('power2',float)]))
            for i in range(setSampleNumber):
                #only when both values are successfully fetched and are both larger than baseline, they will be displayed
                value[i] = GetValueDual("power","power")
                if value[i][0] != "":
                    if normCH == NormIndex.NONE:
                        print("{time:} CH1:{value1:} W  CH2:{value2:} W".format(time = value[i][0],value1 = value[i][1],value2 = value[i][2]))
                    elif normCH == NormIndex.CH1:
                        print("{time:} CH1:{value1:} W  CH2:{value2:} W  Norm.:{value3:}".format(time = value[i][0],value1 = value[i][1],value2 = value[i][2],value3 = value[i][2]/value[i][1]))
                    elif normCH == NormIndex.CH2:
                        print("{time:} CH1:{value1:} W  CH2:{value2:} W  Norm.:{value3:}".format(time = value[i][0],value1 = value[i][1],value2 = value[i][2],value3 = value[i][1]/value[i][2]))
                time.sleep(setInterval)
     
        #CH1:power sensor CH2:energy sensor
        elif sensorType1.value != c_char_p(b'\x03')._objects and sensorType2.value == c_char_p(b'\x03')._objects:
            SetWavelength(setWavelengthCH1,TLPM_SENSOR_CHANNEL1)
            SetWavelength(setWavelengthCH2,TLPM_SENSOR_CHANNEL2)
            SetRange("power",setRangeCH1,setPowerAutoRangeCH1,TLPM_SENSOR_CHANNEL1)
            SetRange("energy",setRangeCH2,False,TLPM_SENSOR_CHANNEL2)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('power',float),('energy',float)]))
            for i in range(setSampleNumber):
                #only when both values are successfully fetched and are both larger than baseline, they will be displayed
                value[i] = GetValueDual("power","energy")
                if value[i][0] != "":
                    print("{time:} CH1:{value1:} W  CH2:{value2:} J".format(time = value[i][0],value1 = value[i][1],value2 = value[i][2]))
                time.sleep(setInterval)
        
        #CH1:energy sensor CH2:no sensor
        elif sensorType1.value == c_char_p(b'\x03')._objects and sensorType2.value == c_char_p(b'')._objects:
            SetWavelength(setWavelengthCH1,TLPM_SENSOR_CHANNEL1)
            SetRange("energy",setRangeCH1,False,TLPM_SENSOR_CHANNEL1)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('energy',float)]))
            for i in range(setSampleNumber):
                #only when the power or energy value is successfully fetched and is larger than baseline, it will be displayed
                value[i] = GetValue("energy",TLPM_SENSOR_CHANNEL1)
                if value[i][0] != "":
                    print("{time:} CH1:{energy:} J".format(time = value[i][0],energy = value[i][1]))
                time.sleep(setInterval)
        
        #CH1:energy sensor CH2:power sensor
        elif sensorType1.value == c_char_p(b'\x03')._objects and sensorType2.value != c_char_p(b'\x03')._objects:
            SetWavelength(setWavelengthCH1,TLPM_SENSOR_CHANNEL1)
            SetWavelength(setWavelengthCH2,TLPM_SENSOR_CHANNEL2)
            SetRange("energy",setRangeCH1,False,TLPM_SENSOR_CHANNEL1)
            SetRange("power",setRangeCH2,setPowerAutoRangeCH2,TLPM_SENSOR_CHANNEL2)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('energy',float),('power',float)]))
            for i in range(setSampleNumber):
                #only when both values are successfully fetched and are both larger than baseline, they will be displayed
                value[i] = GetValueDual("energy","power")
                if value[i][0] != "":
                    print("{time:} CH1:{value1:} J  CH2:{value2:} W".format(time = value[i][0],value1 = value[i][1],value2 = value[i][2]))
                time.sleep(setInterval)
        
        #CH1:energy sensor CH2:energy sensor
        elif sensorType1.value == c_char_p(b'\x03')._objects and sensorType2.value == c_char_p(b'\x03')._objects:
            SetWavelength(setWavelengthCH1,TLPM_SENSOR_CHANNEL1)
            SetWavelength(setWavelengthCH2,TLPM_SENSOR_CHANNEL2)
            SetRange("energy",setRangeCH1,False,TLPM_SENSOR_CHANNEL1)
            SetRange("energy",setRangeCH2,False,TLPM_SENSOR_CHANNEL2)
            value = np.zeros((setSampleNumber),dtype=([('time', np.str_, 19),('energy1',float),('energy2',float)]))
            for i in range(setSampleNumber):
                #only when both values are successfully fetched and are both larger than baseline, they will be displayed
                value[i] = GetValueDual("energy","energy")
                if value[i][0] != "":
                    if normCH == NormIndex.NONE:
                        print("{time:} CH1:{value1:} J  CH2:{value2:} J".format(time = value[i][0],value1 = value[i][1],value2 = value[i][2]))
                    elif normCH == NormIndex.CH1:
                        print("{time:} CH1:{value1:} J  CH2:{value2:} J  Norm.:{value3:}".format(time = value[i][0],value1 = value[i][1],value2 = value[i][2],value3 = value[i][2]/value[i][1]))
                    elif normCH == NormIndex.CH2:
                        print("{time:} CH1:{value1:} J  CH2:{value2:} J  Norm.:{value3:}".format(time = value[i][0],value1 = value[i][1],value2 = value[i][2],value3 = value[i][1]/value[i][2]))
                time.sleep(setInterval)


    tlPM.close()
    print("The program finishes.")

def ConnectDevice():
    deviceCount = c_uint32()
    resourceName = create_string_buffer(1024)
    modelName = create_string_buffer(1024)
    serialNumber = create_string_buffer(1024)
    deviceAvailable = c_bool()
    message =  create_string_buffer(1024)
    sensorType1 =   create_string_buffer(1024)
    sensorType2 =   create_string_buffer(1024)

    try:
        tlPM.findRsrc(byref(deviceCount))
        tlPM.getRsrcName(0, resourceName)
        tlPM.getRsrcInfo(0,modelName, serialNumber,message,deviceAvailable)
        tlPM.open(resourceName, c_bool(True), c_bool(True))
        print(serialNumber.value.decode('utf_8') + " is connected.")
    except:
        print("No Device Found!")
        modelName = 0
        sensorType1.value = c_char_p(b'')._objects
        sensorType2.value = c_char_p(b'')._objects
        return modelName,sensorType1,sensorType2

    try:
        tlPM.getSensorInfo(message,message,message,sensorType1,message,message,TLPM_SENSOR_CHANNEL1)
    except:
        sensorType1.value = c_char_p(b'')._objects

    try:
        tlPM.getSensorInfo(message,message,message,sensorType2,message,message,TLPM_SENSOR_CHANNEL2)
    except:
        sensorType2.value = c_char_p(b'')._objects

    return modelName,sensorType1,sensorType2


def SetWavelength(setWavelength,CHANNEL):
    wavelength = c_double(0)
    try:
        tlPM.setWavelength(c_double(setWavelength),CHANNEL)
        tlPM.getWavelength(TLPM_ATTR_SET_VAL,byref(wavelength),CHANNEL)
    except:
        print("Wavelength of Channel {CHANNEL:} is out of range!".format(CHANNEL = CHANNEL))
        tlPM.getWavelength(TLPM_ATTR_SET_VAL,byref(wavelength),CHANNEL)

    if CHANNEL == TLPM_SENSOR_CHANNEL1:
        print("Wavelength for Channel 1: {wavelength:.2f} nm".format(wavelength = wavelength.value))
    elif CHANNEL == TLPM_SENSOR_CHANNEL2:
        print("Wavelength for Channel 2: {wavelength:.2f} nm".format(wavelength = wavelength.value))


def SetRange(sensorType,setRange,setPowerAutoRange,CHANNEL):
    if sensorType == "power":
        if setPowerAutoRange == True:
            err = tlPM.setPowerAutoRange(True,CHANNEL)
            if CHANNEL == TLPM_SENSOR_CHANNEL1:
                print("Power Range for Channel 1 is set to AUTO")
            elif CHANNEL == TLPM_SENSOR_CHANNEL2:
                print("Power Range for Channel 2 is set to AUTO")
        else:
            tlPM.setPowerAutoRange(False,CHANNEL)
            powerMax = c_double(0)
            powerMin = c_double(0)
            range = c_double(0)
            tlPM.getPowerRange(TLPM_ATTR_MAX_VAL,byref(powerMax),CHANNEL)
            tlPM.getPowerRange(TLPM_ATTR_MIN_VAL,byref(powerMin),CHANNEL)
            if setRange < powerMin.value:
                print("Power Range for Channel 1 is too small!")
                setRange = powerMin.value
            elif setRange > powerMax.value:
                print("Power Range for Channel 1 is too large!")
                setRange = powerMax.value

            tlPM.setPowerRange(c_double(setRange),CHANNEL)
            tlPM.getPowerRange(TLPM_ATTR_SET_VAL,byref(range),CHANNEL)
            if CHANNEL == TLPM_SENSOR_CHANNEL1:
                print("Power Range for Channel 1: {range:} W".format(range = range.value))
            elif CHANNEL == TLPM_SENSOR_CHANNEL2:
                print("Power Range for Channel 2: {range:} W".format(range = range.value))

    elif sensorType == "energy":
        energyMax = c_double(0)
        energyMin = c_double(0)
        range = c_double(0)
        tlPM.getEnergyRange(TLPM_ATTR_MAX_VAL,byref(energyMax),CHANNEL)
        tlPM.getEnergyRange(TLPM_ATTR_MIN_VAL,byref(energyMin),CHANNEL)
        if setRange < energyMin.value:
            print("Energy Range for Channel 1 is too small!")
            setRange = energyMin.value
        elif setRange > energyMax.value:
            print("Energy Range for Channel 1 is too large!")
            setRange = energyMax.value

        tlPM.setEnergyRange(c_double(setRange),CHANNEL)
        tlPM.getEnergyRange(TLPM_ATTR_SET_VAL,byref(range),CHANNEL)

        if CHANNEL == TLPM_SENSOR_CHANNEL1:
            print("Energy Range for Channel 1: {range:} J".format(range = range.value))
        elif CHANNEL == TLPM_SENSOR_CHANNEL2:
            print("Energy Range for Channel 2: {range:} J".format(range = range.value))

def GetValue(sensorType,CHANNEL):
    #The number of digits for 'time' is 19 means the time is displayed in the format of year-month-day-hour-minute-second
    value = np.array([("",0)],dtype=([('time', np.str_, 19),('value',float)]))
    start_time = datetime.now()

    while True:
        if sensorType == "power":
            power =  c_double()
            tlPM.measPower(byref(power), CHANNEL)
            value[0][1] = power.value
        elif sensorType == "energy":
            energy =  c_double()
            try:
                tlPM.measEnergy(byref(energy), CHANNEL)
            except:
                #For consoles except PM5020, if the energy fails to fetch, it will return timeout error
                #if the console is PM5020, it will keep waiting until the energy is fetched
                pass
            finally:
                value[0][1] = energy.value

        if value[0][1] > setRangeCH1*setBaseLineCH1:
            value[0][0] = datetime.now()
            break
        if (datetime.now() -start_time).seconds > setInterval*5:
            print("Time out!")
            break
    return value


def GetValueDual(sensorTypeCH1,sensorTypeCH2):
    #The number of digits for 'time' is 19 means the time is displayed in the format of year-month-day-hour-minute-second
    value = np.array([("",0,0)],dtype=([('time', np.str_, 19),('value1',float),('value2',float)]))
    start_time = datetime.now()

    while True:
        if sensorTypeCH1 == "power":
            power =  c_double()
            tlPM.measPower(byref(power), TLPM_SENSOR_CHANNEL1)
            value[0][1] = power.value
        elif sensorTypeCH1 == "energy":
            energy =  c_double()
            try:
                tlPM.measEnergy(byref(energy), TLPM_SENSOR_CHANNEL1)
            except:
                #For consoles except PM5020, if the energy fails to fetch, it will return timeout error
                #if the console is PM5020, it will keep waiting until the energy is fetched
                pass
            finally:
                value[0][1] = energy.value
        
        if sensorTypeCH2 == "power":
            power =  c_double()
            tlPM.measPower(byref(power), TLPM_SENSOR_CHANNEL2)
            value[0][2] = power.value
        elif sensorTypeCH2 == "energy":
            energy =  c_double()
            try:
                tlPM.measEnergy(byref(energy), TLPM_SENSOR_CHANNEL2)
            except:
                pass
            finally:
                value[0][2] = energy.value

        if value[0][1] > setRangeCH1*setBaseLineCH1 and value[0][2] > setRangeCH2*setBaseLineCH2:
            value[0][0] = datetime.now()
            break
        if (datetime.now() -start_time).seconds > setInterval*5:
            print("Time out!")
            break

    return value

if __name__ == "__main__":
    main()
    


