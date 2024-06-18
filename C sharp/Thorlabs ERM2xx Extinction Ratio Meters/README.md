## Example Description
This example shows how you can control a Thorlabs ERM2xx Extinction Ratio Meter in C Sharp.


## Instructions for Use

Before building and running this example. Please make sure you have downloaded the ERM200 driver from here: https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=ERM200

1) Set the project platform under the properties menu. This should be set to match the intended development platform e.g. x64 for deployment on 64-bit machines. 

2) Add the ERM200 library as a reference by right clicking the References section of the Solution Explorer. Navigate to the appropriate folder for your platform target: 
    * 32-bit: C:\Program Files (x86)\Microsoft.NET\Primary Interop Assemblies\Thorlabs.ERM200_32.interop.dll
    * 64-bit: C:\Program Files (x86)\Microsoft.NET\Primary Interop Assemblies\Thorlabs.ERM200_64.interop.dll
  
   This solution is pre-built for 64-bit systems, so it may be needed to delete and re-add the reference to this dll. 
