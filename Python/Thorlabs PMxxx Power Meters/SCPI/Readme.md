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
Minimal template script ```PMxxx_SCPI_SearchAnyvisa.py``` to run instrument search and open one of the devices found using anyvisa library.

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

If you want to control the Power Meter with the pyvisa library and with SCPI commands, 
you have to install National Instruments :tm: Visa Runtime (May be installed already if you installed NI LabView or NI CVI).
This works also on many Linux systems.
On Windows, you must then switch the driver for the Power Meter manually by using Thorlabs Driver Switcher or Windows 
Device Manager (Experts only). Once the runtime is installed and driver has been switched you can install pyvisa python library
via command. 

```
python -m pip install pyvisa
```

Note: pyvisa does not communicate with Thorlabs Ethernet or Bluetooth LE device interfaces.

### Raspberry Pi 4 
On Raspberry Pi with ARM Linux, both TLVisa and NI Visa do not work. Another approach is using the Pyvisa-Py backend.
We tested the following procedure on Raspberry Pi 4, Linux 13 (Trixie), PM100D3.
```
sudo apt update && sudo apt upgrade -y
```
Most Raspberry Pi OS versions come with Python pre-installed. Check with:
```
python3 --version
```
If Python is not already installed:
```
sudo apt install python3 python3-pip -y
```
If libusb is not installed:
```
sudo apt install libusb-1.0-0-dev
```
Install Pyvisa and Pyvisa-Py:
```
sudo apt install python3-pyvisa
sudo apt install python3-pyvisa-py
sudo apt install python3-usb
sudo apt install zeroconf 
```
In order to get the permission to acces the power meter, create usbgroup and add your user:
```
sudo groupadd usbgroup 
sudo usermod -aG usbgroup $USER
```
then set a udev rule, open the following file to edit:
```
sudo nano /etc/udev/rules.d/99-usbgroup.rules
```
(create directory and file if it does not exist)
Insert the following line into the file
```
SUBSYSTEM=="usb", GROUP="usbgroup", MODE="0666"
```
(This is for all USB devices. You can also set more specific rules)
Reload and reboot to activate the rules
```
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo reboot
```
Plug in the powermeter and check with lsusb, if the device is present.
Run in Python:
```
import pyvisa
rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())
inst = rm.open_resource('USB0::4883::32921::P000000064::0::INSTR')#substitute with the actual resource string that you get from the previous command
print(inst.query('*IDN?'))
print(inst.query('MEAS?'))
```
Also see the above ```PMxxx_SCPI_pyvisa.py```

