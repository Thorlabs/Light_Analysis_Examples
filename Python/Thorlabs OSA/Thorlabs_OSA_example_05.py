"""
Thorlabs_OSA_example_05
Example Date of Creation: 2024-04-24
Example Date of Last Modification on GitHub: 2026-11-02
Version of Python: 3.14.3
Version of the Thorlabs SDK used: ThorSpectra 3.40
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
    # Helper method to stop acquisition if plot window is closed
    osa.stop = True
fig.canvas.mpl_connect('close_event', on_close)

time_data = []
peak_pos_data = []

for data in osa.acquire_continuous():
    # We have the data
    spectrum = data["spectrum"]
    acquisition_time = spectrum.get_datetime()
    x_unit = pyOSA.units.get_formatted_x_unit(spectrum)

    # FindAllPeaks checks the strongest candidates first, so limiting the
    # result to one peak returns the highest peak.
    try:
        peaks = pyOSA.analysis.peak_track(spectrum, max_peaks=1)
        peak_centers, peak_heights, peak_widths, peak_lefts, peak_rights = peaks
        if peak_centers[0] < 0:
            plot_title = "No peaks found"
        else:
            time_data.append(acquisition_time)
            peak_pos_data.append(peak_centers[0])
            plot_title = f"Highest peak: {peak_centers[0]:.4f} {x_unit}"
    except pyOSA.AnalysisException as exc:
        plot_title = f"Peak track analysis failed ({exc})"

    ax.clear()
    ax.plot(time_data, peak_pos_data)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S',
                                                      tz=acquisition_time.tzinfo))
    ax.set_xlabel("Time")
    ax.set_ylabel(f"Peak position ({x_unit})")
    ax.set_title(plot_title)
    plt.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()
