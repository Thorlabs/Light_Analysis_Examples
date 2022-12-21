## Included Examples

### Thorlabs OSA Open, Set Settings, and Acquire Spectrum
This sample code shows how you can control a Thorlabs OSA in Python.
It uses the pythonNet library to load the DLL for the OSA. This library needs to be installed separately on the computer.

The code goes through initialization of the spectrometer and optional virtual spectrometer. Settings are then set for the OSA and a callback method is used to acquire the spectrum and save to file. File is by default saved to the current working directory for your python project. 
