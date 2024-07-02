# Title: PNA1.py
# Created Date: 2024-05-28
# Last modified date: 2024-05-28
# Python Version: 3.10.6
# Thorlabs DLL version: Kinesis 1.1.0.0

import na_sdk as na
import matplotlib.pyplot as mpl
import time

## Example 1: Saving and plotting data. 
# Creates instance PNA1 with logging enabled. 
# Displays Combined RIN trace in dBc/hz units.
# Logging is only started if a log file name is passed to PNA1 CTOR.
# If the SDK user wants to instantiate a PNA1 instance without logging
# and with the default path to TL_NA_SDK.dll
# user would use the following call: na.PNA1("", "") or na.PNA1().

pna =  na.PNA1("example_log", "../bin/TL_NA_SDK.dll") 
pna.Initialize() # Intializes a connected Noise Analyzer.
noise = pna.AnalyzeNoise()
pna.SaveReference(noise, "example_reference") # Saves the reference data.

select = noise[7] # Selects the Combined RIN trace in dBc/Hz units.
x = []
y = []
for i in range(0, len(select)):
    x.append(select[i][0]) # Arranges x coordinates into a seperate list.
    y.append(select[i][1]) # Arranges y coordinates into a seperate list.
mpl.axes().set_xlabel('Frequency, Hz')
mpl.axes().set_ylabel('dBc/Hz')
mpl.plot(x, y)
mpl.xscale('log')
mpl.yscale('linear')
mpl.show()

pna.Close() # Closes connection to the noise analyzer.

time.sleep(1)

## Example 2: Plotting over time domain. 


pna.Initialize() # Intializes a connected Noise Analyzer.
pna.GetTimeDomainData() # Getting time domain data.
pna.GetTimeDomainPlot() # Getting time domain plot.
high = pna.GetSampleRate(2) #  Selects high sample rate,

x = []
y = []

for i in range(0, len(high)):
    x.append(high[i][0])
    y.append(high[i][1])

mpl.axes().set_xlabel('Time')
mpl.axes().set_ylabel('Volts')
mpl.plot(x, y)
mpl.xscale('linear')
mpl.yscale('linear')
mpl.show()

pna.Close() # Closes connection to the noise analyzer.

time.sleep(1)

## Example 3: Background/reference subtraction. 


pna.Initialize()
noise = pna.AnalyzeNoise()
loaded_data = pna.LoadReference("example_reference.csv", 1) # Loads saved reference.
subtracted_data = pna.SubtractReference(loaded_data[6], noise[4]) # Subtracts loaded reference from measured spectrum.
sub_comb_db =  pna.ComputeDB(subtracted_data)

x = []
y = []

# Displays subtracted data.
for i in range(0, len(sub_comb_db)):
    x.append(sub_comb_db[i][0])
    y.append(sub_comb_db[i][1])

mpl.axes().set_xlabel('Frequency, Hz')
mpl.axes().set_ylabel('dBV^2/Hz')
mpl.plot(x, y)
mpl.xscale('log')
mpl.yscale('linear')
mpl.show()

pna.Close() # Closes connection to the noise analyzer.

time.sleep(1)

## Example 4: Average and combine traces. 


pna.Initialize() # Intializes a connected Noise Analyzer.
averaged_noise = pna.AverageNoiseTraces(50) # Averages noise traces.
avg_comb_rin_db = averaged_noise[7]

x = []
y = []

# Displays Averaged noise as Combined RIN trace in dBc/Hz units.
for i in range(0, len(avg_comb_rin_db)):
    x.append(avg_comb_rin_db[i][0])
    y.append(avg_comb_rin_db[i][1])

mpl.axes().set_xlabel('Frequency, Hz')
mpl.axes().set_ylabel('dBc/Hz')
mpl.plot(x, y)
mpl.xscale('log')
mpl.yscale('linear')
mpl.show()

pna.Close() # Closes connection to the noise analyzer.

time.sleep(1)

# Closes log file. 
pna.CloseLog()
