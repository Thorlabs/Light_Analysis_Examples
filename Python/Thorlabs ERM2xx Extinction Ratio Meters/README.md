## Included Examples

### Thorlabs ERM200_sample.py
This sample code shows how you can control a Thorlabs ERM200, ERM210 or ERM220 extinction ratio meter in Python.
It uses the ctypes library to load the DLL file for these polarimeters. This library needs to be installed separately on the computer.

Please note that the code connects to the first available ERM2xx device. If you have more than one ERM2xx connected, you need to change the index number in this line:

lib.TLERM200_getRsrcName(erm_handle, 0, resource)

### ERM200_PyVisa.py
This sample code shows how you can control a Thorlabs ERM200, ERM210 or ERM220 extinction ratio meter in Python with SCPI commands and PyVisa.
Use Visa drivers to run the example.

