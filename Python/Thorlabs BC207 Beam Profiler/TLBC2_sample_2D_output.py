"""
Example Title: TLBC2_sample_2D_output.py
Example Date of Creation: 2024-07-16
Example Date of Last Modification on Github: 2024-07-16
Version of Python used for Testing: 3.11
Version of the Thorlabs SDK used: Beam 9.1
==================
Example Description: The sample code shows how to control a BC207 beam profiler in Python. In the example the available beam profilers are found, 
a connection is extablished, several parameters are set, several output values are displayed and a 2D image is shown.
"""

import os
import TLBC2
import matplotlib.pyplot as plt
import time
import numpy as np
from ctypes import cdll,c_long,c_uint32,c_uint16,c_uint8,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_int8,c_double,c_float,sizeof,c_voidp, c_char, c_ubyte, c_ushort


def error_exit(bc2, err):
    ebuf = create_string_buffer(1024)
    bc2.error_message(err, ebuf)
    print("Error:", ebuf.value)

    bc2.close()

def main():
    """
    "Thorlabs TSI instrument driver sample application"

    """

    #This is needed if you work with python 32 bit on Windows 64 Bit
    os.add_dll_directory(u"C:\Program Files\IVI Foundation\VISA\Win64\Bin") # use this for 64 Bit Python
    #os.add_dll_directory(u"C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin") # use this for 32 Bit Python

    print("Thorlabs TSI instrument driver sample application")
    
    deviceCnt = c_uint32()
    bc2 = TLBC2.TLBC2()
    err = bc2.get_device_count(byref(deviceCnt))

    if err != 0:
        error_exit(bc2, err)
        return
 
    if(deviceCnt.value == 0):
        print("No devices found")
        return

    print("Found instruments: ", deviceCnt.value)

    manufacturer = create_string_buffer(1024)
    resourceName = create_string_buffer(1024)

    k = 0
    for k in range(0, deviceCnt.value):
        print("Device index: ", k)
        modelName = create_string_buffer(1024)
        serialNumber = create_string_buffer(1024)
        available = c_int16() 
        err = bc2.get_device_information(c_uint32(k), manufacturer, modelName, serialNumber, byref(available), resourceName)
        print("Model name: ", modelName.value.decode('utf_8'))
        print("Serial number: ", serialNumber.value.decode('utf_8'))
        print("Resource Name: ", resourceName.value.decode('utf_8'))
        if(available.value):
            break

    if(k >= deviceCnt.value):
        print("No egilable instrument available. Close other programs that might have corrupted a device.")
        return

    bc2.close()
 
    print("Initializing the device...\n")
    bc2 = TLBC2.TLBC2()

    try:

        err = bc2.open(resourceName.value, c_bool(True), c_bool(True))
        if err != 0:
            error_exit(bc2, err) 

        modelName = create_string_buffer(1024)
        serialNumber = create_string_buffer(1024)
        err = bc2.identification_query(modelName, serialNumber)
        if err != 0:
            error_exit(bc2, err) 

        print("Connected to")
        print("Model:", modelName.value.decode('latin-1'))
        print("Serial number:", serialNumber.value.decode('utf_8'))

        driverRev = create_string_buffer(1024)
        firmwareRev = create_string_buffer(1024)
        err = bc2.revision_query(driverRev, firmwareRev)    
        if err != 0:
            error_exit(bc2, err) 

        print("Driver rev.:", driverRev.value.decode('utf_8'))
        print("Firmware rev.:", firmwareRev.value.decode('utf_8'))

        min_wavelength = c_double(0)
        max_wavelength = c_double(0)
        err = bc2.get_wavelength_range(byref(min_wavelength), byref(max_wavelength))
        if err != 0:
            error_exit(bc2, err) 

        print("Wavelength range: {min:.2f}... {max:.2f} nm".format(min = min_wavelength.value, max = max_wavelength.value))

        err = bc2.set_wavelength(c_double((max_wavelength.value - min_wavelength.value) / 2.0 + min_wavelength.value))
        if err != 0:
            error_exit(bc2, err) 

        wavelength = c_double(0)
        err = bc2.get_wavelength(byref(wavelength))
        if err != 0:
            error_exit(bc2, err) 
        
        print("Wavelength: {wavelength:.2f} nm".format(wavelength = wavelength.value))

        err = bc2.set_attenuation(c_double(40))
        if err != 0:
            error_exit(bc2, err)        
        
        attenuation = c_double(0)
        err = bc2.get_attenuation(byref(attenuation))
        if err != 0:
            error_exit(bc2, err) 
        
        print("Attenuation set to : {attenuation:.2f} dB".format(attenuation = attenuation.value))

        err = bc2.set_clip_level(c_double(0.135))
        if err != 0:
            error_exit(bc2, err) 

        #set some camera parameters
        min_exposure = c_double(0)
        max_exposure = c_double(0)
        err = bc2.get_exposure_time_range(byref(min_exposure), byref(max_exposure))
        if err != 0:
            error_exit(bc2, err) 

        test_exposure_time = c_double(0.04)
        err = bc2.set_exposure_time(test_exposure_time)    
        if err != 0:
            error_exit(bc2, err) 

        set_exposure_time = c_double(0)
        err = bc2.get_exposure_time(byref(set_exposure_time))
        if err != 0:
            error_exit(bc2, err) 

        print("Exposure Time: {time:.2f}".format(time = set_exposure_time.value))

        gainMin = c_double(0)
        gainMax = c_double(0)
        err = bc2.get_gain_range(byref(gainMin), byref(gainMax))
        if err != 0:
            error_exit(bc2, err) 

        test_gain = c_double(1.9)
        err = bc2.set_gain(test_gain)
        if err != 0:
            error_exit(bc2, err) 

        err = bc2.set_auto_exposure(TLBC2.VI_ON)
        if err != 0:
            error_exit(bc2, err) 

        auto_exposure = c_bool(False)
        err = bc2.get_auto_exposure(byref(auto_exposure))   
        if err != 0:
            error_exit(bc2, err) 

        if auto_exposure.value:
            print("Auto Exposure is ON")
        else:
            print("Auto Exposure is OFF")

        #set the calculation area  
        err = bc2.set_calculation_area_mode(TLBC2.VI_ON, TLBC2.TLBC1_CalcAreaForm_Rectangle)
        if err != 0:
            error_exit(bc2, err) 

        #set the auto calculation area clip level to 1%
        err = bc2.set_auto_calculation_area_clip_level(c_double(0.01))
        if err != 0:
            error_exit(bc2, err) 

        #set the profile to the peak position
        err = bc2.set_profile_cut_position(TLBC2.TLBC1_Profile_Position_Peak_Position, 0, 0, 0)
        if err != 0:
            error_exit(bc2, err) 

        # set binning mode
        err = bc2.set_binning(c_uint8(TLBC2.TLBC2_Binning_2))
        if err != 0:
            error_exit(bc2, err) 

        #noise level of the camera
        blackLevel = c_double(0)
        err = bc2.get_black_level(byref(blackLevel))    
        if err != 0:
            error_exit(bc2, err) 

        print("Black level set: ", blackLevel.value)

        # display calculated values
        scan_data = TLBC2.TLBC1_Calculations()
        err=0
        for j in range(0, 2):

        
            err = bc2.get_scan_data(byref(scan_data))        
            
            if(err == 0):
                if(scan_data.isValid):
                    print("Peak Value: {peak:.2f}, Position X: {posx:d}, Position Y: {posy:d}".format(peak = scan_data.peakIntensity, posx = scan_data.profilePeakPosX, posy = scan_data.profilePeakPosY))
                    print("Beam Width Clip X: {clipx:.2f}, Beam Width Clip Y: {clipy:.2f}".format(clipx = scan_data.beamWidthClipX, clipy = scan_data.beamWidthClipY))
                    print("Total power: {power:.2f} dBm\n".format( power = scan_data.totalPower))
                else:
                    print("Scan invalid {index:d}\n".format(index = j))

        if(err != 0):
            print("error")
            error_exit(bc2, err)

        # read out the scan data
        #pixeldata=(((c_ubyte*2448)*2048)*2)()
        pixeldata=(((c_ubyte*1224)*1024)*2)()
        width, height=c_ushort(0),c_ushort(0)
        bytesPerPixel=c_ubyte(2)
  
        err=bc2.get_image(pixeldata,byref(width),byref(height),byref(bytesPerPixel))
        if err != 0:
            error_exit(bc2, err) 

        #show image
        imagedataFlat = np.frombuffer(pixeldata, dtype='uint16')
        imagedata = np.array_split(imagedataFlat, 1024)

        fig,ax=plt.subplots()
        ax.imshow(imagedata,cmap='cool')
        plt.show()

    except NameError as inst:
        print(inst)
    except TypeError as inst:
        print(inst)

    bc2.close()
        

    
    print("End")

if __name__ == "__main__":
    main()
