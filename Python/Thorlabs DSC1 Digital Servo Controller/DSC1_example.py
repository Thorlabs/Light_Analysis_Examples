"""
Example Title: DSC1_example.py
Example Date of Creation(YYYY-MM-DD): 2026-04-23
Example Date of Last Modification on Github: 2026-04-23
Version of Python used for Testing: 3.13
Version of the Thorlabs SDK used: DSC1 Software Version 1.1.1.0 
Example Description: It connects to the DSC1 dual channel spectrometer and reads and displays spectral values. 
"""
from dscx_sdk import DSC
import matplotlib.pyplot as plt

if __name__ == "__main__":
    dsc1=DSC()

    dsc1.FindDSC()

    dsc1.SetOperationMode(0, 0, "SERVO")

    dsc1.GetTimeDomain(0)

    spectrum=dsc1.GetSpectrum()

    spectrum_plot = dsc1.GetSpectrumPlot(spectrum)
    
    # Plot the spectrum
    plt.figure(figsize=(10, 6))
    plt.semilogx(spectrum_plot[:, 0], spectrum_plot[:, 1])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD (dBV²/Hz)')
    plt.title('Spectrum')
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.show()
