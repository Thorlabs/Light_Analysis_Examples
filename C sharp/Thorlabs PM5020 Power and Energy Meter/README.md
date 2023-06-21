## Example Description
This example shows how you can control a Thorlabs PM5020 Power and Energy Meter in C Sharp. The example includes the initialization, parameter reading, parameter setting and value display. 
If two power sensors or two energy sensors are connected to the PM5020 simultaneously, data processing like normalization, sum and difference functions are also available.  
This example is also compatible with single-channel meters like PM100 series.

## Instructions for Use

Before building and running this example. Please make sure you have downloaded the Optical Power Meter app from here: https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=OPM

1) Set the project platform under the "properties" menu. This should be set to match the intended development platform e.g. x64 for deployment on 64-bit machines. 

2) Add the library as a reference by right clicking the References section of the Solution Explorer. Navigate to the appropriate folder for your platform target: 
    * 32-bit: C:\Program Files (x86)\Microsoft.NET\Primary Interop Assemblies\Thorlabs.TLPMX_32.Interop.dll
    * 64-bit: C:\Program Files (x86)\Microsoft.NET\Primary Interop Assemblies\Thorlabs.TLPMX_64.Interop.dll
  
   This solution is pre-built for 64-bit systems, so it may be needed to delete and re-add the reference to 32-bit dll. 
