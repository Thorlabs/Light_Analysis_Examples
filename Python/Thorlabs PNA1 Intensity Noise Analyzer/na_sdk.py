#Thorlabs Noise Analyzer Python Software Development Kit
#Copyright 2023-2024 Thorlabs Laser Division

##
# @file na_sdk.py
#
# @brief Thorlabs Noise Analyzer Software Development Kit
#
# @section Copyright
# Copyright 2023-2024 Thorlabs Laser Division

'''
License Information:
C:\Program Files (x86)\Thorlabs\IntensityNoiseAnalyzer\License\Thorlabs\
Thorlabs End-user License.rtf
'''

import csv
import ctypes
import datetime
import decimal
import math
import matplotlib.pyplot as mpl
import numpy as np
import time
from enum import Enum

class NoiseAnalyzer_t(ctypes.Structure):
    _fields_ = [("handle_a_", ctypes.c_void_p),
                ("handle_b_", ctypes.c_void_p),
                ("loc_a_",    ctypes.c_uint64),
                ("loc_b_",    ctypes.c_uint64)]

class PNAExcept(Exception):
   msg_ = "null"
   ec_ = -1

   def __init__(self, msg, ec):
      self.msg_ = msg
      self.ec_ = ec

class PNA1:

#----Class Members------------------------------------------------------------------------

   #Constants:
   kFSample = float(12500000.0)
   kNSamples = 8192
   kHiXScale = kFSample / (kNSamples)
   kHiYScale = float(1.0 / 19200000000.00)
   kM1 = 16
   kM2 = 16
   kMidXScale = kFSample / (kNSamples * kM1)
   kLowXScale = kFSample / (kNSamples * kM1 * kM2)
   kMidYScale = float(1.0 / 1200000000.00)
   kLowYScale = float(1.0 / 75000000.00)
   kHFSR = 4.096
   kMaxFrequency = 3e6
   kMinDiff = 100.00000E-18
   kStartHiIndex = int(0)
   kStartLowIndex = int(((kNSamples / 2) + 1) * 2)
   kStartMidIndex = int((kNSamples / 2) + 1)

   #Variables:
   dcAvg = 0.0
   logging = False
   log_file = ""
   log_init = False
   na = NoiseAnalyzer_t()
   na_sdk_dll = "" 
   rms = 1.0
   scans_in_avg = 1
   scans_to_avg = 1
   win_param = 3
   timeDomainPlot = np.empty(shape=(0,2))
   timeDomain = (ctypes.c_float * (3*8192))()
   rawSpectrum = (ctypes.c_float * 12291)()

