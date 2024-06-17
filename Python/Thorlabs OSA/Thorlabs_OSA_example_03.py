"""
Thorlabs_OSA_example_03
Example Date of Creation: 2024-04-24
Example Date of Last Modification on Github: 2024-04-24
Version of Python: 3.12.2
Version of the Thorlabs SDK used: ThorSpectra 3.31
==================
Example Description: Load and plot spectrum or interferogram from an .spf2 file.
"""
import sys
import tkinter.filedialog

import matplotlib.pyplot as plt

import pyOSA

print('''

#################################################################################################
# Example - Loading an SPF2 file.                                                               #
# If the file holds an interferogram, the central wavelength is determined using the wavemeter. #
# If the file holds a spectrum, its units are converted to the desired ones and peak track      #
# analysis is applied.                                                                          #
# Some instrument settings are extracted from the loaded data and finally, the data is plotted. #
#################################################################################################

''')

x_unit_to_use = 'nm (vac)'    # See the readme for possible units, e.g., 'THz' or 'eV'
y_unit_to_use = 'dBm (norm)'  # See the readme for possible units, e.g., 'dBm' or 'mW'
                              # (The "(norm)" substring in a y_unit indicates that power density should be used)

# Load a file containing measured data
filetypes = (("SPF2 files", "*.spf2"), ("All files", "*.*"))
filename = tkinter.filedialog.askopenfilename(filetypes=filetypes)
measurements = pyOSA.core.load_spf2_file(filename)

# For the purpose of this example, we want to use just a single spectrum or interferogram.
measurement = measurements[0]

if not measurement.is_valid():
    print("This measurement has problems with data quality")

if measurement.is_spectrum():

    # measurement contains a spectrum
    measurement_type_str = 'Spectrum' # Used for the plot

    # Unit conversion - It is possible to convert the spectrum to specific x- and y-axis units.
    measurement.convert_spectrum(x_unit=x_unit_to_use, y_unit=y_unit_to_use)

    # Peak detection
    # It is possible to adjust the threshold level, peaks below this threshold are ignored
    # If the threshold argument is omitted, the threshold is automatically adjusted
    # peak_centers, peak_heights, peak_widths, peak_lefts, peak_rights = OSA_core.apply_peak_track_on_spectrum([measurement])
    threshold = measurement.y_min + (measurement.y_max - measurement.y_min) * 0.5
    max_nr_of_found_peaks = 10  # Maximum nr of peaks found and returned
    min_peak_height_db = 3      # The min height, measured from the peak height and down, for a peak to be considered as peak
    peaks = pyOSA.analysis.peak_track(measurement,
                                          threshold=threshold,
                                          max_peaks=max_nr_of_found_peaks,
                                          min_peak_height_db=min_peak_height_db)
    peak_centers, peak_heights, peak_widths, peak_lefts, peak_rights = peaks

elif measurement.is_interferogram():

    # measurement contains an interferogram
    measurement_type_str = 'Interferogram' # Used for the plot

    # Wavelength meter applied on the interferogram
    wavemeterdata = pyOSA.analysis.wavemeter(measurement, spectral_unit=x_unit_to_use)
    wavemeter_value = wavemeterdata["wavelength"]
    wavemeter_error = wavemeterdata["error"]
    
    print(f'The wavemeter detected the {pyOSA.units.get_formatted_x_quantity(x_unit_to_use).lower()} to '
          f'{wavemeter_value} ± {wavemeter_error} {pyOSA.units.get_formatted_x_unit(x_unit_to_use)}\n')

else:
    print('Error: This file does not contain neither a spectrum nor an interferogram. Program will exit.')
    sys.exit()

# Now the x and y values can be obtained from spectrum/interferogram
x = measurement.get_x()
y = measurement.get_y()

# Grab some of the instrument settings used when acquiring the loaded data
# For more attributes, see the spectrum_t.py file (or the spectrum_t struct in FTSData.h)
model = measurement.get_model()
serial = measurement.get_serial_number()
resolution = measurement.get_resolution()
sensitivity = measurement.get_sensitivity()

plt.figure(figsize=(12, 6))
plt.plot(x, y)
if measurement.is_spectrum():
    for peak_center, peak_height in zip(peak_centers, peak_heights):
        if peak_center > 0:
            # x-value > 0 -> this is found peak
            plt.scatter(peak_center, peak_height)
plt.title(f'{filename}\n{measurement_type_str} from {model} ({resolution} Res. & {sensitivity} Sens.)')
plt.xlabel(measurement.get_xlabel())
plt.ylabel(measurement.get_ylabel())
plt.show()
