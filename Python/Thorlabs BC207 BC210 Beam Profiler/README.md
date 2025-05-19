# TLBC2 sample 2D output

The sample code shows how to control a BC207 or BC210 beam profiler in Python.
In the example the available beam profilers are found, a connection is extablished, several parameters are set, several output values are displayed and a 2D image is shown.
 
The code uses the Python wrapper TLBC2.py, which loads the dll file for the beam profiler.
Conversion between Python data types an C data types is done using the ctypes library.
The matplotlib library is used to create the image and the numpy library is a requirement for the matplotlib library. 
These libraries need to be installed separately on the computer.
