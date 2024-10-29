"""
Example Title: PAX1000 using Pyvisa
Example Date of Creation(YYYY-MM-DD): 2024-10-29
Example Date of Last Modification on Github: 2024-10-29
Version of Python used for Testing and IDE: 3.11
Version of the Thorlabs SDK used: PAX1000 Software Version 1.4
==================
Example Description: This example shows how to read measurement values in binary format, using Pyvisa and SCPI commands
"""


import time
import pyvisa
import sys
import struct

# create a resource manager
rm = pyvisa.ResourceManager()

# open the connection (replace '...' with your device address)
device = rm.open_resource('USB0::0x1313::0x8031::E00000019::INSTR')

# send the *IDN? command
device.write('*IDN?') 
# read the result
result = device.read() 
# print the result
print(result)

"""
Measurement modes:
    IDLE: Value 0, no measurements are taken.</li>
    H512: Value 1, 0.5 revolutions for one measurement, 512 points for FFT.</li>
    H1024:Value 2, 0.5 revolutions for one measurement, 1024 points for FFT</li>
    H2048:Value 3. 0.5 revolutions for one measurement, 2048 points for FFT</li>
    F512:Value 4, 1 revolution for one measurement, 512 points for FFT.</li>
    F1024:Value 5, 1 revolution for one measurement, 1024 points for FFT</li>
    F2048:Value 6, 1 revolution for one measurement, 2048 points for FFT</li>
    D512:Value 7, 2 revolutions for one measurement, 512 points for FFT</li>
    D1024:Value 8, 2 revolutions for one measurement, 1024 points for FFT</li>
    D2048:Value 9, 2 revolutions for one measurement, 2048 points for FFT.</li>
"""

#INP:ROT:VEL 200.0
device.write('INP:ROT:VEL 100')
device.write('SENS:CALC 1')

device.write('INP:ROT:STAT 1') #Turn on motor

print("Power up PAX -> Sleep 8 seconds")
set = 0 
while not set:
    time.sleep(0.5)
    set = int(device.query("INP:ROT:SETT?"))#Tests if motor speed is settled

#time.sleep(8) # wait until PAX is running properly.
print("Powered up! Let's go")

def parseBinPax1000Data(bin:bytearray):
    dataSet = []
    i = 0
    dataSet.append(struct.unpack('<I', bytearray(bin[i:i+4]))[0]) #revCount
    i += 4
    dataSet.append(struct.unpack('<I', bytearray(bin[i:i+4]))[0]) #timeStamp
    i += 4
    dataSet.append(struct.unpack('<I', bytearray(bin[i:i+4]))[0]) #PAXopmode
    i += 4
    dataSet.append(struct.unpack('<I', bytearray(bin[i:i+4]))[0]) #statusFlags
    i += 4
    dataSet.append(struct.unpack('<I', bytearray(bin[i:i+4]))[0]) #gainIdx
    i += 4
    dataSet.append(struct.unpack('<I', bytearray(bin[i:i+4]))[0]) #adcMin
    i += 4
    dataSet.append(struct.unpack('<I', bytearray(bin[i:i+4]))[0]) #adcMax
    i += 4
    dataSet.append(struct.unpack('<f', bytearray(bin[i:i+4]))[0]) #revTime
    i += 4
    dataSet.append(struct.unpack('<f', bytearray(bin[i:i+4]))[0]) #misAdj
    i += 4
    dataSet.append(struct.unpack('<f', bytearray(bin[i:i+4]))[0]) #theta
    i += 4
    dataSet.append(struct.unpack('<f', bytearray(bin[i:i+4]))[0]) #eta
    i += 4
    dataSet.append(struct.unpack('<f', bytearray(bin[i:i+4]))[0]) #DOP
    i += 4
    dataSet.append(struct.unpack('<f', bytearray(bin[i:i+4]))[0]) #Ptotal

    return dataSet


try:
    res = []
    i = 0
    j = 0
    while i < 200 and j < 50000:
        #Query binary pax data. Might contain 0, 1 or 2 calculation results
        device.write('SENS:DATA:OLD:BIN?')
        binVal = device.read_bytes(2)
        length = struct.unpack('<H', bytearray(binVal[0:2]))[0]
        j += 1
        #Contains any results?
        if length > 0:
            #Read the results
            binVal = device.read_bytes(length)
            #Parse first binary result and add to result list
            res.append(parseBinPax1000Data(binVal[0:52]))
            i+=1

            #Parse second optional binary result and add to result list
            if length > 52:
                res.append(parseBinPax1000Data(binVal[52:104]))
                i+=1
finally:
    # Always try to stop motor and close the connection 
    try:
        device.write('SENS:CALC 0;:INP:ROT:STAT 0')
        device.close()
    except Exception:
        pass

#Do the data processing
lastRev = 0
lastTimeStamp = 0
outputData = [] 

for data in res:
    curRev = data[0] # revCount, waveplate half rotations count (Basic scan cycles).
    curTime = data[1] # timeStamp, scan data acquisition timestamp (Arbitrary unit from device).
    paxopmode = data[2] # Measurement mode
    statusFlags= data[3] # Scan evaluation flags
    gainIdx= data[4] # The index of the trans impedance amplifier (TIA) range that was used for a scan
    adcMin = data[5] # Minimum ADC value in scan
    adcMax = data[6] # Maximum ADC value in scan
    revTime = data[7] # The time the waveplate needed for the revolution during which the measurement took place in seconds. (1/s)
    misAdj = data[8] # The misalignment value from a scan
    theta = data[9] # azimuth, the azimuth value in [rad]
    eta = data[10] # ellipticity, the ellipticity value in [rad]
    dop = data[11] # the degree of polarisation value (DOP). Value 1.0 = 100% DOP
    Ptotal = data[12] # The total optical power value in [W]

    #Assert revolution count is ascending
    if curRev < lastRev:
        print(f'Rev is lower {data[0]} < {lastRev}')

    #Assert timestamp is ascending
    if curTime < lastTimeStamp:
        print(f'Time is lower {curTime} < {lastTimeStamp}')
  
    outputData.append([curTime - lastTimeStamp, theta, eta, dop, Ptotal]) 

    #Update last values for comparison
    lastRev = curRev
    lastTimeStamp = curTime

#print(*outputData[-500:],sep='\n') #interval, azimuth, ellipticity, dop, Ptotal
print("revCount; timeStamp; PAXopmode; statusFlags; gainIdx; adcMin; adcMax; revTime; misAdj; theta; eta; DOP; Ptotal;")
print(*res,sep='\n') #revCount; timeStamp; PAXopmode; statusFlags; gainIdx; adcMin; adcMax; revTime; misAdj; theta; eta; DOP; Ptotal;

#sys.exit(1)
sys.exit(0)


