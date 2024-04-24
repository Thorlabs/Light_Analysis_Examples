## Example Description
The sample code shows how to control a BP209 beam profiler in C++. In the example the available beam profilers are found, a connection is extablished, several parameters are set, several output values are displayed and a 2D image is shown.

The code uses OpenCV library to create the images. The OpenCV library needs to be installed on the computer. 

## Instructions for Use
# Install and setup OpenCV for C++ in Windows
Please following the steps below to setup the OpenCV for C++ in Windows:
1. Download the OpenCV:
Download the OpenCV from its offical website https://opencv.org/releases/. For a Windows System, please click on the 'Windows' button. 
2. Extract the OpenCV:
Run the downloaded executable file and extract the OpenCV to the target folder.
3. Set the Environmental Variables:
a. Right-click on 'This PC', then press on 'Properties'. Then press on 'Advanced system settings'. A new window will open.
b. Click on 'Environmental Variable' from there. Another window will open. 
c. In the 'system variables' use scroll bar and select 'path'. Then click 'Edit'. Another window will open.
d. Click 'New' and 'Browse...' accordingly, then find the location of the Extracted OpenCV folder. There's a folder named 'bin' under ...\opencv\build\x64\vc16\, Please add the path of 'bin' to the 'Edit environment variable' then click 'OK' to finish the environmental Variables setting.
P.S. Recent Versions of OpenCV only provide 64-bit libs and dlls. To build a 32-bit version, please refer to the guides in https://docs.opencv.org/4.x/d3/d52/tutorial_windows_install.html  


# Link libraries with the Proejct
Guides written for this example is written with Microsoft's Visual Studio in mind. Other IDEs can be used, but instructions are not provided in this repository.
1. Create a new VC++ project file or open the existed VC++ project file
2. Link the OpenCV library with Microsoft's Visual Studio:
a. Open Project\Properties\Configuration Properties\VC++ Directories\General
b. Enter the path...\opencv\build\include into Include Directories
c. Enter the path ...\opencv\build\x64\vc16\lib into Library Directories
d. Open Project\Properties\Configuration Properties\Linker\Input
3. Under the Solution Explorer, right click the Source Files, then add the BP209_2D_output.cpp to the Source Files
4. Set the path of the BP209 header file according to the bit of the project you want to build:
a. Open Project\Properties\Configuration Properties\C/C++\General
b. Enter the path of the header files into Additional include Directories (C:\Program Files (x86)\IVI Foundation\VISA\WinNT\include or C:\Program Files\IVI Foundation\VISA\Win64\include)
5. Set the path of the BP209 library according to the bit of the project you want to build:
a. Open Project\Properties\Configuration Properties\Linker\General
b. Enter the path of the library files into Additional Library Directories (C:\Program Files (x86)\IVI Foundation\VISA\WinNT\lib\msc or C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\msc)
6. Set the additional depended library:
a. Open Project\Properties\Configuration Properties\Linker\Input
b. Add the additional depended libraries into Additional Dependencies (visa32.lib; or visa64.lib;);
c. Add 'opencv_worldXXXd.lib;' and 'opencv_worldXXX.lib;' into Additional Dependencies(here 'XXX' means the version of the downloaded OpenCV, e.g. if the version is 4.9.0, you should enter opencv_world490d.lib and opencv_world490.lib)