## Included Examples

### Thorlabs PAX1000 Polarimeter Open and Read
This sample code shows how you can control a Thorlabs PAX1000 Polarimeter in Python.
It uses the ctypes library to load the DLL file for these polarimeters. This library needs to be installed separately on the computer.

Please note that the code connects to the first available PAX1000 device. If you have more than one PAX1000 connected, you need to change the index number in this line:

lib.TLPAX_getRsrcName(instrumentHandle, 0, resource)
