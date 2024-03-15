# Fast Mode Example
This command line sample demonstrates how to query fast measurement stream of Thorlabs Power Meter. 
Fast mode allows to fetch all measurement results of the meter as constant data stream. 

# Details 

The fast measure stream needs to be queried as fast as possible to prevent data loss. The meter 
only buffers the recent 10 ms of data in the device. To speed up data exchange a binary format 
is used to exchange data. The fast measure stream does not support averaging or dBm unit. 
Please refer to the Meter datasheet to get the fast mode data rate. For PM5020 this is 100000 
Samples per Seconds. 

## Limitations
Please be aware the stream requires a high transfer bandwidth. Because of this you can not use 
serial interface to query fast measurement data. Also slow network connections can cause a 
loss of data. For closer details about scope mode read [SCPI command documentation](TODO). 

## anyvisa python Library
You can download anyvisa library wheel in this Github repository. Please refer to this [README](TODO) how to install it. 

## Supported Meters
- PM103
- PM103E
- PM5020
