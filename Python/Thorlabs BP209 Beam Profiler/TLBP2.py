import os
import enum
from ctypes import cdll,c_long,c_uint32,c_uint16,c_uint8,byref,create_string_buffer,c_bool, c_char, c_char_p,c_int,c_int16,c_int8,c_double,c_float,sizeof,c_voidp, Structure

_VI_ERROR = (-2147483647-1)
VI_ON = 1
VI_OFF = 0
BP2_VI_FIND_RSC_PATTERN = ("USB?*?{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x8019}")  # < resource pattern for the Visa resource manager function 'viFindRsrc()'
BP2_MAX_DEVICE_COUNT = (10)  # < maximal count of BP2 instrument that can be connected
BP2_MAX_AD_VALUE = (0x7AFF)  # < highest intensity value of a sample
BP2_STATUS_SCAN_AVAILABLE = (0x0001)  # < A scan is available to read over USB.
BP2_STATUS_DRUM_STABILIZED = (0x0002)  # < The drum has been stabilized and the measurement can be used.
BP2_STATUS_DRUM_DESTABILIZED = (0x0004)  # < The drum has been destabilized and the measurement shoukd be rejected.
VI_INSTR_WARNING_OFFSET = (0x3FFC0900 )
VI_INSTR_ERROR_OFFSET = (_VI_ERROR + 0x3FFC0900 )  # xBFFC0900
BP2_ERR_NO_NEW_DATA = (VI_INSTR_ERROR_OFFSET + 0x00)  # < No new scan is available
BP2_ERR_INV_INSTR_DATA = (VI_INSTR_ERROR_OFFSET + 0x01)  # < The internal data is not initialized
BP2_ERR_INV_OBJECT = (VI_INSTR_ERROR_OFFSET + 0x02)  # < One parameter is not initialized
BP2_ERR_PARAMETER_OUT_OF_RANGE = (VI_INSTR_ERROR_OFFSET + 0x03)  # < One parameter is out of range
BP2_ERR_INV_CONSTR_COUNTER = (VI_INSTR_ERROR_OFFSET + 0x04)  # < The construction counter is not initialized
BP2_ERR_INV_ELAPSED_COUNTER = (VI_INSTR_ERROR_OFFSET + 0x05)  # < The elapsed time could not be measured because no scan has been finished.
BP2_ERR_INV_DATA_SIZE = (VI_INSTR_ERROR_OFFSET + 0x06)  # < The requested data does not match with the received data
BP2_ERR_NSUP_STATE = (VI_INSTR_ERROR_OFFSET + 0x07)  # < The device is not in the correct mode to support this operation
BP2_ERR_SLIT_UNUSED = (VI_INSTR_ERROR_OFFSET + 0x08)  # < The slit is not used
BP2_ERR_NO_PEAK_FOUND = (VI_INSTR_ERROR_OFFSET + 0x09)  # < No valid peak was found
BP2_ERR_NO_VALID_WIDTH = (VI_INSTR_ERROR_OFFSET + 0xA0)  # < No valid beam width was found
BP2_ERR_NO_VALID_CENTROID = (VI_INSTR_ERROR_OFFSET + 0xA1)  # < No valid centroid was found
BP2_ERR_NO_VALID_CALIBRATION = (VI_INSTR_ERROR_OFFSET + 0xA2)  # < No valid calibration found
BP2_WARN_NO_BEAM_WIDTH_CLIPX = (VI_INSTR_WARNING_OFFSET + 0x01)  # < Invalid beam width x
BP2_WARN_NO_BEAM_WIDTH_CLIPY = (VI_INSTR_WARNING_OFFSET + 0x02)  # < Invalid beam width y
BP2_WARN_UNKNOWN_ERROR = (VI_INSTR_WARNING_OFFSET + 0x03)  # < The error code is unknown
BP2_WARN_PARAMETER_OUT_OF_RANGE = (VI_INSTR_WARNING_OFFSET + 0x04)  # < The used wavelength/FWBias is out of the response range
BP2_BASELINE_MODE_DARK_WINDOW = (0)  # < The base line is the mean intensity of the dark window
BP2_BASELINE_MODE_FIRST_SAMPLES = (1)  # < The base line is the mean intensity of the first 10 samples of the slit window
BP2_BASELINE_MODE_USER_VALUE = (2)  # < The base line value is given by the user
BP2_AVERAGE_MODE_ROLLING = (0)  # < Holds x buffers in the background and calculates the average on the last x buffer
BP2_AVERAGE_MODE_FLOATING = (1)  # < Multiplies the last sample intensities by x - 1, add the new intensities and divide by x to get the average
BP2_REFERENCE_POSITION_PRESET_SENSOR_CENTER = (0)  # < The reference position is the center of the sensor
BP2_REFERENCE_POSITION_PRESET_ROI_CENTER = (1)  # < The reference position is the center of the defined roi
BP2_REFERENCE_POSITION_PRESET_PEAK_POSITION = (2)  # < The reference position is the calculated peak position. The peak position is the origin of the position coordinate system (0,0)
BP2_REFERENCE_POSITION_PRESET_CENTROID_POSITION = (3)  # < The reference position is the calculated centroid position. The centroid position is the origin of the position coordinate system (0,0)
BP2_REFERENCE_POSITION_PRESET_USER_POSITION = (4)  # < The reference position is a user defined position within the sensor dimensions

class BP2_RECONSTRUCTION_MODE(enum.Enum):
	BP2_Slit_Scanning = 0  # < The beam width is wider than four times the slit width -> the samples are slit scanned
	BP2_Knife_Edge_Scanning = 1  # < The beam width is smaller than the slit width -> the intensities are the integrated profile

class BP2_DEVICE(Structure):
	_fields_ = [
		("resourceString", (c_char * 256)),  # < unique resource string of the pattern "USB0::0x1313::0x8019::Mxxxxxxxx::RAW"
	]

class BP2_SLIT_DATA(Structure):
	_fields_ = [
		("slit_sample_count", c_uint16),  # < count of samples for this slit (maximal 7500)
		("slit_dark_level", c_float),  # < calculated dark level of the dark window for this slit
		("slit_samples_intensities", (c_float * (7500))), # < array of the sample intensities in digits in the range from -darkLevel to BP2_MAX_AD_VALUE with dark level correction
		("slit_samples_positions", (c_float * (7500))), # < position of the sample in �m to the first sample
		("encoder_increments", c_uint16),  # < count of encoder increments inside the slit window (ca. 130); used to set the correct A/D frequency to cover the slit with the measurement
	]

class BP2_CALCULATIONS(Structure):
	_fields_ = [
		("isValid", c_int16),  # < Are all parameter calculated correctly?
		("peakIndex", c_uint16),  # < Index of the sample in the intensity array that contains the peak
		("peakPosition", c_float),  # < Position of highest intensity in the profile in �m
		("peakIntensity", c_float),  # < Profile intensity in percent (range measured from the dark level to the upper value of the AD converter)
		("centroidIndex", c_uint16),  # < Index of the sample that is nearest to the centroid position
		("centroidPosition", c_float),  # < Calculated centroid position in �m
		("beamWidthClip", c_float),  # < Beam width in �m measured from the peak to the clip level left and right
		("gaussianFitAmplitude", c_float),  # < Highest intensity value of the gaussian fit in digits (with dark level correction)
		("gaussianFitCentroid", c_float),  # < Position of the centroid of the gaussian fit in �m
		("gaussianFitDiameter", c_float),  # < Diameter of the gaussian fit in �m
		("gaussianFitPercentage", c_float),  # < Percentage of the conformity of the measured profile with the gaussian fit curve
		("gaussianFitCurve", (c_float * (7500))), # < Array of calculated intensities of the gaussian fit curve (with dark level correction)
		("besselFitPercentage", c_float),  # < Percentage of the conformity of the measured profile with the bessel fit curve
		("besselFitCurve", (c_float * (7500))), # < Array of calculated intensities of the bessel fit curve (with dark level correction)
		("sigma", c_float),  # < Calculated sigma value of the profile
		("calcAreaLeftBorder", c_float),  # < left border in �m either automatically calculated or set by user
		("calcAreaRightBorder", c_float),  # < right border in �m either automatically calculated or set by user
	]


