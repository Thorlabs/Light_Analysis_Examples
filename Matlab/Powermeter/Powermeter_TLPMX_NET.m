% Title: Powermeter_TLPMX_NET.m
% Created Date: 2024-01-15
% Last modified date: 2024-01-15
% Matlab Version:R2022a
% Thorlabs DLL version:5.4.4561.610
%% Notes:The example connects to a powermeter, sets the wavelength and measures the power and current
% The example uses methods from the .NET SDK "TLPMX"
%
clear all;
NET.addAssembly('C:\Program Files (x86)\Microsoft.NET\Primary Interop Assemblies\Thorlabs.TLPMX_64.Interop.dll');

import Thorlabs.TLPMX_64.Interop.*;

%Uncomment the next two lines to see an overview of the available functions
%methodsview('Thorlabs.TLPMX_64.Interop.TLPMX')

%Create a dummy TLPMX object to check for compatible devices.
handle = System.IntPtr(0);
device = TLPMX(handle);

%Look for connected devices
[~,deviceCount] = device.findRsrc();

if deviceCount == 0
    disp( 'Unable to find compatible connected devices. Is the device connected, on, and using the TLPMX driver? This example will not work with the legacy IVI drivers.');
    return
end

%If only one device is connected, connect to this one.
deviceName=System.Text.StringBuilder(256);
if deviceCount == 1
    device.getRsrcName(0, deviceName);
%If multiple are connected, ask which to use
else
    for i = 0:deviceCount-1
        device.getRsrcName(i, deviceName);
        disp(' ');
        disp(['Device #', num2str(i)]);
        disp(deviceName.ToString);
    end
    val=input('Select a device by the number from the above detected devices: ');
    if (floor(val) < deviceCount) && (floor(val) > -1)
        device.getRsrcName(floor(val), deviceName);
    else
        print 'Invalid selection';
        return;
    end
end

%Reassign device to the selected power meter console
device = TLPMX(deviceName.ToString(), true, false);

disp('Device connected:');
disp(deviceName.ToString());

%Check if there are any errors
errormessage=System.Text.StringBuilder(256);
device.errorQuery(errormessage);
disp(errormessage.ToString);

%Set wavelength for channel 1
wavelength= 1000;
channel=1;
try 
    device.setWavelength(wavelength,channel);
    disp('Wavelength Setting [nm]:')
    disp(wavelength);
catch
    disp('Error Setting Wavelength');
    device.Dispose()
end

%Turn off power auto range
device.setPowerAutoRange(false,channel);

%Set power unit to Watt
device.setPowerUnit(0,channel);

%Set power range 
try
    powerrange=0.1; %power range in Watt
    device.setPowerRange(powerrange,channel);
    %The actual power range
    [~, setpowerrange]=device.getPowerRange(0,channel);
    disp('Power Range Setting [W]:');
    disp(setpowerrange);
catch
    disp('Error setting power range');
    device.Dispose();
end

try
    [~, power]=device.measPower(channel);
    disp('Measured power [W]:');
    disp(power);
catch
    disp('Error measuring power');
    device.Dispose();
end

try
    [~, current]=device.measCurrent(channel);
    disp('Measured current [A]:');
    disp(current);
catch
    disp('Error measuring current');
    device.Dispose();
end

disp('Disconnect device')
device.Dispose();

