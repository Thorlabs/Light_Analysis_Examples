## Included Example

### Thorlabs PMxxx Power Meters
In this folder you can find sample codes show how you can control a Thorlabs PMxxx Power Meter in Python using TLPMx driver dll. 
They can be used with Thorlabs power meters which are compatible with the TLPMX drivers.
  
The sample codes in this folder all use the ctypes library to load the DLL TLPMX file for these power meters. 
The ctypes library needs to be installed separately on the computer.
- **TLPMX.py:** This file contains the class definition of the class TLPMX. 
It includes the definitions of methods and constants which are used by this class.

Please note that the TLPMX DLL files are loaded in the "LoadLibrary" commands in lines 239 and 241. 
Depending on the used programming environment and the system settings, these lines might need to be changed slightly 
to make sure that Python finds these files.

This line will look for the DLL file in the current folder :

```
self.dll = cdll.LoadLibrary(".\TLPMX_64.dll")
```

This line will look for the DLL file in the system folders:

```
self.dll = cdll.LoadLibrary("TLPMX_64.dll")
```

This line will look for the DLL file at the given path:

```
self.dll = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll")
```

- **PMxxx using ctypes - Python 3.py:** It connects to the power meter, makes the necessary settings and then 
                                        reads and displays power values.

- **PM5020 using ctypes - Python 3.py:** It connects to the PM5020 dual channel power meter, makes the necessary 
                                        settings and then reads and displays power values. 

- **PM103E_ctypes_connectwithNetSearch:** Find and connect to the PM103E setting a network mask

- **PM103E_ctypes_connectwithIP:** Connect to PM103E using the IP of the powermeter

Additional Python example codes are included in the installation package of the "Optical Power Monitor" software. You can find these codes in this folder after the installation:

```
C:\Program Files (x86)\IVI Foundation\VISA\WinNT\TLPMX\Examples\Python
```
