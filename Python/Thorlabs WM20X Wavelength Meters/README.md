## Included Example

### Thorlabs WM20X Wavelength Meters
In this folder you will find sample codes showing how to control and acquire from
Thorlabs WM20X Wavelength Meters.

There are 4 examples in this folder:

* [Example 1 - Read the wavelength using TCP](./Thorlabs_WM_example_01.py)
* [Example 2 - Read the wavelength using TLWAVE dll (USB/TCP)](./Thorlabs_WM_example_02.py)
* [Example 3 - Read the wavelength using RS232](./Thorlabs_WM_example_03.py)
* [Example 4 - Set fast mode, then read wavelength and estimated power](./Thorlabs_WM_example_04.py)


### Requirements
* The example with TCP-connection is cross-plattform compatible, and uses only native python.

* The example with USB connection requires windows and installation of [Optical power meter software](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=OPM), which includes the USB-driver as well as the needed TLWAVE dll. The DLL is wrapepd by PyTLWAVE.py which is found in the same folder as the example.

* The example with RS232-connection is cross-plattform compatible, but utilizes pyserial.

### More information
For details about the available SCPI commands please refer to the instrument manual.
