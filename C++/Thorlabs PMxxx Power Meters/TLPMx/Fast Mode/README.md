# C++ Fast Mode Example
This C++ sample code demonstrates how to query fast measurement stream of Thorlabs Power Meter using the
Thorlabs instrument driver TLPMx.dll. Fast mode allows to fetch all measurement results of the meter as constant data stream. 

# Details 

The fast measure stream needs to be queried as fast as possible to prevent data loss. The meter 
only buffers the recent 10 ms of data in the device. The fast measure stream does not support 
averaging or dBm unit. Please refer to the Meter datasheet to get the fast mode data rate. 
For PM5020 this is 100000 Samples per Seconds. 

## Limitations
Please be aware the stream requires a high transfer bandwidth. Because of this you can not use 
serial interface to query fast measurement data. Also slow network connections can cause a 
loss of data. For closer details about scope mode read 
[SCPI command documentation](../commandDocu/pm5020.html). 

## TLPMx.dll
To get the TLPMx.dll install the Optical Power Monitor (OPM) Application. You can download it here
[]. After installation the .dll can be found in the folders:

- 64-bit ```C:\Program Files\IVI Foundation\VISA\Win64\Bin```
- 32-bit: ```C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin```

## Supported Meters
- PM103
- PM103E
- PM5020
