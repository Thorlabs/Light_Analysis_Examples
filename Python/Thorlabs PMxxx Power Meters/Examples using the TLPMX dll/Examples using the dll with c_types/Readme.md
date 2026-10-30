## Included Examples

In this folder you can find sample codes show how you can control a Thorlabs PMxxx Power Meter in Python using TLPMx driver dll. 
They can be used with Thorlabs power meters which are compatible with the TLPMX drivers.
For more information on Thorlabs power meters, see https://www.thorlabs.com/optical-power-and-energy-meters

**PM_SimpleExample:** It connects to the power meter, makes the necessary settings and then reads and displays power values. For all powermeters that are compatible with OPM software.

**PM5020_ExtendedExample:** Example for the two channel power meter PM5020. It makes the necessary settings and then reads and displays power values. 
This sample is also compatible with single-channel consoles.

**PM103E_connectwithIP:** Shows how to connect to ethernet if the IP is known.

**PM103E_connectwithNetSearch:** Shows how to connect to ethernet using netsearch.

**PM_WriteReadRaw:** Shows how to use read/write raw to send SCPI commands. For all powermeters that are compatible with OPM software.

**PM_ScopeModeSWTrigger:** Shows how to use an oscilloscope like mode to get a highly resolved snapshot of the signal. Starts without hardware trigger. For PM103x, PM100D3 and PM5020

**PM_ScopeModeHWTrigger:** Shows how to use an oscilloscope like mode to get a highly resolved snapshot of the signal. Triggered by signal incoming on the detector or TTL signal. For PM103x, PM100D3 and PM5020.

**PM_FastMode:** Shows how to access the power meter fast measurement data stream. For PM103x and PM5020.

**PM_PeakMode:**  Shows how to measure peak values. For PM100D2, PM100D3, PM103x and PM5020.

**PM_FastPeakMode:** Shows how to measure peak values for repetition rates higher than 1 kHz. For PM103x and PM5020.

## Notes

The examples require the library TLPMX_64.dll, which is installed together with the Optical Parameter Monitor software, downloadable from the website. https://www.thorlabs.com/software-pages/opm/

The TLPMX_64.dll will be installed in the folder C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll, the 32 bit version in C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin.

The TLPMX command reference is installed in C:\Program Files (x86)\IVI Foundation\VISA\WinNT\TLPMX\Manual.


