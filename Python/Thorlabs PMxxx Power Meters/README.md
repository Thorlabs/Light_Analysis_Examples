## Included Example

### Thorlabs PMxxx Power Meters Control
This sample code shows how you can control a Thorlabs PMxxx Power Meter in Python. It can be used with all types of Thorlabs power meters which use the TLPM driver.

It uses the ctypes library to load the DLL file for these power meters. This library needs to be installed separately on the computer.

Please note that the example consists of two files:

- **TLPM.py:** This file contains the class definition for the class TLPM which also includes the method definitions. The constants which are used by this class are defined here as well.

Please note that the TLPM DLL files are loaded in the "LoadLibrary" commands in lines 239 and 241. Depending on the used programming environment and the system settings, these lines might need to be changed slightly to make sure that Python finds these files.

This line will look for the DLL file in the current folder :

```
self.dll = cdll.LoadLibrary(".\TLPM_64.dll")
```

This line will look for the DLL file in the ... folders:

```
self.dll = cdll.LoadLibrary("TLPM_64.dll")
```

This line will look for the DLL file at the given path:

```
self.dll = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPM_64.dll")
```

- **PMxxx using ctypes - Python 3.py:** This is the actual example code. It connects to the power meter, makes the necessary settings and then reads and displays power values.

Please note that the information in the class definition can be used in programming environments which have intelligent code completion features (e.g. Visual Studio Code). So it is recommended to use a programming environment like this to take full advantage of the information in the class definition.

Additional Python example codes are included in the installation package of the "Optical Power Monitor" software. You can find these codes in this folder after the installation:

```
C:\Program Files (x86)\IVI Foundation\VISA\WinNT\TLPM\Examples\Python
```
