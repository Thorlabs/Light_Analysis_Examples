import typing
import logging
import ctypes as c

import numpy as np

from pyOSA.spectrum_t import spectrum_t
from pyOSA.constants import constants
from pyOSA.FTSLib import FTSLib
from pyOSA.units import units

logger = logging.getLogger("pyOSA")

class analysis(object):
    """
    Collection of methods from FTSLib used to do analysis
    on interferograms and spectra
    """

    @staticmethod
    def wavemeter(interferogram: spectrum_t,
                  spectral_unit:str = "nm (vac)"
                  ) -> typing.Dict[str, float]:
        """Perform wavemeter analysis on an interferogram.

        Returns wavelength data for an interferogram.

        Parameters:
            interferogram (spectrum_t):
                Interferogram of type spectrum_t.

            spectral_unit (str, optional):
                The unit of wavelength. Defaults to "nm (vac)".

        Returns:
            dict:
                The wavemeter data can be accessed as follows:
                    - wavemeter_dict["wavelength"]
                    - wavemeter_dict["error"]

        Example:

        .. code-block:: python

                igram = acquisition["interferogram"]
                wavedata = pyOSA.analysis.wavemeter(igram)
                igramstr = f"{wavedata['wavelength']:.4f} +- {wavedata['error']:.4f}"
        """
        FTSLib.FTS_Wavelengthmeter_ext2.argtypes = (
            c.POINTER(spectrum_t),
            c.c_uint,
            c.c_uint,
            c.c_double,
            c.POINTER(c.c_double),
            c.POINTER(c.c_double),
            c.POINTER(c.c_int),
        )
        wavemeter_spectral_unit = spectral_unit

        wavemeter_dict = {}
        wavenumber_ref = c.c_double()
        wavenumber_error_ref = c.c_double()
        cycle_num = c.c_int()

        if not interferogram.is_interferogram():
            logger.error(
                "Error in wavemeter analysis:"
                " This is not an interferogram, wavelength meter "
                "analysis not possible"
            )
            raise Exception("This is not an interferogram")
        status = FTSLib.FTS_Wavelengthmeter_ext2(
            c.byref(interferogram),
            0,
            interferogram.length - 1,
            interferogram.referenceWavelength_nm_vac,
            c.byref(wavenumber_ref),
            c.byref(wavenumber_error_ref),
            c.byref(cycle_num),
        )
        if constants.error_codes[status] != "FTS Success":
            logger.error(
                "Error in wavemeter analysis:  "
                " Error reading wavelength: "
                + constants.err_msg(status).replace("Error: ", "")
            )
            # Todo, check if this should raise an exception
            # raise AcquisitionException("Error reading wavelength")

        wavemeter_value_inverse_cm = wavenumber_ref.value
        wavemeter_error_inverse_cm = wavenumber_error_ref.value

        # More about the error, see:
        # void Wavelengthmeter::EstimateWavenumberError(double Mean, double Stdev)
        if wavemeter_value_inverse_cm == -1:
            # -1 indicates that no wavelength was detected, do not convert this number
            wavemeter_value_used_x_unit = wavemeter_value_inverse_cm
            wavemeter_error_used_x_unit = -1
        elif units.x_unit_is_inverse_cm(wavemeter_spectral_unit):
            # Todo mustfix, Varför sätter vi unit till ett värde här? Det måste väl ändå vara fel? /Ludde
            wavemeter_value_used_x_unit = wavemeter_value_inverse_cm
            wavemeter_error_used_x_unit = wavemeter_error_inverse_cm
        else:
            wavemeter_value_nm_vac = 1e7 / wavemeter_value_inverse_cm
            wavemeter_error_nm_vac = abs(
                  1e7 / (wavemeter_value_inverse_cm - wavemeter_error_inverse_cm / 2)
                - 1e7 / (wavemeter_value_inverse_cm + wavemeter_error_inverse_cm / 2)
            )
            wavemeter_value_used_x_unit = units.convert_nm_vac(
                wavemeter_value_nm_vac, wavemeter_spectral_unit
            )
            wavemeter_error_used_x_unit = abs(
                units.convert_nm_vac(
                    wavemeter_value_nm_vac - wavemeter_error_nm_vac / 2,
                    wavemeter_spectral_unit,
                )
                - units.convert_nm_vac(
                    wavemeter_value_nm_vac + wavemeter_error_nm_vac / 2,
                    wavemeter_spectral_unit,
                )
            )

        wavemeter_dict = {
                    "wavelength": wavemeter_value_used_x_unit,
                    "error": wavemeter_error_used_x_unit}

        return wavemeter_dict
    
    @staticmethod
    def coherence(interferogram: spectrum_t
                  ) -> typing.Dict[str, float]:
        """Measure the coherence length of an interferogram.

        Returns coherence length data for an interferogram.

        Parameters:
            interferogram (spectrum_t):
                Interferogram of type spectrum_t.

        Returns:
            dict:
                A dictionary containing coherence data with the following keys:
                    - "coherence": The coherence length.
                    - "error": Error associated with the coherence measurement.

        Example:

        .. code-block:: python

            igram = acquisition["interferogram", "Detector 2"]
            coherence_data = pyOSA.analysis.coherence(igram)
            coherence_length = coherence_data["coherence"]
        """
        FTSLib.FTS_CoherenceLength_Array_ext.argtypes = (
            c.POINTER(c.c_float),
            c.c_double,
            c.c_uint,
            c.c_uint,
            c.c_double,
            c.c_float,
            c.c_bool,
            c.POINTER(c.c_double),
            c.POINTER(c.c_double),
        )

        coherence_dict = {}
        coherence_length = c.c_double()
        coherence_error = c.c_double()

        if interferogram.is_OSA200():
            single_sided = False
        elif interferogram.is_Redstone():
            single_sided = True
        else:
            logger.error("Error in coherence analysis: Unknown instrument series")
            raise Exception("Unknown instrument series")

        status = FTSLib.FTS_CoherenceLength_Array_ext(
            interferogram.I,
            interferogram.samplingDistance_cm_vac,
            0,
            interferogram.length,
            interferogram.referenceWavelength_nm_vac,
            interferogram.minOPD_cm,
            c.c_bool(single_sided),
            c.byref(coherence_length),
            c.byref(coherence_error),
        )
        if status != 0:
            msg = f"FTS_CoherenceLength_Array_ext: {constants.err_msg(status)}"
            logger.error(msg)
        logger.info(f"Latest coherence length: {coherence_length.value} cm")
        coherence_dict = {"coherence": coherence_length.value,
                          "error": coherence_error.value}
        return coherence_dict
    
    @staticmethod
    def optical_power(spectrum: spectrum_t,
                      optical_power_mode: int = 0, x_min: float = None, x_max: float = None,
                      threshold = None
                      ) -> float:
        """Measure the optical power in part of a spectrum.

        Returns the optical power of the given spectrum according to the optical power mode.

        Parameters:
            spectrum (spectrum_t):
                The spectrum for which to calculate the optical power.

            optical_power_mode (int, optional):
                Specifies how the optical power is calculated:
                    - 0: Measure over the entire spectrum.
                    - 1: Measure around the largest peak.
                    - 2: Manual mode, requires x_min and x_max inputs.

            x_min (float, optional):
                Starting point for calculating optical power.
                Should be provided in the same unit as the spectrum.
                Only applies if optical power mode is 2 (manual mode).

            x_max (float, optional):
                Stopping point for calculating optical power.
                Should be provided in the same unit as the spectrum.
                Only applies if optical power mode is 2 (manual mode).

        Returns:
            float:
                The calculated optical power.
        
        Example:

        .. code-block:: python

            spectrum = acquisition["spectrum"]
            power = pyOSA.analysis.optical_power(spectrum,
                                                 optical_power_mode=2,
                                                 x_min=1400,
                                                 x_max=1600)
        """
        _optical_power_mode = optical_power_mode
        optical_x_min = x_min
        optical_x_max = x_max
        FTSLib.FTS_OpticalPower.argtypes = (
            c.POINTER(spectrum_t),
            c.c_float,
            c.c_float,
            c.POINTER(c.c_double),
        )
        if _optical_power_mode == 0:
            # Mode 0: Use x_min and x_max from the spectrum_t directly
            x_min = spectrum.x_min
            x_max = spectrum.x_max
        elif _optical_power_mode == 1:
            # Mode 1: Calculate x_min and x_max based on peaks from the spec
            peak_data = analysis.peak_track(spectrum, sort_option=2, threshold=threshold)
            ret = peak_data
            peak_center = ret[0, 0]
            peak_width = ret[2, 0]
            x_min = peak_center - peak_width * 5
            x_max = peak_center + peak_width * 5
        elif _optical_power_mode == 2:
            # Mode 2: Use predefined optical_x_min and optical_x_max
            x_min = optical_x_min
            x_max = optical_x_max
        else:
            raise ValueError("Unrecognized optical power mode")
        logger.debug(f"Get optical power in: x_min, {x_min}, x_max: {x_max}")
        optical_power = c.c_double()
        status = FTSLib.FTS_OpticalPower(c.byref(spectrum), x_min, x_max, c.byref(optical_power))
        if status != 0:
            msg = f"FTS_OpticalPower: {constants.err_msg(status)}"
            logger.error(msg)
            raise Exception(msg)
        logging.info(f"{np.mean(spectrum.get_y())}")
        logger.info(f"Latest optical power: {optical_power.value:.3f} "
                    f"{constants.y_units[spectrum.yAxisUnit]}")
        return optical_power.value
    
    @staticmethod
    def peak_track(spectrum: spectrum_t,
                   start_index: int = 0,
                   stop_index: int = None,
                   threshold: float = None,
                   min_peak_height_db: float = 3,
                   sort_option: int = 1,
                   max_peaks: int = 20) -> np.ndarray:
        """Find and measure parameters of peaks in a spectrum.

        Returns the number of peaks and peak data.

        Parameters:
            spectrum (spectrum_t):
                Spectrum to read peaks from.

            start_index (int, Default: 0):
                Indicates the starting index for the peak search.
                Default 0 is the beginning of the spectrum.

            stop_index (int, Default: None):
                Indicates the stopping index for the peak search.
                Default None means that the spectrum length is used.

            threshold (float, Default: None):
                Sets the threshold for peak searching.
                Peaks below the threshold are not returned.
                Default None sets threshold to 0.1 for y-unit mW and -10 for y-unit dBm.

            min_peak_height_db (float, Default: 3):
                Sets the minimum height for a peak to be tracked, in dB.

            sort_option (int, Default: 1):
                Sets how the peaks are sorted along the rows in peak_data.

                - 0: No sorting,
                - 1: Sorted in order of increasing center position,
                - 2: Sorted in order of increasing height,
                - 3: Sorted in order of increasing width.

            max_peaks (int, Default: 20):
                The maximum number of peaks filled into the array.

        Returns:
            np.ndarray:

                - The peak data read from the spectrum, organized in data type per row, peak number per column.
                - Row one: centroid values of peaks.
                - Row two: peak heights.
                - Row three: peak widths.
                - Row four: first value left of peak where intensity has dropped min_peak_height_db.
                - Row five: same for right side.

        Example:

        .. code-block:: python

            spectrum = acquisition["spectrum"]
            peaks = pyOSA.analysis.peak_track(spectrum, threshold=1.5e-3, sort_option=2)
            peak_centers, peak_heights, peak_widths, peak_lefts, peak_rights = peaks
            print(peak_centers[0])
        """
        peak_start_index = start_index
        peak_stop_index = stop_index
        peak_threshold = threshold
        min_peak_height_db = min_peak_height_db
        peak_sort_option = sort_option
        max_peaks = max_peaks

        FTSLib.FTS_FindPeaks.argtypes = (
            c.POINTER(spectrum_t),
            c.c_uint,
            c.c_uint,
            c.c_float,
            c.c_float,
            c.c_uint,
            c.POINTER(c.c_float),
            c.POINTER(c.c_float),
            c.POINTER(c.c_float),
            c.POINTER(c.c_float),
            c.POINTER(c.c_float),
            c.c_uint,
        )
        array_pc = (c.c_float * max_peaks)()
        array_pw = (c.c_float * max_peaks)()
        array_ph = (c.c_float * max_peaks)()
        array_pl = (c.c_float * max_peaks)()
        array_pr = (c.c_float * max_peaks)()

        peak_centers = c.cast(array_pc, c.POINTER(c.c_float))
        peak_widths = c.cast(array_pw, c.POINTER(c.c_float))
        peak_heights = c.cast(array_ph, c.POINTER(c.c_float))
        peak_lefts = c.cast(array_pl, c.POINTER(c.c_float))
        peak_rights = c.cast(array_pr, c.POINTER(c.c_float))

        if peak_stop_index is None:
            peak_stop_index = spectrum.length

        if peak_threshold is None:
            fraction = 0.15  # 15%
            peak_threshold = spectrum.y_min + fraction * (spectrum.y_max - spectrum.y_min)

        number_of_peaks = FTSLib.FTS_FindPeaks(
            c.byref(spectrum),
            peak_start_index,
            peak_stop_index,
            peak_threshold,
            min_peak_height_db,
            peak_sort_option,
            peak_centers,
            peak_widths,
            peak_heights,
            peak_lefts,
            peak_rights,
            max_peaks,
        )

        if not peak_centers[0:number_of_peaks]:
            peak_data = np.array([[-1], [-1], [-1], [-1], [-1]])
            logger.info(f"Latest peaks: {[-1]} {constants.x_units[spectrum.xAxisUnit]}")
        else:
            peak_data = np.array(
                [
                    peak_centers[0:number_of_peaks],
                    peak_heights[0:number_of_peaks],
                    peak_widths[0:number_of_peaks],
                    peak_lefts[0:number_of_peaks],
                    peak_rights[0:number_of_peaks],
                ]
            )
            logger.info(
                f"Latest peaks: {peak_centers[0:number_of_peaks]}"
                f"{constants.x_units[spectrum.xAxisUnit]}"
            )
        return peak_data
    
    @staticmethod
    def valley_track(spectrum: spectrum_t,
        start_index: int = 0,
        stop_index: int = None,
        threshold: float = None,
        min_valley_depth_db: float = 3,
        sort_option: int = 1,
        max_valleys: int = 20,) -> np.ndarray:
        """Find Valleys and their data from a spectrum.

        Parameters:
            spectrum (spectrum_t):
                Spectrum to read valleys from.

            start_index (int, Default: 0):
                Indicates the starting index for the valley search.
                Default 0 is the beginning of the spectrum.

            stop_index (int, Default: None):
                Indicates the stopping index for the valley search.
                Default None means that the spectrum length is used.

            threshold (float, Default: None):
                Sets the threshold for valley searching.
                Valleys above the threshold are not returned.
                Default None sets threshold to 0.1 for y-unit mW and -10 for y-unit dBm.

            min_valley_depth_db (float, Default: 3):
                Sets the minimum depth for a valley to be tracked, in dB.

            sort_option (int, Default: 1):
                Sets how the valleys are sorted along the rows in valley_data:

                - 0: No sorting,
                - 1: Sorted in order of increasing center position,
                - 2: Sorted in order of increasing depth,
                - 3: Sorted in order of increasing width.

            max_valleys (int, Default: 20):
                The maximum number of valleys filled into the array.

        Returns:
            np.ndarray:
                The valley data read from the spectrum, organized in data type per row, valley number per column.

                - Row one: centroid values of valleys.
                - Row two: valley depths.
                - Row three: valley widths.
                - Row four: first value left of valley where intensity has dropped min_valley_height_db.
                - Row five: same for right side.

        Example:

        .. code-block:: python

            spectrum = acquisition["spectrum"]
            valley_data = pyOSA.analysis.valley_track(spectrum,
                                                      threshold=1.4,
                                                      sort_option=1,
                                                      max_valleys=4)
            valley_centers = valley_data[0]
        """
        valley_start_index = start_index
        valley_stop_index = stop_index
        valley_threshold = threshold
        min_valley_depth_db = min_valley_depth_db
        valley_sort_option = sort_option
        max_valleys = max_valleys

        FTSLib.FTS_FindValleys.argtypes = (
            c.POINTER(spectrum_t),
            c.c_uint,
            c.c_uint,
            c.c_float,
            c.c_float,
            c.c_uint,
            c.POINTER(c.c_float),
            c.POINTER(c.c_float),
            c.POINTER(c.c_float),
            c.POINTER(c.c_float),
            c.POINTER(c.c_float),
            c.c_uint,
        )
        array_vc = (c.c_float * max_valleys)()
        array_vw = (c.c_float * max_valleys)()
        array_vh = (c.c_float * max_valleys)()
        array_vl = (c.c_float * max_valleys)()
        array_vr = (c.c_float * max_valleys)()

        valley_centers = c.cast(array_vc, c.POINTER(c.c_float))
        valley_widths = c.cast(array_vw, c.POINTER(c.c_float))
        valley_heights = c.cast(array_vh, c.POINTER(c.c_float))
        valley_lefts = c.cast(array_vl, c.POINTER(c.c_float))
        valley_rights = c.cast(array_vr, c.POINTER(c.c_float))

        if valley_stop_index is None:
            valley_stop_index = spectrum.length

        if valley_threshold is None:
            if "mW" in constants.y_units[spectrum.yAxisUnit]:
                valley_threshold = 0.1
            elif "dBm" in constants.y_units[spectrum.yAxisUnit]:
                valley_threshold = -10
            else:
                valley_threshold = 0

        number_of_valleys = FTSLib.FTS_FindValleys(
            c.byref(spectrum),
            valley_start_index,
            valley_stop_index,
            valley_threshold,
            min_valley_depth_db,
            valley_sort_option,
            valley_centers,
            valley_widths,
            valley_heights,
            valley_lefts,
            valley_rights,
            max_valleys,
        )
        logger.debug(f"Number of found valleys: {number_of_valleys}")
        logger.debug(f"Valley centers before check {valley_centers[0:number_of_valleys]}")
        if not valley_centers[0:number_of_valleys]:
            valley_data =  np.array([[-1], [-1], [-1], [-1], [-1]])
            logger.info(f"Latest valleys: {[-1]} {constants.x_units[spectrum.xAxisUnit]}")
        else:
            valley_data = np.array([valley_centers[0:number_of_valleys],
                                    valley_heights[0:number_of_valleys],
                                    valley_widths[0:number_of_valleys],
                                    valley_lefts[0:number_of_valleys],
                                    valley_rights[0:number_of_valleys]])
            logger.info(f"Latest valleys: {valley_centers[0:number_of_valleys]}"
                        f"{constants.x_units[spectrum.xAxisUnit]}")
        return valley_data