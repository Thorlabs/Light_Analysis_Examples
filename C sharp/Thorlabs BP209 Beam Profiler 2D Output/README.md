## Example Description
This example demonstrates how to draw a 2D reconstructed beam image from the slit scan data of the Thorlabs BP209 Beam Profiler. The example is based on the C# example which is installed to C:\Program Files (x86)\IVI Foundation\VISA\WinNT\TLBP2\Examples during software installation.  


## Instructions for Use

Before building and running this example, please ensure you have downloaded the BP209 driver from here: https://www.thorlabschina.cn/software_pages/ViewSoftwarePage.cfm?Code=Beam 

1) Set the project platform under the Properties menu. It should be set to match the intended development platform e.g. x64 for deployment on 64-bit machines. 

2) Add the BP209 library as a reference by right clicking the References section of the Solution Explorer. Navigate to the appropriate folder for your platform target: 
    * 32-bit: C:\Program Files (x86)\Microsoft.NET\Primary Interop Assemblies\Thorlabs.TLBP2_32.Interop.dll
    * 64-bit: C:\Program Files (x86)\Microsoft.NET\Primary Interop Assemblies\Thorlabs.TLBP2_64.Interop.dll
  
   This solution is pre-built for 64-bit systems, so it may be necessary to delete and re-add the reference to ensure compatibility with your system's architecture. If you are targeting a 32-bit system, you will need to remove the 64-bit reference and add the 32-bit version dll instead.
