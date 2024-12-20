## Included Example

### Thorlabs Optical Spectrum Analyzers
In this folder you will find sample codes showing how to control and acquire from
Thorlabs Optical Spectrum Analyzers (OSAs). The examples work on the OSA20X and OSA30X series.

There are 5 examples in this folder:

* [Example 1 - Measure a spectrum](./Thorlabs_OSA_example_01.py)
* [Example 2 - Measure spectra using all different sensitivities and resolutions, save them to files](./Thorlabs_OSA_example_02.py)
* [Example 3 - Load a spectrum or interferogram from an .spf2 file, perform wavemeter analysis on interferogram, or peak track on spectrum](./Thorlabs_OSA_example_03.py)
* [Example 4 - Continuous acquisition with wavemeter and peak detection. Displayed live using matplotlib](./Thorlabs_OSA_example_04.py)
* [Example 5 - Continuous peak track, plotting peakposition over time](./Thorlabs_OSA_example_05.py)

### Requirements
The examples require an installation of [ThorSpectra 3.35 or later](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=osa), 
which include installation files for the python SDK: pyOSA. The python library requires numpy, and the examples utilize matplotlib for plotting.

You can install pyOSA with pip by navigating to the installation file folder and running

```
pip install .
```

In case FTSLib.dll is not found, please edit the last line of pyOSA/FTSLib.py to
point to the folder of your ThorSpectra installation.


### More information
For details please refer to the SDK documentation pyosa.pdf located in your ThorSpectra Programs folder.
