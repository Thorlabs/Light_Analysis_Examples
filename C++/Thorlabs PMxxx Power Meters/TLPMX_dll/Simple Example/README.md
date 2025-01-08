# Example Description
The sample code shows how to control a powermeter in C++. In the example the available powermeter is found, a connection is established and device parameters and a measurement value is measured and displayed.

# Instructions for Use
Guides written for this example is written with Microsoft's Visual Studio in mind. Other IDEs can be used, but instructions are not provided in this repository.
1. Create a new VC++ project file or open the existed VC++ project file;
2. Under the Solution Explorer, right click the Source Files, then add the Powermeter Simple Example.cpp to the Source Files;
3. Set the path of the TLPMX.h header file according to the bit of the project you want to build:  
a. Open Project\Properties\Configuration Properties\C/C++\General  
b. Enter the path of the header files into Additional include Directories (C:\Program Files (x86)\IVI Foundation\VISA\WinNT\include or C:\Program Files\IVI Foundation\VISA\Win64\include)
4. Set the path of the TLPMX library according to the bit of the project you want to build:  
a. Open Project\Properties\Configuration Properties\Linker\General  
b. Enter the path of the library files into Additional Library Directories (C:\Program Files (x86)\IVI Foundation\VISA\WinNT\lib\msc or C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\msc)
5. Set the additional depended library:  
a. Open Project\Properties\Configuration Properties\Linker\Input  
b. Add the additional depended libraries into Additional Dependencies (TLPMX_32.lib; or TLPMX_64.lib;).