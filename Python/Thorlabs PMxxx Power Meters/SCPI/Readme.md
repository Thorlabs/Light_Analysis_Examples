# Python example on SCPI command level

This folder contains python examples on [SCPI](https://de.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments) command level. The examples are not using TLPMx driver but send
text base low level commands to communicate with the Thorlabs Power Meter. Most examples rely on Thorlabs
anyvisa library. Some others use the third-party pyvisa python library based on National Instruments :tm: driver.

## Included Examples

### Simple Example
The example ```PMxxx_SCPI_pyvisa.py``` shows how to to open a powermeter connected with USB using the pyvisa library, make settings and get measurement values. It will not work for ethernet connection, check the anyvisa examples for that case.

### Fast Mode
Demonstrates how to query fast measurement stream of Thorlabs Power Meter. 
Fast mode allows to fetch all measurement results of the meter as constant data stream.
For closer details refer to [Readme](fastMode). Available for PM103, PM103E and PM5020.

### Parallel Peak Measurement Example
Demonstrates how to use multiple Thorlabs Power Meters within one experiment to measure 
peak energy in Joule simultaniously. The example is based on SCPI commands and uses the anyvisa Thorlabs library.
For closer details refer to [Readme](parallelPeakMeas).  Available for PM103, PM103E and PM5020.

### Scope Examples
The Thorlabs Power Meters supports Scope Mode to measure and store a software or hardware triggered measurement sequence within the device memory.
For closer details refer to [Readme](scopeMode). Available for PM6x, PM103, PM103E and PM5020.

### Open Anyvisa
Minimal template script ```PMxxx_SCPI_OpenAnyvisa.py``` to open a known instrument resource using anyvisa library.

### Search Anyvisa
Minimal template script ```PMxxx_SCPI_SearchAnyvisa.py``` to run instrument search and open one of the devices found using anvisa library.

## SCPI Command documentation
For most of the Thorlabs Powermeter there is a detail [SCPI command documentation](commandDocu) in .html file format available. 

## USB instrument driver
Thorlabs Power Meters USB interface enumerate for communication with [Test and Measurement Class(TMC)](https://de.wikipedia.org/w/index.php?title=Test_and_Measurement_Class). 
This USB class requires a custom driver by Thorlabs or National Instruments :tm:. You can install both drivers on your local 
PC and switch between the drivers with the Thorlabs Driver Switcher executable.

### TLVisa 

After installation your Power Meter will use the Thorlabs Visa TMC driver. This allows communication via all device interfaces 
like USB, Serial, Ethernet, Bluetooth and Bluetooth LE. Thorlabs Visa is available for Windows only at the moment. To use this driver in python
you have to use anyvisa Python library. You will not find the device with pyvisa library.

You can download the recent [aynvisa Python Wheel](anvisa) installer and install it with the command:

```
python -m pip install anyvisa*.whl
```


### National Instruments :tm: Visa

If you want to control the Power Meter on Linux, with pyvisa library or with SCPI commands within your CVI or LabView application, 
you have to install National Instruments :tm: Visa Runtime (May be installed already if you installed NI LabView or NI CVI). 
Once installed you must switch the driver for the Power Meter manually by using Thorlabs Driver Switcher or Windows 
Device Manager (Experts only). Once the runtime is installed and driver has been switched you can install pyvisa python library
via command. 

```
python -m pip install pyvisa
```

Note: pyvisa does communicate with Thorlabs Ethernet or Bluetooth LE device interfaces.
