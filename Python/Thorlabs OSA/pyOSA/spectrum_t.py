import logging
import typing
import ctypes as c
import datetime

import numpy as np

from pyOSA.FTSLib import FTSLib
from pyOSA.constants import constants
from pyOSA.units import units

# This file contains the Python implementation of the spectrum_t class
# (spectrum_t is originaly a struct implemented in C++, see FTSData.h)
# In addition to the struct itself, the Python class also contains
# some functions that return information from a spectrum_t object
#
# Note: Do not change anything in this file that concerns the spectrum_t definition!
#       If you miss a function to obtain some specific parameter from an
#       spectrum_t object, please let us know through techsupport.se@thorlabs.com
#       Of course, you may add such functions yourself, but please let us know anyway;
#       there are probably more customers who could have use of the same function

logger = logging.getLogger('pyOSA')

### Code for python implementation of spectrum_t ###


data_defines = constants.data_defines
OSA200_resolutions = constants.OSA200_resolutions
OSA200_sensitivities = constants.OSA200_sensitivities
Redstone_resolutions = constants.Redstone_resolutions
Redstone_sensitivities = constants.Redstone_sensitivities
instrument_series = constants.instrument_series
instrument_models = constants.instrument_models


# Defined array lengths used in spectrum_t

INSTRUMENT_SERIES_IDENTIFIER_STRLENGTH = 32
MAX_PHASE_POLY_ORDER = 3
SPECTRUM_SOURCE_STRLENGTH = 24
GENERAL_FIRMWARE_REV_STRLENGTH = 30
MAX_CALIBRATION_COEFFICIENTS = 32
SPECTRUM_OPERATOR_STRLENGTH = 24
SPECTRUM_COMMENT_LONG_LENGTH = 4096
MAX_SPECTROMETER_CHANNELS = 6
SPECTRUM_MODEL_STRLENGTH = 24
MAX_SMOOTH_PARAMETERS = 4
SPECTRUM_COMMENT_LENGTH = 128
SERIALNUMBER_LENGTH = 32
MAX_GAINLEVELS_PER_SCAN = 16
SPECTRUM_NAME_LENGTH = 32


AUTOGAIN_STATUS_SATISFIED = 2
AUTOGAIN_STATUS_WANTS_TO_DECREASE_BUT_NO_SUITABLE_GAIN_WAS_FOUND = 5
AUTOGAIN_STATUS_WANTS_TO_INCREASE_BUT_NO_SUITABLE_GAIN_WAS_FOUND = 6

# Definition of spectrum_t

