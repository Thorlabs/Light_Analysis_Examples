import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\ThorSpectra\\ThorlabsOSAWrapper.dll")

from System import Array
from System import Double
from ThorlabsOSAWrapper import *
from ThorlabsOSAWrapper import InstrumentModel
from ThorlabsOSAWrapper import AcquisitionUpdateFlag
from ThorlabsOSAWrapper import SpectrumStruct
from ThorlabsOSAWrapper import FileIOInterface


#method to be called when the OSA has a spectrum ready
def OnSingleAcquisition(sender, event_args):
    if event_args.CallbackMessage.LastDataTypeUpdateFlag == AcquisitionUpdateFlag.Spectrum:
        print('Spectrum Acquired')
        spectrum = SpectrumStruct(sender.ChannelInterfaces[0].GetLastSpectrumLength(), True)
        sender.ChannelInterfaces[0].GetLastSpectrum(spectrum)

        #Write to file
        file_interface = FileIOInterface()
        file_interface.WriteSpectrum(spectrum, str(os.getcwd() + r'\spectrum.txt'), 1)


def main():
    osa = 0
    locator = DeviceLocator()
    if locator.InitializeSpectrometers() > 0: 
        print('Spectrometer Found.... Opening')
        osa = LibDeviceInterface(0)

    else:
        print('No Devices Found... Starting Simulator')
        #Create Virtuial OSA203
        device_index = DeviceLocator.CreateVirtualSpectrometer(InstrumentModel.VirtualOSA203)
        #number of peaks in the sample spectrum
        peak_num = 2
        #amplitude of Each peak in the sample spectrum
        peak_amplitude_array = Array[Double]([.6, .3])
        #FWHM wavelength of each peak
        fwhm_array = Array[Double]([20, 12])
        #center wavelength of each peak
        center_wavelength_array = Array[Double]([1200, 1865])

        virtual_config = VirtualSpectrometerConfiguration(peak_num)
        virtual_config.peakAmplitude = peak_amplitude_array
        virtual_config.fwhm_nm = fwhm_array
        virtual_config.centerWavelength_nm = center_wavelength_array

        #Load the Configuration to the virtual device
        DeviceLocator.ConfigureVirtualSpectrometer(device_index, virtual_config)
        time.sleep(1)
        osa = LibDeviceInterface(device_index)
        print('Device open')

    # set some settings on the OSA
    osa.SetSensitivityMode(1)
    osa.SetResolutionMode(1)

    #Add method as a callback for spectrum acquisition and acquire
    osa.OnSingleAcquisition += OnSingleAcquisition
    osa.AcquireSingleSpectrum()

    #give the OSA a few seconds to allow the spectrum to acquire and save. 
    # This can be replaced by a loop as well to check completion. 
    time.sleep(3)

    #close the device
    osa.CloseSpectrometer
    print('Device Closed')

if __name__ == "__main__":
    main()
