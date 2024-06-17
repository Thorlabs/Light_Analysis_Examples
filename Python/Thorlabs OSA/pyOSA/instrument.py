import re
import time
import queue
import typing
import logging
import ctypes as c
from collections import defaultdict

import numpy as np

from pyOSA.spectrum_t import spectrum_t
from pyOSA.constants import constants
from pyOSA.FTSLib import FTSLib
from pyOSA.units import units

logger = logging.getLogger("pyOSA")

class InstrumentSeriesException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return f"InstrumentSeriesException: {self.message}"


class AcquisitionException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return f"AcquisitionException: {self.message}"

class TupleDict(dict):
    """
    This is a dictionary which has tuples as keys and
    the second value in the tuple can have a default value.
    In pyOSA, this is used to make a convenient data structure
    for using OSAs with a single or multiple number of detectors.
    
    If a single key is provided, it defaults to the value set as defaultkey.
    data["spectrum"] returns 1,2,3,4
    data["spectrum", "Stitched"] returns the same thing
    """
    def __init__(self, defaultkey=None, *args, **kwargs):
        self._defaultkey = defaultkey
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return super().__getitem__(key)
        else:
            if self._defaultkey is None:
                raise KeyError("No default detector set")
            return super().__getitem__((key, self._defaultkey))

