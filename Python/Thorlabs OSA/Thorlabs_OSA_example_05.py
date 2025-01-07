"""
Thorlabs_OSA_example_05
Example Date of Creation: 2024-04-24
Example Date of Last Modification on Github: 2024-12-20
Version of Python: 3.12.2
Version of the Thorlabs SDK used: ThorSpectra 3.35
==================
Example Description: Continuously measure spectra, find the highest peak, and plot
the peak position over time.
"""
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pyOSA

print('''

#####################################################################################
# Example - Plotting peak position over time continuously                           #
#####################################################################################

''')

# Get the connection to the OSA
virtual_osa = False

if not virtual_osa:
    # Connects to all OSA instruments in the system
    osa = pyOSA.initialize()
else:
    # Create a virtual OSA to enable testing with no physical OSA connected
    pyOSA.create_virtual_OSA20X(spectrometer_index=0, model='OSA201C', source_type=0, peak_num=1, centerWavelengths_nm=[650], FWHMs_nm=[1], peak_amplitudes=[1])
    #pyOSA.create_virtual_Redstone(spectrometer_index=0, model='Redstone305', source_type=0)
    osa = pyOSA.initialize(virtual_nr=1)

osa.setup()

plt.ion()
fig, ax = plt.subplots(1, 1)
def on_close(ev):
    # Helper method to stop acquisition if plotwindow is closed
    osa.stop = True
fig.canvas.mpl_connect('close_event', on_close)

time_data = []
peak_pos_data = []

for data in osa.acquire_continuous():
    # We have the data
    spectrum = data["spectrum"]

    # Let's do some analysis
    peaks = pyOSA.analysis.peak_track(spectrum)

    # Format the output of the analysis
    peak_centers, peak_heights, peak_widths, peak_lefts, peak_rights = peaks
    time_data.append(spectrum.get_datetime())
    peak_pos_data.append(peak_centers[0])

    ax.clear()
    ax.plot(time_data,peak_pos_data)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S', tz="Europe/Stockholm"))
    ax.set_xlabel("Time")
    ax.set_ylabel("Peakposition (nm)")
    plt.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()
