"""
Thorlabs_OSA_example_01
Example Date of Creation: 2024-04-24
Example Date of Last Modification on Github: 2024-04-24
Version of Python: 3.12.2
Version of the Thorlabs SDK used: ThorSpectra 3.31
==================
Example Description: Read a spectrum from a Thorlabs Optical Spectrum analyzer
"""
import logging
import pyOSA
from matplotlib import pyplot as plt
print("""

################################################################################
# Example - Read a spectrum from an OSA                                        #
################################################################################

""")
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format)
logger = logging.getLogger('pyOSA')
logger.setLevel(logging.WARNING) # Available logging levels: DEBUG, INFO, WARNING, ERROR

virtual_osa = False

if not virtual_osa:
    # Initialize the OSA connection
    osa = pyOSA.initialize()
else:
    # Create a virtual OSA to enable testing with no physical OSA connected
    pyOSA.create_virtual_OSA20X(spectrometer_index=0, model='OSA201C', source_type=0, peak_num=1, centerWavelengths_nm=[650], FWHMs_nm=[1], peak_amplitudes=[1])
    #pyOSA.create_virtual_Redstone(spectrometer_index=0, model='Redstone305', source_type=0)
    osa = pyOSA.initialize(virtual_nr=1)

osa.setup()
acquisitions = osa.acquire(number_of_acquisitions=1)

# Take the last acquisition from the list of 1 acquisitions
acquisition = acquisitions[-1]
spectrum = acquisition["spectrum"]

# Now the x- and y-values can be obtained from spectrum.
x = spectrum.get_x()
y = spectrum.get_y()

# Getting the labels for the different axes
xlabel = spectrum.get_xlabel()
ylabel = spectrum.get_ylabel()

# Plot the measured spectrum
plt.figure()
plt.plot(x, y)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.show()

print("fin")