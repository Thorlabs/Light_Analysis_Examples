## Included Example

### Thorlabs PMxxx Power Meters
This sample code shows how you can control a Thorlabs PMxxx Power Meter in Python. It can be used with all types of Thorlabs power meters, e.g. PM100D, PM400.

It uses the ctypes library to load the DLL file for these power meters. This library needs to be installed separately on the computer.


Please note that the code consists of two files:

- **TLPM.py:** This file contains the class definition for the class TLPM. This class implements the methods ...
- **PMxxx using ctypes - Python 3.py:** This is the actual example code. It connects to the power meter, makes the necessary settings and then reads and displays power values.


Additional Python example codes are included in the installation package of the "Optical Power Monitor" software. You can find these codes in this folder after the installation:

```
C:\Program Files (x86)\IVI Foundation\VISA\WinNT\TLPM\Examples\Python
```
