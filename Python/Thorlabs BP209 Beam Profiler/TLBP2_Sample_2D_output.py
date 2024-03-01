"""
Example Title
Example Date of Creation(YYYY-MM-DD) 2024-03-01
Example Date of Last Modification on Github 2024-03-01
Version of Python/.NET/Matlab/C++ used for Testing and IDE
Version of the Thorlabs SDK used: Beam version 9.1.5787.615 
==================
Example Description
"""

import os
from ctypes import cdll, c_uint32,byref,create_string_buffer,c_bool, c_uint8, c_int16, c_uint16, c_double,c_float
import matplotlib.pyplot as plt
import TLBP2 
import time

def print_error_msg(bp2, errorCode):
    messageBuffer = create_string_buffer(1024)
    bp2.error_message(errorCode, messageBuffer)

    if((errorCode & TLBP2._VI_ERROR) == 0):
        print("Beam Profiler Warning:", messageBuffer.value)
    else:
        print("Beam Profiler Error:", messageBuffer.value)

        bp2.close()

def main():
    """
    Main Method
    """
    #This is needed if you work with python 32 bit on Windows 64 Bit
    os.add_dll_directory(u"C:\Program Files\IVI Foundation\VISA\Win64\Bin") # use this for 64 Bit Python
    #os.add_dll_directory(u"C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin") # use this for 32 Bit Python

    print("Start")
    bp2 = TLBP2.TLBP2()

    #Find connected devices

    deviceCount = c_uint32()
    res = bp2.get_connected_devices(None, byref(deviceCount))

    if(res != 0):
        print_error_msg(bp2, res)
        return

    if(deviceCount.value == 0):
        print("No device connected")
        return
    
    print("Found devices: ", deviceCount.value)

    resStr = (TLBP2.BP2_DEVICE * deviceCount.value)()

    res = bp2.get_connected_devices(resStr, byref(deviceCount))
 
    if(res != 0):
        print_error_msg(bp2, res)
        return

    bp2.close() 

    # Open first beam profiler
    
    print("Openning device: ", resStr[0].resourceString)

    bp2 = TLBP2.TLBP2()

    try:

        res = bp2.open(resStr[0].resourceString, c_bool(True), c_bool(True))

        if(res != 0):
            print_error_msg(bp2, res) 

        sampleCount = c_uint16()
        resolution = c_double()

        res = bp2.set_drum_speed_ex(c_double(5.0), byref(sampleCount), byref(resolution)) # drum rotation starts here

        if(res != 0):
            print_error_msg(bp2, res)
            return
        

        # initialize gain, then set auto gain to adapt to incident power

        gain_buffer = (c_uint8 * 5)()
        gain_buffer[0] = c_uint8(12)
        gain_buffer[1] = c_uint8(12)
        gain_buffer[2] = c_uint8(12)
        gain_buffer[3] = c_uint8(12)
        gain_buffer[4] = c_uint8(12)
        bp2.set_gains(gain_buffer, gain_buffer[4])

        res = bp2.set_auto_gain(c_bool(True))

        if(res != 0):
            print_error_msg(bp2, res)

        
        #set wavelength

        res = bp2.set_wavelength(c_double(900)) # set wavelength to 900 nm

        if(res != 0):
            print_error_msg(bp2, res)


        res = bp2.set_position_correction(c_int16(TLBP2.VI_ON))

        if(res != 0):
            print_error_msg(bp2, res)
            
        res = bp2.set_speed_correction(c_int16(TLBP2.VI_ON))


        if(res != 0):
            print_error_msg(bp2, res)

        time.sleep(10) # wait a few seconds to let stabilize drum speed

        # get scan data

        maxscan=5 # number of scans
        loopCnt = 0
        while (loopCnt < maxscan):
            device_status = c_uint16(0)
            res = 0
            while (res == 0 and (device_status.value & TLBP2.BP2_STATUS_SCAN_AVAILABLE) == 0):
                res = bp2.get_device_status(byref(device_status))
                            
            print("\n Found scan: ", loopCnt)
            if(res == 0):
                slit_data = (TLBP2.BP2_SLIT_DATA * 4)()
                calculation_result = (TLBP2.BP2_CALCULATIONS * 4)()
                power = c_double()
                powerSaturation = c_double()
                power_intensities = (c_double * 7500)()# intensities for power window
                print("Calling get_slit_scan_data")
                res = bp2.get_slit_scan_data(slit_data, calculation_result, byref(power), byref(powerSaturation), power_intensities)
                if(res == 0):
                    print("Power: {value:.2f}".format(value = power.value))
                    print("Power Saturation: {value:.2f}".format(value = powerSaturation.value))
                    print("Peak Position Slit 1: {value:.2f}".format(value = calculation_result[0].peakPosition))
                    print("Centroid Position Slit 1: {value:.2f}".format(value = calculation_result[0].centroidPosition))
                    print("Peak Position Slit 2: {value:.2f}".format(value = calculation_result[1].peakPosition))
                    print("Centroid Position Slit 2: {value:.2f}".format(value = calculation_result[1].centroidPosition))
           
                else:
                    print("The scan returned the error:", res)
                
                # get intensities for slit 0 and 1
                power_window_saturation=c_double()
                power=c_double()
                sample_intensitiesx = (c_double * 7500)()
                sample_intensitiesy = (c_double * 7500)()
                sample_positionsx=(c_double * 7500)()
                sample_positionsy=(c_double * 7500)()
                bp2.request_scan_data(byref(power_window_saturation),byref(power),power_intensities)
                bp2.get_sample_intensities(0,sample_intensitiesx,sample_positionsx)
                bp2.get_sample_intensities(1,sample_intensitiesy,sample_positionsy)

                # get Gaussian fit for slit 0 and 1
                gaussian_fit_amplitudex=c_double()
                gaussian_fit_amplitudey=c_double()
                gaussian_fit_diameterx=c_double()
                gaussian_fit_diametery=c_double()
                gaussian_fit_percentagex=c_double()
                gaussian_fit_percentagey=c_double()
                gaussian_fit_intensitiesx = (c_double * 7500)()
                gaussian_fit_intensitiesy = (c_double * 7500)()
                bp2.get_slit_gaussian_fit(0,byref(gaussian_fit_amplitudex),byref(gaussian_fit_diameterx), byref(gaussian_fit_percentagex),gaussian_fit_intensitiesx)
                bp2.get_slit_gaussian_fit(1,byref(gaussian_fit_amplitudey),byref(gaussian_fit_diametery), byref(gaussian_fit_percentagey),gaussian_fit_intensitiesy)


            else:
                print("The device status returned the error:", res)
            loopCnt+=1 

        # Plot sample intensities for slit 0 for last scan           
        fig,ax=plt.subplots()
        ax.plot(sample_positionsx, sample_intensitiesx)
        plt.title('Intensities for Slit 0')

        #Plot Gaussian fit for slit 0
        fig,ax=plt.subplots()
        ax.plot(sample_positionsx, gaussian_fit_intensitiesx)   
        plt.title('Gaussian Fit for Slit 0')     


        # 2D Reconstruction 
        imagedata=((c_float*750)*750)()
        for ix in range(750):
            for iy in range(750):
                ixz=ix*10
                iyz=iy*10
                imagedata[ix][iy]=sample_intensitiesx[ixz]*gaussian_fit_intensitiesx[ixz]*sample_intensitiesy[iyz]*gaussian_fit_intensitiesy[iyz];

        fig,ax=plt.subplots()
        ax.imshow(imagedata,cmap='hot')
        plt.axis('off')
        plt.title('2D Reconstruction')
        plt.show()
                    
    except NameError as inst:
        print("Name Error: ", inst)
    except ValueError as inst:
        print("Value Error: ", inst)

    bp2.close()
    print("End")

if __name__ == "__main__":  
    main()