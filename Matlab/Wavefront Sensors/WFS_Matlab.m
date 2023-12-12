% Title: WFS_Example
% Created Date: 2023-12-11
% Last modified date: 2023-12-11
% Matlab Version:R2022a
% Thorlabs DLL version: 6.0.282.119
%% Notes: The example connects to a wavefront sensor, configures the camera, takes a spotfield image and displays it.
% It uses functions from the C SDK 
% Tested for DMP40-5C
%
clc;
clear;

% Loading the dll and header file into MATLAB
libname='C:\Program Files\IVI Foundation\VISA\Win64\Bin\WFS_64.dll';
hfile='C:\Program Files\IVI Foundation\VISA\Win64\Include\WFS.h';
if (~libisloaded('WFS_64'))
 loadlibrary(libname,hfile,'includepath','C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\msc', ...
     'includepath','C:\Program Files\IVI Foundation\VISA\Win64\Include','addheader', ...
     'C:\Program Files\IVI Foundation\VISA\Win64\Include\visa.h','addheader', ...
     'C:\Program Files\IVI Foundation\VISA\Win64\Include\vpptype.h');
end

% Uncomment the following line to displays the functions in the library
% libfunctionsview 'WFS_64';

% Some dll functions use pointers
% The 'libpointer' command has to be used in MATLAB for this
% Get connected WFS sensors
length=libpointer('longPtr',0);
calllib('WFS_64', 'WFS_GetInstrumentListLen',0,length);
disp(['There are ', num2str(length.value), ' wavefront sensors connected']);
if length.value>0
    disp(' ');
    DevID=libpointer('longPtr',0);
    InUse=libpointer('longPtr',0);
    InstrName=libpointer('int8Ptr',int8(zeros(1,25)));
    InstrSN=libpointer('int8Ptr',int8(zeros(1,25)));
    ResourceName=libpointer('int8Ptr',int8(zeros(1,25)));
    for i=0:(length.value-1)
     calllib('WFS_64','WFS_GetInstrumentListInfo',0,i,DevID,InUse,InstrName,InstrSN,ResourceName);
     disp(['Device ID: ', num2str(DevID.value)]);
     disp(char(InstrName.value));
     disp(['SN: ', char(InstrSN.value)]);
     disp(' ');
    end

    % Select one of the connected WFS sensors
    %UsedDeviceNum = input('Device ID of the WFS you want to use: ');
    
    % Initialize the first WFS
    %UsedDeviceStr = ['USB::0x1313::0x0000::',num2str(UsedDeviceNum)];
    UsedDeviceStr = ['USB::0x1313::0x0000::','1'];
    res=libpointer('int8Ptr',int8(UsedDeviceStr));
    hdl=libpointer('ulongPtr',0);
    calllib('WFS_64', 'WFS_init',res,1,1,hdl);
    
    % Select microlens array 0 and configure camera
    calllib('WFS_64','WFS_SelectMla',hdl.value,0);
    spotsx=libpointer('int32Ptr',0);
    spotsy=libpointer('int32Ptr',0);
    calllib('WFS_64','WFS_ConfigureCam',hdl.value, 0, 0, spotsx, spotsy);
    calllib('WFS_64','WFS_SetReferencePlane',hdl.value,0);
    calllib('WFS_64','WFS_SetPupil',hdl.value, 0.0, 0.0, 5.0, 5.0);
    
    for j=1:100
     % Take spotfield image
     exposureTimeAct=libpointer('doublePtr',0.0);
     masterGainAct=libpointer('doublePtr',0.0);
     calllib('WFS_64','WFS_TakeSpotfieldImageAutoExpos',hdl.value,exposureTimeAct, masterGainAct);
     imageBuf=libpointer('uint8Ptr',zeros(1,(1280*1024)));
     rows=libpointer('int32Ptr',0);
     cols=libpointer('int32Ptr',0);
     calllib('WFS_64','WFS_GetSpotfieldImageCopy',hdl.value, imageBuf, rows,cols);
     % Change buffer array and show image of spotfield
     pic=reshape(imageBuf.value,[1280,1024]);
     image(pic);
     pause(0.25);
    end
    
    % Closing the WFS driver session and unloading the dll
    a=calllib('WFS_64','WFS_close', hdl.value);
end
unloadlibrary('WFS_64');