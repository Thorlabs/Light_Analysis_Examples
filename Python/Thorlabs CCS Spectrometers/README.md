## Included Examples

### Thorlabs CCS Spectrometer Control
These sample codes show how you can control a Thorlabs CCS spectrometer in Python.
They uses the ctypes library to load the DLL file for these spectrometers and the Matplotlib library to plot the measured spectrum. These libraries need to be installed separately on the computer.

Please note that the resource name (“USB0::0x1313::…”) in the sample code needs to be adjusted to the used spectrometer type and unit.

### CCS using ctypes - Python 3.py

This example shows the basic operation of a CCS spectrometer. The necessary settings are made, a spectrum is recorded and then plotted.

### CCS using ctypes - Python 3 - absorption measurement.py

This example shows a more advanced operation for an absorption measurement. A reference spectrum (without sample) and a spectrum with sample is recorded. The absorption and the optical density of the sample are calculated from these spectra. All the data is plotted.
