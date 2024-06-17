import os
import json
import logging
logger = logging.getLogger("pyOSA")

## Loading constants from file
file_path = os.path.abspath(__file__)
directory = os.path.dirname(file_path)
with open(os.path.join(directory,"defines_dictionaries.json")) as fp:
    defines_dictionaries = json.load(fp)

error_codes = {int(key):value for key, value in defines_dictionaries["error_codes"].items()}
data_defines = defines_dictionaries["data_defines"]
apodizations = {int(key):value for key, value in defines_dictionaries["apodizations"].items()}
OSA200_resolutions = {int(key):value for key, value in defines_dictionaries["OSA200_resolutions"].items()}
OSA200_sensitivities = {int(key):value for key, value in defines_dictionaries["OSA200_sensitivities"].items()}
Redstone_resolutions = {int(key):value for key, value in defines_dictionaries["Redstone_resolutions"].items()}
Redstone_sensitivities = {int(key):value for key, value in defines_dictionaries["Redstone_sensitivities"].items()}
y_units = {int(key):value for key, value in defines_dictionaries["y_units"].items()}
x_units = {int(key):value for key, value in defines_dictionaries["x_units"].items()}
detector_types = {int(key):value for key, value in defines_dictionaries["detector_types"].items()}
instrument_series = {int(key):value for key, value in defines_dictionaries["instrument_series"].items()}
instrument_models = {int(key):value for key, value in defines_dictionaries["instrument_models"].items()}
OSA200_status = {int(key):value for key, value in defines_dictionaries["OSA200_status"].items()}
Redstone_status = {int(key):value for key, value in defines_dictionaries["Redstone_status"].items()}


logger.debug("Constants loaded from jsonfile")

class constants:
    """ Making the constants available through a class
    """
    defines_dictionaries = defines_dictionaries
    error_codes = error_codes
    data_defines = data_defines
    apodizations = apodizations
    OSA200_resolutions = OSA200_resolutions
    OSA200_sensitivities = OSA200_sensitivities
    Redstone_resolutions = Redstone_resolutions
    Redstone_sensitivities = Redstone_sensitivities
    y_units = y_units
    x_units = x_units
    detector_types = detector_types
    instrument_series = instrument_series
    instrument_models = instrument_models
    OSA200_status = OSA200_status
    Redstone_status = Redstone_status

    @staticmethod
    def err_msg(status: int) -> str:
        """Takes an error_code and returns a string with the error message
        """
        if status not in constants.error_codes:
            msg = "Invalid error code"
            logger.error(msg)
            return msg
        if status != 0:
            return f"{constants.error_codes[status]}"
        else:
            return ""

    @staticmethod
    def _is_OSA200(inst_series: int) -> bool:
        """Checks if the instrument belongs to the OSA200 series"""
        if inst_series in constants.instrument_series:
            return constants.instrument_series[inst_series] == "OSA200"
        else:
            return False

    @staticmethod
    def get_Redstone_detector_name_from_detector_type(detector_type: int) -> str:
        if detector_type == constants.data_defines['DETECTOR_TYPE_REF']:
            return "Ref"
        elif detector_type == constants.data_defines['DETECTOR_TYPE_BROADBAND_REF']:
            return "Broadband Ref"
        elif detector_type == constants.data_defines['DETECTOR_TYPE_DUT1']:
            return "Detector 1"
        elif detector_type == constants.data_defines['DETECTOR_TYPE_DUT2']:
            return "Detector 2"
        else:
            raise ValueError("Unknown detector")

    @staticmethod
    def _is_Redstone(inst_series: int) -> bool:
        """Checks if the instrument belongs to the Redstone series"""
        if inst_series in constants.instrument_series:
            return constants.instrument_series[inst_series] == "Redstone"
        else:
            return False

