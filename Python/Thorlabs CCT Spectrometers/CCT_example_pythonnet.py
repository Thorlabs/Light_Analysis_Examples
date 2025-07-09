"""
Example Title: CCT_pythonnet.py
Example Date of Creation(YYYY-MM-DD): 2025-02-26
Example Date of Last Modification on Github: 2025-02-26
Version of Python used for Testing and IDE: 3.11.0
Version of the Thorlabs SDK used: CCT Series Spectrometer Software 
==================
Example Description: This example shows how to connect to a Thorlabs CCT spectrometer, set the exposure time, set hardware averaging, 
acquire a apectrum and write it to a file. 

"""
import clr
import csv
import sys
import os
import time

# Get absolute path of the executing code
print("Execution in path: '{0}'".format(os.getcwd()))

# Set the DLL path relative to the current working directory
dll_path = os.path.abspath(os.path.join(os.getcwd(), './pyCCT/net48'))  # Replace with the correct path to your DLL files
if dll_path not in sys.path:
    sys.path.append(dll_path)
os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']

# Load the Compact Spectrometer SDK DLLs
clr.AddReference(os.path.join(dll_path, 'Thorlabs.ManagedDevice.CompactSpectrographDriver'))

# Load DLLs needed to use .NET Logging
clr.AddReference(os.path.join(dll_path, 'Microsoft.Extensions.Logging'))
clr.AddReference(os.path.join(dll_path, 'Microsoft.Extensions.Logging.Console'))
clr.AddReference(os.path.join(dll_path, 'Microsoft.Extensions.Options'))

# Load basic .NET Libraries
from System.Collections.Generic import List
from System.Threading import CancellationTokenSource

# Import necessary classes from the Compact Spectrometer SDK
from Thorlabs.ManagedDevice.CompactSpectrographDriver.Workflow import StartupHelperCompactSpectrometer
from Thorlabs.ManagedDevice.CompactSpectrographDriver import ICompactSpectrographDriver

# Enable use of .NET Logging
from Microsoft.Extensions.Logging import LogLevel, LoggerFactory, ILoggerProvider, LoggerFilterOptions, ILogger
from Microsoft.Extensions.Logging.Console import ConsoleLoggerProvider, ConsoleLoggerOptions
from Microsoft.Extensions.Options import OptionsFactory, IConfigureNamedOptions, IPostConfigureOptions, OptionsMonitor, IOptionsChangeTokenSource, OptionsCache

def main():
    # Use .NET Logger, because it can be shared with SDK of the Compact Spectrometers
    logger = initialize_logger(LogLevel.Information, "CctGetSpectrum")

    # Constructing the startup helper that manages required device interactions
    startup_helper_cct = StartupHelperCompactSpectrometer(logger)

    try:
        cancellation_token = CancellationTokenSource().Token
        
        ## If necessary, add a Network Device at specific IP Address
        #startup_helper_cct.RegisterEthernetIpAddress("192.168.0.160")
        
        ## If necessary, add a Virtual Device
        #startup_helper_cct.WithVirtual = True

        # Constructing the startup helper that manages required device interactions
        print("Discovering spectrometers...")
       
        # Running device discovery and  Getting the list of available devices
        connection_keys = list(startup_helper_cct.GetKnownDevicesAsync(cancellation_token).Result)
        
        if not connection_keys:
            print("No spectrometers found.")
            return
        else:
            # Print all found devices
            print("Found spectrometers:")
            for key in connection_keys:
                print(f"- {key}")

        # Assuming the first device in the list is our target
        spectrometer_id = connection_keys[0]
        spectrometer = startup_helper_cct.GetCompactSpectrographById(spectrometer_id)
        print("Connected to Spectrometer: " + spectrometer_id)

        # Set exposure for spectrum acquisition
        exposure = 8.3
        exposure_result = spectrometer.SetManualExposureAsync(exposure, cancellation_token).Result
        if exposure_result:
            print("Set exposure time: {0} ms".format(str(exposure)))
        else:
            print("Cannot set exposure time")
            return

        # Set hardware averaging in the spectrometer
        ave = 5
        ave_result = spectrometer.SetHwAverageAsync(ave, cancellation_token).Result
        if ave_result:
            print("Set hardware averaging: {0} frames".format(str(ave)))
        else:
            print("Cannot set hardware averaging")
            return

        # Acquire Dark Spectrum
        # First, close the shutter
        dark = spectrometer.SetShutterAsync(False, cancellation_token).Result
        # Mechanical Shutter requires some time to travel into changed position
        time.sleep(0.04)
        if dark:
            # acquire the dark spectrum
            dark = spectrometer.UpdateDarkSpectrumAsync(False, cancellation_token).Result
        if dark:
            # open the shutter for further acquisition
            dark = spectrometer.SetShutterAsync(True, cancellation_token).Result
        # Mechanical Shutter requires some time to travel into changed position
        time.sleep(0.04)
        if dark:
            print("Acquired Dark Spectrum")
        else:
            print("Cannot acquire Dark Spectrum")
            return

        # Acquire the spectrum
        spectrum = spectrometer.AcquireSingleSpectrumAsync(cancellation_token).Result

        # Extracting spectrum data
        wavelengths = list(spectrum.Wavelength)
        intensities = list(spectrum.Intensity)

        # Save the spectrum to a CSV file
        filename = 'spectrum_data.csv'
        with open(filename, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Wavelength (nm)', 'Intensity'])
            for wavelength, intensity in zip(wavelengths, intensities):
                csv_writer.writerow([wavelength, intensity])

        print("Spectrum data saved into file '{0}'".format(filename))

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Startup Helper disposes registered connection managers automatically
        startup_helper_cct.Dispose()

def initialize_logger(log_verbosity, name):
    options_setups = List[IConfigureNamedOptions[ConsoleLoggerOptions]]()
    options_post = List[IPostConfigureOptions[ConsoleLoggerOptions]]()
    options_factory = OptionsFactory[ConsoleLoggerOptions](options_setups, options_post)
    options_sources = List[IOptionsChangeTokenSource[ConsoleLoggerOptions]]()
    options_cache = OptionsCache[ConsoleLoggerOptions]()
    options_monitor = OptionsMonitor[ConsoleLoggerOptions](options_factory, options_sources, options_cache)
    logger_provider = ConsoleLoggerProvider(options_monitor)
    logger_providers = List[ILoggerProvider]()
    logger_providers.Add(logger_provider)
    options = LoggerFilterOptions()
    options.MinLevel = log_verbosity
    logger_factory = LoggerFactory(logger_providers, options)
    return logger_factory.CreateLogger(name)

if __name__ == '__main__':
    main()