#----Class Methods------------------------------------------------------------------------
   
   ## __init__
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param log_file_name parameter log filename. If left blank or empty string
   #  e.g. "", logging will not be started.
   #  @param dll_path parameter the path to the TL_NA_SDK.dll. The default path 
   #  "../bin/TL_NA_SDK.dll" is use if parameter is an empty string e.g. "".
   #  @note If user wants to start logging by specifying a filename, but use default
   #  TL_NA_SDK.dll path, the call to PNA1 constructor should be as follows: 
   #  PNA1("example_log", "").
   #  Likewise, if the user wants to load TL_NA_SDK.dll from a user specified path, the call
   #  to the PNA1 constructor should be as follows: 
   #  PNA1("", "./TL_NA_SDK.dll").
   #  @return no return.
   def __init__(self, log_file_name="", dll_path=""):
       na = NoiseAnalyzer_t(0, 0, 0, 0)

       if log_file_name != "":
           self.logging = True
           self.InitLog(log_file_name)

       if dll_path != "":
          self.na_sdk_dll = ctypes.cdll.LoadLibrary(dll_path)
       else:
          self.na_sdk_dll = ctypes.cdll.LoadLibrary("C:\Program Files (x86)\Thorlabs\IntensityNoiseAnalyzer\Bin\TL_NA_SDK.dll")



   ## AnalyzeNoise
   #  Analyses noise from PNA1. This method perform the same operation the PNA1 graphical user 
   #  interface performs in fetching and processing one scan, and producing a set of plots from
   #  that scan.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @return returns a tuple as follows: (RMS(float), DC Average(float), PSD Trace(NumPy array), 
   #  RIN Trace(NumPy array), PSD Trace Combined(NumPy array), RIN Trace Combined(NumPy array), 
   #  PSD Trace Combined Decibel(NumPy array), RIN Trace Combined Decibel(NumPy array), 
   #  Integrated PSD Data(NumPy array),  Integrated RIN Data(Numpy array)). 
   def AnalyzeNoise(self):
      self.GetTimeDomainData()
      self.dcAvg = self.CalculateDCAvg(self.timeDomain)
      self.rms = self.CalculateRMS(self.timeDomain)
      self.TimeToFrequency(True)
      rs = self.rawSpectrum
      plts = self.FormatFrequency(rs)
      psd_plt = plts[0]
      rin_plt = plts[1]
      comb_psd = self.CombineSpectra(psd_plt)
      comb_rin = self.CombineSpectra(rin_plt)
      comb_psd_db = self.ComputeDB(comb_psd)
      comb_rin_db = self.ComputeDB(comb_rin)
      int_psd_data = self.IntegrateData(comb_psd)
      int_rin_data = self.IntegrateData(comb_rin, True)
      
      return (self.rms, self.dcAvg, psd_plt, rin_plt, comb_psd, comb_rin,\
              comb_psd_db, comb_rin_db, int_psd_data, int_rin_data)

   ## AverageNoiseTraces
   #  Averages a given a number of scans.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param scans_to_avg parameter is number of scans to average.
   #  @return returns a tuple in same form that the AnalyzeNoise method returns, but the data
   #  has been averaged a specified number of times.
   def AverageNoiseTraces(self, scans_to_avg):
      self.scans_to_avg = scans_to_avg
      rawFreqData = []
      self.GetTimeDomainData()
      temp_rms = self.CalculateRMS(self.timeDomain)
      temp_dcavg = self.CalculateDCAvg(self.timeDomain)
      rfd = self.TimeToFrequency()
      for i in range(0, len(rfd)):
         rawFreqData.append(rfd[i])
      td = []
      for i in range(1, scans_to_avg+1):
         td = self.GetTimeDomainData()
         self.CalculateRMS(self.timeDomain)
         self.CalculateDCAvg(self.timeDomain)
         newRawFreqData = self.TimeToFrequency(True)
         for j in range(0, len(newRawFreqData)):
            rawFreqData[j] = rawFreqData[j] + (newRawFreqData[j] - rawFreqData[j])/float(i)
         temp_dcavg = (temp_dcavg + self.dcAvg) /2.0 
         temp_rms = math.sqrt((self.rms * self.rms + temp_rms * temp_rms)/ 2.0)
         time.sleep(0.3)

      self.rms = temp_rms
      plts = self.FormatFrequency(rawFreqData)
      psd_plt = plts[0]
      rin_plt = plts[1]
      comb_psd = self.CombineSpectra(psd_plt)
      comb_rin = self.CombineSpectra(rin_plt)
      comb_psd_db = self.ComputeDB(comb_psd)
      comb_rin_db = self.ComputeDB(comb_rin)
      int_psd_data = self.IntegrateData(comb_psd)
      int_rin_data = self.IntegrateData(comb_rin)

      return (self.rms, self.dcAvg, psd_plt, rin_plt, comb_psd, comb_rin,\
              comb_psd_db, comb_rin_db, int_psd_data, int_rin_data)

   ## CalculateDCAvg
   #  Calculates DC average from data in time_domain parameter.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param time_domain parameter time_domain from which the DC average is calculated.
   #  @return returns DC Average.
   def CalculateDCAvg(self, time_domain):
      acc = 0.0
      for i in range(0, len(time_domain)):
         acc += time_domain[i]

      return (acc/float(len(time_domain)))

   ## CalculateRMS
   #  Calculates RMS from data in time_domain parameter.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param time_domain parameter time_domain from which the RMS is calculated.
   #  @return returns rms.
   def CalculateRMS(self, time_domain):
      acc = 0.0
      for i in range(0, len(time_domain)):
         acc += math.pow(time_domain[i], 2.0)

      return math.sqrt(acc/len(time_domain))

   ## Close Method
   #  Closes connection with PNA1.
   #  This Method should be called at the end of a session
   #  in which the noise analyzer was initialized.
   #  Note: If connection is not closed, an error may occur
   #  the next time a the Initailize method is called.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @throws exception is raised if noise analyzer does not disconnect.
   #  @return no return
   def Close(self):
      res = self.na_sdk_dll.CloseNoiseAnalyzer(self.na)
      if res == 0:
         print("Noise Analyzer Disconnected")
         if self.logging:
             self.Log("Noise Analyzer Disconnected")
      else: 
         self.Log("Noise Analyzer could not be disconnected --> EC: "+ str(res))
         raise PNAExcept("Noise Analyzer could not be disconnected --> EC: ", res)

   ## CloseLog
   #  Closes log file
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @return no return.
   def CloseLog(self):
      if self.log_init:
          self.log_file.close()
      self.log_init = False

   ## CombineSpectra
   #  This function puts the trace data in order
   #  with the low sample rate data first, mid sample rate data second, 
   #  and high sample rate data last.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param trace parameter is a psd or rin trace in the form of a NumPy array.
   #  @return returns a NumPy array with previously described operation perform on it.
   def CombineSpectra(self, trace):
      combined = np.empty(shape=(0,2)) 
      last = 0.0

      if len(trace) == 0:
         return combined

      for i in range(self.kStartLowIndex, len(trace)):
         combined = np.append(combined, [trace[i]], axis=0)
      last = combined[-1][0]
      
      for i in range(self.kStartMidIndex, self.kStartLowIndex):
         if trace[i][0] > last:
            combined = np.append(combined, [trace[i]], axis=0)
      last = combined[-1][0]

      for i in range(0, self.kStartMidIndex):
         if trace[i][0] > last:
            combined = np.append(combined, [trace[i]], axis=0)
         if trace[i][0] >= self.kMaxFrequency:
            break

      return combined

   ## ComputeDB 
   #  Converts trace units to dBV^2/Hz and dBc/Hz to PSD and RIN
   #  traces respectively.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param trace parameter is either a combined PSD or combined RIN trace.
   #  @return returns a NumPy array with units converted to dBV^2/Hz or dBc/Hz for
   #  PSD and RIN respectively. 
   def ComputeDB(self, trace):
      combined_db = np.empty(shape=(0,2)) 
      temp = 0.0

      for i in range(0, len(trace)):
         temp =  10.0 * math.log10(trace[i][1])
         if math.isinf(temp):
            combined_db = np.append(combined_db, [[trace[i][0], -140.0]], axis=0)
         else:
            combined_db = np.append(combined_db, [[trace[i][0], temp]], axis=0)

      return combined_db

   ## FormatFrequency
   #  Formats raw frequency data; adds x coordinate
   #  for plotting.
   #  Creates PSD Trace and RIN Trace.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param data parameter is the raw spectrum. This is the time domain after FFT.
   #  @return returns tuple of PSD Trace(NumPy array) and RIN Trace(NumPy array).
   def FormatFrequency(self, data):
      psd_trace = np.empty(shape=(0,2))
      rin_trace = np.empty(shape=(0,2))

      for i in range(0, len(data)):
         if i <= 4096:
            psd_trace = np.append(psd_trace, [[float(i) * self.kHiXScale, data[i] *\
                                                            self.kHiYScale]], axis=0)
            rin_trace = np.append(rin_trace, [[float(i) * self.kHiXScale, (data[i]*\
                    self.kHiYScale)/math.pow(self.rms * self.kHFSR, 2.0)]], axis=0)
         elif i < self.kStartLowIndex:
            psd_trace = np.append(psd_trace, [[(float(i) - self.kStartMidIndex)*\
                                             self.kMidXScale, data[i] * self.kMidYScale]], axis=0)
            rin_trace = np.append(rin_trace, [[(float(i) - self.kStartMidIndex)* self.kMidXScale,\
                       (data[i] * self.kMidYScale)/math.pow(self.rms * self.kHFSR, 2.0)]], axis=0)
         else:
            psd_trace = np.append(psd_trace, [[(float(i) - self.kStartLowIndex)* self.kLowXScale,\
                                               data[i] * self.kLowYScale]], axis=0)
            rin_trace = np.append(rin_trace, [[(float(i) - self.kStartLowIndex)* self.kLowXScale,\
                    (data[i]*self.kLowYScale)/math.pow(self.rms * self.kHFSR, 2.0)]], axis=0)
      return (psd_trace, rin_trace)

   ## GetSampleRate
   #  This method divides sample rates of the time domain data into low, medium, or, high.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param speed parameter can be one of three options: 0=LOW, 1=MID, 2=HIGH.
   #  #return returns a time domain plot (NumPy array) of low, medium, or high sample rate 
   #  depending on the speed parameter.
   def GetSampleRate(self, speed):
      match speed:
         case 0:
            low = np.empty(shape=(0,2))
            for i in range(16384, 24576):
               low = np.append(low, [self.timeDomainPlot[i]], axis=0)

            return low

         case 1:
            mid = np.empty(shape=(0,2))
            for i in range(8192, 16384):
               mid = np.append(mid, [self.timeDomainPlot[i]], axis=0)
             
            return mid

         case 2:
            high = np.empty(shape=(0,2))
            for i in range(0, 8192):
               high = np.append(high, [self.timeDomainPlot[i]], axis=0)

            return high 
      
         case default:
            low = np.empty(shape=(0,2))
            for i in range(16384, 24576):
               low = np.append(low, [self.timeDomainPlot[i]], axis=0)

            return low
   
   ## GetTimeDomainData Method
   #  Gets time domain data from PNA1.
   #  This method can return new data once every 200 milliseconds.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @throws exception is raised if unable to retrieve time domain data.
   #  @return returns time domain (NumPy array).
   def GetTimeDomainData(self):
      res = self.na_sdk_dll.GetTimeDomain(self.na, ctypes.byref(self.timeDomain))
      if res == 0:
         print("Successfully Retrieved Time Domain Data")
         if self.logging:
            self.Log("Successfully Retrieved Time Domain Data")
      else: 
         if self.logging:
            self.Log("Could not retrieve time domain data --> EC: "+ str(res))
         raise PNAExcept("Could not retrieve time domain data --> EC: ", res)

      td = np.empty(0)
      for i in range(0, len(self.timeDomain)):
         td = np.append(td, float(self.timeDomain[i]))
      return td

   ## GetTimeDomainPlot
   #  Converts time domain data to a time domain plot.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @return returns a time domain plot as a NumPy array.
   def GetTimeDomainPlot(self):
      for i in range(0,  len(self.timeDomain)):
         if i <  self.kNSamples:
            self.timeDomainPlot = np.append(self.timeDomainPlot, \
                             [[float(i)/self.kFSample, self.timeDomain[i] * self.kHFSR]], axis=0)
         elif i <  self.kNSamples * 2:
            self.timeDomainPlot = np.append(self.timeDomainPlot, \
                             [[float(i - self.kFSample) * self.kM1/self.kFSample,\
                                self.timeDomain[i] * self.kHFSR]], axis=0)
         else:
            self.timeDomainPlot = np.append(self.timeDomainPlot, \
                             [[float(i - self.kFSample*2) * self.kM1 * self.kM2/self.kFSample,\
                     self.timeDomain[i] * self.kHFSR]], axis=0)
      return self.timeDomainPlot.copy()
               
   ## Initialize Method
   #  Finds and Initializes Thorlabs PNA1.
   #  This method must be called before
   #  any other methods involving the operation of the PNA1 can be called.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @throws exception is raised if noise analyzer is not found. 
   #  @throws exception is raised if noise analyzer could not be initialized. 
   #  @return no return.
   def Initialize(self):
      res = self.na_sdk_dll.FindNoiseAnalyzer(ctypes.byref(self.na))
      if res == 0:
         print("Noise Analyzer Found")
         if self.logging:
            self.Log("Noise Analyzer Found")
         res = self.na_sdk_dll.InitNoiseAnalyzer(ctypes.byref(self.na))
         if res == 0:
            print("Noise Analyzer Initialized")
            if self.logging:
                self.Log("Noise Analyzer Initialized")
         else:
            print("Could not initialize Noise Analyzer --> EC: ", res)
            if self.logging:
                self.Log("Could not initialize Noise Analyzer --> EC: "+ str(res))
            raise PNAExcept("Could not initialize Noise Analyzer --> EC: ", res)
      else:
         if self.logging:
             self.Log("Noise Analyzer not found: " + str(res))
         raise PNAExcept("Noise Analyzer not found", res)
      
   ## InitLog
   #  Opens log file
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param file_name parameter is the log file name.
   #  @return no return
   def InitLog(self, file_name):
      self.log_file = open(file_name, 'a')
      self.log_init = True

   ## IntegrateData
   #  method return integrated data from a combined PSD or RIN trace
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param combined_trace parameter is a combined PSD or RIN Trace
   #  @param pct parameter is False by default. If True, the trace is scaled to 
   #  a percentage scale.
   #  @return returns an integrated trace as a NumPy array.
   def IntegrateData(self, combined_trace, pct = False):
      int_combined_trace = np.empty(shape=(0,2))
      acc = 0.0
      val = 0.0

      if len(combined_trace) == 0:
         return int_combined_trace
      
      int_combined_trace = np.append(int_combined_trace, [[0.0, 0.0]], axis=0)
      
      for i in range(1, len(combined_trace)):
         acc += ((combined_trace[i][1] + combined_trace[i-1][1]) *\
                 (combined_trace[i][0] - combined_trace[i-1][0])/2.0)
         if not pct:
            int_combined_trace = np.append(int_combined_trace, [[combined_trace[i][0],\
                                                                math.sqrt(float(acc))]], axis=0)
         else:
           val = 100.0 * math.sqrt(float(acc))
           if val > 100.0:
              int_combined_trace = np.append(int_combined_trace, [[combined_trace[i][0],\
                                                                                100.0]], axis=0)
           else:
              int_combined_trace = np.append(int_combined_trace, [[combined_trace[i][0],\
                                                                                  val]], axis=0)

      return int_combined_trace

   ## LoadDLL
   #  Loads tl_na_sdk dll
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param dll_path parameter is a user specified path to the tl_na_sdk dll 
   #  @return no return
   def LoadDLL(self, dll_path):
      self.na_sdk_dll = ctypes.cdll.LoadLibrary(dll_path)

   ## LoadReference
   #  Loads a saved reference from file.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param ref_name parameter is the name of the reference file to be loaded
   #  with the .csv suffix included in the string.
   #  @param col_choice parameter is 1 by default. The col_choice parameter selects which
   #  column of the reference file is loaded. 0=Frequency, 1=Combined PSD Trace, 2=Combined PSD 
   #  trace in dBV^2/Hz units, 3=Combined RIN trace in dBc/HZ units, 4=Integrated Combined PSD 
   #  trace, 5=Integrated Combined RIN trace.
   #  @return returns list with following format: 
   #  [Timestamp, Scans in Average, Termination, V_RMS(V), V_DC(V), RMS_Noise %, selected column as 
   #  NumPy array]
   def LoadReference(self, ref_name, col_choice=1):
      ref_info = ["", 0.0, 0.0, 0.0, 0.0, 0.0, []]
      with open(ref_name, newline='') as opened_file:
         reader = csv.reader(opened_file, delimiter=',')
         for row in reader:
            match row[0]:
               case "Timestamp":
                  ref_info[0] = row[1]
               case "Scans in Average":
                  ref_info[1] = float(row[1])

               case "Termination":
                  ref_info[2] = float(row[1])

               case "V_RMS(V)":
                  ref_info[3] = float(row[1])

               case "V_DC (V)":
                  ref_info[4] = float(row[1])

               case "RMS_Noise %":
                  ref_info[5] = float(row[1])

               case "Frequency (Hz)":
                  loaded = np.empty(shape=(0,2))
                  cnt = 0
                  for i in reader:
                     loaded = np.append(loaded, [[float(cnt), float(i[col_choice])]], axis=0)
                     cnt+=1
                  ref_info[6] = loaded
                  break

      return ref_info 

   ## Log
   #  Writes message to log file
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param msg parameter is the message to be written to the log file
   #  @return no return
   def Log(self, msg):
      if self.log_init:
          self.log_file.write(str(datetime.datetime.now()) + ':' + msg + '\n')
      else:
          raise PNAExcept("Log file not initialized", 1)

   ## SaveReference
   #  Saves a reference trace.
   #  The required data should be in the same format as the tuple returned by the AnalyzeNoise
   #  and AverageNoiseTraces methods.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param data parameter is a tuple the following format: 
   #  (RMS(float), DC Average(float), PSD Trace(NumPy array), 
   #  RIN Trace(NumPy array), PSD Trace Combined(NumPy array), RIN Trace Combined(NumPy array), 
   #  PSD Trace Combined Decibel(NumPy array), RIN Trace Combined Decibel(NumPy array), 
   #  Integrated PSD Data(NumPy array),  Integrated RIN Data(Numpy array)). 
   #  @param parameter is the name of the reference file without an extension suffix.
   #  @return no return.
   def SaveReference(self, data, ref_name): 
      with open(str(ref_name)+".csv", 'w', newline='') as save_file:
         saveref = csv.writer(save_file)
         t = datetime.datetime.now()
         t.strftime('%m.%d.%Y:%H:%M:%S')
         saveref.writerow(["Timestamp", str(t.strftime('%m.%d.%Y:%H:%M:%S'))])
         saveref.writerow(["Scans in Average", str(self.scans_in_avg)])
         saveref.writerow(["Termination", "10000"])
         saveref.writerow(["V_RMS(V)", str(float(self.rms*self.kHFSR))])
         saveref.writerow(["V_DC (V)", str(float(self.dcAvg))])
         saveref.writerow(["RMS_Noise %", str(data[9][-1][1])])
         saveref.writerow(["Frequency (Hz)", "Mag^2 (V^2 / Hz)", "PSD (dBV^2 / Hz)", \
                           "RIN (dBc / Hz)", "Integrated Volts RMS", "Integrated RIN (%RMS)"])
         for i in range(0, len(data[4])):
            saveref.writerow([str(float(data[4][i][0])), str(float(data[4][i][1])), \
                    str(float(data[6][i][1])), str(float(data[7][i][1])), \
                    str(float(data[8][i][1])), str(float(data[9][i][1]))])

   ## SetWindowParameter
   #  Sets the window function to apply to the time domain for the FFT.
   #  Window functions: RECT_1, BLACKMAN_HARRIS, HANNING -- Default is HANNING
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param win_param parameter is an integer corresponding to a windowing function where, 
   #  0=RECT_1, 1=BLACKMAN_HARRIS, and 3=HANNING.
   #  @return no return.
   def SetWindowParameter(self, win_param):
      self.win_param = win_param

   ## SubtractReference
   #  Subtracts a loaded reference from a measured spectrum
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param combined parameter reference PSD trace.
   #  @param combined parameter measured PSD trace.
   #  @return Returns a NumPy array where combined reference psd trace subtracted 
   #  from combined measured psd trace.
   def SubtractReference(self, combined_ref_trace,  combined_trace):
      diff = 0.0
      subtracted_combined = np.empty(shape=(0,2))

      if len(combined_trace) != len(combined_ref_trace):
         return

      for i in range(0, len(combined_trace)):
         diff =  combined_trace[i][1] - combined_ref_trace[i][1]
         if diff < self.kMinDiff:
             diff = self.kMinDiff
         subtracted_combined = np.append(subtracted_combined, \
                                          [[combined_trace[i][0], diff]], axis=0)

      return subtracted_combined

   ## TimeToFrequency method
   #  Performs FFT on time domain yielding frequency data.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param sub_avg parameter is False by default. If True, subtracts the DC average from the
   #  time domain data before the FFT. 
   #  @throws exception is raised if unable to retieve spectrum.
   #  @return returns frequency data NumPy array.
   def TimeToFrequency(self, sub_avg=False):
      if sub_avg:
         for i in range(0, len(self.timeDomain)):
            self.timeDomain[i] = self.timeDomain[i] - self.dcAvg
          
      for i in range(0 , len(self.timeDomain)):
         self.timeDomain[i] = self.timeDomain[i] * self.kHFSR

      res = self.na_sdk_dll.GetSpectrum(ctypes.byref(self.timeDomain), \
              ctypes.byref(self.rawSpectrum), self.win_param)
      if res == 0:
         print("Succesfully Retrieved Spectrum")
         if self.logging:
            self.Log("Succesfully Retrieved Spectrum")
         else:
            if self.logging:
                self.Log("Could Not Retrieve Spectrum --> EC: " + str(res))
            raise PNAExcept("Could Not Retrieve Spectrum --> EC: ", res)
      rs =  np.empty(0)
      for i in range(0, len(self.rawSpectrum)):
         rs = np.append(rs, float(self.rawSpectrum[i]))
      return rs

   ## Window
   #  Window applies a specified windowing function to the time domain.
   #  @param self parameter is the current object instance of the PNA1 class.
   #  @param win_param parameter is an integer corresponding to a windowing function where, 
   #  0=RECT_1, 1=BLACKMAN_HARRIS, and 3=HANNING.
   #  @throws exception is raised if windowing function application is not successful.
   #  @return no return.
   def Window(self, win_param=-1):
      wp = 3
      if win_param < 0:
         wp = self.win_param
      else:
         wp = win_param
      res = self.na_sdk_dll.Window(ctypes.byref(self.timeDomain), ctypes.c_uint(8192), wp)
      if res != 0:
         if self.logging:
             self.Log("Could Not Apply Windowing Function: "+ str(res))
         raise PNAExcept("Could Not Apply Windowing Function: ", res)

