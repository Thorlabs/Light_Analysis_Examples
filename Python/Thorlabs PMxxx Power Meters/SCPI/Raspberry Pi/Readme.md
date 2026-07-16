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
In order to get the permission to access the power meter, create usbgroup and add your user:
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

