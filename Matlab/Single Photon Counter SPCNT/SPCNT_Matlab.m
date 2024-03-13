%% Header
% Title: SPCNT_Matlab
% Created Date: 2024-02-28
% Last modified date: 2024-02-28
% Matlab Version:R2022a
% Thorlabs DLL version:0.1.1239.177
%% Notes:The example connects to a SPCNT device and shows the frequency

clear all;

lib=NET.addAssembly('C:\Program Files\IVI Foundation\VISA\VisaCom64\Primary Interop Assemblies\Thorlabs.SPCNT_64.Interop.dll');

import Thorlabs.SPCNT_64.Interop.*;

%Uncomment the next two lines to see an overview of the available functions
%methodsview('Thorlabs.SPCNT_64.Interop.TLSPCNT')

handle = System.IntPtr(0);
tlspcnt = TLSPCNT(handle);


% Search for available devices
[~,devicecount]=tlspcnt.findRsrc();
disp([num2str(devicecount),' device(s) found']);

if devicecount>0

    %get information about first available device
    modelName=System.Text.StringBuilder(256);
    vendor=System.Text.StringBuilder(256);
    serialNumber=System.Text.StringBuilder(256);
    ressourceString=System.Text.StringBuilder(256);
    
    [~,available]=tlspcnt.getRsrcInfo(0, modelName, vendor, serialNumber);
    result=tlspcnt.getRsrcName(0,ressourceString);
    
    disp(modelName.ToString);
    disp(vendor.ToString);
    disp(serialNumber.ToString);
    disp(ressourceString.ToString);
    
    
    %initialize device
    counter=TLSPCNT(ressourceString.ToString(),false,false);

    %set bin width
    counter.setBinWidth(20);
    [~,binwidth]=counter.getBinWidth();
    disp(['Bin Width:',num2str(binwidth),' ms']);

    %set dead time
    counter.setDeadtime(0);
    [~,deadtime]=counter.getDeadtime();
    disp(['Dead Time:',num2str(deadtime),' ms']);

    %get frequency

    %wait until frequency value is present 
    [~,registervalue]=counter.readRegister(4); % Operation Condition Register
    while(0==bitand(registervalue,512))% register value 512 means "Frequency to fetch"
        [~,registervalue]=counter.readRegister(4); % Operation Condition Register
    end

    [frequency,frequency_min,frequency_max,frequency_avg]=counter.getFrequency();
   
    disp(['Frequency: ',num2str(frequency_avg),' Hz']);

    %disconnect
    counter.Dispose();
    
end
