## Example Description
This example shows how you can control a Thorlabs CCS spectrometer in C Sharp.The necessary settings are made; the continuous scanning and display are realized with a set integration time.

## Instructions for Use

Before building and running this example. Please make sure you have downloaded the CCS spectrometers app from here: https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=CCS

1) Set the project platform under the properties menu. This should be set to match the intended development platform e.g. x64 for deployment on 64-bit machines. 

2) Add the CCS library as a reference by right clicking the References section of the Solution Explorer. Navigate to the appropriate folder for your platform target: 
    * 32-bit: C:\Program Files (x86)\Microsoft.NET\Primary Interop Assemblies\Thorlabs.ccs.interop.dll
    * 64-bit: C:\Program Files (x86)\Microsoft.NET\Primary Interop Assemblies\Thorlabs.ccs.interop64.dll
  
   This solution is pre-built for 64-bit systems, so it may be needed to delete and re-add the reference to this dll. 
