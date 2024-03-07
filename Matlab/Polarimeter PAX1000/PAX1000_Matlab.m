%% Header
% Title: PAX1000_Matlab.m
% Created Date: 2024-03-07
% Last modified date: 2024-03-07
% Matlab Version:R2022a
% Thorlabs DLL version:1.1.2041.116
%% Notes:
% Tested for PAX1000VIS/M
%
clc;
clear;
disp('Start');

%   Loading the dll and header file into MATLAB
libname='C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPAX_64.dll';
hfile='C:\Program Files\IVI Foundation\VISA\Win64\Include\TLPAX.h';
loadlibrary(libname,hfile,'includepath','C:\Program Files\IVI Foundation\VISA\Win64\Include\', 'includepath', 'C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\');
disp('Library loaded.');


%   Displays the functions in the library
%   Also gives the data types used in a command
%   - Not necessary for normal use -
%libfunctionsview 'TLPAX_64';


% Find connected PAX1000
devcount=libpointer('ulongPtr',0);
calllib('TLPAX_64','TLPAX_findRsrc',0,devcount);
disp(['Number of found devices: ',num2str(devcount.value)]);

if devcount.value>0

    %   Initialize the first PAX1000
    resource=libpointer('int8Ptr',int8(zeros(1,256)));
    calllib('TLPAX_64','TLPAX_getRsrcName',0,0,resource);
    handle=libpointer('ulongPtr',0);
    [a,b,c]=calllib('TLPAX_64', 'TLPAX_init', resource, 1, 0, handle);
    disp(['Initialize device (0 = correct, rest = error): ', num2str(a)]);
    
    % Make settings
    calllib('TLPAX_64','TLPAX_setMeasurementMode',handle.value,9);% mode 9 corresponds to 2 revolutions for one measurement, 2048 points for FFT
    calllib('TLPAX_64','TLPAX_setWavelength',handle.value,633e-9);% wavelength in m
    calllib('TLPAX_64','TLPAX_setBasicScanRate',handle.value,60.);% basic scan rate in 1/s

    wavelength=libpointer('doublePtr',0);
    calllib('TLPAX_64','TLPAX_getWavelength',handle.value,wavelength);
    disp(['The wavelength is set to ',num2str(wavelength.value),' m']);
    
    pause(5)
    
    % Take 5 scans and output values for azimuth and ellipticity
    for i=1:5
        scanID=libpointer('ulongPtr',0);
        calllib('TLPAX_64','TLPAX_getLatestScan',handle.value,scanID);
        
        azimuth=libpointer('doublePtr',0);
        ellipticity=libpointer('doublePtr',0);
        calllib('TLPAX_64','TLPAX_getPolarization',handle.value,scanID.value,azimuth,ellipticity);
    
        disp(['Azimuth: ',num2str(azimuth.value)]);
        disp(['Ellipticity: ',num2str(ellipticity.value)]);
    
        calllib('TLPAX_64','TLPAX_releaseScan',handle.value,scanID.value);
    
        pause(0.5);
    end
    
    
    %   Close spectrometer connection, unload library
    calllib('TLPAX_64','TLPAX_close', handle.value);

end

unloadlibrary 'TLPAX_64';