"""
Example Title: WFS_Example.py
Example Date of Creation(YYYY-MM-DD): 2023-02-07
Example Date of Last Modification on Github: 2023-02-07
Version of Python used for Testing and IDE: 3.10.0
Version of the Thorlabs SDK used: WFS Wavefront Sensors Software Version 6.1
==================
Example Description: This example shows how to initialize the wavefront sensor and configure the attached microlens array. 
This also goes through the suggested process for acquiring spotfield images and outputting calculation data like centroid and wavefront values.
"""

import os
import sys
import time
import numpy
import ctypes
from ctypes import byref, c_double, c_float, c_int64, c_uint64, create_string_buffer, c_bool, c_char_p, c_uint32, c_int32, c_ulong, CDLL, cdll, sizeof, windll, c_long, Array

def main():
    #load dll for the wavefront sensor
    lib = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\WFS_64.dll")
    
    #values requested from the dll are passed by reference, this gets thr number of connects WFS devices
    num_devices = c_int32()
    lib.WFS_GetInstrumentListLen(None,byref(num_devices))

    #if no devices connected, close the program
    if num_devices.value == 0:
        print("No availble devices.... closing program")
        quit()
    
    #get connection information for first available WFS device
    device_id = c_int32()
    device_in_use = c_int32() 
    device_name = create_string_buffer(20)
    serial_number = create_string_buffer(20)
    resource_name = create_string_buffer(30)

    lib.WFS_GetInstrumentListInfo(None, 0, byref(device_id), byref(device_in_use), device_name, serial_number, resource_name)

    #check if WFS is in use, if not, connect to device
    if device_in_use:
        print("Wavefront sensor currently in use.... closing program")
        quit()

    instrument_handle = c_ulong()
    lib.WFS_init(resource_name, c_bool(False), c_bool(True), byref(instrument_handle))
    print(f"Connected to {device_name.value} with Serial Number {serial_number.value}")

    #Get the number of calibrated microlens arrays and print out data
    mla_count = c_int32()
    lib.WFS_GetMlaCount(instrument_handle, byref(mla_count))

    mla_name = create_string_buffer(20)
    cam_pitch = c_double()
    lenslet_pitch = c_double()
    spot_offset_x = c_double()
    spot_offset_y = c_double()
    lenslet_focal_length = c_double()
    astigmatism_correction_0 = c_double()
    astigmatism_correction_45 = c_double()
 
    print("Available Microlens Arrays: ")
    for i in range(mla_count.value):
        lib.WFS_GetMlaData(instrument_handle,i ,mla_name, byref(cam_pitch), byref(lenslet_pitch), byref(spot_offset_x), 
            byref(spot_offset_y), byref(lenslet_focal_length), byref(astigmatism_correction_0), byref(astigmatism_correction_45))
        print(f"Index: {i} - MLA Name: {mla_name.value} with lenslet pitch {lenslet_pitch.value}")

    #select MLA    
    lib.WFS_SelectMla(instrument_handle, 0)

    #configure cam resolution and pixel format. Method outputs number of spots in the X and Y for selected MLA
    # PIXEL_FORMAT_MONO8 = 0
    # CAM_RES_1280 = 0
    #Full lists of available sensor reolutions are in the WFS.h header file in C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Include
    num_spots_x = c_int32()
    num_spots_y = c_int32()
    lib.WFS_ConfigureCam(instrument_handle, c_int32(0), c_int32(0), byref(num_spots_x), byref(num_spots_y))
    print(f"Number of detectable spots in X: {num_spots_x.value} \nNumber of detectable spots in Y: {num_spots_y.value}")

    #set WFS internal reference plane
    #other user-defined reference planes can be configured in the WFS software. These are saved to a .ref file and are accessed by passing a 1 instead of 0
    lib.WFS_SetReferencePlane(instrument_handle, c_int32(0))
    lib.WFS_SetPupil(instrument_handle, c_double(0.0), c_double(0.0), c_double(2.0), c_double(2.0))

    #Take a series of images until one is usable. Check the device status after each image to determine usability
    actual_exposure = c_double()
    actual_gain = c_double()
    device_status = c_int32()
    for i in range(10):
        lib.WFS_TakeSpotfieldImageAutoExpos(instrument_handle, byref(actual_exposure), byref(actual_gain))
        lib.WFS_GetStatus(instrument_handle, byref(device_status))
        if device_status.value & 0x00000002:
            print("Power too high")
        elif device_status.value & 0x00000004:
            print("Power too low")
        elif device_status.value & 0x00000008:
            print("High ambient light")
        else:
            print("Image is usable.... breaking loop")
            break
    
    #close program if image is not usable
    if device_status.value & 0x00000002 or device_status.value & 0x00000004 or device_status.value & 0x00000008:
        print("Image is not usable.... closing program")
        quit()

    #calculate all spot centroid positions using dynamic noise cut option
    lib.WFS_CalcSpotsCentrDiaIntens(instrument_handle, c_int32(1), c_int32(1))

    #Calculate Beam Centroid and print values
    beam_centroid_x = c_double()
    beam_centroid_y = c_double()
    beam_diameter_x = c_double()
    beam_diameter_y = c_double()
    lib.WFS_CalcBeamCentroidDia(instrument_handle, byref(beam_centroid_x), byref(beam_centroid_y), byref(beam_diameter_x), byref(beam_diameter_y))
    
    print("Input beam is measured as: ")
    print(f"Centroid X = {beam_centroid_x.value}, Centroid Y = {beam_centroid_y.value}")
    print(f"Diameter X = {beam_diameter_x.value}, Diameter Y = {beam_diameter_y.value}")

    #calculate spot deviations to internal reference
    lib.WFS_CalcSpotToReferenceDeviations(instrument_handle, c_int32(0))

    print('checking spot intensities and printing first 15x15 elements')
    spot_intensities = numpy.zeros((80,80), dtype= numpy.float32)  
    lib.WFS_GetSpotIntensities(instrument_handle, spot_intensities.ctypes.data_as(ctypes.POINTER(c_int32)))

    for i in range(15):
        for j in range(15):
            print(spot_intensities[i][j], end=" ")
        print("")

    print('Calculating Wavefront and printing first 5x5 elements')
    wavefront = numpy.zeros((80,80), dtype= numpy.float32)  
    lib.WFS_CalcWavefront(instrument_handle,c_int32(0), c_int32(0), wavefront.ctypes.data_as(ctypes.POINTER(c_int32)))

    for i in range(5):
        for j in range(5):
            print(wavefront[i][j], end=" ")
        print("")

    print('Closing WFS')
    lib.WFS_close(instrument_handle)


if __name__ == "__main__":
    main()
