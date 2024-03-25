# Included Examples

## Thorlabs PMxxx Power Meters
In this folder you can find sample codes show how you can control a Thorlabs PMxxx Power Meter in C++ using the TLPMx driver dll. 

 - **Burst Mode:** This sample shows how to configure and use the Power Meter in burst mode. In burst mode an external hardware trigger causes a fixed amount of measurements beeing taken and stored in an device internal intermediate memory. For closer details read [Readme](Burst%20Mode).
 - **Fast Mode:** This sample shows how to configure and query the Power Meter fast measurement stream. Fast measurement stream contains all values beeing sampled by Meter. For closer details read [Readme](Fast%20Mode).
 - **Scope Mode:** This sample shows how to configure and use the Power Meter like an oszilloscope to measure software or hardware triggered fast signals. For closer details read [Readme](Scope%20Mode).

## Environment
The folder contains a Visual Studio Solution grouping all samples in this folders as projects.

## TLPMx.dll
To get the TLPMx.dll install the Optical Power Monitor (OPM) Application. You can download it [OPM](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=OPM)
here. After installation the .dll can be found in the folders:

- 64-bit ```C:\Program Files\IVI Foundation\VISA\Win64\Bin```
- 32-bit: ```C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin```
