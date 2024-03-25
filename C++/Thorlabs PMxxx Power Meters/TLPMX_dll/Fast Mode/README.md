# C++ Fast Mode Example
This C++ sample code demonstrates how to query fast measurement stream of Thorlabs Power Meter using the
Thorlabs instrument driver TLPMx.dll. Fast mode allows to fetch all measurement results of the meter as constant data stream. 

# Details 

The fast measure stream needs to be queried as fast as possible to prevent data loss. The meter 
only buffers the recent 10 ms of data in the device. The fast measure stream does not support 
averaging or dBm unit. Please refer to the Meter datasheet to get the fast mode data rate. 
For PM5020 this is 100000 Samples per Seconds. 

For more technical background information about Fast Mode refer to SCPI command description. You can find a description for every Meter in the commandDocu folder. For example the PM103 SCPI command description html file.

## Limitations
Please be aware the stream requires a high transfer bandwidth. Because of this you can not use 
serial interface to query fast measurement data. Also slow network connections can cause a 
loss of data. 

## Supported Meters
- PM103
- PM103E
- PM5020