class spectrum_t(c.Structure):
    """
    Represents the internal data format used by ThorSpectra.
    
    This Python object grants access to the internal attributes and offers some
    methods for convenient access.
    """
    _fields_ = [
        ("hdrsize", c.c_ushort),
        ("hdrversion", c.c_ushort),
        ("length", c.c_uint),
        ("xAxisUnit", c.c_ushort),
        ("yAxisUnit", c.c_ushort),
        ("acquisitionMode", c.c_ubyte),
        ("xValueFormat", c.c_ubyte),
        ("x_minWnr", c.c_float),
        ("x_maxWnr", c.c_float),
        ("x_min", c.c_float),
        ("x_max", c.c_float),
        ("y_min", c.c_float),
        ("y_max", c.c_float),
        ("gainLevel", c.c_double * MAX_GAINLEVELS_PER_SCAN),
        ("gainPos", c.c_uint * MAX_GAINLEVELS_PER_SCAN),
        ("resolution", c.c_float),
        ("type", c.c_ushort),
        ("interferometerSerial", c.c_char * SERIALNUMBER_LENGTH),
        ("referenceWavelength_nm_vac", c.c_double),
        ("samplingDistance_cm_vac", c.c_double),
        ("date", c.c_uint),
        ("time", c.c_uint),
        ("gmtTime", c.c_uint),
        ("averageNum", c.c_uint),
        ("smoothParam", c.c_ushort * MAX_SMOOTH_PARAMETERS),
        ("smoothType", c.c_ushort),
        ("igramSmoothParam", c.c_ushort * MAX_SMOOTH_PARAMETERS),
        ("igramSmoothType", c.c_ushort),
        ("phaseCorrection", c.c_ubyte),
        ("apodization", c.c_ubyte),
        ("zeroFillFactor", c.c_float),
        ("air_temp", c.c_float),
        ("air_press", c.c_float),
        ("air_relHum", c.c_float),
        ("name", c.c_char * SPECTRUM_NAME_LENGTH),
        ("comment", c.c_char * SPECTRUM_COMMENT_LENGTH),
        ("allocatedLengthI", c.c_uint),
        ("allocatedLengthx", c.c_uint),
        ("adcBits", c.c_ubyte),
        ("sensitivityMode", c.c_ushort),
        ("resolutionMode", c.c_ushort),
        ("rollingAverage", c.c_bool),
        ("source", c.c_char * SPECTRUM_SOURCE_STRLENGTH),
        ("calibWaveNr", c.c_float * MAX_CALIBRATION_COEFFICIENTS),
        ("calib_Coeff", c.c_float * MAX_CALIBRATION_COEFFICIENTS),
        ("calibCoeffNum", c.c_ubyte),
        ("samplesPerReference", c.c_ubyte),
        ("minOPD_cm", c.c_float),
        ("maxOPD_cm", c.c_float),
        ("air_measureOption", c.c_uint),
        ("phasePolynomial", c.c_float * (MAX_PHASE_POLY_ORDER + 1)),
        ("interferogramProperty", c.c_int),
        ("instr_operator", c.c_char * SPECTRUM_OPERATOR_STRLENGTH),
        ("interferogramOffset", c.c_float),
        ("apodizationPowerCompensation", c.c_float),
        ("instrument_model", c.c_ushort),
        ("phiValueFormat", c.c_ubyte),
        ("allocatedLengthPhi", c.c_uint),
        ("instrumentType", c.c_ushort),
        ("triggerMode", c.c_ushort),
        ("integrationTime_ms", c.c_double),
        ("instr_model_str", c.c_char * SPECTRUM_MODEL_STRLENGTH),
        ("allocatedLengthLog", c.c_uint),
        ("wavelength_correction", c.c_double * 4),
        ("wavenr_shift", c.c_double * 4),
        ("wavelength_shift", c.c_double * 4),
        ("detector_temperature_C", c.c_float),
        ("external_temperature_C", c.c_float),
        ("external_pressure_hPa", c.c_float),
        ("external_relHum_percent", c.c_float),
        ("detectorCoolingState", c.c_ushort),
        ("instrumentStatus", c.c_uint),
        ("calculatedWithCUDA", c.c_bool),
        ("series", c.c_ushort),
        ("channelIndex", c.c_ushort),
        ("channelStatus", c.c_uint),
        ("detectorType", c.c_ushort),
        ("detectorOffset", c.c_ushort),
        ("samplingRate_MHz", c.c_float),
        ("fractionalIdxZeroPathDifference", c.c_double),
        ("halfRange_DoubleSidedLowRes_cm", c.c_double),
        ("halfRange_SingleSidedFullRes_cm", c.c_double),
        ("sourceType", c.c_ushort),
        ("DoNotUse_usedToBeIsBroadband", c.c_ushort),
        ("commentLong", c.c_char * SPECTRUM_COMMENT_LONG_LENGTH),
        ("refLaserLocked", c.c_ushort),
        ("refLaserLowPower", c.c_ushort),
        ("refLaserHighPower", c.c_ushort),
        ("contrast", c.c_double),
        ("approximateSamplesPerRefInRawIgram", c.c_ushort),
        ("attenuationFilterUsed", c.c_ushort),
        ("x_minHz", c.c_float),
        ("x_maxHz", c.c_float),
        ("gainIndex", c.c_ushort),
        ("noiseAmplitudeCutoffTimes10", c.c_ushort),
        ("offsetPlot", c.c_double),
        ("isPulsed", c.c_ushort),
        ("approximatePulseFrequency", c.c_double),
        ("detectorSort", c.c_ushort),
        ("amplifierSort", c.c_ushort),
        ("interferogramAverageNum", c.c_uint),
        ("extra_for_temporary_debugging_double_1", c.c_double),
        ("extra_for_temporary_debugging_double_2", c.c_double),
        ("extra_for_temporary_debugging_double_3", c.c_double),
        ("extra_for_temporary_debugging_double_4", c.c_double),
        ("extra_for_temporary_debugging_double_5", c.c_double),
        ("extra_for_temporary_debugging_int_1", c.c_int),
        ("extra_for_temporary_debugging_int_2", c.c_int),
        ("extra_for_temporary_debugging_int_3", c.c_int),
        ("extra_for_temporary_debugging_int_4", c.c_int),
        ("extra_for_temporary_debugging_int_5", c.c_int),
        ("isStitched", c.c_ushort),
        ("stitched_x_minWnr", c.c_float * MAX_SPECTROMETER_CHANNELS),
        ("stitched_x_maxWnr", c.c_float * MAX_SPECTROMETER_CHANNELS),
        ("stitched_detectorType", c.c_ushort * MAX_SPECTROMETER_CHANNELS),
        ("stitched_gainLevel", c.c_double * MAX_SPECTROMETER_CHANNELS),
        ("stitched_detector_temperature_C", c.c_float * MAX_SPECTROMETER_CHANNELS),
        ("stitched_channelStatus", c.c_uint * MAX_SPECTROMETER_CHANNELS),
        ("stitched_detectorOffset", c.c_ushort * MAX_SPECTROMETER_CHANNELS),
        ("stitched_contrast", c.c_double * MAX_SPECTROMETER_CHANNELS),
        ("stitched_attenuationFilterUsed", c.c_ushort * MAX_SPECTROMETER_CHANNELS),
        ("stitched_detectorSort", c.c_ushort * MAX_SPECTROMETER_CHANNELS),
        ("stitched_amplifierSort", c.c_ushort * MAX_SPECTROMETER_CHANNELS),
        ("stitched_gainIndex", c.c_ushort * MAX_SPECTROMETER_CHANNELS),
        ("startPos_um", c.c_int),
        ("endPos_um", c.c_int),
        ("trigPos_um", c.c_int),
        ("distanceFromStagePosAtoZPD_cm", c.c_float),
        ("gainOrOffsetHasChangedSignificantly", c.c_ushort),
        ("speedFactor", c.c_float),
        ("maxInterferogram", c.c_float),
        ("minInterferogram", c.c_float),
        ("stitched_maxInterferogram", c.c_float * MAX_SPECTROMETER_CHANNELS),
        ("stitched_minInterferogram", c.c_float * MAX_SPECTROMETER_CHANNELS),
        ("stitched_detectorCoolingState", c.c_ushort * MAX_SPECTROMETER_CHANNELS),
        ("fractionalIdxZeroPathDifference_BBRef", c.c_double),
        ("fractionalIdxZeroPathDifference_Ref", c.c_double),
        ("fractionalIdxZeroPathDifference_DUT1", c.c_double),
        ("fractionalIdxZeroPathDifference_DUT2", c.c_double),
        ("idxAtMaxP2Pin200interferogramOr300RawInterferogram", c.c_int),
        ("maxControlLoopError", c.c_int),
        ("stageStatus", c.c_uint),
        ("latchedStageStatus", c.c_uint),
        ("latchedChannelStatus", c.c_uint),
        ("latchedInstrumentStatus", c.c_uint),
        ("stitched_latchedChannelStatus", c.c_uint * MAX_SPECTROMETER_CHANNELS),
        ("softwareVersion", c.c_char * GENERAL_FIRMWARE_REV_STRLENGTH),
        ("firmwareVersion", c.c_char * GENERAL_FIRMWARE_REV_STRLENGTH),
        ("motorFirmwareVersion", c.c_char * GENERAL_FIRMWARE_REV_STRLENGTH),
        ("hdrversionOriginal", c.c_ushort),
        ("importedFileformat", c.c_ushort),
        ("softwareVersionReconstructionAlgorithms", c.c_char * GENERAL_FIRMWARE_REV_STRLENGTH),
        ("firmwareVersionSensor", c.c_char * GENERAL_FIRMWARE_REV_STRLENGTH),
        ("instrumentSeriesIdentifier", c.c_char * INSTRUMENT_SERIES_IDENTIFIER_STRLENGTH),
        ("excitationWavelength_nm", c.c_double),
        ("stacking_count", c.c_ushort),
        ("sensorExposure_ms", c.c_ushort),
        ("sensorGain_dB", c.c_float),
        ("sensorBlackLevel_count", c.c_ushort),
        ("offsetDarkLevel_double", c.c_double),
        ("dynamicRange_count", c.c_ushort),
        ("dynamicRangeMedian_count", c.c_ushort),
        ("dynamicRangeUtil_count", c.c_ushort),
        ("flagsMath_64bit", c.c_ulonglong),
        ("flagsSample_64bit", c.c_ulonglong),
        ("flagsEnvironment_64bit", c.c_ulonglong),
        ("UUIDTagTimeLow_32bit", c.c_ulong),
        ("UUIDTagTimeMid_16bit", c.c_uint),
        ("UUIDTagTimeHiAndVer_16bit", c.c_uint),
        ("UUIDTagClockSeqHiAndReserved_8bit", c.c_ushort),
        ("UUIDTagClockSeqLow_8bit", c.c_ushort),
        ("UUIDTagNode_48bit", c.c_ulonglong),
        ("refGainIndex", c.c_ushort),
        ("refSignalInPercent", c.c_float),
        ("BBRefGainIndex", c.c_ushort),
        ("BBRefSignalInPercent", c.c_float),
        ("autogainStatus", c.c_ushort),
        ("stitched_autogainStatus", c.c_ushort * MAX_SPECTROMETER_CHANNELS),
        ("phi", c.POINTER(c.c_float)),
        ("I", c.POINTER(c.c_float)),
        ("x", c.POINTER(c.c_float)),
        ("logData", c.c_void_p),
    ]

    ### End of code for python implementation of spectrum_t ###


    ##################################################################################
    # The following functions grab information from a spectrum_t object
    # For more attributes, see above or look at the spectrum_t struct in FTSData.h
    ##################################################################################


    def is_spectrum(self) -> bool:
        """Returns True if the measured data is a spectrum.
        """
        spectrum_types = [data_defines["SPEC_EMISSION"], data_defines["SPEC_TRANSMITTANCE"], data_defines["SPEC_ABSORBANCE"], data_defines["SPEC_KUBELKA_MUNK"], data_defines["SPEC_REFLECTANCE"], data_defines["SPEC_LOG_1_R"], data_defines["SPEC_RAMAN"]]
        return self.type in spectrum_types

    def is_interferogram(self) -> bool:
        """Returns True if the measured data is an interferogram.
        """
        return self.type == data_defines["SPEC_INTERFEROGRAM"]

    def is_OSA200(self) -> bool:
        """Returns True if the measured data was captured using an OSA20X.
        """
        return constants._is_OSA200(self.series)

    def is_Redstone(self) -> bool:
        """Returns True if the measured data was captured using a Redstone series spectrometer.
        """
        return constants._is_Redstone(self.series)

    def _is_virtual(self) -> bool:
        """Returns true if the measured data was captured using a virtual OSa200/Redstone
        """
        for model, model_name in constants.instrument_models.items():
            if 'VIRTUAL' in model_name.upper():
                if self.instrument_model == model:
                    return True
        return False
    
    def _is_interferogram_clipped(self) -> bool:
        """Returns True if the interferogram was clipped/saturated.

        If called for a spectrum (also a stitched spectrum), it is still the clipping/saturation of the
        interferogram resulting in this spectrum which is tested.
        """
        if not (self.is_OSA200() or self.is_Redstone()):
            error_message = "Error in _is_interferogram_clipped(): Unknown instrument model."
            logger.error(error_message)
            raise Exception(error_message)

        # Check the saturation/clipping flag set by the instrument firmware; this works also for a stitched spectrum
        INTERFEROGRAM_PROPERTY_SATURATED = 0x01 # Flag set to indicate that the interferogram is saturated
        if (self.interferogramProperty & INTERFEROGRAM_PROPERTY_SATURATED):
            return True

        # Check if the interferogram min and max values are within the range of the instrument's detector
        if self.is_interferogram():
            y_min_list = [self.y_min]
            y_max_list = [self.y_max]
        elif self.is_spectrum():
            if not self.isStitched:
                y_min_list = [self.minInterferogram] # #MUSTFIX These values seems to be 0.0 on a virtual device. Why?
                y_max_list = [self.maxInterferogram]
            else:
                # Stitched spectrum -> we need to check 
                y_min_list = []
                y_max_list = []
                dut_detector_indices = self._getchannel_idx_for_dut_detectors()
                for dut_detector_index in dut_detector_indices.values():
                    y_min_list.append(self.stitched_minInterferogram[dut_detector_index])
                    y_max_list.append(self.stitched_maxInterferogram[dut_detector_index])
        else:
            error_message = "Error in _is_interferogram_clipped(): Unknown spectrum_t type."
            logger.error(error_message)
            raise Exception(error_message)

        detector_range = (2 ** self.adcBits) - 1
        MARGIN = 10 # The same definition as in FTSLib
        for y_min, y_max in zip(y_min_list, y_max_list):
            if (y_min < (0 + MARGIN)) or (y_max > (detector_range - MARGIN)):
                return True
        return False

    def _getchannel_idx_for_dut_detectors(self) -> dict:
        """
        Returns the channel indices for detector 1 and Detector 2 for a stitched spectrum
        """
        dut_detector_indices = {}
        if self.isStitched:
            for i in range(len(self.stitched_detectorType)):
                if self.stitched_detectorType[i] == constants.data_defines['DETECTOR_TYPE_DUT1']:
                    dut_detector_indices["Detector 1"] = i
                elif self.stitched_detectorType[i] == constants.data_defines['DETECTOR_TYPE_DUT2']:
                    dut_detector_indices["Detector 2"] = i
        return dut_detector_indices

    # Note that since interferogramProperty is set as bitwise-or of the individual interferograms, this works also for a stitched spectrum
    def _is_interferogram_nonlinear(self) -> bool:
        """Returns True if the interferogram is nonlinear.

        If called for a spectrum (also a stitched spectrum), it is still the nonlinearity of the
        interferogram resulting in this spectrum which is tested.
        """
        INTERFEROGRAM_PROPERTY_NONLINEAR_REGIME = 0x02 # Flag set to indicate that the intensity of the interferogram is so high that there is a risk of non-linear behavior
        interferogram_is_nonlinear  = self.interferogramProperty & INTERFEROGRAM_PROPERTY_NONLINEAR_REGIME
        if self.is_Redstone():
            INTERFEROGRAM_PROPERTY_TOO_STRONG_WITH_FILTER = 0x04 # Flag set to indicate that the interferogram signal is too strong even though a filter is already active
            interferogram_is_nonlinear = interferogram_is_nonlinear or (self.interferogramProperty & INTERFEROGRAM_PROPERTY_TOO_STRONG_WITH_FILTER)
        return interferogram_is_nonlinear != 0

    @staticmethod
    # Calculates the signal (in %)
    def _signal_in_percent(y_min: float, y_max: float, detector_range:float) -> float:
        return 100 * (y_max - y_min) / detector_range

    def get_interferogram_signal_in_percent(self, detector=None) -> float:
        """Returns the interferogram signal (in percent) for the measured data

        This function can be called for either an interferogram or a spectrum. If called for a spectrum,
        it is still the signal of the interferogram resulting in the spectrum which is tested.
        For a stitched Redstone spectrum, the detector ('Detector 1' or 'Detector 2') needs to be specified.

        Examples:
        
        .. code-block:: python
        
            interferogram.get_interferogram_signal_in_percent()
            
            spectrum.get_interferogram_signal_in_percent()

            stitched_spectrum.get_interferogram_signal_in_percent('Detector 1')
        """
        if not (self.is_OSA200() or self.is_Redstone()):
            error_message = "Error in get_interferogram_signal_in_percent(): Unknown instrument model."
            logger.error(error_message)
            raise Exception(error_message)
        if  self.isStitched and (not self.is_Redstone()):
            error_message = "Error in get_interferogram_signal_in_percent(): A stitched spectrum must be from a Redstone."
            logger.error(error_message)
            raise ValueError(error_message)
        if (detector is not None) and not (self.is_spectrum() and self.isStitched):
            error_message = "Error in get_interferogram_signal_in_percent(): No detector should be given unless a stitched spectrum is used."
            logger.error(error_message)
            raise ValueError(error_message)
        if (self.is_spectrum() and self.isStitched) and (detector.upper() not in ['DETECTOR 1', 'DETECTOR 2']):
            error_message = "Error in get_interferogram_signal_in_percent(): Can only be called for 'Detector 1' or 'Detector 2'."
            logger.error(error_message)
            raise ValueError(error_message)
        
        detector_range = (2 ** self.adcBits) - 1

        if self.is_interferogram():
            y_min = self.y_min
            y_max = self.y_max
            return self._signal_in_percent(y_min, y_max, detector_range)

        elif not self.is_spectrum():
            error_message = "Error in get_interferogram_signal_in_percent(): Only callable for an interferogram or a spectrum."
            logger.error(error_message)
            raise Exception(error_message)

        # Spectrum

        if not self.isStitched:
            y_min = self.minInterferogram
            y_max = self.maxInterferogram
            return self._signal_in_percent(y_min, y_max, detector_range)

        # Stitched spectrum

        channel_detector_indices = self._getchannel_idx_for_dut_detectors()
        channel_detector_index = channel_detector_indices[detector.lower().capitalize()]

        y_min = self.stitched_minInterferogram[channel_detector_index]
        y_max = self.stitched_maxInterferogram[channel_detector_index]
        return self._signal_in_percent(y_min, y_max, detector_range)

        
    def get_model(self) -> str:
        """Returns the instrument model used to measure the data as a string, e.g., 'OSA201C'
        """
        if self.instrument_model in instrument_models:
            return instrument_models[self.instrument_model]
        else:
            error_message = "Error in get_model(): Unknown instrument model."
            logger.error(error_message)
            raise Exception(error_message)

    def get_serial_number(self) -> str:
        """Returns the serial number of the instrument used to measure the data.
        """
        return self.interferometerSerial.decode("utf-8")

    def get_resolution(self) -> str:
        """Returns the instrument resolution.
        """
        if self.is_OSA200():
            if self.resolutionMode not in OSA200_resolutions:
                error_message = f"Error in get_resolution(): Invalid resolution mode: {self.resolutionMode}."
                logger.error(error_message)
                raise Exception(error_message)
            return OSA200_resolutions[self.resolutionMode]
        elif self.is_Redstone():
            if self.resolutionMode not in Redstone_resolutions:
                error_message = f"Error in get_resolution(): Invalid resolution mode: {self.resolutionMode}."
                logger.error(error_message)
                raise Exception(error_message)
            return Redstone_resolutions[self.resolutionMode]
        else:
            error_message = "Error in get_resolution(): Unknown instrument model."
            logger.error(error_message)
            raise Exception(error_message)

    def get_sensitivity(self) -> str:
        """Returns the instrument sensitivity."""
        if self.is_OSA200():
            if self.sensitivityMode not in OSA200_sensitivities:
                error_message = f"Error in get_sensitivity(): Invalid sensitivity mode: {self.sensitivityMode}."
                logger.error(error_message)
                raise Exception(error_message)
            return OSA200_sensitivities[self.sensitivityMode]
        elif self.is_Redstone():
            if self.sensitivityMode not in Redstone_sensitivities:
                error_message = f"Error in get_sensitivity(): Invalid sensitivity mode: {self.sensitivityMode}."
                logger.error(error_message)
                raise Exception(error_message)
            return Redstone_sensitivities[self.sensitivityMode]
        else:
            error_message = "Error in get_sensitivity(): Unknown instrument model."
            logger.error(error_message)
            raise Exception(error_message)

    def get_datetime(self) -> datetime.datetime:
        """
        Returns a datetime object of when the data was acquired.

        Example:

        .. code-block:: python

            # Convert datetime object to a string
            datestr = spectrum.get_datetime().strftime("%Y-%m-%d %H:%M:%S")
        """
        hour = self.gmtTime // 1000000
        minute = (self.gmtTime % 1000000) // 10000
        second = (self.gmtTime % 10000) // 100
        millisecond = (self.gmtTime % 100) * 10

        year = self.date // 10000
        month = (self.date % 10000) // 100
        day = self.date % 100

        datetime_obj = datetime.datetime(year, month, day, hour, minute, second,
                                         millisecond * 1000,
                                         tzinfo=datetime.timezone.utc)
        local_datetime_obj = datetime_obj.astimezone() # Convert to local timezone
        return local_datetime_obj

    def get_xlabel(self) -> str:
        """
        Returns formatted xlabel e.g., 'Optical Frequency (THz)' or 'Wavelength (nm (vac))'
        """
        return units.get_formatted_x_quantity_and_unit(self)

    def get_ylabel(self) -> str:
        """
        Returns formatted ylabel e.g., 'Absolute Power (mW)' or 'Power Density (dBm/nm)'
        """
        return units.get_formatted_y_quantity_and_unit(self)

    def convert_spectrum(self, x_unit: typing.Union[int, str], y_unit: typing.Union[int, str]) -> None:
        """Converts the spectrum to specified x- and y-units.
        
        Parameters:
            x_unit (int | str):
                The target x-axis unit. Possible units are listed in the manual.
            y_unit (int | str):
                The target y-axis unit.
        
        Examples:
        
        .. code-block:: python
        
            spectrum.convert_spectrum(x_unit="nm (vac)", y_unit="dBm (norm)")

            spectrum.convert_spectrum(x_unit="Thz", y_unit="mW")
        """
        if not self.is_spectrum():
            error_message = "Invalid input: convert_spectrum() can only convert a spectrum"
            logger.error(error_message)
            raise ValueError(error_message)
        
        # Get the integer values for x_unit and y_unit
        x_unit_idx = units.find_x_unit_index(x_unit)
        y_unit_idx = units.find_y_unit_index(y_unit)
        
        FTSLib.FTS_ConvertSpectrumTo.argtypes = c.POINTER(spectrum_t), c.c_ushort, c.c_ushort
        status = FTSLib.FTS_ConvertSpectrumTo(c.byref(self), x_unit_idx, y_unit_idx)
        
        if status != 0:
            error_message = f"Error in FTS_ConvertSpectrumTo (called from convert_spectrum()), Status: {constants.err_msg(status)}"
            logger.error(error_message)
            raise Exception(error_message)
        
        logger.info(f"Converting spectrum to x-unit {constants.x_units[x_unit_idx]} and y-unit {constants.y_units[y_unit_idx]} {constants.err_msg(status)}") 
        
    def is_autogain_satisfied(self) -> bool:
        """Returns True if the measured data was collected with the best possible gain setting.

        This is useful to get rid of measurements collected during the autogain process
        which typically occurs if the light level changed since the last measurement.
        Note that this function currently only works for the OSA200-series.
        (FTSLib does not yet handle autogainStatus for the Redstone series.)
        """
        if not self.is_OSA200():
            error_message = "Error in is_autogain_satisfied(): Currently only works for the OSA200-series. (FTSLib does not yet handle autogainStatus for the Redstone series.)"
            logger.error(error_message)
            raise Exception(error_message)

        ag_state = self.autogainStatus
        return (ag_state == AUTOGAIN_STATUS_SATISFIED or
                ag_state == AUTOGAIN_STATUS_WANTS_TO_DECREASE_BUT_NO_SUITABLE_GAIN_WAS_FOUND or
                ag_state == AUTOGAIN_STATUS_WANTS_TO_INCREASE_BUT_NO_SUITABLE_GAIN_WAS_FOUND)


    def get_gain_level(self) -> float:
        """Returns the instrument detector gain.

        Typical values: 1.0, 2.154, ... """
        return float(self.gainLevel[0])


    def get_gain_index(self) -> int:
        """Returns the instrument detector gain index.

        Typical values: 0, 1, 2, ...
        """
        return self.gainIndex


    def get_x(self) -> typing.List[float]:
        """Returns the x values from the measurement"""
        # The x values can be stored in two different ways
        if self.xValueFormat == data_defines["X_VAL_ARRAY"]:
            # Non-equidistant values -> values stored in an array
            # The values must be sliced this way, otherwise the output is empty
            return self.x[0:self.length]
        elif self.xValueFormat == data_defines["X_VAL_MINMAX"]:
            # Equidistant values -> No array is stored -> calculate from min, max, and length
            return np.linspace(self.x_min, self.x_max, self.length)
        else:
            error_message = "Error in get_x(): Unknown xValueFormat."
            logger.error(error_message)
            raise Exception(error_message)

    def get_y(self) -> typing.List[float]:
        """Returns the intensity values from the measurement"""
        # The values must be sliced this way, otherwise the output is empty
        return self.I[0:self.length]

    def set_name(self, new_name: str) -> None:
        """Set the name of this spectrum_t."""
        # Check if the new name is too long
        if len(new_name) < SPECTRUM_NAME_LENGTH:
            # Encode the new name as bytes and set it in the struct
            self.name = new_name.encode("utf-8").ljust(SPECTRUM_NAME_LENGTH, b"\x00")
        else:
            error_message = f"Name is too long. Maximum length is {SPECTRUM_NAME_LENGTH} characters."
            logger.error(error_message)
            raise ValueError(error_message)

    def set_comment(self, new_comment: str) -> None:
        """Set the comment of this spectrum_t."""
        # Check if the new comment is too long
        if len(new_comment) < SPECTRUM_COMMENT_LENGTH:
            # Encode the new comment as bytes and set it in the struct
            self.comment = new_comment.encode("utf-8").ljust(SPECTRUM_COMMENT_LENGTH, b"\x00")
        else:
            error_message = f"Comment is too long. Maximum length is {SPECTRUM_COMMENT_LENGTH} characters."
            logger.error(error_message)
            raise ValueError(error_message)

    def set_operator(self, new_operator: str) -> None:
        """Set the operator of this spectrum_t."""
        # Check if the new operator is too long
        if len(new_operator) < SPECTRUM_OPERATOR_STRLENGTH:
            # Encode the new operator as bytes and set it in the struct
            self.instr_operator = new_operator.encode("utf-8").ljust(SPECTRUM_OPERATOR_STRLENGTH, b"\x00")
        else:
            error_message = f"Operator is too long. Maximum length is {SPECTRUM_OPERATOR_STRLENGTH} characters."
            logger.error(error_message)
            raise ValueError(error_message)

    def _is_interferogram_measured_with_best_gain_according_to_autogain(self) -> bool:
        """Returns True if the interferogram was measured with best gain according to autogain
        """
        if self.is_OSA200():
            if self.autogainStatus == 0: # 0 = constants.data_defines('AUTOGAIN_STATUS_NOT_IN_USE')
                return True
            return self.is_autogain_satisfied()
        elif self.is_Redstone():
            error_message = "_is_interferogram_measured_with_best_gain_according_to_autogain() is not yet available for Redstone."
            logger.error(error_message)
            raise ValueError(error_message)
        else:
            error_message = "_is_interferogram_measured_with_best_gain_according_to_autogain(): unknown instrument model."
            logger.error(error_message)
            raise ValueError(error_message)

    def check_validity(self) -> typing.Dict[str, bool]:
        """ Returns a dictionary containing the "validity statuses" for the measured data.

        The measured data can be an interferogram, a spectrum, or a stitched spectrum
        The following parameters are checked:
          1. The reference laser was locked during the measurement
          2. The interferogram signal was not clipped (also checked for a spectrum)
          3. The interferogram was not nonlinear (tested only for OSA205, OSA207, and Redstone305)
          4. Only for OSA200: The optimal gain was used during the measurement (only tested if autogain is enabled)

        Returns:
            dict[str, bool]: A dictionary containing the validity statuses. The following keys are possible:
                - 'ref_laser_locked': True if the reference laser was locked, False otherwise.
                - 'interferogram_within_detector_range': True if the interferogram signal was not clipped, False otherwise.
                - 'interferogram_is_linear': True if the interferogram was linear, False otherwise.
                - 'autogain_satisfied': True if autogain was satisfied, False otherwise. This key is only available for OSA20X.
        """
        ref_laser_is_locked = bool(self.refLaserLocked)

        if self._is_virtual():
            interferogram_is_clipped = False
        else:
            interferogram_is_clipped = self._is_interferogram_clipped()

        interferogram_is_nonlinear = self._is_interferogram_nonlinear()

        validity_data = {
            'ref_laser_locked': ref_laser_is_locked,
            'interferogram_within_detector_range': not interferogram_is_clipped,
            'interferogram_is_linear': not interferogram_is_nonlinear
            }

        # TODO the following needs to be updated as soon as _is_interferogram_measured_with_best_gain_according_to_autogain()
        #      works also for Redstone
        if self.is_OSA200():
            autogain_is_satisfied = self._is_interferogram_measured_with_best_gain_according_to_autogain()
            validity_data['autogain_satisfied'] = autogain_is_satisfied

        return validity_data


    def is_valid(self) -> bool:
        """ Returns True if no problems were detected with the measured data.

        The following parameters are checked:
          1. The reference laser was locked during the measurement
          2. The interferogram signal was not clipped (also checked for a spectrum)
          3. The interferogram was not nonlinear (tested for OSA205, OSA207, and Redstone305)
          4. Only for OSA200: The optimal gain was used during the measurement (only tested if autogain is enabled)
        """
        validity = self.check_validity()
        if not validity.get('ref_laser_locked', True):
            logger.warning("Data quality warning, reference laser not warmed up. Wavelength accuracy not guaranteed.")
        if not validity.get('interferogram_within_detector_range', True):
            logger.warning("Data quality warning, the interferogram is clipped.") 
        if not validity.get('interferogram_is_linear', True):
            logger.warning("Data quality warning, the interferogram is not linear")
        if not validity.get('autogain_satisfied', True):
            logger.warning("Data quality warning, the autogain was not finished adjusting the gain.")

        for key in validity:
            if not validity[key]:
                return False
        return True

    
    