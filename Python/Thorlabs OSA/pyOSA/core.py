import os
import time
import typing
import logging
import ctypes as c

from pyOSA.spectrum_t import spectrum_t
from pyOSA.constants import constants
from pyOSA.FTSLib import FTSLib
from pyOSA.instrument import Instrument

logger = logging.getLogger("pyOSA")

# Constants
VIRTUAL_SOURCE_MAX_PEAK_NUM = 64
MAX_TRACEBUFFER_NUM = 64


class FTSTraceData(c.Structure):
    _fields_ = [
        ("trace", c.POINTER(spectrum_t) * MAX_TRACEBUFFER_NUM),
    ]


class core(object):
    """pyOSA core, takes care of instrument parameters,
    initialization of instruments and
    loading/saving of spf2 files
    """


    @staticmethod
    def _allocate_spectrum(
        allocated_length_I: int,
        allocated_length_x: int = 0,
        allocated_length_phi: int = 0,
        allocated_length_log: int = 0,
    ) -> spectrum_t:
        """Allocate an empty spectrum_t with the lengths specified"""
        spectrum = spectrum_t()

        spectrum.allocatedLengthI = allocated_length_I
        array_I = (c.c_float * allocated_length_I)()
        spectrum.I = c.cast(array_I, c.POINTER(c.c_float))

        spectrum.allocatedLengthx = allocated_length_x
        array_x = (c.c_float * allocated_length_x)()
        spectrum.x = c.cast(array_x, c.POINTER(c.c_float))

        spectrum.allocatedLengthPhi = allocated_length_phi
        array_phi = (c.c_float * allocated_length_phi)()
        spectrum.phi = c.cast(array_phi, c.POINTER(c.c_float))

        spectrum.allocatedLengthLog = allocated_length_log
        array_logData = (c.c_byte * allocated_length_log)()
        spectrum.logData = c.cast(array_logData, c.c_void_p)

        return spectrum

    @staticmethod
    def load_spf2_file(filename: str) -> typing.List[spectrum_t]:
        """Loads an spf2 file containing spectra or interferograms.

        Parameters:
            filename (str): The filename, including path, to the file to load.

        Returns:
            list of spectrum_t: A list of spectra if filename is given.
        """
        if not os.path.exists(filename):
            raise Exception("File does not exist")
        if not filename.endswith(".spf2"):
            raise Exception("Filename is not .spf2")

        filename_utf8 = filename.encode("utf-8")
        number_of_acquisitions = core._count_acquisitions_in_file(filename_utf8)
        if number_of_acquisitions < 1:
            raise Exception("No acquistions in file")

        core._allocate_phi_x_arrays(number_of_acquisitions)
        array_traces = core._get_array_traces()
        spec_list = core._read_spectrum(
            filename_utf8, number_of_acquisitions, array_traces
        )
        # Clear the data in the FTSTraceData struct, since it is allocated in the DLL, not Python
        core._clear_fts_traces(number_of_acquisitions)
        return spec_list

    @staticmethod
    def _count_acquisitions_in_file(filename_utf8: bytes):
        """
        Count number of acquisitions in file
        """
        FTSLib.FTS_CountSpectraInFile.argtypes = (c.c_char_p,)
        number_of_acquisitions = FTSLib.FTS_CountSpectraInFile(c.c_char_p(filename_utf8))
        return number_of_acquisitions

    @staticmethod
    def _get_array_traces():
        """
        Helper method to get array traces, used when loading data
        """
        FTSLib.FTS_GetFTSTraceData.restype = c.POINTER(FTSTraceData)
        pointer_trace_data = FTSLib.FTS_GetFTSTraceData()
        trace_data = pointer_trace_data.contents
        array_traces = trace_data.trace
        return array_traces

    @staticmethod
    def _read_spectrum(
        filename_utf8: bytes, number_of_acquisitions: int, array_traces
    ):
        """
        Helper method when loading .spf2 file, reads, loads, copies, spectra
        """
        FTSLib.FTS_ReadSpectrum.argtypes = (c.POINTER(spectrum_t), c.c_char_p)
        FTSLib.FTS_ReadSpectrum_indexed.argtypes = (
            c.POINTER(spectrum_t),
            c.c_char_p,
            c.c_uint,
        )
        FTSLib.FTS_CopySpectrum.argtypes = (c.POINTER(spectrum_t), c.POINTER(spectrum_t))
        spec_list = []
        for index_to_read in range(number_of_acquisitions):
            # TODO: Maybe switch to FTS_ReadSpectra when FTSLib is updated
            status = FTSLib.FTS_ReadSpectrum_indexed(
                array_traces[index_to_read], c.c_char_p(filename_utf8), index_to_read
            )
            if status != 0:
                raise Exception("Error reading spectrum from file")
            spec = core._allocate_spectrum(
                allocated_length_I=array_traces[index_to_read].contents.allocatedLengthI,
                allocated_length_x=array_traces[index_to_read].contents.allocatedLengthx,
                allocated_length_phi=array_traces[
                    index_to_read
                ].contents.allocatedLengthPhi,
                allocated_length_log=array_traces[
                    index_to_read
                ].contents.allocatedLengthLog,
            )

            status = FTSLib.FTS_CopySpectrum(spec, array_traces[index_to_read].contents)
            if status != 0:
                raise Exception("Error copying traces when loading file")
            # Two fields are currently not copied correctly; do it manually
            # TODO these can probably be removed, but we have to check,
            # it also depends on the version of ftslib.
            spec.hdrsize = array_traces[index_to_read].contents.hdrsize
            spec.hdrversion = array_traces[index_to_read].contents.hdrversion
            spec_list.append(spec)
            logger.debug(f"Reading spectra {constants.err_msg(status)}")
        return spec_list

    @staticmethod
    def _allocate_phi_x_arrays(number_of_acquisitions: int):
        """
        Helper function to allocating arrays when loading file
        """
        buffer_length = c.c_uint(10000)
        FTSLib.FTS_Trace_Allocate.argtypes = (c.c_uint, c.c_uint, c.c_bool)
        for trace_index in range(number_of_acquisitions):
            # Since we do not know whether the x and phi array are used or not,
            # we need to allocate space for them to avoid a potential crash
            allocate_x_array = True
            status = FTSLib.FTS_Trace_Allocate(
                trace_index, buffer_length, c.c_bool(allocate_x_array)
            )
            if status != 0:
                raise Exception("Error loading file")
            logger.debug(f"Allocating trace buffer {constants.err_msg(status)}")
            allocate_phi_array = True
            status = FTSLib.FTS_Trace_Resize(
                trace_index,
                buffer_length,
                c.c_bool(allocate_x_array),
                c.c_bool(allocate_phi_array),
            )
            if status != 0:
                raise Exception("Error loading file")
            logger.debug(
                "Allocating phi array to trace buffer " f"{constants.err_msg(status)}"
            )

    @staticmethod
    def _clear_fts_traces(number_of_acquisitions):
        """
        Helper method for clearing ftstraces in ftslib, used when loading spf2file
        """
        for trace_index in range(number_of_acquisitions):
            status = FTSLib.FTS_Trace_Clear(trace_index)
            if status != 0:
                raise Exception(
                    f"Couldn't clear fts trace. Status: " f"{constants.err_msg(status)}"
                )
            logger.debug("Clearing trace buffer " f"{constants.err_msg(status)}")

    @staticmethod
    def save_spf2_file(
        specs: typing.Union[spectrum_t, typing.List[spectrum_t], typing.Dict[str, spectrum_t]], filename: str
    ):
        """Saves a list of spectra/interferograms, or one single spectrum/interferogram, to file.

        Inputs:
            specs (List(spectrum_t) | spectrum_t): List of spectrum_t structs to save, or a single spectrum_t
            filename (String): Full file path with file name
        """
        FILEFORMAT = 2  # SPF2
        if isinstance(specs, spectrum_t):
            core._write_spectrum_to_spf2(specs, filename, FILEFORMAT)
        elif isinstance(specs, list):
            core._write_spectra_to_spf2(specs, filename, FILEFORMAT)
        elif isinstance(specs, dict):
            speclist = list(specs.values())
            core._write_spectra_to_spf2(speclist, filename, FILEFORMAT)
        else:
            raise TypeError("Invalid parameter in save spf2")

    @staticmethod
    def _write_spectrum_to_spf2(spec: spectrum_t, filename: str, FILEFORMAT: int):
        """
        Write single spectrum/interferogram to a file
        """
        filename_bytes = filename.encode("utf-8")
        FTSLib.FTS_WriteSpectrum.argtypes = (c.POINTER(spectrum_t), c.c_char_p, c.c_int)
        status = FTSLib.FTS_WriteSpectrum(
            c.byref(spec), c.c_char_p(filename_bytes), FILEFORMAT
        )
        logger.info(f"Writing single spectrum/interferogram to file {filename}")
        if status != 0:
            raise Exception("Error saving: {}".format(constants.err_msg(status)))

    @staticmethod
    def _write_spectra_to_spf2(
        specs: typing.List[spectrum_t], filename: str, FILEFORMAT: int
    ):
        """
        Write multiple spectra/interferograms to a file
        """
        # MAX_SPECTRA_PER_FILE = 256
        FTSLib.FTS_WriteSpectra.argtypes = (
            c.POINTER(c.POINTER(spectrum_t)),
            c.c_uint,
            c.c_char_p,
            c.c_int,
        )
        filename_bytes = filename.encode("utf-8")
        number_of_acquisitions = len(specs)
        spec_array = (c.POINTER(spectrum_t) * number_of_acquisitions)()
        for i, spec in enumerate(specs):
            if not isinstance(spec, spectrum_t):
                raise TypeError("Invalid input to save spf2, list in not of spectrum_t")
            spec_array[i] = c.pointer(spec)
        status = FTSLib.FTS_WriteSpectra(
            spec_array, number_of_acquisitions, c.c_char_p(filename_bytes), FILEFORMAT
        )
        logger.info(f"Writing spectra/interferograms to file {filename}")
        if status != 0:
            raise Exception("Error saving: {}".format(constants.err_msg(status)))

    ####CALLBACK FUNCTIONS####
    @staticmethod
    def __init_callback(
        spectrometer_index: int,
        channel_index,
        status_code: int,
        unused,
        type_of_status: int,
        message: bytes,
    ) -> int:
        """The callback function takes six parameters:
        spectrometer_index: the index of the spectrometer
        channel_index: the index of the channel, but not used
        status_code: e.g. FTS_SUCCESS, see FTSErrorCodes.h
        unused: unused
        type_of_status: e.g. FTS_ERROR_FLAG
        message: a message for the user
        """
        logger.debug(
            "Init callback!\n spectrometer_index, channel_index, status_code, unused, type_of_status, message: "
            " {} {} {} {} {} {}".format(
                spectrometer_index,
                channel_index,
                status_code,
                unused,
                type_of_status,
                c.string_at(message).decode("utf-8"),
            )
        )
        return 0

    @classmethod
    def initialize(cls, virtual_nr: int = 0, multiple: bool= False
                   ) -> typing.Union["Instrument", typing.List["Instrument"]]:
        """Initializes and opens a connection to a single or all OSAs connected to the system.

        Parameters:
            virtual_nr (int, default 0): Indicates how many virtual machines are in use.
                        Note that virtual and real machines can't be used concurrently.
            multiple (bool, default False): If True, initializes connections to all available
                        OSAs. If False, initializes connection to a single OSA.

        Returns:
            Union[Instrument, List[Instrument]]: Either a single OSA_instrument instance or
                        a list of OSA_instrument instances opened and initialized.
        """
        init_callback_format = c.WINFUNCTYPE(c.c_void_p, c.c_ushort, c.c_uint, c.c_uint)
        CALLBACK_INIT = init_callback_format(core.__init_callback)

        OSAs = []
        virtual = False
        if virtual_nr > 0:
            virtual = True
            nr_of_spectrometers = virtual_nr
        if virtual_nr > 1:
            multiple = True

        if not virtual:
            nr_of_spectrometers = FTSLib.FTS_InitializeSpectrometers(CALLBACK_INIT)
            logger.info(f"Nr of spectrometers found: {nr_of_spectrometers}")
            if nr_of_spectrometers == 0:
                raise Exception("No OSA found")
        
        if not multiple and nr_of_spectrometers > 1:
            raise Exception("There are multiple OSAs connected to the system"
                            "Please use multiple=True when initializing")

        for spectrometer_index in range(nr_of_spectrometers):
            try:
                FTSLib.FTS_CloseSpectrometer(spectrometer_index)
            except Exception as e:
                logger.debug(f"Closing spectrometers: {e}")

            status = FTSLib.FTS_OpenSpectrometer(spectrometer_index)
            logger.info(f"Opened spectrometer {spectrometer_index}")
            if status != 0:
                raise Exception(constants.err_msg(status))
            time.sleep(0.1)
            current_OSA = cls._instrument_creator(spectrometer_index, virtual=virtual)

            if not virtual:
                # Virtual OSAs always give error
                current_OSA._check_spectrometer(spectrometer_index,
                                                ignore_errors=["Reference Warmup"])
            OSAs.append(current_OSA)
        
        if not multiple:
            return OSAs[0]
        else:
            return OSAs

    @staticmethod
    def _instrument_creator(*args, **kwargs):
        """Helper class for when OSA_instrument is subclassed"""
        return Instrument(*args, **kwargs)

    @staticmethod
    def close(osa: "Instrument"):
        """Closes the connection to the OSA.

        Parameters:
            osa (Instrument): The OSA instrument to close the connection for.

        Raises:
            RuntimeError: If an error occurs while closing the connection.

        """
        c_spectrometer_index = c.c_ushort(osa.spectrometer_index)
        status = FTSLib.FTS_CloseSpectrometer(c_spectrometer_index)
        if status != 0:
            raise RuntimeError(
                "FTS_CloseSpectrometer. Status: " f"{constants.err_msg(status)}"
            )
        logger.info(
            f"OSA connection to spectrometer {osa.spectrometer_index} "
            f"closed{constants.err_msg(status)}"
        )

    # Struct needed to define virtual source for OSA20x
    class __virtual_source_parameter(c.Structure):
        _fields_ = [
            ("peakNum", c.c_uint),
            ("centerWavelength_nm", c.c_double * VIRTUAL_SOURCE_MAX_PEAK_NUM),
            ("fwhm_nm", c.c_double * VIRTUAL_SOURCE_MAX_PEAK_NUM),
            ("peakAmplitude", c.c_double * VIRTUAL_SOURCE_MAX_PEAK_NUM),
        ]

    @staticmethod
    def create_virtual_OSA20X(
        spectrometer_index: int,
        model: str,
        source_type: int,
        peak_num: int,
        centerWavelengths_nm: typing.List[float],
        FWHMs_nm: typing.List[float],
        peak_amplitudes: typing.List[float],
    ) -> None:
        """Creates a virtual OSA20X instrument with a specified virtual source.

        Inputs:
            spectrometer_index (int): Spectrometer index of the created instrument
            model (String): String specifying instrument model, eg 'OSA201C', 'OSA203B'...
            source_type (int): Either monochromatic (0) or broadband (1)
            peak_num (int): Number of peaks, must be less than VIRTUAL_SOURCE_MAX_PEAK_NUM
            centerWavelengths_nm (list(doubles)): List of center wavelengths, peak_num elements
            FWHMs_nm (list(doubles)): List of Full Width at Half Maximum for each peak, peak_num elements
            peak_amplitudes (list(doubles)): List of each peak's amplitude in mW, peak_num elements
        """
        if peak_num > VIRTUAL_SOURCE_MAX_PEAK_NUM:
            raise ValueError(
                f"ERROR: Too many peaks (peakNum = {peak_num} > "
                f" max peaks = {VIRTUAL_SOURCE_MAX_PEAK_NUM})"
            )
        if len(centerWavelengths_nm) > peak_num:
            raise ValueError("ERROR: centerWavelengths_nm has more values than peakNum")
        if len(FWHMs_nm) > peak_num:
            raise ValueError("ERROR: FWHMs_nm has more values than peakNum")
        if len(peak_amplitudes) > peak_num:
            raise ValueError("ERROR: peak_amplitudes has more values than peakNum")

        logger.info("Creating a virtual spectrometer...")
        model = model.upper()
        c_model = c.c_ushort(constants.data_defines["INSTRUMENT_VIRTUAL_" + model])
        status = FTSLib.FTS_CreateVirtualSpectrometer(spectrometer_index, c_model)
        if status != 0:
            raise VirtualOSAException("Error creating virtual spectrometer!")

        array_init = c.c_double * VIRTUAL_SOURCE_MAX_PEAK_NUM
        cwl = array_init(*centerWavelengths_nm)
        fwh = array_init(*FWHMs_nm)
        pa = array_init(*peak_amplitudes)
        vsp = core.__virtual_source_parameter(peak_num, cwl, fwh, pa)

        logger.info("Creating a virtual source...")
        status = FTSLib.FTS_SetupVirtualSource(spectrometer_index, source_type, c.byref(vsp))
        if status != 0:
            raise VirtualOSAException("Error creating virtual source!")

    @staticmethod
    def create_virtual_Redstone(spectrometer_index: int, model: str, source_type: int) -> None:
        """Creates OSA30X Redstone virtual instrument.

        Inputs:
            spectrometer_index (int): Spectrometer index of the created instrument
            model (String): String specifying instrument model, eg 'REDSTONE305'
            source_type (int): Indicates what virtual source is created:
                0: Laser emitting at 1530 nm
                1: Superluminescent diode (SLD) with center wavelength at 1550 nm
                2: Laser emitting at 4600 nm
                3: Blackbody with a temperature of 1500 K
        """
        logger.info("Creating a virtual spectrometer...")
        c_spectrometer_index = c.c_ushort(spectrometer_index)
        c_source_type = c.c_ushort(source_type)
        model = model.upper()
        c_model = c.c_ushort(constants.data_defines["INSTRUMENT_VIRTUAL_" + model])

        status = FTSLib.FTS_CreateVirtualSpectrometer(c_spectrometer_index, c_model)
        if status != 0:
            raise VirtualOSAException(
                "Error creating virtual spectrometer! " f"{constants.err_msg(status)}"
            )
        logger.info("Creating a virtual source...")
        status = FTSLib.FTS_SetupVirtualRedstoneSource(c_spectrometer_index, c_source_type)
        if status != 0:
            raise VirtualOSAException(
                f"Error creating virtual spectrometer! {constants.err_msg(status)}"
            )

class VirtualOSAException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return f"VirtualOSAException: {self.message}"
