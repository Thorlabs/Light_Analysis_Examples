"""
Thorlabs_OSA_example_04
Example Date of Creation: 2024-04-24
Example Date of Last Modification on GitHub: 2026-11-02
Version of Python: 3.14.3
Version of the Thorlabs SDK used: ThorSpectra 3.40
==================
Example Description: Continuous acquisition combined with wavemeter and peak detection.
"""
from matplotlib import pyplot as plt
import pyOSA

print('''

#####################################################################################
# Example - Continuous acquisitions combined with wavemeter and peak detection      #
#####################################################################################

''')

# Get the connection to the OSA
virtual_osa = False

if not virtual_osa:
    # Initialize the OSA connection
    osa = pyOSA.initialize()
else:
    # Create a virtual OSA to enable testing with no physical OSA connected
    pyOSA.create_virtual_OSA20X(spectrometer_index=0, model='OSA201C', source_type=0,
                                peak_num=1, centerWavelengths_nm=[650],
                                FWHMs_nm=[0.01], peak_amplitudes=[1])
    osa = pyOSA.initialize(virtual_nr=1)

osa.setup(resolution="Low", sensitivity="Low")

plt.ion()
fig, axs = plt.subplots(2, 1)
def on_close(ev):
    # Helper method to stop acquisition if plot window is closed
    osa.stop = True
fig.canvas.mpl_connect('close_event', on_close)

ax1, ax2 = axs

for acquisition in osa.acquire_continuous(interferogram=True, spectrum=True):
    # We have the data
    spectrum = acquisition["spectrum"]
    if osa.is_Redstone():
        # For Redstone instruments we need to specify interferogram detector
        igram = acquisition["interferogram", "Detector 1"]
    else:
        igram = acquisition["interferogram"]

    # Let's do some analysis
    timestamp = spectrum.get_datetime().strftime("%H:%M:%S")
    x_unit = pyOSA.units.get_formatted_x_unit(spectrum)
    try:
        peaks = pyOSA.analysis.peak_track(spectrum)
        peak_centers, peak_heights, peak_widths, peak_lefts, peak_rights = peaks
        spectrum_str = f"{timestamp}: {peak_centers[0]:.4f} {x_unit}"
    except pyOSA.AnalysisException as exc:
        spectrum_str = f"{timestamp}: Peak track analysis failed ({exc})"

    try:
        wavemeter_data = pyOSA.analysis.wavemeter(igram, spectral_unit=x_unit)
        igram_str = (f"{timestamp}: {wavemeter_data['wavelength']:.4f} "
                     f"+- {wavemeter_data['error']:.8f} {x_unit}")
    except pyOSA.AnalysisException as exc:
        igram_str = f"{timestamp}: Wavemeter analysis failed ({exc})"

    # Now plot the spectrum
    x = spectrum.get_x()
    y = spectrum.get_y()
    x_label = spectrum.get_xlabel()
    y_label = spectrum.get_ylabel()
    ax1.clear()
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.set_title(spectrum_str)
    ax1.plot(x,y)

    # And let's plot the interferogram
    x = igram.get_x()
    y = igram.get_y()
    x_label = igram.get_xlabel()
    y_label = igram.get_ylabel()
    ax2.clear()
    ax2.set_xlabel(x_label)
    ax2.set_ylabel(y_label)
    ax2.plot(x,y)
    ax2.set_title(igram_str)

    # Draw the plot
    plt.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()
