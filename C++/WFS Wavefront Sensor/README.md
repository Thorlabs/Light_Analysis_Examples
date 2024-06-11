# Example Description
The sample code shows how to control a WFS wavefront sensor in C++. In the example the available wavefront sensors are found, a connection is established, several parameters including black level, noise floor and pupil are set, beam position and wavefront value are measured and displayed.


# Special Reminder
If the project is 64-bit and Thorlabs's camera software ThorCam is installed in the PC, the example may pop up an error, saying that "The ordinal 540 could not be located in the dynamic link library C:\Program Files\IVI Foundation\VISA\Win64\Bin\WFS_64.dll".  
Please copy the uc480_64.dll from C:\Program Files\IVI Foundation\VISA\Win64\Bin, and paste it to ...\x64\Debug in the project folder to fix the error. 


# Instructions for Use
Guides written for this example is written with Microsoft's Visual Studio in mind. Other IDEs can be used, but instructions are not provided in this repository.
1. Create a new VC++ project file or open the existed VC++ project file;
2. Under the Solution Explorer, right click the Source Files, then add the WFS_Example.cpp to the Source Files;
3. Set the path of the WFS header file according to the bit of the project you want to build:  
a. Open Project\Properties\Configuration Properties\C/C++\General  
b. Enter the path of the header files into Additional include Directories (C:\Program Files (x86)\IVI Foundation\VISA\WinNT\include or C:\Program Files\IVI Foundation\VISA\Win64\include)
4. Set the path of the WFS library according to the bit of the project you want to build:  
a. Open Project\Properties\Configuration Properties\Linker\General  
b. Enter the path of the library files into Additional Library Directories (C:\Program Files (x86)\IVI Foundation\VISA\WinNT\lib\msc or C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\msc)
5. Set the additional depended library:  
a. Open Project\Properties\Configuration Properties\Linker\Input  
b. Add the additional depended libraries into Additional Dependencies (WFS_32.lib; or WFS_64.lib;).