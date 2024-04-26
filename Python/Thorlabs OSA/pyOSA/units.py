import logging
import typing
import re
import ctypes as c

from pyOSA.FTSLib import FTSLib
from pyOSA.constants import constants

logger = logging.getLogger('pyOSA')


class units(object):
    """ Class that keeps track of all units and quantitites needed for pyOSA and FTSLib
    """
    # Functions that verifies specific x-units, see constants.x_units for all available x-units
    @staticmethod
    def x_unit_is_cm(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "1" or unit_str == "cm")

    @staticmethod
    def x_unit_is_inverse_cm(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "2" or unit_str == "cm^-1" or unit_str == "cm-1")

    @staticmethod
    def x_unit_is_THz(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "3" or unit_str == "thz")

    @staticmethod
    def x_unit_is_nm_vac(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "4" or unit_str == "nm (vac)")

    @staticmethod
    def x_unit_is_nm_air(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "5" or unit_str == "nm (air)")

    @staticmethod
    def x_unit_is_nm(unit: typing.Union[int, str]) -> bool:
        return (units.x_unit_is_nm_vac(unit) or units.x_unit_is_nm_air(unit))

    @staticmethod
    def x_unit_is_eV(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "6" or unit_str == "ev")

    @staticmethod
    def x_unit_is_index(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "7" or unit_str == "index")

    @staticmethod
    def x_unit_is_seconds(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "8" or unit_str == "seconds")

    @staticmethod
    def x_unit_is_pixel(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "9" or unit_str == "pixel")

    @staticmethod
    def x_unit_is_Hz(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "10" or unit_str == "hz")

    @staticmethod
    def x_unit_is_inverse_cm_raman(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "11" or unit_str == "cm^-1 (raman)" or unit_str == "cm-1 (raman)")

    # Functions that verifies specific y-units, see constants.y_units for all available y-units
    @staticmethod
    def y_unit_is_counts(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "32770" or unit_str == "counts")

    @staticmethod
    def y_unit_is_dBm(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "32771" or unit_str == "dbm")

    @staticmethod
    def y_unit_is_dBm_norm(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "32772" or unit_str == "dbm (norm)")

    @staticmethod
    def y_unit_is_mW(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "32773" or unit_str == "mw")

    @staticmethod
    def y_unit_is_mW_norm(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "32774" or unit_str == "mw (norm)")

    @staticmethod
    def y_unit_is_percent(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "32775" or unit_str == "percent")

    @staticmethod
    def y_unit_is_intensity(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "32785" or unit_str == "intensity")

    @staticmethod
    def y_unit_is_log_intensity(unit: typing.Union[int, str]) -> bool:
        unit_str = str(unit).strip().lower()
        return (unit_str == "32786" or unit_str == "logintensity")

    @staticmethod
    def convert_nm_vac(wavelength_nm_vac: float, desired_unit: typing.Union[int, str]) -> float:
        """#MUSTFIX_PYTHON look if we can use the umbrella function in FTSLib
        Functions for conversion from nm to various units
        (There are functions in FTSLib that allows conversion between any of these units, e.g., THz to cm-1,
         but they not been implemented in Python yet)
        """
        if units.x_unit_is_inverse_cm(desired_unit):
            return units.convert_nm_vac_to_wavenumber(wavelength_nm_vac)
        elif units.x_unit_is_THz(desired_unit):
            return units.convert_nm_vac_to_THz(wavelength_nm_vac)
        elif units.x_unit_is_eV(desired_unit):
            return units.convert_nm_vac_to_eV(wavelength_nm_vac)
        elif units.x_unit_is_nm_air(desired_unit):
            return units.convert_nm_vac_to_nm_air(wavelength_nm_vac)
        elif units.x_unit_is_nm_vac(desired_unit):
            return wavelength_nm_vac # No conversion needed
        else:
            logger.error("Error in convert_nm_vac: Unknown unit, conversion not possible")
            raise ValueError("Unknown unit conversion not possible")

    @staticmethod
    def convert_nm_vac_to_wavenumber(wavelength_nm: float) -> float:
        FTSLib.FTS_Convert_nm_vac_To_WaveNumber.argtypes = (c.c_double,)
        FTSLib.FTS_Convert_nm_vac_To_WaveNumber.restype = c.c_double
        return FTSLib.FTS_Convert_nm_vac_To_WaveNumber(wavelength_nm)

    @staticmethod
    def convert_nm_vac_to_THz(wavelength_nm: float) -> float:
        FTSLib.FTS_Convert_nm_vac_To_THz.argtypes = (c.c_double,)
        FTSLib.FTS_Convert_nm_vac_To_THz.restype = c.c_double
        return FTSLib.FTS_Convert_nm_vac_To_THz(wavelength_nm)

    @staticmethod
    def convert_nm_vac_to_eV(wavelength_nm: float) -> float:
        FTSLib.FTS_Convert_nm_vac_To_eV.argtypes = (c.c_double,)
        FTSLib.FTS_Convert_nm_vac_To_eV.restype = c.c_double
        return FTSLib.FTS_Convert_nm_vac_To_eV(wavelength_nm)

    @staticmethod
    def convert_nm_vac_to_nm_air(wavelength_nm: float) -> float:
        """Using standard dry air as defined by E.R. Peck and K. Reeder (JOSA, 62, 958-962 (1972)) and used in the
        NIST Atomic Spectra Database (15degreeC, 101.325kPa, and 0% relative humidity)
        """
        FTSLib.FTS_Convert_nm_vac_To_nm_air_PeckAndReeder.argtypes = (c.c_double,)
        FTSLib.FTS_Convert_nm_vac_To_nm_air_PeckAndReeder.restype = c.c_double
        return FTSLib.FTS_Convert_nm_vac_To_nm_air_PeckAndReeder(wavelength_nm)

    @staticmethod
    def get_formatted_x_quantity_and_unit(var: typing.Union[int, str, object]) -> str:
        """ Function for formatting the quantity and unit for a given x-unit, e.g., 'Optical Frequency (THz)' or 'Wavelength (nm (vac))'
        It can be called either as
            str = get_formatted_x_quantity_and_unit(measurement)
        where measurement is a spectrum_t object or
            str = get_formatted_x_quantity_and_unit(x_unit)
        where x_unit can be given either as the keys or values of constants.x_units
        """
        quantity = units.get_formatted_x_quantity(var)
        unit = units.get_formatted_x_unit(var)
        return f"{quantity} ({unit})"

    @staticmethod
    def get_formatted_x_quantity(var: typing.Union[int, str, object]) -> str:
        """Function for formatting the quantity for a given x-unit, e.g., 'Optical Frequency' or 'Wavelength'
        It can be called either as
            str = get_formatted_x_quantity(measurement)
        where measurement is a spectrum_t object or
            str = get_formatted_x_quantity(x_unit)
        where x_unit can be given either as the keys or values of constants.x_units
        """
        if hasattr(var, 'xAxisUnit'):
            x_unit_idx = var.xAxisUnit
        else:
            x_unit_idx = units.find_x_unit_index(var)  # Converts a possible string to the corresponding index, e.g., 'THz' -> 3

        x_unit_idx_to_quantity = {
            0:     "No unit",
            1:     "Optical Path Difference",
            2:     "Wavenumbers",
            3:     "Optical Frequency",
            4:     "Wavelength",
            5:     "Wavelength",
            6:     "Photon Energy",
            7:     "Index",
            8:     "Time",
            9:     "Pixel Number",
            10:    "Frequency",
            11:    "Raman Shift",
            65534: "Unknown",
        }

        if x_unit_idx in x_unit_idx_to_quantity:
            return x_unit_idx_to_quantity[x_unit_idx]
        else:
            return "Unknown"

    @staticmethod
    def get_formatted_x_unit(var: typing.Union[int, str, object]) -> str:
        """Function for formatting the unit for a given x-unit, e.g., 'THz' or 'nm (vac)'
        It can be called either as
            str = get_formatted_x_unit(measurement)
        where measurement is a spectrum_t object or
            str = get_formatted_x_unit(x_unit)
        where x_unit can be given either as the keys or values of constants.x_units
        """
        if hasattr(var, 'xAxisUnit'):
            x_unit_idx = var.xAxisUnit
        else:
            # Convert a possible string to the corresponding index, e.g., 'THz' -> 3
            x_unit_idx = units.find_x_unit_index(var)

        if x_unit_idx in constants.x_units:
            return constants.x_units[x_unit_idx]
        else:
            return "Unknown"

    @staticmethod
    def get_formatted_y_quantity_and_unit(*args: typing.Union[object, str, typing.Tuple[str, str]]) -> str:
        """Format the quantity and unit for a given y-unit.

        This function formats the quantity and unit for a given y-unit, e.g., 'Absolute Power (mW)' or 'Power Density (dBm/nm)'.

        It can be called either as:
            - str = get_formatted_y_quantity_and_unit(measurement)
            where measurement is a spectrum_t object, or
            - str = get_formatted_y_quantity_and_unit(y_unit)
            - str = get_formatted_y_quantity_and_unit(y_unit, x_unit)
            where y_unit and x_unit (the latter is used in the cases when the y-unit is in power density)
            can be given either as the keys or values of constants.y_units and constants.x_units, respectively.
        """
        x_unit_idx, y_unit_idx = units._x_unit_and_y_unit_indices_from_args(args)
        quantity = units.get_formatted_y_quantity(y_unit_idx)
        unit = units.get_formatted_y_unit(y_unit_idx, x_unit_idx)
        return f"{quantity} ({unit})"

    @staticmethod
    def get_formatted_y_quantity(y_unit: typing.Union[int, str]) -> str:
        """Format the quantity given a y-unit.

        This function formats the quantity given a y-unit, e.g., 'Absolute Power' or 'Power Density'.
        y_unit can be given either as the keys or values of constants.y_units.
        """
        y_unit_idx_to_quantity = {
            32769: "Arbitrary Units, or Absorbance Units",
            32770: "AD Signal",
            32771: "Absolute Power",
            32772: "Power Density",
            32773: "Absolute Power",
            32774: "Power Density",
            32775: "Percent",
            32776: "Angle",
            32777: "Angle",
            32778: "Temperature",
            32779: "Temperature",
            32780: "Pressure",
            32781: "General log unit",
            32782: "Relative Power",
            32783: "Percentage Points",
            32784: "Mixed units",
            32785: "Non-Calibrated Intensity",
            32786: "log Non-Calibrated Intensity",
            32787: "Calibrated Intensity",
            32788: "log Calibrated Intensity",
            32789: "Pressure",
            32790: "Pressure",
            32791: "Pressure",
            32792: "Logarithm of Counts",
            32793: "Cross Section of cm^2 per Molecule",
            32794: "Number Concentration x Distance",
            32795: "Mass Concentration x Distance",
            32796: "Number Concentration",
            32797: "Mass Concentration",
            32798: "Number Concentration",
            32799: "Transmittance",
            65535: "Unknown",
        }
        y_unit_idx = units.find_y_unit_index(y_unit)  # Converts a possible string to the corresponding index, e.g., 'mW' -> 32773
        if y_unit_idx in y_unit_idx_to_quantity:
            return y_unit_idx_to_quantity[y_unit_idx]
        else:
            return "Unknown"

    @staticmethod
    def get_formatted_y_unit(*args: typing.Union[object, str, typing.Tuple[str, str]]) -> str:
        """Function for formatting the unit for a given y-unit, e.g., 'mW' or 'dBm/nm'
        It can be called either as
            str = get_formatted_y_unit(measurement)
        where measurement is a spectrum_t object or
            str = get_formatted_y_unit(y_unit)
            str = get_formatted_y_unit(y_unit, x_unit)
        where y_unit and x_unit (the latter is used in the cases when the y-unit is in power density)
        can be given either as the keys or values of OSA_constants.y_units and OSA_constants.x_units, respectively
        """
        x_unit_idx, y_unit_idx = units._x_unit_and_y_unit_indices_from_args(args)
        if y_unit_idx in constants.y_units:
            if units.y_unit_is_normalized(y_unit_idx):
                # Formatting for power density
                y_unit = constants.y_units[y_unit_idx].replace("(norm)", "").strip()
                x_unit = constants.x_units[x_unit_idx]
                return f"{y_unit}/{x_unit}"
            else:
                return constants.y_units[y_unit_idx]
        else:
            return "Unknown"

    @staticmethod
    def y_unit_is_normalized(y_unit: typing.Union[int, str]) -> bool:
        """Checks if the y-unit is normalized, i.e., if the quantity is 'Power Density'
        """
        return units.y_unit_is_dBm_norm(y_unit) or units.y_unit_is_mW_norm(y_unit)

    @staticmethod
    def find_x_unit_index(x_unit: typing.Union[int, str]) -> int:
        """Function that returns the x-unit index used in constants.x_units
        x_unit can be given either as the keys or values of constants.x_units

        Raises:
            ValueError: If x_unit cannot be found in constants.x_units.
        """
        try:
            return units._find_index_from_dictionary(var=x_unit, dict=constants.x_units)
        except ValueError:
            error_message = "Error in find_x_unit_index: Unknown unit; not possible to find the index"
            logger.error(error_message) # TODO Det verkar också finnas logger.exception. ska vi använda den istället?
            raise ValueError(error_message)
        
    @staticmethod
    def find_y_unit_index(y_unit: typing.Union[int, str]) -> int:
        """Function that returns the y-unit index used in constants.y_units
        y_unit can be given either as the keys or values of constants.y_units

        Raises:
            ValueError: If y_unit cannot be found in constants.y_units.
        """
        try:
            return units._find_index_from_dictionary(var=y_unit, dict=constants.y_units)
        except ValueError:
            error_message = "Error in find_y_unit_index: Unknown unit; not possible to find the index"
            logger.error(error_message) # TODO Det verkar också finnas logger.exception. ska vi använda den istället?
            raise ValueError(error_message)

    @staticmethod
    def get_available_constants(constant_name: str) -> typing.List[str]:
        """Return a list of values corresponding to the provided constant name.

        If constant_name corresponds to a key in defines_dictionaries, which is a dictionary containing names of constants,
        then returns a list of the values in defines_dictionaries[constant_name]. For example, calling 
        get_available_constants("instrument models") returns a list of all possible instrument models.

        Parameters:
            constant_name (str):
                String corresponding to a certain type of constant, such as "instrument model" or "x unit".

        Returns:
            List[str]:
                List of strings containing all possible values for the given constant_name,
                such as "nm (vac)" and "THz" for the constant_name "x unit".
        """
        matching_keys = []
        for key in constants.defines_dictionaries.keys():
            cleaned_key = re.sub(r"[^a-zA-Z0-9]", "", key.lower())
            cleaned_constant_name = re.sub(r"[^a-zA-Z0-9]", "", constant_name.lower())

            if cleaned_constant_name in cleaned_key:
                matching_keys.append(key)

        #unsuccessful searches returns an empty list
        if not matching_keys:
            logger.error("No matching keys found.")
            raise ValueError("No matching keys found.")
        elif len(matching_keys) == 1:
            dict = constants.defines_dictionaries[matching_keys[0]]
            constant_list = [value for value in dict.values()]

            #Removes duplicates
            constant_list = list(dict.fromkeys(constant_list))
            return constant_list  # Exactly one matching key found
        else:
            logger.error("Error in get_available_constants: More than one key matches. Please specify constant_name further.")
            raise ValueError("More than one key matches")

    # Helper function that extracts x_unit_idx and y_unit_idx from the tuple args holding either
    # a single spectrum_t object, a single parameter (either an index or a string), or
    # two parameters (either indices or string)
    @staticmethod
    def _x_unit_and_y_unit_indices_from_args(args):
        if len(args)==1:
            if hasattr(args[0], 'xAxisUnit'):
                y_unit_idx = args[0].yAxisUnit
                x_unit_idx = args[0].xAxisUnit
            else:
                y_unit_idx = units.find_y_unit_index(args[0])  # Converts a possible string to the corresponding index, e.g., 'mW'  -> 32773
                x_unit_idx = -1
        elif len(args)==2:
            y_unit_idx = units.find_y_unit_index(args[0])      # Converts a possible string to the corresponding index, e.g., 'mW'  -> 32773
            x_unit_idx = units.find_x_unit_index(args[1])      # Converts a possible string to the corresponding index, e.g., 'THz' -> 3
        else:
            logger.error("Error in get_available_constants(args):   args must have length 1 or 2")
            y_unit_idx = -1
            x_unit_idx = -1
            raise TypeError("invalid number of arguments")
        return x_unit_idx, y_unit_idx

    # Helper function that returns an index (key) from a dictionary corresponding to
    # var which can be either the index or the value
    @staticmethod
    def _find_index_from_dictionary(var, dict):
        if isinstance(var, int):
            # This is a key?
            if var in dict:
                return var
        elif isinstance(var, str):
            # This is a value?
            var_lower = var.strip().lower()
            reversed_dict = {value.lower(): key for key, value in dict.items()}
            if var_lower in reversed_dict:
                return reversed_dict[var_lower]

        # Try to return the index containing 'unknown'
        for key, value in dict.items():
            if value.lower() == "unknown":
                return key

        logger.error("Error in get_available_constants:   Not possible to find the index")
        raise LookupError("Not possible to find the index")

    ###### Private helper functions
    @staticmethod
    def _format_wavelength_range(lower_limit_nm, upper_limit_nm, desired_unit):
        # Helper function that converts and formats a range in nm to the desired unit, e.g., '1000-2500 nm' or ' THz'
        lower_limit = lower_limit_nm
        upper_limit = upper_limit_nm
        unit = "nm"
        nr_of_decimals = 0
        # Convert to the desired unit
        if units.x_unit_is_inverse_cm(desired_unit):
            # Convert to cm^-1
            tmp = upper_limit
            upper_limit = units.convert_nm_vac_to_wavenumber(lower_limit)
            lower_limit = units.convert_nm_vac_to_wavenumber(tmp)
            unit = "cm-1"
            nr_of_decimals = 0
        elif units.x_unit_is_THz(desired_unit):
            # Convert to THz
            tmp = upper_limit
            upper_limit = units.convert_nm_vac_to_THz(lower_limit)
            lower_limit = units.convert_nm_vac_to_THz(tmp)
            unit = "THz"
            nr_of_decimals = 1
        elif units.x_unit_is_nm(desired_unit):
            pass # Do nothing (for this large range we ignore air/vac differences)
        elif units.x_unit_is_eV(desired_unit):
            # Convert to eV
            tmp = upper_limit
            upper_limit = units.convert_nm_vac_to_eV(lower_limit)
            lower_limit = units.convert_nm_vac_to_eV(tmp)
            unit = "eV"
            nr_of_decimals = 4
        else:
            pass # Non-allowed/unknown unit, keep values in nm
        return f"{lower_limit:.{nr_of_decimals}f}-{upper_limit:.{nr_of_decimals}f} {unit}"

