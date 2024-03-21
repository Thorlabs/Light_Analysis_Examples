## Example Description
This example shows some of the functionality of PMXXX series power meter with SCPI commands.
It demonstrates how to connect the power meter, make settings, and get the power values.

## Instructions for Use

If Thorlabs's "Optical Power Monitor" software has already been installed in the PC, please switch the driver to "PM100D(NI-VISA)" before running the project. 

Guides written for these examples are written with Microsoft's Visual Studio in mind. Other IDEs can be used, but instructions are not provided in this repository.
1) Create a new VC++ project file or open the existed VC++ project file

2) Under the Solution Explorer, right click the Source Files, then add the PMXXX_SCPI.cpp to the Source Files

3) Set the path of the header file according to the bit of the project you want to build:   
   a. Open Project\Properties\Configuration Properties\C/C++\General  
   b. Enter the path of the header files into Additional include Directories (**C:\Program Files(x86)\IVI Foundation\VISA\WinNT\include** or **C:\Program Files\IVI Foundation\VISA\Win64\include**)  

4) Set the path of the library according to the bit of the project you want to build:  
   a. Open Project\Properties\Configuration Properties\Linker\General  
   b. Enter the path of the library files into Additional Library Directories (**C:\Program Files(x86)\IVI Foundation\VISA\WinNT\lib\msc** or **C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\msc**)

5) Set additional depended library:  
   a. Open Project\Properties\Configuration Properties\Linker\Input  
   b. Enter the additional depended libraries into Additional Dependencies (**visa32.lib;** or **visa64.lib;**);