class Instrument:
    """This class serves as a representation of an Optical Spectrum Analyzer (OSA)
    instrument. It provides users with the capability to configure instrument settings
    and retrieve data.
    """

    def __init__(self, spectrometer_index: int, virtual:bool=False):
        self.spectrometer_index: int = spectrometer_index
        self.model: str = self.get_model()
        self.serial_number: str = self.get_serial_number()
        self.inst_series: int = FTSLib.FTS_GetInstrumentProperty_Series(self.spectrometer_index)

        self._is_virtual = virtual

        # Lets keep track of setvalues for different settings
        self._setvalue_sensitivity: str = None
        self._setvalue_resolution: str = None
        self._setvalue_apodization: str = None
        self._setvalue_zerofill: int = None
        self._setvalue_autogain: bool = None
        ## Setvalues per detector
        self._setvalue_spectrum_averaging: typing.Dict[str,int] = defaultdict(lambda: None)
        self._setvalue_gain_level: typing.Dict[str,int] = defaultdict(lambda: None)
        self._setvalue_detector_offset: typing.Dict[str,int] = defaultdict(lambda: None)
        self._setvalue_attenuation_filter: typing.Dict[str,int] = defaultdict(lambda: None)

        if not self.is_OSA200() and not self.is_Redstone():
            logger.info(self.model)
            logger.info(self.inst_series)
            raise InstrumentSeriesException(
                "Cannot create OSA instrument object with unknown instrument series"
            )

        self.detector_properties = self._get_detector_properties()
        self.channels_dict = {
            self.detector_properties[key]["channel index"]: key
            for key in self.detector_properties.keys()
        }

        settings_callback_format = c.WINFUNCTYPE(c.c_void_p, c.c_ushort, c.c_uint, c.c_uint)
        autosetup_callback_format = c.WINFUNCTYPE(
            c.c_void_p, c.c_ushort, c.c_ushort, c.c_uint, c.c_ushort, c.c_uint, c.c_wchar_p
        )
        callback_settings = settings_callback_format(self.__settings_callback)
        callback_autosetup = autosetup_callback_format(self.__autosetup_callback)
        self.callbacks = {
            "settings": callback_settings,
            "autosetup": callback_autosetup,
        }

        self._setup_spectra()

        acquisition_callback_format = c.WINFUNCTYPE(
            c.c_void_p, c.c_ushort, c.c_ushort, c.c_uint, c.c_uint, c.c_ushort
        )
        self._acquisition_callback = acquisition_callback_format(self.__acquisition_callback)

        self._interferogram_queue = queue.Queue()
        self._spectrum_queue = queue.Queue()
        self._continuous_acq_running = False # Flag for clean shutdown

        if self.is_OSA200():
            self._spectrum_detectors = ("Detector 1",)
            self._interferogram_detectors = ("Detector 1",)
            self._default_detector = "Detector 1"
        elif self.is_Redstone():
            self._spectrum_detectors = ("Detector 1", "Detector 2", "Stitched",)
            self._interferogram_detectors = ("Detector 1", "Detector 2")
            self._default_detector = "Stitched"
        else:
            raise InstrumentSeriesException(
                "Cannot set detectors for unknown instrument series"
            )

        logger.debug("--------------------------------")
        logger.debug(f"Opened spectrometer number {self.spectrometer_index}")
        logger.debug(f"Model: {self.model}")
        logger.debug(f"Serial nr: {self.serial_number}")
        logger.debug("Detector information:")
        for detector, properties in self.detector_properties.items():
            logger.debug(f"   Detector name: {detector}")
            logger.debug(f"      Properties: {properties}")
        logger.debug("--------------------------------")

    def __del__(self):
        """
        Called by python when object is destroyed,
        
        Clean up acquisition queues in python,
        data in FTSLib and close connection to spectrometer
        """
        logger.debug("In Instrument destructor")
        if self._continuous_acq_running:
            logger.debug("Stopping continous acq")
            self.__stop_continuous_acq()
        try:
            self._clear_data()
        except Exception as e:
            logging.error(f"Error clearing data {e}")
        try:
            c_spectrometer_index = c.c_ushort(self.spectrometer_index)
            logger.debug(f"Closing instrument {self.spectrometer_index}")
            status = FTSLib.FTS_CloseSpectrometer(c_spectrometer_index)
            if status != 0:
                raise RuntimeError(
                    "FTS_CloseSpectrometer. Status: " f"{constants.err_msg(status)}"
                )
        except Exception as e:
            logging.error(f"Error closing instrument {e}")

    @staticmethod
    def _check_spectrometer(spectrometer_index:int, ignore_errors: typing.List[str] = []):
        status = FTSLib.FTS_CheckSpectrometer(spectrometer_index)
        logger.info(
            f"Checked spectrometer {spectrometer_index} " + constants.err_msg(status)
        )
        if status != 0 and status != 266:
            raise AcquisitionException(constants.err_msg(status))
        if status == 266:
            # Error: Instrument Status, could be e.g. cold reference
            instrumentstatus = Instrument._get_instrument_status(spectrometer_index)
            msg = f"Instrument error: {instrumentstatus}"
            logger.error(msg)
            if sorted(instrumentstatus) == sorted(ignore_errors):
                logger.error(f"Ignoring errors: {instrumentstatus}")
            else:
                raise AcquisitionException(msg)

    @staticmethod
    def _get_instrument_status(spectrometer_index:int) -> typing.List[str]:
        """
        Return a string with the instrument status message, i.e. "Reference Warming up"
        """
        statuscode: int = FTSLib.FTS_GetInstrumentProperty_InstrumentStatus(spectrometer_index)
        inst_series: int = FTSLib.FTS_GetInstrumentProperty_Series(spectrometer_index)
        
        if constants._is_OSA200(inst_series):
            statusdict = constants.OSA200_status
        elif constants._is_Redstone(inst_series):
            statusdict = constants.Redstone_status
        else:
            raise AcquisitionException("Unknown instrument series")
        
        # Accumulate error messages in a list
        error_messages = []
        for code, message in statusdict.items():
            if statuscode & code:
                error_messages.append(message)
        if len(error_messages) == 0 and statuscode != 0:
            raise AcquisitionException(f"Unknown instrument status {statuscode}")
        return error_messages

    def __autosetup_callback(
        self,
        spectrometer_index: int,
        channel_index: int,
        _,
        type_of_status: int,
        status_code: int,
        message: bytes,
    ):
        """The callback function takes six parameters:
        spectrometer_index: the index of the spectrometer
        channel_index: the index of the channel, but not used
        unused: unused
        type_of_status: e.g. FTS_ERROR_FLAG
        status_code: e.g. FTS_SUCCESS, see FTSErrorCodes.h
        message: a message for the user
        """
        logger.debug(
            f"Autosetup callback! spectrometer_index: {spectrometer_index}, "
            f"channel_index: {channel_index}, "
            f"type_of_status: {constants.error_codes[type_of_status]}, "
            f"status_code: {constants.error_codes[status_code]}, "
            f"message: {c.string_at(message).decode('utf-8')}"
        )

        self.autosetup_status = constants.error_codes[status_code]
        return 0

    def __settings_callback(
        self,
        spectrometer_index: int, 
        channel_index: int, 
        _, 
        status_code: int, 
        type_of_status: int
    ) -> int:
        """The callback function takes five parameters:
        spectrometer_index (int): the index of the spectrometer
        channel_index (int): the index of the channel, but not used
        unused: unused
        status_code (int): e.g. FTS_SUCCESS, see FTSErrorCodes.h
        type_of_status (int): e.g. FTS_ERROR_FLAG
        """
        logger.debug(
            f"Settings callback!\n spectrometer_index: {spectrometer_index}, channel_index: {channel_index},"
            f"unused, status_code: {status_code}, type_of_status: {type_of_status}"
        )
        self.setup_status = status_code
        return 0

    def is_OSA200(self) -> bool:
        """Returns true if the instrument belongs to the OSA200 series"""
        return constants._is_OSA200(self.inst_series)

    def is_Redstone(self) -> bool:
        """Returns true if the instrument belongs to the Redstone series"""
        return constants._is_Redstone(self.inst_series)

    def get_model(self) -> str:
        """Returns the model of the instrument"""
        model_number = FTSLib.FTS_GetInstrumentProperty_Model(self.spectrometer_index)
        model = constants.instrument_models[model_number]
        return model

    def get_serial_number(self) -> str:
        """Returns the serial number of the instrument"""
        SERIALNUMBER_LENGTH = 32
        serial_byte_str = c.create_string_buffer(SERIALNUMBER_LENGTH)
        FTSLib.FTS_GetInstrumentProperty_Serial(self.spectrometer_index, serial_byte_str)
        serial_number = serial_byte_str.value.decode("utf-8")
        return serial_number

    def _get_detector_names(self) -> typing.List[str]:
        """Returns a list of the detector names"""
        return list(self.detector_properties.keys())

    def _get_detector_name(self, detector: str) -> str:
        """Returns the detector name from key"""
        detector_names = self._get_detector_names()
        return detector_names[detector]
    
    def _get_detector_from_channel(self, channel_index: int) -> str:
        """Returns the detector name from key"""
        for det in self.detector_properties:
            if self.detector_properties[det]["channel index"] == channel_index:
                return det
        raise AcquisitionException(f"No such detector found: idx {channel_index}")
    
    # To ensure that this function works accurately,
    # make sure you are using FTSLib version 3.31 or a later release.
    def get_formatted_model_range(self, desired_unit: typing.Union[int, str]) -> str:
        """Returns a formatted string of the range of the model

        The format is on
                         x_min-x_max x_unit, e.g., '1000-2500 nm'
        desired_unit can be given either in the indices or the corresponding names found
        in OSA_constants.x_units. Only the spectral units are allowed.
        """
        FTSLib.FTS_GetInstrumentProperty_MinWavenumber.restype = c.c_float
        FTSLib.FTS_GetInstrumentProperty_MaxWavenumber.restype = c.c_float
        maxWnr = FTSLib.FTS_GetInstrumentProperty_MaxWavenumber(self.spectrometer_index)
        minWnr = FTSLib.FTS_GetInstrumentProperty_MinWavenumber(self.spectrometer_index)
        lower_limit_nm = 1e7 / maxWnr
        upper_limit_nm = 1e7 / minWnr
        return units._format_wavelength_range(
            lower_limit_nm, upper_limit_nm, desired_unit
        )

    def get_formatted_detector_range(
        self, detector_name: str, desired_unit: typing.Union[int, str]
    ) -> str:
        """Returns a string containing the range of the detector:

        The format is:
        x_min-x_max x_unit, e.g., '1000-2500 nm'
        desired_unit can be given either in the indices or the corresponding names
        found in OSA_constants.x_units. Only the spectral units are allowed.
        """
        lower_limit_nm = self.detector_properties[detector_name]["lower limit (nm)"]
        upper_limit_nm = self.detector_properties[detector_name]["upper limit (nm)"]
        return units._format_wavelength_range(
            lower_limit_nm, upper_limit_nm, desired_unit
        )

    def set_resolution(self, resolution: str):
        """Sets the resolution setting
        """
        input_resolution = re.sub(r"[^a-zA-Z0-9]+", "_", resolution)
        input_resolution = input_resolution.upper()
        if self.is_OSA200():
            desired_resolution_int = c.c_ushort(
                constants.data_defines["OSA200_RESOLUTION_" + input_resolution]
            )
        elif self.is_Redstone():
            actual_sens = FTSLib.FTS_GetAcquisitionOption_SensitivityMode(self.spectrometer_index)
            desired_resolution_int = c.c_ushort(
                constants.data_defines["REDSTONE_RESOLUTION_" + input_resolution]
            )
            if input_resolution == "HIGH" and actual_sens == 12:
                self.set_sensitivity("HIGH")
        else:
            raise InstrumentSeriesException("Cannot set resolution for unknown instrument")

        status = FTSLib.FTS_SetResolutionMode(self.spectrometer_index, desired_resolution_int)
        if status != 0:
            raise AcquisitionException(f"Couldn't set resolution: {constants.err_msg(status)}")
        logger.info(
            f"Setting resolution to {resolution.capitalize()}"
            + constants.err_msg(status)
        )
        self._setvalue_resolution = resolution

    def set_sensitivity(self, sensitivity: str):
        """Sets the sensitivity setting
        """
        input_sensitivity = re.sub(r"[^a-zA-Z0-9]+", "_", sensitivity)
        input_sensitivity = input_sensitivity.upper()
        if self.is_OSA200():
            sensstr = "OSA200_SENSITIVITY_" + input_sensitivity
            desired_sensitivity_int = c.c_ushort(constants.data_defines[sensstr])
        elif self.is_Redstone():
            actual_res = FTSLib.FTS_GetAcquisitionOption_ResolutionMode(self.spectrometer_index)
            if sensitivity == "HIGH" and actual_res == 3:
                sensstr = "REDSTONE_SENSITIVITY_" + input_sensitivity + "_SECONDARY"
                desired_sensitivity_int = c.c_ushort(constants.data_defines[sensstr])
            else:
                sensstr = "REDSTONE_SENSITIVITY_" + input_sensitivity
                desired_sensitivity_int = c.c_ushort(constants.data_defines[sensstr])
        else:
            raise InstrumentSeriesException("Cannot set sensitivity for unkown instrument")

        status = FTSLib.FTS_SetSensitivityMode(self.spectrometer_index, desired_sensitivity_int)
        if status != 0:
            raise AcquisitionException(
                "Couldn't set sensitivity mode " f"{constants.err_msg(status)}"
            )
        logger.info(
            f"Setting sensitivity to {sensitivity.capitalize()}"
            + constants.err_msg(status)
        )
        self._setvalue_sensitivity = sensitivity

    def set_apodization(self, apodization: str) -> None:
        """Sets the apodization setting
        """
        input_apodization = re.sub(r"[^a-zA-Z0-9]+", "_", apodization)
        input_apodization = input_apodization.upper()
        key_to_check = "APODIZATION_" + input_apodization
        if key_to_check in constants.data_defines:
            desired_apodization_int = constants.data_defines[key_to_check]
        else:
            raise KeyError("Error in set_apodization:  Unknown apodization")
        status = FTSLib.FTS_SetAcquisitionOption_ApodizationType(
            self.spectrometer_index, desired_apodization_int
        )
        if status != 0:
            raise AcquisitionException(
                "Couldn't set apodization type. "
               f"Status: {constants.err_msg(status)}"
            )
        logger.info(
            f"Setting apodization to {apodization.capitalize()}"
            + constants.err_msg(status)
        )
        self._setvalue_apodization = apodization

    def set_zerofill(self, zerofill: int):
        """Sets the zerofill setting
        """
        status = FTSLib.FTS_SetAcquisitionOption_ZeroFillFactor(self.spectrometer_index, zerofill)
        if status != 0:
            raise AcquisitionException(
               f"Couldn't set zero fill factor to {zerofill}. Status: {constants.err_msg(status)}"
            )
        logger.info(f"Setting zero fill to {zerofill}" + constants.err_msg(status))
        self._setvalue_zerofill = zerofill

    def set_autogain(self, autogain: bool = True):
        """Sets whether autogain should be used or not.

        Parameters:
            autogain (bool, optional):
                If True, autogain is enabled; if False, autogain is disabled.
                Defaults to True.
        """
        if self.is_OSA200():
            status = FTSLib.FTS_SetAcquisitionOption_AutoGain(
                self.spectrometer_index, autogain
            )
            if status != 0:
                raise AcquisitionException(f"Couldn't set autogain to {autogain}. "
                                           "Status: {constants.err_msg(status)}")
        if self.is_Redstone():
            detectors = ("Detector 1", "Detector 2")
            for detector in detectors:
                channel = self.detector_properties[detector]["channel index"]
                status = FTSLib.FTS_SetAcquisitionOption_AutoGain_ext(
                    self.spectrometer_index, channel, autogain)
        logger.info(f"Setting autogain to {autogain}")
        self._setvalue_autogain = autogain

    def _set_spectrum_averaging(
        self,
        nr_of_averages: int
    ):
        """Sets the number of averaged spectra to collect
        """
        if self.is_OSA200():
            detectors = ("Detector 1",)
        elif self.is_Redstone():
            detectors = ("Stitched", "Detector 1", "Detector 2")
        else:
            raise InstrumentSeriesException("_set_spectrum_averaging() can only be used for an OSA200 or a Redstone")

        for detector in detectors:
            channel = self.detector_properties[detector]["channel index"]
            status = FTSLib.FTS_SetAcquisitionOption_AverageSpectrum_ext(
                self.spectrometer_index, channel, nr_of_averages
            )
            if status != 0:
                raise AcquisitionException("Couldn't set number of averages. Status: "
                                f"{constants.err_msg(status)}")

        logger.info(f"Setting number of averages to {nr_of_averages}" + constants.err_msg(status))
        self._setvalue_nr_of_averages = nr_of_averages

    def set_gain_level(
        self,
        gain_level: int,
        detectors: typing.Tuple[str] = None,
    ):
        """Sets the used gain level

        For an OSA200, detector can be omitted since the OSA200 only has one detector
        For a Redstone, this function needs to be called for each detector/channel or
        with multiple detectors specified as argument
        """
        if detectors is None:
            if self.is_OSA200():
                detectors = ("Detector 1",)
            elif self.is_Redstone():
                detectors = ("Detector 1", "Detector 2")
            else:
                raise InstrumentSeriesException(
                    "Cannot set detectors for unknown instrument series"
                )
        self.set_autogain(False)
        for detector in detectors:
            channel = self.detector_properties[detector]["channel index"]
            status = FTSLib.FTS_SetAcquisitionOption_SingleGain_ext(
                self.spectrometer_index, channel, gain_level
            )
            if status != 0:
                raise AcquisitionException(
                    f"Couldn't set gain level. Status: {constants.err_msg(status)}"
                )
            logger.info(
                f"Setting gain level {gain_level} for detector {channel}: "
                f"{constants.err_msg(status)}"
            )
            self._setvalue_gain_level[detector] = gain_level


    def set_detector_offsets(
        self,
        detector_offsets: typing.List[int],
        detectors: typing.Tuple[str] = None,
    ) -> None:
        """Set the detector offset for Redstone detectors

        Example:

        .. code-block:: python

            osa.set_detector_offsets([1472,1472], ["Detector 1", "Detector 2"])
        
        """
        if not self.is_Redstone():
            raise InstrumentSeriesException("Detector offsets only available for Redstone instruments")
        if detectors is None:
            raise ValueError("Please select detector")

        for detector, detector_offset in zip(detectors, detector_offsets):
            channel = self.detector_properties[detector]["channel index"]
            status = FTSLib.FTS_SetAcquisitionOption_SignalOffset(
                self.spectrometer_index, channel, detector_offset)
            if status != 0:
                raise AcquisitionException("Couldn't set detector offset. Status: "
                                          f"{constants.err_msg(status)}")
            logger.info(f"Setting set_detector_offset {detector_offset} for detector "
                        f"{detector}: {constants.err_msg(status)}")
            self._setvalue_detector_offset[detector] = detector_offset

    def set_attenuation_filter(self, detector: str, active: bool=False, automatic: bool=False) -> None:
        """Set the attenuation filter state for a specified detector channel.

        Parameters:
            detector (str):
                The name of the detector for which to set the attenuation filter.

            active (bool):
                True to activate the attenuation filter, False to deactivate.

            automatic (bool):
                True to set the attenuation filter to automatic mode,
                False for manual mode.
        """
        if not self.is_Redstone():
            raise InstrumentSeriesException(
                f"Cannot set attenuation filter for the instrument type {self.inst_series}"
            )
        attenuationFilterStatus = 0
        if active:
            attenuationFilterStatus |= (1 << 1)
        if automatic:
            attenuationFilterStatus |= (1 << 2)
        channel = self.detector_properties[detector]["channel index"]
        logger.info(f"Trying to set attenuation filter to: {bin(attenuationFilterStatus)}")
        FTSLib.FTS_SetAttenuationFilterOnAndOff.argtypes = (c.c_int, c.c_int, c.c_int)
        status = FTSLib.FTS_SetAttenuationFilterOnAndOff(self.spectrometer_index, channel, attenuationFilterStatus)
        if status != 0:
            raise AcquisitionException(f"Couldn't set attenuation filter. Status: {status}")
        logger.info(f"Setting attenuation filter, Status: {constants.err_msg(status)}")
        self._setvalue_attenuation_filter[detector] = attenuationFilterStatus


    def get_attenuation_filter(self, detector: str) -> typing.Tuple[bool, bool, bool, int]:
        """Retrieve information about the attenuation filter for a given detector channel.

        Parameters:
            detector (str):
                The name of the detector for which to retrieve attenuation filter information.

        Returns:
            tuple[bool, bool, bool, str]:
                A tuple containing the following information:
                
                - available (bool):
                    True if the attenuation filter is available for the specified detector channel.
                
                - active (bool):
                    True if the attenuation filter is currently active for the specified detector channel.
                
                - automatic (bool):
                    True if the attenuation filter is set to automatic mode for the specified detector channel.
                
                - bits (int):
                    A binary representation of the attenuation filter status for additional details.
        """
        if not self.is_Redstone():
            raise InstrumentSeriesException("Attenuation filter is not available in your spectrometer")
        # MUSTFIX: Functions do not return correct values - Automatic is always False,
        # and when both Active and Automatic should be True
        # they are False and the returned bits are 101 not 111. Trace Log is correct
        logger.error("TODO Mustfix in get_attenuation_filter")
        channel = self.detector_properties[detector]["channel index"]
        FTSLib.FTS_GetDetectorProperty_AttenuationFilterAvailable.restype = c.c_bool
        FTSLib.FTS_GetDetectorProperty_AttenuationFilterActive.restype = c.c_bool
        FTSLib.FTS_GetDetectorProperty_AttenuationFilterAutomatic.restype = c.c_bool
        available = FTSLib.FTS_GetDetectorProperty_AttenuationFilterAvailable(
            self.spectrometer_index, channel
        )
        active = FTSLib.FTS_GetDetectorProperty_AttenuationFilterActive(
            self.spectrometer_index, channel
        )
        automatic = FTSLib.FTS_GetDetectorProperty_AttenuationFilterAutomatic(
            self.spectrometer_index, channel
        )
        bits = FTSLib.FTS_GetAttenuationFilterStatus(self.spectrometer_index, channel)
        return available, active, automatic, bits

    def get_autogain(self) -> int:
        """Retrieve the current autogain setting for the spectrometer.

        Returns:
            int:
                The current autogain setting used by the spectrometer.
        """
        if self._is_virtual:
            return self._setvalue_autogain
        if self.is_OSA200():
            actual_autogain = FTSLib.FTS_GetAcquisitionOption_AutoGain(self.spectrometer_index)
        if self.is_Redstone():
            autogains = []
            for det in self._interferogram_detectors:
                channel = self.detector_properties[det]["channel index"]
                autogain = FTSLib.FTS_GetAcquisitionOption_AutoGain_ext(self.spectrometer_index, channel)
                autogains.append(autogain)
            actual_autogain = autogains[0]
            if not all([actual_autogain == a for a in autogains]):
                actual_autogain = -1
                # This is a hack, but it means that await_setvalues will wait rather than to have
                # an exception here
        return actual_autogain

    def _get_resolution_int(self) -> int:
        """Returns the used resolution setting as an int"""
        return FTSLib.FTS_GetAcquisitionOption_ResolutionMode(self.spectrometer_index)

    def get_resolution(self) -> str:
        """Returns the used resolution setting"""
        actual_res = self._get_resolution_int()
        if self.is_OSA200():
            return constants.OSA200_resolutions[actual_res]

        elif self.is_Redstone():
            return constants.Redstone_resolutions[actual_res]

        else:
            raise InstrumentSeriesException("Cannot get resolution for unknown instrument")

    def _get_sensitivity_int(self) -> int:
        """Returns the used sensitivity setting as int"""
        return FTSLib.FTS_GetAcquisitionOption_SensitivityMode(self.spectrometer_index)

    def get_sensitivity(self) -> str:
        """Returns the used sensitivity setting"""
        actual_sens = self._get_sensitivity_int()
        if self._is_virtual:
            if self.is_OSA200():
                if actual_sens not in constants.OSA200_sensitivities:
                    self.set_sensitivity("Low")
                    return "Low"
            elif self.is_Redstone():
                if actual_sens not in constants.Redstone_sensitivities:
                    self.set_sensitivity("Low")
                    return "Low"
            else:
                raise InstrumentSeriesException("Unknown virtual")

        if self.is_OSA200():
            return constants.OSA200_sensitivities[actual_sens]
        elif self.is_Redstone():
            return constants.Redstone_sensitivities[actual_sens]
        else:
            raise InstrumentSeriesException("Cannot get sensitivity for unknown instrument")

    def get_zerofill(self) -> int:
        """Returns the used zerofill setting"""
        actual_zerofill = FTSLib.FTS_GetAcquisitionOption_ZeroFillFactor(self.spectrometer_index)
        return actual_zerofill

    def get_apodization(self) -> str:
        """Returns the used apodization setting"""
        actual_apod = FTSLib.FTS_GetAcquisitionOption_ApodizationType(self.spectrometer_index)
        return constants.apodizations[actual_apod]

    def _get_spectrum_averaging(self) -> typing.List[int]:
        """Returns the number of acquisitions used to average spectra setting"""
        actual_nr_of_avgs = []
        for ch in self.channels_dict.keys():
            avgs = FTSLib.FTS_GetAcquisitionOption_AverageSpectrum_ext(self.spectrometer_index, ch)
            actual_nr_of_avgs.append(avgs)
        return actual_nr_of_avgs

    def get_gain_level(self, detectors: typing.Tuple[str] = None) -> typing.List[int]:
        """Returns the used gain level setting for the supplied detectors
        For Redstone, this depends on which channel/detector is used
        """
        gain_levels = []
        if detectors is None:
            if self.is_OSA200():
                detectors = ("Detector 1",)
            elif self.is_Redstone():
                raise Exception("Please specify detectors")
            else:
                raise InstrumentSeriesException(
                    "Cannot set detectors for unknown instrument series"
                )
        for detector in detectors:
            channel = self.detector_properties[detector]["channel index"]
            actual_gain_level = FTSLib.FTS_GetAcquisitionOption_SingleGainLevel_ext(
                self.spectrometer_index, channel
            )
            gain_levels.append(actual_gain_level)
        return gain_levels

    def get_available_gain_levels(
        self, detectors: typing.Tuple[str] = None
    ) -> typing.List[typing.List[float]]:
        """Returns the available gain levels (depends on instrument and sensitivity setting)

        For Redstone, this depends also on which channel/detector is used
        It will return a list of gain_levels, with one list for each supplied detector

        Args:
            detectors (Tuple[str], optional): Detector names. Defaults based on instrument.

        Returns:
            List[List[float]]: Gain levels for each specified detector.
        """
        # TODO MUSTFIX_PYTHON Make sure this works!
        # It returns something at least
        gain_levels = []
        if detectors is None:
            if self.is_OSA200():
                detectors = ("Detector 1",)
            elif self.is_Redstone():
                detectors = ("Detector 1", "Detector 2")
            else:
                raise InstrumentSeriesException

        for detector in detectors:
            channel = self.detector_properties[detector]["channel index"]
            max_nr_of_gain_levels = 100  # This is far more than enough
            available_gain_levels = (c.c_double * max_nr_of_gain_levels)()
            nr_of_available_gain_levels: int = (
                FTSLib.FTS_GetInstrumentProperty_AvailableGainLevels_ext(
                    self.spectrometer_index, channel, available_gain_levels
                )
            )
            gain_levels.append(available_gain_levels[0:nr_of_available_gain_levels])
        return gain_levels

    def get_detector_offsets(self, detectors: typing.Tuple[str] = None) -> typing.List[int]:
        """Returns the detector offsets for each specified detector

        If no detector is specified then it will be returned for all
        """
        if not self.is_Redstone():
            raise Exception("Detector offsets only available in redstone")
        offsets = []
        if detectors is None:
            detectors = ("Stitched", "Detector 1", "Detector 2")
        for detector in detectors:
            channel = self.detector_properties[detector]["channel index"]
            actual_detector_offset = FTSLib.FTS_GetAcquisitionOption_DetectorOffsetSet(
                self.spectrometer_index, channel
            )
            offsets.append(actual_detector_offset)
        return offsets

    def get_available_resolutions(self) -> typing.List[str]:
        """Returns the available resolutions (depends on instrument)"""
        if self.is_OSA200():
            resolutions = units.get_available_constants("OSA200 resolutions")
            return resolutions
        elif self.is_Redstone():
            resolutions = units.get_available_constants("Redstone resolutions")
            return resolutions
        else:
            raise InstrumentSeriesException(
                "Cannot get available resolutions for unknown instrument"
            )

    def get_available_sensitivities(self) -> typing.List[str]:
        """Returns the available sensitivities (depends on instrument)"""
        if self.is_OSA200():
            sensitivities = units.get_available_constants("OSA200 sensitivities")
            return sensitivities
        elif self.is_Redstone():
            sensitivities = units.get_available_constants("Redstone sensitivities")
            return sensitivities
        else:
            raise InstrumentSeriesException(
                "Cannot get available sensitivities for unknown instrument"
            )

    def setup(
        self,
        autosetup: bool = False,
        autogain: bool = True,
        resolution: str = "low",
        sensitivity: str = "low",
    ) -> None:
        """Applies chosen settings to an instrument, or runs auto-setup.
        
        Parameters:
            autosetup (bool):
                True if auto-setup should be run, False for manual setup.
                Auto-setup ignores all manual settings.

            autogain (bool, Default: True):
                If True, activates auto-gain for all channels.

            resolution (str, Default: "low"):
                Sets the resolution to the input value.
                Valid values are 'low', 'high' for OSA20X,
                and 'low', 'medium low', 'medium high', 'high' for OSA30X.

            sensitivity (str, Default: "low"):
                Sets the sensitivity to the input value.
                Valid values are 'low', 'medium low', 'medium high', 'high' for OSA20X,
                and 'low', 'medium', 'high' for OSA30X.
       """
        if self.is_OSA200() or self.is_Redstone():
            pass
        else:
            raise InstrumentSeriesException("Cannot setup for unknown instrument series.")

        if autosetup:
            # MUSTFIX_PYTHON: Autosetup crashes for virtual Redstone. Problem in FTSLib, not Python
            self._perform_autosetup()
        else:  # Manual setup
            logger.info("Instrument configuration")
            self.set_autogain(autogain)
            self.set_resolution(resolution)
            self.set_sensitivity(sensitivity)
            self.set_zerofill(0)
            self.set_apodization("Hann")
            self._set_spectrum_averaging(1)

        logger.info(f"Autogain: {self.get_autogain()}")
        logger.info(f"Resolution: {self.get_resolution()}")
        logger.info(f"Sensitivity: {self.get_sensitivity()}")
        logger.info(f"Zero-fill factor: {self.get_zerofill()}")
        logger.info(f"Apodization type: {self.get_apodization()}")
        logger.info(f"Spectrum averaging: {self._get_spectrum_averaging()[0]}")

    def _perform_autosetup(self):
        """
        Run autosetup, helper method for setup_OSA
        """
        options_pointer = None
        fCancel = c.c_bool()

        ret = FTSLib.FTS_AutoSetup_ext(
            self.spectrometer_index, options_pointer, fCancel, self.callbacks["autosetup"]
        )
        logger.info("Performing auto Setup: " + constants.err_msg(ret))
        self.autosetup_status = "FTS Progress"
        j = 0
        while self.autosetup_status == "FTS Progress":
            if j % 10 == 0:
                logger.info("Still setting up...")
            time.sleep(0.1)
            j += 1
        logger.info(f"Autosetup finished! {self.autosetup_status}")

    def _set_default(self):
        """Sets default options"""
        FTSLib.FTS_SetAcquisitionOptions_Default_ext.argtypes = (c.c_ushort, c.c_ushort)
        for channel_index in self.channels_dict.keys():
            FTSLib.FTS_SetAcquisitionOptions_Default_ext(self.spectrometer_index, channel_index)
            logger.info(
                f"Setting acquisition options to default for detector {self.channels_dict[channel_index]}"
            )
            logger.info(f"Autogain: {self.get_autogain()}")
            logger.info(f"Resolution: {self.get_resolution()}")
            logger.info(f"Sensitivity: {self.get_sensitivity()}")
            logger.info(f"Zero-fill factor: {self.get_zerofill()}")
            logger.info(f"Apodization type: {self.get_apodization()}")

    def _get_detector_properties(self) -> dict:
        """Returns a dictionary containing properties for each detector belonging to the instrument

        Dictionary output:
            property_dict[detector_name] = {channel_index: int, lower limit (nm): int, upper limit (nm): int}
            (The limits are rounded to nearest int value)
        """
        property_dict: typing.Dict[str, typing.Dict[str, int]] = {}
        for channel_index in range(FTSLib.FTS_GetNumberOfChannels(self.spectrometer_index)):

            if self.is_OSA200():
                # TODO : Vad ger denna för en OSA200? Kan detector_num variera mellan olika OSOr? (Det kan David inte tänka sig)
                # David tänker: vi borde vilja ha ut detector_type?
                detector_num = FTSLib.FTS_GetDetectorProperty_DetectorType(
                    self.spectrometer_index, channel_index
                )
                detector_type = "Detector 1"
            elif self.is_Redstone():
                detector_num = FTSLib.FTS_GetDetectorProperty_DetectorType(
                    self.spectrometer_index, channel_index
                )
                detector_type = constants.detector_types[detector_num]
            else:
                raise InstrumentSeriesException(
                    "Cannot get detector properties for unknown instrument"
                )
            if "Detector" not in detector_type:
                continue

            FTSLib.FTS_GetDetectorProperty_WavelengthRangeLowerNm.restype = c.c_float
            FTSLib.FTS_GetDetectorProperty_WavelengthRangeUpperNm.restype = c.c_float

            lower_limit = FTSLib.FTS_GetDetectorProperty_WavelengthRangeLowerNm(
                self.spectrometer_index, channel_index
            )
            upper_limit = FTSLib.FTS_GetDetectorProperty_WavelengthRangeUpperNm(
                self.spectrometer_index, channel_index
            )

            # MUSTFIX_PYTHON: Verify that the code above now works (when 3.31 has been released)
            # The detector property above didn't give any valid output, FTSLib problem?
            # FTSLib.FTS_GetInstrumentProperty_MinWavenumber_ext.restype = c.c_float
            # FTSLib.FTS_GetInstrumentProperty_MaxWavenumber_ext.restype = c.c_float
            #
            # upper_limit = 1e7/FTSLib.FTS_GetInstrumentProperty_MinWavenumber_ext(self.spec_index, channel_index)
            # lower_limit = 1e7/FTSLib.FTS_GetInstrumentProperty_MaxWavenumber_ext(self.spec_index, channel_index)

            property_dict[detector_type] = {
                "channel index": channel_index,
                "lower limit (nm)": round(lower_limit),
                "upper limit (nm)": round(upper_limit),
            }
        if self.is_Redstone():
            stitched_channel = FTSLib.FTS_GetStitchedChannelIndex()
            lower_limits = []
            upper_limits = []
            for detector in property_dict.keys():
                if "Detector" in detector:
                    lower_limits.append(property_dict[detector]["lower limit (nm)"])
                    upper_limits.append(property_dict[detector]["upper limit (nm)"])

            property_dict["Stitched"] = {
                "channel index": stitched_channel,
                "lower limit (nm)": min(lower_limits),
                "upper limit (nm)": max(upper_limits),
            }

        elif self.is_OSA200():
            pass
        else:
            raise InstrumentSeriesException(
                "Cannot get stitched channel for unknown instrument"
            )

        return property_dict

    def _clear_data(self):
        """Clear data that is loaded into the ftslib DLL.
        This can be used after reading the data in python to free up some space #MUSTFIX "can be used" or must be used. Test if the eaxmples works without clear_data()
        """
        for idxChannel in range(FTSLib.FTS_GetNumberOfChannels(c.c_ushort(self.spectrometer_index))):
            status = FTSLib.FTS_ClearLastRawInterferogram(c.c_ushort(self.spectrometer_index), idxChannel)
            status = FTSLib.FTS_ClearLastInterferogram_ext(c.c_ushort(self.spectrometer_index), idxChannel)
            logger.info(f"Clear last interferogram in channel {idxChannel} "+constants.err_msg(status))
            status = FTSLib.FTS_ClearLastSpectrum_ext(c.c_ushort(self.spectrometer_index), idxChannel)
            logger.info(f"Clear last spectrum in channel {idxChannel} "+ constants.err_msg(status))
        FTSLib.FTS_ClearCallbacks()
        logger.info("Cleared callbacks")
        # Clearing callback queues of spectrum_t
        for q in [self._interferogram_queue, self._spectrum_queue]:
            with q.mutex:
                q.queue.clear()


    def _await_setvalues(self, timeout=5):
        """
        Wait for all settings to be a the specified setvalues,
        if they are not set within timeout(seconds), then raise an Exception
        """
        starttime = time.time()
        while not self._setvalues_ready():
            time.sleep(0.1)
            if time.time() > starttime+timeout:
                raise TimeoutError("Timeout waiting for instrument settings")

    def _setvalues_ready(self):
        """
        Checks all instrument setvalues, return True if setvalues equals getvalues
        otherwise returns False
        """
        if self.get_sensitivity().upper() != self._setvalue_sensitivity.upper():
            logger.debug("Sensitivity has not reached setvalue")
            logger.debug(f"{self.get_sensitivity()} != {self._setvalue_sensitivity}")
            return False
        if self.get_resolution().upper() != self._setvalue_resolution.upper():
            logger.debug("Resolution has not reached setvalue")
            logger.debug(f"{self.get_resolution()} != {self._setvalue_resolution}")
            return False
        if self.get_apodization().upper() != self._setvalue_apodization.upper():
            logger.debug("Apodization has not reached setvalue")
            logger.debug(f"{self.get_apodization()} != {self._setvalue_apodization}")
            return False
        if self.get_zerofill() != self._setvalue_zerofill:
            logger.debug("Zerofill has not reached setvalue")
            logger.debug(f"{self.get_zerofill()} != {self._setvalue_zerofill}")
            return False

        avgs = self._get_spectrum_averaging()
        avg = avgs[0]
        if not all([avg == a for a in avgs]):
            # Not same for all detectors
            logger.debug("spectrum averaging not same for all detectors")
            return False
        if not self._setvalue_nr_of_averages == avg:
            logger.debug("spectrum averaging is not at setvalue")
            return False
        if self._setvalue_autogain != self.get_autogain():
            logger.debug("Autogain is not at setvalue")
            logger.debug(f"{self.get_autogain()} != {self._setvalue_autogain}")
            return False
        # Multiple detectors
        for det in self._get_detector_names():
            if det in self._setvalue_detector_offset:
                if self.get_detector_offsets([det])[0] != self._setvalue_detector_offset[det]:
                    logger.debug("get_detector_offsets has not reached setvalue")
                    logger.debug(f"{self.get_detector_offsets([det])[0]} != {self._setvalue_detector_offset[det]}")
                    return False
            if det in self._setvalue_attenuation_filter:
                if self.get_attenuation_filter([det])[0] != self._setvalue_attenuation_filter[det]:
                    logger.debug("get_attenuation_filter has not reached setvalue")
                    logger.debug(f"{self.get_attenuation_filter([det])[0]} != {self._setvalue_attenuation_filter[det]}")
                    return False
            
            # Lets check gain level, but not if we are in autogain
            if det == "Stitched":
                # Gain is not applicable, lets skip the rest of the loop
                # for this detector
                continue
            if self._setvalue_gain_level[det] is not None:
                # Check if the setvalue is something
                if self._setvalue_autogain is False:
                    # Don't check if we are using autogain
                    if self.get_gain_level([det])[0] != self._setvalue_gain_level[det]:
                        logger.debug("get_gain_level has not reached setvalue")
                        logger.debug(f"{self.get_gain_level([det])[0]} != {self._setvalue_gain_level[det]}")
                        return False
        return True

    def _setup_spectra(
        self,
        power_type: str = "Absolute power",
        x_unit: str = "nm (vac)",
        y_unit: str = "mW"
    ):
        """
        Internal init when creating OSA_acquisition, also used when starting a new
        acquisition
        """
        FTSLib.FTS_GetLastSpectrum_ext.argtypes = (
            c.c_ushort,
            c.c_ushort,
            c.POINTER(spectrum_t),
            c.POINTER(c.c_uint),
        )
        # Setting power type
        if (
            power_type.casefold() != "absolute power"
            and power_type.casefold() != "power density"
        ):
            raise KeyError(
                "Error setting power type"
                f"Invalid power type {power_type}"
            )
        self.power_type = power_type.title()

        # Setting x and y units
        if y_unit not in constants.y_units.values():
            raise KeyError(
                "Error in setting y_unit: "
                f"Invalid y-unit {y_unit}"
            )
        if self.power_type.casefold() == "power density":
            y_unit = y_unit + " (norm)"
        if x_unit not in constants.x_units.values():
            raise KeyError(
                "Error setting x_unit: "
                f"Invalid x-unit {x_unit}"
            )
        if "(norm)" in y_unit:
            power_type = "Power density"

        for integer, unit in constants.y_units.items():
            if unit == y_unit:
                self.spectrum_y_unit = integer
                break
        for integer, unit in constants.x_units.items():
            if unit == x_unit:
                self.spectrum_x_unit = integer
                break

    def __acquisition_callback(
        self,
        spectrometer_index: int,
        channel_index: int,
        event_code: int,
        status_code: int,
        type_of_status: int,
    ) -> int:
        """Acqusition callback from FTSLib
        
        This is called when there is data available to read.
        """
        if spectrometer_index != self.spectrometer_index:
            logger.error("Got Callback from different spectrometer")
            return 0
        logger.debug("In __acquisition_callback:"
                     f"self.spectrometer_index:({self.spectrometer_index})"
                     f"spectrometer_index:({spectrometer_index})"
                     f"channel_index:({channel_index})"
                     f"event_code:({event_code})"
                     f"status_code:({status_code})"
                     f"type_of_status:({type_of_status})")

        if event_code == 1:
            self.___callback_interferogram(channel_index)
        elif event_code == 2:
            self.___callback_spectrum(channel_index)
        elif event_code == 3:
            pass
        elif event_code == 4:
            pass
        elif event_code == 5:
            pass
        else:
            logger.error(
                "Error in acquisition callback:   "
                f"Unknown OSAs state.\n spectrometer_index: {spectrometer_index},"
                f"channel_index: {channel_index}, event_code: {event_code}, "
                f"status_code: {status_code}, type_of_status: {type_of_status}"
            )
            raise RuntimeError("Error in acquisition callback, check logs")
        return 0

    def ___callback_interferogram(self, channel_index):
        """
        Helper method that handles the acquisition callback when a
        new interferogram is available
        """
        logger.debug(f"Interferogram from {self.model} available.")
        interferogram = self._get_last_interferogram_channel(channel_index)
        if self.is_OSA200() and self._setvalue_autogain:
            # Special handling for OSA20X series, wait for autogain
            validity = interferogram.check_validity()
            if validity["autogain_satisfied"]:
                self._interferogram_queue.put((channel_index, interferogram))
            else:
                logger.info("Autogain not ready, skipping this interferogram.")
        else:
            self._interferogram_queue.put((channel_index, interferogram))

    def ___callback_spectrum(self, channel_index):
        """
        Helper method that handles the acquisition callback when a
        new spectrum is available
        """
        logger.debug(f"Spectrum from {self.model} available.")
        spectrum = self._get_last_spectrum_channel(channel_index)
        if self.is_OSA200() and self._setvalue_autogain:
            # Special handling for OSA20X series, wait for autogain
            validity = spectrum.check_validity()
            if validity["autogain_satisfied"]:
                self._spectrum_queue.put((channel_index, spectrum))
            else:
                logger.info("Autogain not ready, skipping this spectrum.")
        else:
            self._spectrum_queue.put((channel_index, spectrum))

    def acquire(
        self,
        spectrum: bool = True,
        interferogram: bool = False,
        number_of_acquisitions: int = 1,
        spectrum_averaging: int = 1,
        zerofill: int = 0,
        apodization: str = "Hann",
        ignore_errors: typing.List[str] = [],
        power_type="Absolute power",
        x_unit="nm (vac)",
        y_unit="mW",
        **kwargs
    ) -> typing.List[TupleDict]:
        """Acquire spectra and/or interferogram, returns after all measurements are complete.

        Parameters:
            spectrum (bool, default True):
                Indicates if spectra should be returned.
            interferogram (bool, default False):
                Indicates if interferograms should be returned.
            number_of_acquisitions (int, default 1):
                Indicates the number of acquisitions. -1 will start an infinite acquisition
                (stopped by setting osa.stop = True).
            spectrum_averaging (int, Default: 1):
                Sets the number of spectra to average over when retrieving a spectrum.
            zerofill (int, Default: 0):
                Sets the zero-fill factor. Valid values are 0, 1, 2
            apodization (str, Default: "Hann"):
                Sets the apodization type. Valid values are listed below.

                - "None"
                - "Norton beer weak"
                - "Norton beer medium"
                - "Norton beer strong"
                - "Triangular"
                - "Cosine"
                - "Hann"
                - "Hamming"
                - "Blackmanharris3"
                - "Blackmanharris4"
                - "Gaussian"
                - "Two pass hann"

            ignore_errors: (list[str], default False):
                List of errors to ignore, for examples ["Reference Warmup"] to
                ignore cold reference laser.
            power_type (str, default "Absolute power"):
                The spectrum intensity can be either "Absolute power" or "Power Density".
            x_unit (str, default "nm (vac)"):
                The x unit for the spectrum. Refer to the manual for possible units.
            y_unit (str, default "mW"):
                The y unit for the spectrum. Refer to the manual for possible units.

        Returns:
            Returns a list of acquisitions, where each acquisition is a TupleDict.

            Possible keys for OSA200:
                - acquisition["spectrum"]
                - acquisition["interferogram"]

            Possible keys for Redstone:
                - acquisition["spectrum"] which returns the same as Stitched
                - acquisition["spectrum", "Stitched"]
                - acquisition["spectrum", "Detector 1"]
                - acquisition["spectrum", "Detector 2"]
                - acquisition["interferogram", "Detector 1"]
                - acquisition["interferogram", "Detector 2"]

          Each value in the TupleDict is a spectrum_t
        """
        return_data = []
        for data in self.acquire_continuous(spectrum=spectrum,
                                            interferogram=interferogram,
                                            number_of_acquisitions=number_of_acquisitions,
                                            spectrum_averaging=spectrum_averaging,
                                            zerofill=zerofill,
                                            apodization=apodization,
                                            ignore_errors=ignore_errors,
                                            power_type=power_type,
                                            x_unit=x_unit,
                                            y_unit=y_unit,
                                            **kwargs):
            return_data.append(data)
        return return_data

    def acquire_continuous(self,
        spectrum: bool = True,
        interferogram: bool = False,
        number_of_acquisitions: int = -1,
        spectrum_averaging: int = 1,
        zerofill: int = 0,
        apodization: str = "Hann",
        ignore_errors: typing.List[str] = [],
        power_type="Absolute power",
        x_unit="nm (vac)",
        y_unit="mW",
        **kwargs
    ) -> typing.Iterator[TupleDict]:
        """
        Acquire spectra and/or interferograms, yielding data continuously.

        To stop the acquistion set osa.stop = True in your code
        """
        self._set_spectrum_averaging(spectrum_averaging)
        self.set_zerofill(zerofill)
        self.set_apodization(apodization)
        self._setup_spectra(power_type=power_type, x_unit=x_unit, y_unit=y_unit)
        if spectrum is False and interferogram is False:
            raise Exception("Both spectra and interferograms cannot be false")
        self._await_setvalues()
        avgs = self._get_spectrum_averaging()
        if np.max(avgs) > 1 and interferogram:
            raise Exception("You cannot acquire interferograms while spectrum_averging "
                            "is enabled. Please change spectrum_averging to 1.")
        if self._interferogram_queue.qsize() > 0:
            raise Exception("Even before starting there are interferograms in the queue")
        if self._spectrum_queue.qsize() > 0:
            raise Exception("Even before starting there are spectra in the queue")
        
        if not self._is_virtual:
            self._check_spectrometer(self.spectrometer_index,
                                         ignore_errors=ignore_errors)

        self.__start_continous_acq()
        # Flag to make sure that we shut down cleanly
        self._continuous_acq_running = True

        yield from self.__acquisition_loop(
            number_of_acquisitions=number_of_acquisitions,
            spectrum=spectrum,
            interferogram=interferogram,
            **kwargs)
        self.__stop_continuous_acq()
        self._clear_data()
        self._continuous_acq_running = False
        logger.info("Stopped continuous acquisition")

    def __start_continous_acq(self):
        """
        Helper method to run FTS_StartContinuousAcquisition_ext 
        """
        status = FTSLib.FTS_StartContinuousAcquisition_ext(c.c_ushort(self.spectrometer_index), self._acquisition_callback)
        if status != 0:
            msg = (
                "Couldn't start acquisition."
                f"Status: {constants.err_msg(status)}"
            )
            raise Exception(msg)
        logger.info("Started continuous acquisition" + constants.err_msg(status))

    def __stop_continuous_acq(self):
        """
        Helper method to run FTS_StopContinuousAcquisition 
        """
        status = FTSLib.FTS_StopContinuousAcquisition(c.c_ushort(self.spectrometer_index))
        if status != 0:
            msg = (
                "Couldn't stop acquisition."
                f"Status: {constants.err_msg(status)}"
            )
            raise Exception(msg)

    def __acquisition_loop(
        self,
        number_of_acquisitions: int = 1,
        spectrum: bool = False,
        interferogram: bool = False,
        **kwargs
    ) -> typing.Iterator[TupleDict]:
        """Acquisition loop for internal use.
        Requires an acqusition to be started before calling the loop.
        Returns a dictionary of measured data.
        See parameters and returns in the docstring of acquire
        """
        self._set_cycle_counting(True)
        self._set_coherence_analysis(True)

        avgs = self._get_spectrum_averaging()
        avg = avgs[0]
        if not all([avg == a for a in avgs]):
            raise Exception(f"Not same average for all detectors: {avgs}")

        self.stop = False
        acq_iter = 0
        logger.debug(f"Avg: {avg}, Nr: {number_of_acquisitions}")
        while not self.stop:
            logger.debug(f"Starting acq loop number: {acq_iter}")
            latestdata = self.__inner_acquisition_loop(spectrum, interferogram, avg, **kwargs)
            acq_iter += 1
            if number_of_acquisitions != -1:
                if acq_iter >= number_of_acquisitions:
                    self.stop = True
            yield latestdata

    def __inner_acquisition_loop(self, spectrum, interferogram, avg, **kwargs):
        latestdata = TupleDict(defaultkey=self._default_detector)
        # Get interferogram data
        nr_of_interferograms = avg*len(self._interferogram_detectors)
        self._wait_for_interferograms(nr_of_interferograms)

        nr_of_spectra = 1*len(self._spectrum_detectors)
        self._wait_for_spectra(nr_of_spectra)

        interferograms = self._get_last_interferograms(nr_of_interferograms)
        if interferogram:
            for key,value in interferograms.items():
                latestdata["interferogram",key] = value
        # Get spectrum data
        specs = self._get_last_spectra(nr_of_spectra)
        if spectrum:
            for key,value in specs.items():
                latestdata["spectrum",key] = value
        return latestdata


    def _wait_for_interferograms(self, nr):
        """
        Helper function that waits until the interferograms are ready
        """
        self.__wait_for_queue(self._interferogram_queue,
                              "Waiting for interferogram to become available...",
                              nr)

    def _wait_for_spectra(self, nr):
        """
        Helper function that waits until the spectra are ready
        """
        self.__wait_for_queue(self._spectrum_queue,
                              "Waiting for spectrum to become available...",
                              nr)

    @staticmethod
    def __wait_for_queue(q, msg, nr):
        """
        Helper function to wait for interferogram or for spectra
        """
        starttime = time.time()
        lastmsg = time.time()
        if q.qsize() > nr:
            logger.warning("Readout queue is filling faster than it is read. "
                          f"Queue size: {q.qsize()}")
        while q.qsize() < nr:
            time.sleep(0.01)
            if time.time() - lastmsg > 1:
                lastmsg = time.time()
                logger.info(f"{msg} Got {q.qsize()} out of {nr}")
            if time.time()-starttime > 60*5 * nr: # 5 minutes per item
                raise Exception("Timeout waiting for data")

    def _set_cycle_counting(self, poll_wave: bool):
        """Enables or disables cycle counting for each channel, needed for reading wavelength."""
        if self.spectrometer_index is None:
            return
        for ch in self.channels_dict.keys():
            status = FTSLib.FTS_SetAcquisitionOption_CycleCounting_ext(
                c.c_ushort(self.spectrometer_index), c.c_ushort(ch), c.c_bool(poll_wave)
            )
            if status != 0:
                raise Exception(
                    f"Couldn't set cycle counting."
                    f"Status: {constants.err_msg(status)}"
                )
            logger.info(
                f"Setting cycle counting to {poll_wave} for channel {ch}"
                + constants.err_msg(status)
            )

    def _set_coherence_analysis(self, poll_coherence: bool):
        """Enables or disables coherence analysis for each channel,
        needed for reading coherence length.
        """
        if self.spectrometer_index is None:
            return
        for ch in self.channels_dict.keys():
            status = FTSLib.FTS_SetAcquisitionOption_CoherenceAnalysis_ext(
                c.c_ushort(self.spectrometer_index), c.c_ushort(ch), c.c_bool(poll_coherence)
            )
            if status != 0:
                raise Exception(
                    "Couldn't set coherence analysis."
                    f" Status: {constants.err_msg(status)}"
                )
            logger.info(
                f"Setting coherence analysis to {poll_coherence} for channel {ch}"
                + constants.err_msg(status)
            )

    def _get_last_spectra(self, nr:int) -> typing.Dict[str, spectrum_t]:
        """Internal helper method.
        
        Retrieve the last nr of spectra acquired by the instrument,
        The callback from ftslib puts the spectra in a queue, and this
        method is used to get the spectra from that queue.

        Parameters:
            nr (int):
                Number of spectra to get.

        Returns:
            typing.Dict[str, spectrum_t]:
                A dictionary containing the last acquired spectra. 
        """
        specs = {}
        for i in range(nr):
            channel,spec = self._spectrum_queue.get()
            logger.debug(f"Getting spec ch:{channel} from the queue")
            detector = self._get_detector_from_channel(channel)
            specs[detector] = spec
            if not spec.is_valid():
                logger.error("Problems with data quality")
        logger.debug(f"Got spectra: {specs}")
        return specs

    def _get_last_spectrum_channel(self, channel):
        c_spectrometer_index = c.c_ushort(self.spectrometer_index)
        length = c.c_uint()
        status = FTSLib.FTS_GetLastSpectrum_ext(
                c_spectrometer_index, channel, None, c.byref(length)
            )
        if status != 0:
            raise Exception(
                    "Couldn't get last spectrum. Status:"
                    f" {constants.err_msg(status)}"
                )
        spec = spectrum_t()
        spec.allocatedLengthI = length.value
        spec.allocatedLengthx = length.value
        array_I = (c.c_float * length.value)()
        array_x = (c.c_float * length.value)()
        spec.I = c.cast(array_I, c.POINTER(c.c_float))
        spec.x = c.cast(array_x, c.POINTER(c.c_float))

        status = FTSLib.FTS_GetLastSpectrum_ext(
                c_spectrometer_index, channel, c.byref(spec), c.byref(length)
            )
        if status != 0:
            raise Exception(
                    f"Couldn't get last spectrum. Status: "
                    f"{constants.err_msg(status)}"
                )
        logger.info(
                f"Retrieved last spectrum for {channel}" + constants.err_msg(status)
            )
        spec.convert_spectrum(self.spectrum_x_unit, self.spectrum_y_unit)
        return spec

    def _get_last_interferograms(self, nr:int) -> typing.Dict[str, spectrum_t]:
        """Internal helper method.

        Retrieve the last interferogram(s) acquired by the instrument.
        The callback from ftslib puts the data in a queue, and this
        method is used to get the data from that queue.
        
        Parameters:
            nr (int):
                Number of interferograms to get.

        Returns:
            typing.Dict[str, spectrum_t]:
                A dictionary with keys for each detector, where each value is a spectrum_t.
                Example:
                    output["Detector 1"] will be a spectrum_t.
        """
        if self.spectrometer_index is None:
            raise KeyError(
                "Error in get_last_interferogram "
                "No spectrometer_index given"
            )

        return_dict = {}
        for i in range(nr):
            channel,interferogram = self._interferogram_queue.get()
            logger.debug(f"Getting igram ch:{channel} from the queue")
            detector = self._get_detector_from_channel(channel)
            return_dict[detector] = interferogram
            if not interferogram.is_valid():
                logger.error("Problems with data quality")
        return return_dict

    def _get_last_interferogram_channel(self, channel_index):
        length = c.c_uint()
        FTSLib.FTS_GetLastInterferogram_ext(
                c.c_ushort(self.spectrometer_index),
                c.c_ushort(channel_index),
                None,
                c.byref(length),
            )
        FTSLib.FTS_GetLastInterferogram_ext.argtypes = (
            c.c_ushort,
            c.c_ushort,
            c.POINTER(spectrum_t),
            c.POINTER(c.c_uint),
        )
        interferogram = spectrum_t()
        interferogram.allocatedLengthI = length.value
        array_II = (c.c_float * length.value)()
        interferogram.I = c.cast(array_II, c.POINTER(c.c_float))
        status = FTSLib.FTS_GetLastInterferogram_ext(
                c.c_ushort(self.spectrometer_index),
                c.c_ushort(channel_index),
                c.byref(interferogram),
                c.byref(length),
            )
        logger.info(
                f"Retrieved last interferogram for ch {channel_index}"
                + constants.err_msg(status)
            )
        return interferogram
