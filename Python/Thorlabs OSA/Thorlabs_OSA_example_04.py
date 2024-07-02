"""
Thorlabs_OSA_example_04
Example Date of Creation: 2024-04-24
Example Date of Last Modification on Github: 2024-04-24
Version of Python: 3.12.2
Version of the Thorlabs SDK used: ThorSpectra 3.31
==================
Example Description: Continous acquisition combined with wavemeter and peakdetection.
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

osa.setup(resolution="Low", sensitivity="High")

plt.ion()
fig, axs = plt.subplots(2, 1)
def on_close(ev):
    # Helper method to stop acquisition if plotwindow is closed
    osa.stop = True
fig.canvas.mpl_connect('close_event', on_close)

ax1, ax2 = axs

for acquisition in osa.acquire_continuous(interferogram=True, spectrum=True):
    # We have the data
    spectrum = acquisition["spectrum"]
    igram = acquisition["interferogram"]
    # For Redstone instruments we would need to specify interferogram detector
    #igram = data["interferogram", "Detector 1"]

    # Lets do some analysis
    peaks = pyOSA.analysis.peak_track(spectrum)
    wavedata = pyOSA.analysis.wavemeter(igram)

    # Format the output of the analysis
    peak_centers, peak_heights, peak_widths, peak_lefts, peak_rights = peaks
    timestamp = spectrum.get_datetime().strftime("%H:%M:%S")
    spectrumstr = f"{timestamp}: {peak_centers[0]:.4f} nm"
    igramstr = f"{timestamp}: {wavedata['wavelength']:.4f} +- {wavedata['error']:.8f}"

    # Now plot the spectrum
    x = spectrum.get_x()
    y = spectrum.get_y()
    xlabel = spectrum.get_xlabel()
    ylabel = spectrum.get_ylabel()
    ax1.clear()
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(spectrumstr)
    ax1.plot(x,y)

    # And lets plot the interferogram
    x = igram.get_x()
    y = igram.get_y()
    xlabel = igram.get_xlabel()
    ylabel = igram.get_ylabel()
    ax2.clear()
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel(ylabel)
    ax2.plot(x,y)
    ax2.set_title(igramstr)

    # Draw the plot
    plt.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()

    # You can stop the acquisition by setting the following flag
    #osa.stop = True