class TLBP2:

	def __init__(self):
		if sizeof(c_voidp) == 4:
			self.dll = cdll.LoadLibrary("TLBP2_32.dll")
		else:
			self.dll = cdll.LoadLibrary("TLBP2_64.dll")

		self.devSession = c_long()
		self.devSession.value = 0

	def __testForError(self, status):
		if status < 0:
			self.__throwError(status)
		return status

	def __throwError(self, code):
		msg = create_string_buffer(1024)
		self.dll.TLBP2_error_message(self.devSession, c_int(code), msg)
		raise NameError(c_char_p(msg.raw).value)

	def get_connected_devices(self, device_list, device_count):
		"""
		Gets a list of connected devices.
		If this function is called with the parameter "Device_List" as VI_NULL, the function just returns the Device_Count.
		The Device_List has to be initialized with Device_Count elements.
		
		ViUInt32 deviceCount;
		ViStatus err = TLBP2_get_connected_deviced(vi, VI_NULL, &deviceCount);
		
		BP2_DEVICE* deviceList = (BP2_DEVICE*) malloc(sizeof(BP2_DEVICE)*deviceCount);
		err = TLBP2_get_connected_deviced(vi, deviceList, &deviceCount);
		
		...
		
		free(deviceList);
		
		Args:
			device_list( (BP2_DEVICE * arrayLength)()) : The initialized list of BP2_DEVICE is filled with the information of the connected devices. If the parameter is VI_NULL, the parameter will be ignored. The list has to be initialized with the number of elements that is given by the Device_Count parameter. Maximal BP2_MAX_DEVICE_COUNT (10) devices can be connected.
			device_count(c_uint32 use with byref) : Returns the number of connected devices.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_connected_devices(self.devSession, device_list, device_count)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def open(self, resourceName, IDQuery, resetDevice):
		"""
		This function initializes the instrument driver session and performs the following initialization actions:
		
		(1) Opens a session to the Default Resource Manager resource and a session to the selected device using the Resource Name.
		(2) Performs an identification query on the Instrument.
		(3) Resets the instrument to a known state.
		(4) Sends initialization commands to the instrument.
		(5) Returns an instrument handle which is used to differentiate between different sessions of this instrument driver.
		
		Notes:
		(1) Each time this function is invoked an unique session is opened. 
		
		
		The instrument starts with these parameter:
		
		Drum circum             DRUM_CIRCUM
		Clip Level:             13.5%
		Average mode:           floating
		Average count:          1 ( = no averaging; every scan is used)
		Base line mode:         BP2_BASELINE_MODE_DARK_WINDOW (base line is the mean intentsity of the dark window)
		Beam width correction:  active
		Max hold:               inactive
		Auto gain:              inactive
		Wavelength:             minimum wavelength the instrument supports
		ROI:                    not used ( the scan window is 9mm)
		Reference Position      BP2_REFERENCE_POSITION_PRESET_SENSOR_CENTER
		Drum speed:             0 Hz
		Speed Correction        inactive
		Power sample count:     2128
		
		If the parameter "Reset Device" is set to VI_TRUE then these parameter are changed:
		Drum speed:     6 Hz
		Auto gain:      active
		
		For each slit these parameter are resetted:
		Scanning Method         BP2_Slit_Scanning
		Base Line Mode          BP2_BASELINE_MODE_DARK_WINDOW
		Base Line Value         0
		Beam Width Correction   active 
		Sample count            7500
		Gain:                   1
		Samples frequency:      2 MHz
		Bandwidth:              111 kHz
		
		all other parameter are read out of the instrument:
		
		default user power factor: 1
		
		Length Slit 1: 9mm
		Length Slit 2: 9mm
		Length Slit 3: 9mm
		Length Slit 4: 9mm
		Width Slit 1: 25µm
		Width Slit 2: 25µm
		Width Slit 3: 5µm
		Width Slit 4: 5µm
		Orientation Slit 1: X
		Orientation Slit 2: Y
		Orientation Slit 3: X
		Orientation Slit 4: Y
		
		
		Args:
			resourceName (create_string_buffer)
			IDQuery (c_bool):Performs an In-System Verification.
			Checks if the resource matches the BP2 vendor and product id.
			resetDevice (c_bool):Performs Reset operation and places the instrument in a pre-defined reset state.
		Returns:
			int: The return value, 0 is for success
		"""
		self.dll.TLBP2_close(self.devSession)
		self.devSession.value = 0
		pInvokeResult = self.dll.TLBP2_init(resourceName, IDQuery, resetDevice, byref(self.devSession))
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def close(self):
		"""
		Terminates the software connection to the instrument and deallocates system resources associated with that instrument.
		
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_close(self.devSession)
		return pInvokeResult

	def reset(self):
		"""
		Places the instrument in a default state.
		These parameter are resetted:
		
		- Drum speed         = 6 Hz
		- Auto Gain          = active.
		- Drum circum        = DRUM_CIRCUM
		- Clip Level         = 13.5%
		- Averaging          = inactive (set mode to floating and count to 1)
		- Max Hold           = inactive
		- Speed Correction   = inactive
		- Reference Position = BP2_REFERENCE_POSITION_PRESET_SENSOR_CENTER
		
		For each slit these parameter are resetted:
		- Scanning Method       = BP2_Slit_Scanning
		- Base Line Mode        = BP2_BASELINE_MODE_DARK_WINDOW
		- Base Line Value       = 0
		- Beam Width Correction = active
		
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_reset(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def self_test(self, test_result, test_message):
		"""
		This function causes the instrument to perform a self-test and returns the result of that self-test.
		
		Args:
			test_result(c_int16 use with byref) : Numeric result from self-test operation 
			0 = no error (test passed).
			test_message(create_string_buffer(1024)) : Self-test status message.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_self_test(self.devSession, test_result, test_message)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def revision_query(self, driver_rev, instr_rev):
		"""
		This function returns the revision of the instrument driver and the firmware revision of the instrument being used.
		
		Args:
			driver_rev(create_string_buffer(1024)) : Instrument driver revision.
			instr_rev(create_string_buffer(1024)) : Instrument firmware revision.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_revision_query(self.devSession, driver_rev, instr_rev)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def error_query(self, error_code, error_message):
		"""
		This function queries the instrument and returns instrument-specific error information.
		
		Args:
			error_code(c_int use with byref) : Instrument error code returned by driver functions.
			error_message(create_string_buffer(1024)) : Error message.
			The message buffer has to be intialized with 256 bytes.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_error_query(self.devSession, error_code, error_message)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def error_message(self, status_code, message):
		"""
		This function translates the error return value from a VXIplug&play instrument driver function to a user-readable string.
		
		Args:
			status_code(ViStatus) : Instrument driver error code.
			message(create_string_buffer(1024)) : VISA or instrument driver Error message.
			The message buffer has to be initalized with 256 bytes.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_error_message(self.devSession, status_code, message)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_service_mode(self, password):
		"""
		The protected service functions have to be enabled with this function.
		Please enter the access code to enable all the service functions.
		For users of the instrument who need some of the functions may find the corresponding function in the tree "Configuration Functions".
		
		Args:
			password(c_uint8) : Password to enable the service functions.
			The password is only used for Thorlabs internal production and is not available for customers.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_service_mode(self.devSession, password)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_instrument_name(self, instrument_name):
		"""
		Get the model name of the slit beam profiler (e.g. "BP209-VIS").
		
		Args:
			instrument_name(create_string_buffer(1024)) : To get the instrument name the name buffer has to be initialized with 256 bytes and will be filled with the instrument name by this function.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_instrument_name(self.devSession, instrument_name)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_instrument_name(self, instrument_name):
		"""
		Sets the instrument name. The service mode has to be enabled to use this function.
		
		Args:
			instrument_name(create_string_buffer(1024)) : Instrument name with a maximal length of 10 characters.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_instrument_name(self.devSession, instrument_name)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_serial_number(self, serial_number):
		"""
		Gets the serial number from the instrument.
		
		Args:
			serial_number(create_string_buffer(1024)) : Serial number of the instrument.
			The buffer for the serial number has to be initialized with 256 bytes.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_serial_number(self.devSession, serial_number)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_serial_number(self, serial_number):
		"""
		Sets the serial number in ASCII format. (e.g. M00123456).
		Format of the serial number: M + eight numerics + ''
		
		The service mode has to be enabled to use this function.
		
		Args:
			serial_number(create_string_buffer(1024)) : Sets the serial number.
			Maximal 10 Bytes: 9 characters + ''.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_serial_number(self.devSession, serial_number)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_elapsed_time_counter(self, years, months, days, hours, minutes):
		"""
		Gets the duration of the use of the device.
		The elapsed time is separated into Years, Months, Days, Hours and Minutes.
		
		Args:
			years(ViPUInt16 use with byref) : Get the elapsed years.
			months(ViPUInt8 use with byref) : Get the elapsed months.
			days(ViPUInt8 use with byref) : Get the elapsed days.
			hours(ViPUInt8 use with byref) : Get the elapsed hours.
			minutes(ViPUInt8 use with byref) : Get the elapsed minutes.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_elapsed_time_counter(self.devSession, years, months, days, hours, minutes)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def update_elapsed_time_counter(self):
		"""
		Updates the elapsed time in the device.
		Should be set periodically but not more than every 10 Minutes to protect the EEPROM of the device.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_update_elapsed_time_counter(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_cpld_version(self, cpld_version):
		"""
		Gets the version from the cpld inside the instrument.
		The cpld version is written during the upload of the firmware.
		
		Args:
			cpld_version(create_string_buffer(1024)) : Cpld version of the instrument.
			The buffer for the cpld version has to be initialized with minimum 5 bytes.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_cpld_version(self.devSession, cpld_version)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_wavelength_range(self, min_wavelength, max_wavelength):
		"""
		Gets the wavelength range the instruments supports.
		The wavelength range can differ from the instrument model.
		
		Args:
			min_wavelength(ViPUInt16 use with byref) : Lower bound of the wavelength range in nm.
			max_wavelength(ViPUInt16 use with byref) : Upper bound of the wavelength range in nm.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_wavelength_range(self.devSession, min_wavelength, max_wavelength)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_wavelength_range(self, min_wavelength, max_wavelength):
		"""
		Sets the supported wavelength for the instrument in µm.
		The service mode has to be enabled to use this function.
		
		Args:
			min_wavelength(c_uint16) : Minimum wavelength in nm.
			max_wavelength(c_uint16) : Maximum wavelength in nm.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_wavelength_range(self.devSession, min_wavelength, max_wavelength)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_start_offset_range(self, min_offset, max_offset):
		"""
		Gets the start offset range the instruments supports.
		
		
		
		Args:
			min_offset(ViPUInt16 use with byref) : Lower bound of the offset range in digits.
			max_offset(ViPUInt16 use with byref) : Upper bound of the offset range in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_start_offset_range(self.devSession, min_offset, max_offset)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_start_offset(self, offset):
		"""
		Gets the programmed start value of the offset where the instrument starts securely.
		
		Args:
			offset(ViPUInt16 use with byref) : Start Offset in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_start_offset(self.devSession, offset)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_start_offset(self, offset):
		"""
		Sets the start value for the offset where the instrument starts under every conditions.
		The service mode has to be enabled to use this function.
		
		Args:
			offset(c_uint16) : Offset in digits. Maximal 0xFFFF.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_start_offset(self.devSession, offset)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_drum_circum(self, drum_circum):
		"""
		Gets the current operating drum circum in µm/sqrt(2).
		
		Args:
			drum_circum(c_double use with byref) : Drum Circum in µm/sqrt(2).
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_drum_circum(self.devSession, drum_circum)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_drum_circum(self, drum_circum):
		"""
		Sets the current operating drum circum in µm/sqrt(2).
		The service mode has to be enabled to use this function.
		
		Args:
			drum_circum(c_double) : Drum Circum in µm/sqrt(2).
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_drum_circum(self.devSession, drum_circum)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_fwbias_range(self, min_fw_bias, max_fw_bias):
		"""
		Gets the forward bias range the photodiode of the instrument supports.
		
		
		
		Args:
			min_fw_bias(ViPUInt16 use with byref) : Lower bound of the forward bias in digits.
			max_fw_bias(ViPUInt16 use with byref) : Upper bound of the forward bias in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_fwbias_range(self.devSession, min_fw_bias, max_fw_bias)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_fwbias(self, fw_bias):
		"""
		Gets the current operating forward bias.
		
		Args:
			fw_bias(ViPUInt16 use with byref) : Forward bias in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_fwbias(self.devSession, fw_bias)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_fwbias(self, fw_bias):
		"""
		Sets the current operating forward bias in digits.
		
		Args:
			fw_bias(c_uint16) : Forward bias in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_fwbias(self.devSession, fw_bias)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_parameter(self, slit_used, slit_length, slit_width, slit_orientation):
		"""
		Gets the number of slits, the used slits, the slit lengths and widths.
		
		The buffer has to be initialized for maximal BP2_MAX_SLIT_COUNT slits.
		
		Args:
			slit_used( (c_uint8 * arrayLength)()) : Gets the information if the slit is used.
			0 = slit is not available
			1 = slit is usable
			slit_length( (c_uint8 * arrayLength)()) : Get the length in mm of each of the BP2_MAX_SLIT_COUNT slits.
			slit_width( (c_uint8 * arrayLength)()) : Get the width in µm of each of the BP2_MAX_SLIT_COUNT slits.
			slit_orientation( (c_uint8 * arrayLength)()) : Get the orientation of the BP2_MAX_SLIT_COUNT slits.
			0 = X
			1 = Y
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_parameter(self.devSession, slit_used, slit_length, slit_width, slit_orientation)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_slit_parameter(self, slit_used, slit_length, slit_width, slit_orientation):
		"""
		Sets the number of slits, the used slits, the slit lengths and widths.
		Maximal BP2_MAX_SLIT_COUNT slits can be used.
		The service mode has to be enabled to use this function.
		
		Args:
			slit_used( (c_uint8 * arrayLength)()) : Sets if the slit has to be used.
			
			0 = do not use the slit
			1 = the slit can be used.
			slit_length( (c_uint8 * arrayLength)()) : Set the length in mm of each of the BP2_MAX_SLIT_COUNT slits.
			slit_width( (c_uint8 * arrayLength)()) : Set the width in µm of each of the BP2_MAX_SLIT_COUNT slits.
			slit_orientation( (c_uint8 * arrayLength)()) : Set the orientation of the BP2_MAX_SLIT_COUNT slits.
			0 = X
			1 = Y
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_slit_parameter(self.devSession, slit_used, slit_length, slit_width, slit_orientation)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_sensor_response(self, response_data_count, lowest_wavelength, highest_wavelength, wavelength_step, response_data):
		"""
		This function returns the sensitivity curve for the photidiode in combination with the nd filter for the power measurement.
		
		Args:
			response_data_count(ViPUInt8 use with byref) : Get the number of valid data. Maximal 20 data can be returned.
			lowest_wavelength(ViPUInt16 use with byref) : Get the lowest wavelength in nm.
			highest_wavelength(ViPUInt16 use with byref) : Get the highest wavelength in nm.
			wavelength_step(ViPUInt8 use with byref) : Get the step in nm between two data.
			response_data( (c_uint16 * arrayLength)()) : Buffer which contains maximal 20 data.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_sensor_response(self.devSession, response_data_count, lowest_wavelength, highest_wavelength, wavelength_step, response_data)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_sensor_response(self, response_data_count, lowest_wavelength, highest_wavelength, wavelength_step, response_data):
		"""
		Sets sensitivity curve for the photodiode.
		The curve for a VIS model differs from a UV model.
		The service mode has to be enabled to use this function.
		
		Args:
			response_data_count(c_uint8) : Set the number of valid data. Maximal 20 data can be set.
			lowest_wavelength(c_uint16) : Set the lowest wavelength in nm.
			highest_wavelength(c_uint16) : Set the highest wavelength in nm.
			wavelength_step(c_uint8) : Set the step in nm between two data.
			response_data( (c_uint16 * arrayLength)()) : Buffer which contains maximal 20 data.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_sensor_response(self.devSession, response_data_count, lowest_wavelength, highest_wavelength, wavelength_step, response_data)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_construction_parameter(self, constrution_year, constrution_month, constrution_day, assembler_name):
		"""
		Gets the date and name of the construction.
		
		Args:
			constrution_year(ViPUInt8 use with byref) : Year of the construction.
			constrution_month(ViPUInt8 use with byref) : Month of the construction.
			constrution_day(ViPUInt8 use with byref) : Day of the construction.
			assembler_name(create_string_buffer(1024)) : Name of the assembler.
			The buffer can be filled with 8 characters.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_construction_parameter(self.devSession, constrution_year, constrution_month, constrution_day, assembler_name)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_construction_parameter(self, constrution_year, constrution_month, constrution_day, assembler_name):
		"""
		Sets name and date of the construction.
		The service mode has to be enabled to use this function.
		
		Args:
			constrution_year(c_uint8) : Get the number of mounted slits.
			constrution_month(c_uint8) : Get the number of mounted slits.
			constrution_day(c_uint8) : Get the number of mounted slits.
			assembler_name(create_string_buffer(1024)) : Name of the assembler. The buffer can contain up to 8 characters + ''.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_construction_parameter(self.devSession, constrution_year, constrution_month, constrution_day, assembler_name)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_calibration_parameter(self, calibration_year, calibration_month, calibration_day, calibration_firmware, calibration_SW_version, assembler_name):
		"""
		Gets the parameter of the calibration.
		
		Args:
			calibration_year(ViPUInt8 use with byref) : Year of the calibration.
			calibration_month(ViPUInt8 use with byref) : Month of the calibration.
			calibration_day(ViPUInt8 use with byref) : Day of the calibration.
			calibration_firmware(create_string_buffer(1024)) : Minimum size of the firmware buffer is 8 characters.
			calibration_SW_version(create_string_buffer(1024)) : Length of the version buffer minimum 8 characters.
			assembler_name(create_string_buffer(1024)) : Name of the assembler with maximal 8 characters.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_calibration_parameter(self.devSession, calibration_year, calibration_month, calibration_day, calibration_firmware, calibration_SW_version, assembler_name)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_calibration_parameter(self, calibration_year, calibration_month, calibration_day, calibration_firmware, calibration_SW_version, assembler_name):
		"""
		Sets the parameter of the calibration.
		The service mode has to be enabled to use this function.
		
		Args:
			calibration_year(c_uint8) : Year of the calibration.
			calibration_month(c_uint8) : Month of the calibration.
			calibration_day(c_uint8) : Day of the calibration.
			calibration_firmware(create_string_buffer(1024)) : Minimum size of the firmware buffer is 8 characters.
			calibration_SW_version(create_string_buffer(1024)) : Minimum size of the firmware buffer is 8 characters.
			assembler_name(create_string_buffer(1024)) : Name of the assembler with maximal 8 characters.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_calibration_parameter(self.devSession, calibration_year, calibration_month, calibration_day, calibration_firmware, calibration_SW_version, assembler_name)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_position_range(self, min_position, max_position):
		"""
		Gets the position range of the slits.
		
		
		
		Args:
			min_position(ViPUInt16 use with byref) : Lower bound of the slit position in digits.
			max_position(ViPUInt16 use with byref) : Upper bound of the slit position in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_position_range(self.devSession, min_position, max_position)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_positions(self, slit_positions):
		"""
		Gets the current operating positions of the slits.
		
		Args:
			slit_positions( (c_uint16 * arrayLength)()) : Array of positions with maximal MEAS_WINDOW_COUNT entries.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_positions(self.devSession, slit_positions)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_slit_positions(self, slit_positions):
		"""
		Sets the current operating slit positions in digits.
		These values are used until the device is connected. Unplug the device will reset the positions to the last saved values.
		
		Default values:
		
		Slit_Positions[0] = 215; // position of the power window
		Slit_Positions[1] = 482; // position of the power dark window
		        
		Slit_Positions[2] = 632; // position of the first slit
		Slit_Positions[3] = 898; // position of the first dark window
		
		Slit_Positions[4] = 1048;// position of the second slit
		Slit_Positions[5] = 1315;// position of the second dark window
		
		Slit_Positions[6] = 1465;// position of the third slit
				Slit_Positions[7] = 1732;	// position of the third dark window
		
				Slit_Positions[8] = 1882;	// position of the fourth slit
				Slit_Positions[9] = 2149;	// position of the fourth dark window 	
		
		Args:
			slit_positions( (c_uint16 * arrayLength)()) : Array with positions of the slits. Array has MEAS_WINDOW_COUNT entries.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_slit_positions(self.devSession, slit_positions)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def save_slit_positions(self, slit_positions):
		"""
		Sets the current operating slit positions in digits and stores them into the eeprom. 
		The service mode has to be enabled to use this function.
		
		Args:
			slit_positions( (c_uint16 * arrayLength)()) : Array with positions of the slits. Array has MEAS_WINDOW_COUNT entries.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_save_slit_positions(self.devSession, slit_positions)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_positions_roi(self, slit_positions_roi):
		"""
		Gets the current operating positions of the slits in the ROI mode.
		
		Args:
			slit_positions_roi( (c_uint16 * arrayLength)()) : Array of positions with maximal MEAS_WINDOW_COUNT entries.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_positions_roi(self.devSession, slit_positions_roi)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_slit_positions_roi(self, slit_positions_roi):
		"""
		Sets the current operating slit positions in the ROI mode.
		These values are only available until unplugging the instrument.
		
		Args:
			slit_positions_roi( (c_uint16 * arrayLength)()) : Array of ROI positions of the slits with MEAS_WINDOW_COUNT entries.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_slit_positions_roi(self.devSession, slit_positions_roi)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def save_slit_positions_roi(self, slit_positions_roi):
		"""
		Sets the current operating slit positions for the ROI in digits and stores them into the eeprom. 
		The service mode has to be enabled to use this function.
		
		Args:
			slit_positions_roi( (c_uint16 * arrayLength)()) : Array with positions of the ROI slits. Array has MEAS_WINDOW_COUNT entries.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_save_slit_positions_roi(self.devSession, slit_positions_roi)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_motor_dac_range(self, min_dac_value, max_dac_value):
		"""
		Gets the motor dac range the instruments supports.
		
		
		
		Args:
			min_dac_value(ViPUInt16 use with byref) : Lower bound of the motor dac value in digits.
			max_dac_value(ViPUInt16 use with byref) : Upper bound of the motor dac value in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_motor_dac_range(self.devSession, min_dac_value, max_dac_value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_motor_dac(self, motor_dac_value):
		"""
		Gets the current operating motor dac value.
		
		Args:
			motor_dac_value(ViPUInt16 use with byref) : DAC value for the motor.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_motor_dac(self.devSession, motor_dac_value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_motor_dac(self, motor_dac_value):
		"""
		Set the DAC value for the motor.
		
		Args:
			motor_dac_value(c_uint16) : Set the DAC value for the motor.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_motor_dac(self.devSession, motor_dac_value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_motor_dac_5_20hz(self, dac_value_5hz, dac_value_20hz):
		"""
		Gets the current stored DAC value where the drum has a rotation frequency of 5 and 20 Hz.
		
		Args:
			dac_value_5hz(ViPUInt16 use with byref) : Calibrated dac value for a drum rotation of 5 Hz.
			dac_value_20hz(ViPUInt16 use with byref) : Calibrated dac value for a drum rotation of 20 Hz.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_motor_dac_5_20hz(self.devSession, dac_value_5hz, dac_value_20hz)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_motor_dac_5_20hz(self, dac_value_5hz, dac_value_20hz):
		"""
		Sets the DAC value where the drum has a rotation frequency of 5 and 20 Hz.
		The service mode has to be enabled to use this function.
		
		Args:
			dac_value_5hz(c_uint16) : Calibrated dac value where the drum rotates with 5 Hz.
			dac_value_20hz(c_uint16) : Calibrated dac value where the drum rotates with 20Hz.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_motor_dac_5_20hz(self.devSession, dac_value_5hz, dac_value_20hz)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_motor_dac_2_5_20hz(self, dac_value_2hz, dac_value_5hz, dac_value_20hz):
		"""
		Gets the current stored DAC value where the drum has a rotation frequency of 2, 5 and 20 Hz.
		
		Args:
			dac_value_2hz(ViPUInt16 use with byref) : Calibrated dac value for a drum rotation of 2 Hz.
			dac_value_5hz(ViPUInt16 use with byref) : Calibrated dac value for a drum rotation of 5 Hz.
			dac_value_20hz(ViPUInt16 use with byref) : Calibrated dac value for a drum rotation of 20 Hz.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_motor_dac_2_5_20hz(self.devSession, dac_value_2hz, dac_value_5hz, dac_value_20hz)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_motor_dac_2_5_20hz(self, dac_value_20z, dac_value_5hz, dac_value_20hz):
		"""
		Sets the DAC value where the drum has a rotation frequency of 2, 5 and 20 Hz.
		The service mode has to be enabled to use this function.
		
		Args:
			dac_value_20z(c_uint16) : Calibrated dac value where the drum rotates with 2 Hz.
			dac_value_5hz(c_uint16) : Calibrated dac value where the drum rotates with 5 Hz.
			dac_value_20hz(c_uint16) : Calibrated dac value where the drum rotates with 20Hz.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_motor_dac_2_5_20hz(self.devSession, dac_value_20z, dac_value_5hz, dac_value_20hz)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_construction_operating_hours_counter(self, days, hours, minutes):
		"""
		Gets the elapsed time to the last construction date.
		
		Args:
			days(ViPUInt16 use with byref) : Days to the last construction.
			hours(ViPUInt8 use with byref) : Hours to the last construction.
			minutes(ViPUInt8 use with byref) : MInutes to the last construction.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_construction_operating_hours_counter(self.devSession, days, hours, minutes)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_calibration_operating_hours_counter(self, days, hours, minutes):
		"""
		Gets the elapsed time to the last calibration date.
		
		Args:
			days(ViPUInt16 use with byref) : Elapsed days to the last calibration.
			hours(ViPUInt8 use with byref) : Elapsed hours to the last calibration.
			minutes(ViPUInt8 use with byref) : Elapsed minutes to the last calibration.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_calibration_operating_hours_counter(self.devSession, days, hours, minutes)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def reset_calibration_operating_hours_counter(self):
		"""
		Resets the calibration date to the current date.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_reset_calibration_operating_hours_counter(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def reset_construction_operating_hours_counter(self):
		"""
		Resets the construction date to the current date.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_reset_construction_operating_hours_counter(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_power_factor(self, power_factor):
		"""
		Get the Power Correction Factor from the eeprom of the device.
		
		Args:
			power_factor(c_double use with byref) : Get the Power Correction Factor.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_power_factor(self.devSession, power_factor)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_power_factor(self, power_factor):
		"""
		Set the Power Correction Factor and stores the value in the eeprom of the device.
		The service mode needs to be enabled to use this function.
		
		Args:
			power_factor(c_double) : Set the Power Correction Factor.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_power_factor(self.devSession, power_factor)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_device_status(self, device_status):
		"""
		This function queries the status register of the BP2.
		
		
		
		Args:
			device_status(ViPUInt16 use with byref) : This parameter returns the instruments status.
			
			// a new scan is available
			BP2_STATUS_SCAN_AVAILABLE     0x00000001  
			
			// the drum speed has been stabilized 
			BP2_STATUS_DRUM_STABILIZED    0x00000002 
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_device_status(self.devSession, device_status)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_samples_count_range(self, min_sample_count, max_sample_count):
		"""
		Gets the range of sample counts the instrument supports.
		The sample count depends on the drum speed and the sample frequency.
		
		Args:
			min_sample_count(ViPUInt16 use with byref) : Lower bound of the sample count.
			max_sample_count(ViPUInt16 use with byref) : Upper bound of the sample count.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_samples_count_range(self.devSession, min_sample_count, max_sample_count)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_samples_counts(self, sample_count_buffer):
		"""
		Gets the current operating slit sample buffer.
		
		Args:
			sample_count_buffer( (c_uint16 * arrayLength)()) : Buffer which contains the sample count for each slit.
			Size of the buffer is BP2_MAX_SLIT_COUNT * 2 bytes = 8 bytes.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_samples_counts(self.devSession, sample_count_buffer)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_slit_samples_counts(self, sample_count_buffer):
		"""
		Sets the current operating sample count for each slit.
		Setting the sample count may change the sample frequency.
		
		Remark: Using the function "Set Drum Speed Extended" will overwrite the manual set sample count.
		
		Args:
			sample_count_buffer( (c_uint16 * arrayLength)()) : Buffer which contains the sample count for each slit.
			Size of the buffer is BP2_MAX_SLIT_COUNT * 2 bytes = 8 bytes.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_slit_samples_counts(self.devSession, sample_count_buffer)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_samples_frequency_range(self, min_samples_frequency, max_samples_frequency):
		"""
		Gets the sample frequency range the instruments supports in kHz.
		
		
		
		Args:
			min_samples_frequency(c_float use with byref) : Lower bound of the samples frequency in kHz.
			max_samples_frequency(c_float use with byref) : Upper bound of the samples frequency in kHz.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_samples_frequency_range(self.devSession, min_samples_frequency, max_samples_frequency)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_samples_frequencies(self, samples_frequencies_buffer):
		"""
		Gets the current operating samples frequency for each slit in kHz.
		
		Args:
			samples_frequencies_buffer( (c_double * arrayLength)()) : Buffer for the samples frequencies in kHz.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_samples_frequencies(self.devSession, samples_frequencies_buffer)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_slit_samples_frequencies(self, samples_frequencies_buffer):
		"""
		Sets the current operating samples frequency for each slit.
		
		Remark: Using the function "Set Drum Speed Extended" will overwrite the manual set sample count.
		
		Args:
			samples_frequencies_buffer( (c_double * arrayLength)()) : Frequency for the samples of each slit.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_slit_samples_frequencies(self.devSession, samples_frequencies_buffer)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_offset_range(self, minOffset, maxOffset):
		"""
		Gets the offset range to correct the dark level.
		
		
		
		Args:
			minOffset(ViPUInt16 use with byref) : Lower bound of the offset range in digits.
			maxOffset(ViPUInt16 use with byref) : Upper bound of the offset range in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_offset_range(self.devSession, minOffset, maxOffset)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_offsets(self, offset_slits, offset_power):
		"""
		Gets the currently used offset values for the slits.
		
		Args:
			offset_slits( (c_uint16 * arrayLength)()) : Array of offset value for the slits in digits.
			offset_power(ViPUInt16 use with byref) : Offset value for the power window in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_offsets(self.devSession, offset_slits, offset_power)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_offsets(self, offset_slits, offset_power):
		"""
		Sets the currently used offset values for the slits.
		
		Args:
			offset_slits( (c_uint16 * arrayLength)()) : Array of offset value for the slits in digits.
			offset_power(c_uint16) : Array of offset value for the power window in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_offsets(self.devSession, offset_slits, offset_power)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_gain_range(self, min_gain, max_gain):
		"""
		Get the range of the gain the instrument supports.
		
		Args:
			min_gain(ViPUInt8 use with byref) : Lower bound of the gain range.
			max_gain(ViPUInt8 use with byref) : Upper bound of the gain range.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_gain_range(self.devSession, min_gain, max_gain)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_gains(self, gain_buffer, gain_power):
		"""
		Gets the gains for each slit.
		
		Args:
			gain_buffer( (c_uint8 * arrayLength)()) : Buffer of BP2_MAX_SLIT_COUNT elements which contains the gain for each slit.
			gain_power(ViPUInt8 use with byref) : Get the gain for the power window.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_gains(self.devSession, gain_buffer, gain_power)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_gains(self, gain_buffer, gain_power):
		"""
		Set the gains for each slit.
		
		Args:
			gain_buffer( (c_uint8 * arrayLength)()) : Buffer of BP2_MAX_SLIT_COUNT elements which contains the gain for each slit.
			gain_power(c_uint8) : Set the gain for the power window.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_gains(self.devSession, gain_buffer, gain_power)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_auto_gain(self, auto_gain):
		"""
		Gets the automatic calculation of the gain.
		Manual setting of a gain value will fail when auto gain is activated.
		
		Args:
			auto_gain(c_int16 use with byref) : Get the configuration if automatic calculation of the gain is activated.
			VI_ON  = auto gain is active
			VI_OFF = auto gain is inactive
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_auto_gain(self.devSession, auto_gain)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_auto_gain(self, auto_gain):
		"""
		Sets the automatic calculation of the gain.
		The gain will be corrected with every measurement and take effect in the next measurement.
		
		Manual setting of a gain value will fail when auto gain is activated.
		
		Args:
			auto_gain(c_int16) : Set the configuration if automatic calculation of the gain has to be activated.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_auto_gain(self.devSession, auto_gain)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_bandwidth_range(self, min_bandwidth, max_bandwidth):
		"""
		Gets the bandwidth range in kHz the instruments supports.
		
		default: 16.00 to 2500 kHz
		
		Args:
			min_bandwidth(c_double use with byref) : Lower bound of the bandwith range in kHz.
			max_bandwidth(c_double use with byref) : Upper bound of the bandwith range in kHz.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_bandwidth_range(self.devSession, min_bandwidth, max_bandwidth)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_bandwidths(self, bandwidth_buffer):
		"""
		Gets the bandwidth for each slit.
		
		Args:
			bandwidth_buffer( (c_double * arrayLength)()) : Buffer which contains the bandwidth for each of the maximal BP2_MAX_SLIT_COUNT slit.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_bandwidths(self.devSession, bandwidth_buffer)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_bandwidths(self, bandwidth_buffer):
		"""
		Sets the bandwidth for each slit.
		
		Args:
			bandwidth_buffer( (c_double * arrayLength)()) : Buffer which contains the bandwidth for each of the BP2_MAX_SLIT_COUNT slit.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_bandwidths(self.devSession, bandwidth_buffer)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_drum_speed_range(self, min_speed, max_speed):
		"""
		Gets the speed range the instruments supports.
		Default: 2.0 to 20.0 Hz.
		
		Args:
			min_speed(c_double use with byref) : Lower bound of the speed range in drum rotation per second.
			max_speed(c_double use with byref) : Upper bound of the speed range in drum rotation per second.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_drum_speed_range(self.devSession, min_speed, max_speed)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_drum_speed(self, drum_speed):
		"""
		Gets the speed of the drum rotation per second.
		
		Args:
			drum_speed(c_double use with byref) : Speed of the drum in rotation per second.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_drum_speed(self.devSession, drum_speed)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_drum_speed(self, drum_speed):
		"""
		Sets the speed of the drum in rotations per seconds.
		
		To use the full slit length (9mm) for your measurements, adopt the sample count and frequency to the new scan rate.
		
		Set the freqencies with the function "set_samples_frequencies":
		sample_frequency_kHz = (sample_count / 1000) * (get_drum_circum / 1000 / slit_length_mm) *drum_speed_Hz.
		
		sample_frequency_kHz = (7500 / 1000) * ((55800*PI) / sqrt(2.0) / 1000 / 9)*10
		
		For a sample count of 7500 and a scan rate of 10 Hz, the samples frequency is 1033 kHz.
		
		Args:
			drum_speed(c_double) : sets the speed of the drum in rotations per seconds.
			Range of the speed: 0 to 20 U/sec.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_drum_speed(self.devSession, drum_speed)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_drum_speed_ex(self, drum_speed, sample_count, sample_resolution):
		"""
		Sets the speed of the drum in rotations per seconds.
		
		The sample count and freqency is changed automatically.
		
		Args:
			drum_speed(c_double) : sets the speed of the drum in rotations per seconds.
			Range of the speed: 2 to 20 U/sec.
			sample_count(ViPUInt16 use with byref) : Count of samples for a slit.
			sample_resolution(c_double use with byref) : Mean distance in µm between two samples.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_drum_speed_ex(self.devSession, drum_speed, sample_count, sample_resolution)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def add_drum_speed_offset(self, drum_speed_offset):
		"""
		Adds a speed to the current drum speed to correct the motor speed. Please call "Set Drum Speed" to see the effect. With "Clear Drum Offset" the offset can be resetted.
		
		Args:
			drum_speed_offset(c_float) : corrects the speed of the drum in rotations per seconds.
			Range of the correction speed: -3.0 to 3.0 U/sec.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_add_drum_speed_offset(self.devSession, drum_speed_offset)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def clear_drum_speed_offset(self):
		"""
		Clears the drum speed offset. This function is useful if the dum speed has been changed.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_clear_drum_speed_offset(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_speed_correction(self, correction):
		"""
		Gets the automatic correction of the drum speed.
		The target drum speed can be set by the function "set_drum_speed".
		The drum speed will be corrected if the measured drum speed differs from the target drum speed by more than 0.5Hz.
		The drum speed can increase with higher temperature or during longer measurements.
		
		Args:
			correction(c_int16 use with byref) : Get the configuration if automatic correction of the drum speed is activated.
			VI_ON  = auto correction is active
			VI_OFF = auto correction is inactive
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_speed_correction(self.devSession, correction)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_speed_correction(self, correction):
		"""
		With a higher temperature or longer measurements the drum speed can increase. This causes a complession of the beam profile in the calculation results. Then the beam profile may be clipped and the calculation results have false values. To avoid the drift the speed correction can be activated. If the measured drum speed differs from the target drum speed of more than 0.5 Hz the speed will corrected. This has the effect that the centroid moves to a new position if the speed correction is done. The effect depends on the position of the base line and the noise of the signal.
		
		Args:
			correction(c_int16) : Activate the automatic correction of the drum speed.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_speed_correction(self.devSession, correction)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_averaged_drum_speed(self, drum_speed):
		"""
		Gets the speed of the drum rotation per second.
		The drum speed is calculated from the 156 segments of the elapsed time measurement.
		
		Args:
			drum_speed(c_double use with byref) : Speed of the drum in rotation per second.
			The value is the sum of the 156 elapsed times, divided by 156 and multiplied by 156.25. This value is more stable than the "Get Drum Speed" measurement.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_averaged_drum_speed(self.devSession, drum_speed)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_user_power_factor_range(self, min_power_factor, max_power_factor):
		"""
		Gets the range for the power factor.
		
		Args:
			min_power_factor(c_double use with byref) : Lower bound of the power factor.
			max_power_factor(c_double use with byref) : Upper bound of the power factor.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_user_power_factor_range(self.devSession, min_power_factor, max_power_factor)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_user_power_factor(self, power_factor):
		"""
		Get the User Power Correction Factor.
		This factor takes effect on the calculation of the total power.
		Total Power = Measured Power * User Factor.
		
		Args:
			power_factor(c_double use with byref) : Get the Power Correction Factor.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_user_power_factor(self.devSession, power_factor)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_user_power_factor(self, power_factor):
		"""
		Set the User Power Correction Factor.
		This factor takes effect on the calculation of the total power.
		Total Power = Power calculated from the slit measurement * User Factor.
		
		To set the user power factor:
		1. measure the power of your light source with an external power meter
		2. set the user power factor to 1.0 and get the Total Power from the slit measurement.
		3. Calculate the power factor. User power factor = external measured power / slit measured power.
		
		
		Args:
			power_factor(c_double) : Set the Power Correction Factor.
			The power factor can be set in a range from 0.01 to 65.0.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_user_power_factor(self.devSession, power_factor)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_wavelength(self, wavelength):
		"""
		Returns the currently used wavelength in nm.
		
		Args:
			wavelength(c_double use with byref) : Get the currently used wavelength in nm.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_wavelength(self.devSession, wavelength)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_wavelength(self, wavelength):
		"""
		Set the wavelength in nm.
		
		Args:
			wavelength(c_double) : Set the wavelength in nm for calculations.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_wavelength(self.devSession, wavelength)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_use_roi(self, use_roi):
		"""
		Returns if the instrument uses a smaller ROI than the slit aperture.
		
		Args:
			use_roi(c_int16 use with byref) : Get the use of the ROI.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_use_roi(self.devSession, use_roi)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_use_roi(self, use_roi):
		"""
		Activates or deactivates the use of the ROI.
		
		Args:
			use_roi(c_int16) : Sets the use of the ROI on or off.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_use_roi(self.devSession, use_roi)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_averaging(self, average_count, average_mode):
		"""
		Returns the number of scans which are averaged and the used averaging mode.
		
		Args:
			average_count(ViPUInt8 use with byref) : Get the number of scans that are averaged.
			1 = No Averaing
			2... 100 the intensities are summed over the scans and averaged.
			All Calculations are done on the averaged data.
			average_mode(ViPUInt8 use with byref) : Mode how the scans are averaged.
			0 = Rolling Averaging (The average over the last x measurements is calculated)
			1 = Floating Averaging ( The new scan is added to the averaged scans)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_averaging(self.devSession, average_count, average_mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_averaging(self, average_count, average_mode):
		"""
		Sets the number of scans which are averaged and the avaraging mode.
		
		Args:
			average_count(c_uint8) : Set the number of scans that are averaged.
			1 = No Averaing
			2... 100 the intensities are summed over the scans and averaged.
			All Calculations are done on the averaged data.
			average_mode(c_uint8) : Mode how the scans are averaged.
			0 = Rolling Averaging (The last x scans are summed up and averaged)
			1 = Floating Averaging ( The new scan is added to the averaged scans)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_averaging(self.devSession, average_count, average_mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_scanning_method(self, slit_index, scanning_method):
		"""
		Returns the mode of a slit which is used to reconstruct the beam profile.
		
		Args:
			slit_index(c_uint8) : The reconstruction mode of the slit identified by the index.
			Slit index range: 0 to BP2_MAX_SLIT_COUNT - 1
			scanning_method(ViPUInt8 use with byref) : Mode how the scans are reconstructed.
			0 = Slit scanning
			1 = Knife-Edge Mode
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_scanning_method(self.devSession, slit_index, scanning_method)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_scanning_method(self, slit_index, scanning_method):
		"""
		Sets the mode of a slit which is used to reconstruct the beam profile.
		
		Args:
			slit_index(c_uint8) : The reconstruction mode of the slit identified by the index.
			Slit index range: 0 to BP2_MAX_SLIT_COUNT - 1
			scanning_method(c_uint8) : Mode how the scans are reconstructed.
			0 = Slit scanning
			1 = Derivated
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_scanning_method(self.devSession, slit_index, scanning_method)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_clip_level(self, clip_level):
		"""
		Returns the clip level where the calculations are made.
		
		Args:
			clip_level(c_float use with byref) : Clip Level in a range from 0.0 to 1.0.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_clip_level(self.devSession, clip_level)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_clip_level(self, clip_level):
		"""
		Set the clip level where the beam width is calculated.
		
		Args:
			clip_level(c_float) : Set the Clip Level in ragen from 0.0 to 1.0. 0.135 and 0.50 are common values.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_clip_level(self.devSession, clip_level)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_max_hold(self, max_hold):
		"""
		Returns the use of the max hold function for a slit.
		
		Args:
			max_hold(c_int16 use with byref) : Is the max hold mode used?
			ON  = Max hold is active
			OFF = Max hold is inactive
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_max_hold(self.devSession, max_hold)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_max_hold(self, max_hold):
		"""
		Sets if only the maximum values of all scans are used for the calculation.
		
		Args:
			max_hold(c_int16) : Set the Use of Max Hold.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_max_hold(self.devSession, max_hold)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_base_line(self, slit_index, mode, base_line):
		"""
		Set the Auto Base Line Correction if the slit measurement contains a lot of ambient light. This measurement will reduce the influence of the ambient light.
		
		The base line calculated from the dark windows will be placed by the mean of the first 10 samples of the slit measurement.
		Be sure that the beam profile is in the middle of the slit window and only the ambient light is measured within the first 10 samples.
		
		Args:
			slit_index(c_uint8) : Index of the slit.
			mode(ViPUInt8 use with byref) : Returns the mode how the base line is calculated.
			
			Mean of the intensities of the dark window.     (0)
			Mean of the first 10 samples of the slit window (1)
			Fixed user base line value                      (2)
			base_line(c_float use with byref) : Returns the used base line fo the mode 'User Base Level'.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_base_line(self.devSession, slit_index, mode, base_line)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_base_line(self, slit_index, mode, base_line):
		"""
		Sets a digit value for the base line or automatic.
		
		Args:
			slit_index(c_uint8) : Index of the slit.
			mode(c_uint8) : Change the mode how the base line is calculated.
			
			Mean of the intensities of the dark window.     (0)
			Mean of the first 10 samples of the slit window (1)
			Fixed user base line value                      (2)
			
			base_line(c_float) : Manual digit value for the base line. This parameter has to be set if the mode is set to "User Base Level". Fo all other modes, this parameter is ignored.
			
			BaseLine <= 0.1: The base line is calculated automatically from the dark windows.
			
			Base Line > 0.1: The base line from the dark window is replaced by the Base Line value. The Base Line value is up to 65.535 digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_base_line(self.devSession, slit_index, mode, base_line)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_beam_width_correction(self, slit_index, beam_width_correction):
		"""
		Gets a correction for beam width smaller than the slit with.
		
		Args:
			slit_index(c_uint8) : Index of the slit.
			beam_width_correction(c_int16 use with byref) : Enables the correction.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_beam_width_correction(self.devSession, slit_index, beam_width_correction)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_beam_width_correction(self, slit_index, beam_width_correction):
		"""
		Sets a correction for beam width smaller than the slit with.
		
		Args:
			slit_index(c_uint8) : Index of the slit.
			beam_width_correction(c_int16) : Enables the correction.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_beam_width_correction(self.devSession, slit_index, beam_width_correction)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_calculation_area(self, slit_index, mode, clip_level, left_border, right_border):
		"""
		Returns the calculation area for the slit where the calculations are made.
		
		Args:
			slit_index(c_uint8) : Index of the slit.
			mode(c_int16 use with byref) : Mode for the calculation area.
			VI_ON  = automatic (default)
			VI_OFF = manual
			clip_level(c_float use with byref) : Get the clip level for the automatic calculation area.
			The clip level is a threshold from the peak intensity to the base line which includes the samples for calculation.
			Clip Level in a range from 0.0 to 13.5.
			left_border(c_float use with byref) : Position in µm where the left border for the calculation area is.
			right_border(c_float use with byref) : Position in µm where the right border for the calculation area is.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_calculation_area(self.devSession, slit_index, mode, clip_level, left_border, right_border)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_calculation_area(self, slit_index, mode, clip_level, left_border, right_border):
		"""
		Sets the calculation area for the slit where the calculations are made.
		
		Args:
			slit_index(c_uint8) : Index of the slit.
			mode(c_int16) : Set the calculation area either automatic or manual.
			Automatic = 1 = VI_ON  = true
			Manual    = 0 = VI_OFF = false
			
			If the mode is set to "Automatic" then the parameter "Automatic Mode Clip Level" has to be set. The parameter "Left Border" and "Right Border" are ignored.
			
			If the mode is set to "Manual" then the parameter "Left Border" and "Right Border" have to be set. The parameter "Automatic Mode Clip Level" is ignored.
			clip_level(c_float) : Set the clip level for the automatic calculation area. This parameter has to be set with the "Automatic Mode".
			The clip level is a threshold in percent between the peak intensity and the base line.
			A clip level of 0.01 means that beginning at the peak position and lookking in both directions to the edges of the measurement window, all samples that have an intensity higher than 1% of the range between the peak and the base line are used for calculations. With the first sample in each direction that is below the threshold, all further samples are not used.
			
			left_border(c_float) : Position in µm where the left border of the calculation area is.
			The range for the left border is from 0 to 9000µm. Samples that are below the border are not used for the calculations.
			right_border(c_float) : Position in µm where the right border for the calculation area is.
			The range for the right border is from 0 to 9000µm. Samples that are greater the border are not used for the calculations.
			The right border has to be a greater value than the left border.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_calculation_area(self.devSession, slit_index, mode, clip_level, left_border, right_border)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_position_correction(self, position_correction):
		"""
		Gets a correction for the centroid and peak position. The correction translates the centroid and peak position under the influence of the bandwidth, gain and drum speed.
		
		Args:
			position_correction(c_int16 use with byref) : Enables the position correction.
			
			ON  = Position correction is active
			OFF = Position correction is deactive
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_position_correction(self.devSession, position_correction)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_position_correction(self, position_correction):
		"""
		Sets a correction for the centroid and peak position. The correction translates the centroid and peak position under the influence of the bandwidth, gain and drum speed. This correction is used for this calculation result:
		- centroid position
		- peak position
		- positions arrays for the slits
		
		Args:
			position_correction(c_int16) : Enables the position correction.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_position_correction(self.devSession, position_correction)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_reference_position(self, slit_index, preset, reference_position):
		"""
		Gets the position offset which is added to the centroid and peak position.
		
		Args:
			slit_index(c_uint8) : Index of the slit.
			preset(ViPUInt8 use with byref) : Either fix the offset to a calulation parameter or set a user defined offset.
			0 = Sensor Center
			1 = Roi Center
			2 = Peak Position
			3 = Centroid Position
			4 = User Position
			reference_position(c_double use with byref) : Offset to the calculation parameter centroid and peak position in µm.
			Corrected Centroid Position = Reference Position - Centroid position
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_reference_position(self.devSession, slit_index, preset, reference_position)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_reference_position(self, slit_index, preset, reference_position):
		"""
		Gets the position offset which is added to the centroid and peak position.
		This parameter only is used if the positin correction is activated with the function "set_position_correction(VI_TRUE)".
		
		Args:
			slit_index(c_uint8) : Index of the slit.
			preset(c_uint8) : Either fix the offset to a calulation parameter or set a user defined offset.
			0 = Sensor Center
			1 = Roi Center
			2 = Peak Position
			3 = Centroid Position
			4 = User Position
			reference_position(c_double) : Offset to the calculation parameter centroid and peak position in µm.
			Corrected Centroid Position = Reference Position - Centroid position
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_set_reference_position(self.devSession, slit_index, preset, reference_position)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_scan_data(self, slit_data, calculation_result, power, powerSaturation, power_intensities):
		"""
		This function reads out the processed scan data. 
		The beam profile is analyzed for each of the maximal BP2_MAX_SLIT_COUNT slits independently.
		
		Args:
			slit_data( (BP2_SLIT_DATA * arrayLength)()) : This buffer contains the data of each of the BP2_MAX_SLIT_COUNT slits. Please provide an array of BP2_MAX_SLIT_COUNT structures of BP2_SLIT_DATA.
			
			
			To identify a slit, please use the function get_slit_parameter.
			calculation_result( (BP2_CALCULATIONS * arrayLength)()) : Fills the data buffer with the calculation result for each slit.
			The parameter is optional. You may pass VI_NULL if you don't need this parameter.
			Please provide an array of BP2_MAX_SLIT_COUNT structures of BP2_CALCULATIONS.
			power(c_double use with byref) : Returns the power in mW of the drum segment with the ND filter.
			You may pass VI_NULL if you don't need this parameter.
			powerSaturation(c_float use with byref) : Returns the saturation of the power window in percent.
			You may pass VI_NULL if you don't need this parameter.
			power_intensities( (c_double * arrayLength)()) : Fills a buffer of minimum 2128 entries with the intensities from the power window. You may pass VI_NULL if you don't need this parameter.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_scan_data(self.devSession, slit_data, calculation_result, power, powerSaturation, power_intensities)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_knife_edge_reconstruction(self, slit_data, calculation_result, slit_indices, slit_data_knife_edge, calculation_results_knife_edge):
		"""
		This function calculates the knife edge data from the slit data.
		
		Args:
			slit_data( (BP2_SLIT_DATA * arrayLength)()) : A buffer of max 7500 entries with the intensites of the slit data. The base level is substracted from the intensities. Max intensity value is 32767.
			calculation_result( (BP2_CALCULATIONS * arrayLength)()) : A buffer with the calculation result for each slit.
			slit_indices( (c_int16 * arrayLength)()) : This array contains the information if the knife edge is calculated for this slit. If this parameter is not used, all slits become the knife edge data. This parameter is useful to increase the performance by suppress the calculation on slits that are not of interest.
			
			
			Example for the calculation on the last two slits:
			slit_indices[0] = VI_FALSE;
			slit_indices[1] = VI_FALSE;
			slit_indices[2] = VI_TRUE;
			slit_indices[3] = VI_TRUE;
			slit_data_knife_edge( (BP2_SLIT_DATA * arrayLength)()) : Fills the data buffer of max 7500 entries with the intensites of the slit data. The base level is substracted from the intensities. Max intensity value is 32767.
			calculation_results_knife_edge( (BP2_CALCULATIONS * arrayLength)()) : Fills the data buffer with the calculation result for each slit.
			The parameter is optional. If the calculations are not needed, please use VI_NULL as value instead of the calculations buffer.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_knife_edge_reconstruction(self.devSession, slit_data, calculation_result, slit_indices, slit_data_knife_edge, calculation_results_knife_edge)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_drum_elapsed_times(self, elapsed_time_buffer):
		"""
		This function reads out the measured elapsed times between two impulses. 156 Impulses are measured for each drum rotation.
		
		Args:
			elapsed_time_buffer( (c_uint16 * arrayLength)()) : Array with the measurement of the elapsed times in µsec between the 156 impulses per drum rotation.
			
			The array has ELAPSED_TIME_COUNTS entries.
			Size of the buffer: 156 Words = 312 Bytes. 
			
			To get the drum rotation frequency multiply the mean of the elapsed times with 156.25.
			
			( The encoder creates 2500 impulses. Every 16 impulses the elapsed time is measured => 156.25 measurements per drum roration).
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_drum_elapsed_times(self.devSession, elapsed_time_buffer)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def request_scan_data(self, power, power_window_saturation, power_intensities):
		"""
		This function reads a new measurement from the device and stores the calculation results internally.
		
		Args:
			power(c_double use with byref) : Returns the power in mW of the drum segment with the ND filter.
			power_window_saturation(c_float use with byref) : Returns the saturation of the power window in percent.
			If the parameter is not needed, use VI_NULL as value instead.
			power_intensities( (c_double * arrayLength)()) : Fills a buffer of minimum 2128 entries with the intensities from the power window. If the values are not needed please use the value VI_NULL instead of a buffer.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_request_scan_data(self.devSession, power, power_window_saturation, power_intensities)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_scan_data_information(self, slit_index, sample_count, dark_level):
		"""
		This function reads out the processed scan data. 
		
		Args:
			slit_index(c_uint8) : Index of the slit which should be analyzed.
			To identify a slit, please use the function get_slit_parameter.
			sample_count(ViPUInt16 use with byref) : Number of samples which are taken for the slit during the scan.
			dark_level(c_float use with byref) : Dark level intensity in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_scan_data_information(self.devSession, slit_index, sample_count, dark_level)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_sample_intensities(self, slit_index, sample_intensities, sample_positions):
		"""
		This function reads out the processed scan data. 
		
		Args:
			slit_index(c_uint8) : Index of the slit which data is of interest.
			To identify a slit, please use the function get_slit_parameter.
			sample_intensities( (c_double * arrayLength)()) : Fills the data buffer of max 7500 entries with the intensites of the slit data. The base level is substracted from the intensities. Max intensity value is 65535.
			sample_positions( (c_double * arrayLength)()) : Fills the data buffer of max 7500 entries with the positions of the slit data in µm.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_sample_intensities(self.devSession, slit_index, sample_intensities, sample_positions)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_peak(self, slit_index, peak_index, peak_position, peak_intensity):
		"""
		This function reads out measured peak parameter.
		
		Args:
			slit_index(c_uint8) : Index of the slit of which the peak interests.
			peak_index(ViPUInt16 use with byref) : Index of the peak in the data intensity buffer.
			peak_position(c_float use with byref) : Position of the peak in µm beginning from the first data in the intensity buffer.
			peak_intensity(c_float use with byref) : Intensity of the peak in digits. The dark level is substracted.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_peak(self.devSession, slit_index, peak_index, peak_position, peak_intensity)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_centroid(self, slit_index, centroid_index, centroid_position):
		"""
		This function reads out the centroid parameter.
		
		Args:
			slit_index(c_uint8) : The index of the slit which should be analyzed for it's centroid.
			centroid_index(ViPUInt16 use with byref) : Index of the centroid in the intensity buffer.
			centroid_position(c_float use with byref) : Position of the centroid in µm beginning from the first data in the intensity buffer.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_centroid(self.devSession, slit_index, centroid_index, centroid_position)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_beam_width(self, slit_index, beam_width_clip, beam_width_sigma):
		"""
		This function reads out the beam with measured at the clip level.
		
		Args:
			slit_index(c_uint8) : Index of the slit which should give the beam width.
			beam_width_clip(c_float use with byref) : Beam width in µm measured at the clip level.
			beam_width_sigma(c_float use with byref) : The sigma width is calculated of all scan data of this slit.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_beam_width(self.devSession, slit_index, beam_width_clip, beam_width_sigma)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_slit_gaussian_fit(self, slit_index, gaussian_fit_amplitude, gaussian_fit_diameter, gaussian_fit_percentage, gaussian_fit_intensities):
		"""
		This function reads out the gaussian parameter.
		
		Args:
			slit_index(c_uint8) : Index of the slit which is analyzed for it's gaussian parameter.
			gaussian_fit_amplitude(c_float use with byref) : Intensity of the calculated gaussian fit curve. The intensity can be higher than the peak intensity of the beam.
			gaussian_fit_diameter(c_float use with byref) : Diameter of the gaussian curve.
			gaussian_fit_percentage(c_float use with byref) : Fit percentage of the gaussian curve to the scan data.
			gaussian_fit_intensities( (c_double * arrayLength)()) : Array of maximal 7500 entries which contains the gaussian curve.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBP2_get_slit_gaussian_fit(self.devSession, slit_index, gaussian_fit_amplitude, gaussian_fit_diameter, gaussian_fit_percentage, gaussian_fit_intensities)
		self.__testForError(pInvokeResult)
		return pInvokeResult

