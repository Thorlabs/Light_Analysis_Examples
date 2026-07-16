%% Header
% Title: CCT_example.m
% Created Date: 2026-04-15
% Last modified date: 2026-04-15
% Matlab Version:R2023a
% Thorlabs DLL version:1.0.35.5413
%% Notes: The example shows how to connect to a CCT spectrometer, set the exposure time and acquire a spectrum
% Tested with CCT11
%
scriptFolder = fileparts(mfilename('fullpath'));
% Load the Compact Spectrometer SDK DLLs
NET.addAssembly(fullfile(scriptFolder, 'Microsoft.Extensions.Logging.Abstractions.dll')); 
NET.addAssembly(fullfile(scriptFolder, 'Thorlabs.ManagedDevice.CompactSpectrographDriver.dll'));  
NET.addAssembly(fullfile(scriptFolder, 'Thorlabs.ManagedDevice.dll'));  
NET.addAssembly('System.Runtime');

import Thorlabs.ManagedDevice.CompactSpectrographDriver.Workflow.StartupHelperCompactSpectrometer.*;
import Thorlabs.ManagedDevice.Trace.ExampleLogger.*;
import Microsoft.Extensions.Logging.Abstractions.*;
import Thorlabs.ManagedDevice.CompactSpectrographDriver.ICompactSpectrographDriver.*;

logger = Thorlabs.ManagedDevice.Trace.ExampleLogger('ML',Microsoft.Extensions.Logging.LogLevel.Trace,1==1,'MatLab');
startupHelper = Thorlabs.ManagedDevice.CompactSpectrographDriver.Workflow.StartupHelperCompactSpectrometer(logger);

cts = System.Threading.CancellationTokenSource();
cancellationToken = cts.Token;

%find devices
discoveredDevicestask=startupHelper.GetKnownDevicesAsync(cancellationToken);
discoveredDevicestask.Wait();
discoveredDevices=discoveredDevicestask.Result;

for i=0:discoveredDevices.Count-1
    disp("Discovered devices:")
    disp(discoveredDevices.Item(i));
end

%if spectrometers are found
if(discoveredDevices.Count>0)

    disp("Connecting to first device ...")

    Deviceid=discoveredDevices.Item(0);
    
    spectrometer=startupHelper.GetCompactSpectrographById(Deviceid);

    %set exposure time
    exposure=500; %exposure time in milliseconds
    exposure_result=spectrometer.SetManualExposureAsync(exposure,cancellationToken).Result;
    if exposure_result==1
        disp(['Exposure time is set to ',num2str(exposure),' ms']);
    end
   
    %acquire spectrum
    spectrumtask=spectrometer.AcquireSingleSpectrumAsync(cancellationToken);
    spectrumtask.Wait();
    spectrum=spectrumtask.Result;

    %plot spectrum
    figure; plot(spectrum.Wavelength,spectrum.Intensity)
          
else
    disp("No CCT spectrometer connected")
end
        
       
%dispose startup helper
startupHelper.Dispose();




