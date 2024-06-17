"""
Thorlabs_OSA_example_02
Example Date of Creation: 2024-04-24
Example Date of Last Modification on Github: 2024-04-24
Version of Python: 3.12.2
Version of the Thorlabs SDK used: ThorSpectra 3.31
==================
Example Description: Measure spectra with different resolutions and sensitvities
Save the result in .spf2 file format.
"""
from itertools import product

from matplotlib import pyplot as plt

import pyOSA

print('''

################################################################################
# Example - Measuring spectra in all possible resolutions and sensitivities    #
# Initializing OSA instruments, apply the desired settings, acquiring spectra, #
# and save the spectra to individual files in the .spf2 format                 #
################################################################################

''')

x_unit_to_use = 'nm (vac)'    # see the readme for possible units, e.g., 'THz' or 'eV'
y_unit_to_use = 'dBm (norm)'  # see the readme for possible units, e.g., 'dBm' or 'mW'
                              # (The "(norm)" substring in a y_unit indicates that power density should be used)

virtual_osa = False

if not virtual_osa:
    # Initialize the OSA connection
    osa = pyOSA.initialize()
else:
    # Create a virtual OSA to enable testing with no physical OSA connected
    pyOSA.create_virtual_OSA20X(spectrometer_index=0, model='OSA201C', source_type=0, peak_num=1, centerWavelengths_nm=[650], FWHMs_nm=[1], peak_amplitudes=[1])
    #pyOSA.create_virtual_Redstone(spectrometer_index=0, model='Redstone305', source_type=0)
    osa = pyOSA.initialize(virtual_nr=1)

# Grab the model name of the connected instrument
model = osa.get_model()

# Depending on which OSA model is connected, the possible resolutions and sensitivity settings differ
# The following commands return the allowed settings
available_resolutions = osa.get_available_resolutions()
available_sensitivities = osa.get_available_sensitivities()

print(f'{model} -> Available resolutions: {available_resolutions}')
print(f'{model} -> Available sensitivities: {available_sensitivities}\n')

osa.setup(autosetup = False,
          autogain = True)


for res, sens in product(available_resolutions, available_sensitivities):
    # Loop over all resolutions and sensitivities
    osa.set_resolution(res)
    osa.set_sensitivity(sens)
    print(f'Measuring a spectrum in {res} resolution and {sens} sensitivity') 

    acquisitions = osa.acquire(number_of_acquisitions=1, spectrum_averaging=5)
    acquisition = acquisitions[0]
    spectrum = acquisition["spectrum"]

    # Unit conversion - We want to convert the spectrum to different x- and y-axis units.
    spectrum.convert_spectrum(x_unit=x_unit_to_use, y_unit=y_unit_to_use)

    # Now the x- and y-values can be obtained from spectrum.
    x = spectrum.get_x()
    y = spectrum.get_y()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.ticklabel_format(useOffset=False, style='plain')
    ax.plot(x, y)
    ax.set_xlabel(spectrum.get_xlabel())
    ax.set_ylabel(spectrum.get_ylabel())
    ax.set_title(f'Spectrum read from {model} ({res} Res. & {sens} Sens.)')
    plt.tight_layout()
    plt.show()

    # Tip: save_file_spf2 can take as input a list of specs or just one spectrum
    # Note that you need to change the path to get this to work 
    res_for_filename = res.replace(" ", "")
    sens_for_filename = sens.replace(" ", "")
    # Note: this path need to be changed to suit your computer
    #pyOSA.save_file_spf2(spectrum, f"C:\\temp2\\spectrum_{model}_{res_for_filename}Res_{sens_for_filename}Sens.spf2") 
    pyOSA.core.save_spf2_file(spectrum, f"C:\\temp\\spectrum_{model}_{res_for_filename}Res_{sens_for_filename}Sens.spf2") 
