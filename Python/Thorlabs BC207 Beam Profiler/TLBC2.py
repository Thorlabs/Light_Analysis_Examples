import os
from ctypes import cdll,c_long,c_uint32,c_uint16,c_uint8,byref,create_string_buffer,c_bool, c_char, c_char_p,c_int,c_int16,c_int8,c_double,c_float,sizeof,c_voidp, Structure

_VI_ERROR = (-2147483647-1)
VI_ON = 1
VI_OFF = 0
MAX_CAMERA_DEVICES = 16 #< number of possible camera devices
INV_DEVICE_HANDLE = MAX_CAMERA_DEVICES  # < The index of a camera can never reach the max device count
TLBC1_ERR_DESCR_BUFFER_SIZE = 256  # < Minimum error description buffer size
BC1_RESOURCE_NAME = "USB::0x1313::0x8012::"  # < Pseudo Resource Name to code the serial number and device index
MIN_AVERAGE_COUNT = 1  # < minimum of frames that can be averaged (1 = no averaging)
MAX_AVERAGE_COUNT = 100  # < maximum of frames that can be averaged
VI_SPECIFIC_STATUS_MIN = (0x3FFC0800 )  # < Minimum value of instrument specific ViStatus codes.
VI_SPECIFIC_STATUS_MAX = (0x3FFC0FFF )  # < Maximum value of instrument specific ViStatus codes.
VI_SPECIFIC_ERROR_MIN = (_VI_ERROR + VI_SPECIFIC_STATUS_MIN)  # < Minimum value of instrument specific ViStatus error codes.
VI_SPECIFIC_ERROR_MAX = (_VI_ERROR + VI_SPECIFIC_STATUS_MAX)  # < Maximum value of instrument specific ViStatus error codes.
VI_DRIVER_STATUS_OFFSET = (VI_SPECIFIC_STATUS_MIN)  # < Offset for driver specific ViStatus codes. (Warnings)
VI_DRIVER_ERROR_OFFSET = (VI_SPECIFIC_ERROR_MIN)  # < Offset for driver specific ViStatus codes. (Errors)
VI_INSTR_STATUS_OFFSET = (VI_DRIVER_STATUS_OFFSET + 0x00000040 )  # < Offset for instrument specific ViStatus codes. (Warnings) (0x3FFC0840)
VI_INSTR_ERROR_OFFSET = (VI_DRIVER_ERROR_OFFSET + 0x00000040 )  # < Offset for instrument specific ViStatus codes. (Errors) (0xBFFC0840)
VI_ERROR_INVALID_IMAGE_SIZE = (VI_DRIVER_ERROR_OFFSET)  # < The image dimensions are not as expected.
VI_ERROR_NOT_SUPPORTED = (VI_DRIVER_ERROR_OFFSET + 1)  # < this function is not supported in this mode
VI_ERROR_INVALID_HANDLE = (VI_DRIVER_ERROR_OFFSET + 2)  # < this camera handle is invalid
VI_ERROR_NO_VALID_IMAGE = (VI_DRIVER_ERROR_OFFSET + 3)  # < this camera image is invalid
VI_ERROR_INV_CENTROID = (VI_DRIVER_ERROR_OFFSET + 4)  # < the calculated centroid is outside the image
VI_ERROR_INV_SIGMA = (VI_DRIVER_ERROR_OFFSET + 5)  # < the calculated sigma value is below 0
VI_ERROR_INV_BEAM_WIDTH = (VI_DRIVER_ERROR_OFFSET + 6)  # < the calculated beam width is below 0
VI_ERROR_IMAGE_BRIGHT = (VI_DRIVER_ERROR_OFFSET + 7)  # < The image is too bright for this operation
VI_ERROR_PARAM_OUT_OF_RANGE = (VI_DRIVER_ERROR_OFFSET + 8)  # < this parameter is not inside the valid range
VI_ERROR_INV_ELLIPSE = (VI_DRIVER_ERROR_OFFSET + 9)  # < The ellipse can not be calculated
VI_ERROR_RSC_NOT_FOUND = (VI_DRIVER_ERROR_OFFSET + 10)  # < The sdk dll can not be found
VI_ERROR_RSC_NOT_INITIALIZED = (VI_DRIVER_ERROR_OFFSET + 11)  # < The sdk dll can not be found
VI_ERROR_RSC_NOT_VALID = (VI_DRIVER_ERROR_OFFSET + 12)  # < The serial number is invalid
VI_ERROR_NO_FREE_HANDLE = (VI_DRIVER_ERROR_OFFSET + 13)  # < All 12 camera slots are opened
VI_ERROR_INV_ALC_STATUS = (VI_DRIVER_ERROR_OFFSET + 14)  # < The ambient light correction is in an invalid state
VI_ERROR_INV_VALUE = (VI_DRIVER_ERROR_OFFSET + 15)  # < One internal parameter has an unexpected value
VI_ERROR_INV_ROI = (VI_DRIVER_ERROR_OFFSET + 16)  # < The given ROI is not valid. Maybe not inside the sensor dimensions
VI_ERROR_NO_MUTEX = (VI_DRIVER_ERROR_OFFSET + 17)  # < The mutex could not be created
VI_WARN_CALC_AREA_CLIPPED = (VI_DRIVER_STATUS_OFFSET)  # < this calculation area has been clipped
VI_WARN_WAITING_FOR_TRIGGER = (56454)
TLBC1_Trigger_Mode_No_Trigger = 0  # < Camera runs in continuous mode.
TLBC1_Trigger_Mode_HW_Trigger_Pulse = 2  # < Camera triggers on a TTL impulse and starts exposure after user defined delay.
TLBC1_Trigger_Mode_HW_Trigger_Repetition = 3  # < Camera triggers exposure with user defined frequency and phase locks on a TTL impulse.
TLBC1_Precision_Mode_Fast = 0  # < 8 bit pixel depth
TLBC1_Precision_Mode_Precise = 1  # < 12/16 bit pixel depth
TLBC1_Trigger_Edge_Rising = 0  # < Trigger on the rising edge
TLBC1_Trigger_Edge_Falling = 1  # < Trigger on the falling edge
TLBC1_CalcAreaForm_Rectangle = (0)  # <  Nonrotated rectangular calculation area. Fast calculation in auto calc area mode.
TLBC1_CalcAreaForm_Ellipse = (1)  # <  Rotated elliptical calculation area. Fast calculation in auto calc area mode.
TLBC1_CalcAreaForm_AutoIso = (2)  # <  Automatically determined rotated rectangular calculation area. Iterative calculation, slower but ISO compliant. Only available in auto calc area mode.
TLBC1_Profile_Position_ROI_Center = 0  # < Center of the ROI is the position of the profile cut.
TLBC1_Profile_Position_Peak_Position = 1  # < The position of the highest intensity inside the calculation area.
TLBC1_Profile_Position_Centroid_Position = 2  # < The position of the centroid inside the calculation area.
TLBC1_Profile_Position_User_Position = 3  # < A user defined position inside the ROI.
TLBC1_Ellipse_Mode_ClipLevel_Contour = 0  # < find the countour where the intensities are around the clip level
TLBC1_Ellipse_Mode_Approximated = 1  # < approximate the ellipse with the contour data
TLBC1_MeasurementMethod_FullImage = 0  # < Use all pixel information in the calculation area.
TLBC1_MeasurementMethod_Slit = 1  # < Emulate a slit beam profiler.
TLBC1_AmbientLightCorrection_Mode_Off = 0  # < Ambient light correction disabled. A device specific base level is used.
TLBC1_AmbientLightCorrection_Mode_On = 1  # < Ambient light correction enabled. Measurement configuration specific base level measured by a special procedure will be used.
TLBC1_AmbientLightCorrection_Status_Ready = 0  # < Ambient light correction data availabel. ALC can be enabled.
TLBC1_AmbientLightCorrection_Status_Never = 1  # < Ambient light correction measurement procedure was never run since TLBC1_init(). ALC can't be enabled.
TLBC1_AmbientLightCorrection_Status_Fail = 2  # < The latest ambient light correction measurement procedure failed. ALC can't be enabled.
TLBC1_AveragingMode_Floating = 0
TLBC1_AveragingMode_Moving = 1
TLBC1_MAX_ROWS = (3000)  # <	Maximum number of vertical pixel.
TLBC1_MAX_COLUMNS = (4096)  # <	Maximum number of horizontal pixel.
TLBC2_MAX_CAMERA_DEVICES = 12
TLBC2_INV_DEVICE_HANDLE = 0xFF  # < The index of a camera can never reach the max device count
TLBC2_ERR_DESCR_BUFFER_SIZE = 256  # < Minimum error description buffer size
TLBC2_MIN_AVERAGE_COUNT = 1  # < minimum of frames that can be averaged (1 = no averaging)
TLBC2_MAX_AVERAGE_COUNT = 100  # < maximum of frames that can be averaged
TLBC2_MAX_COLUMNS = 1360
TLBC2_MAX_ROWS = 1024
TLBC2_No_Binning = 1  # < Full image resolution
TLBC2_Binning_2 = 2  # < Camera image is reduced by 2 in the with and 2 in the height
TLBC2_Binning_4 = 4  # < Camera image is reduced by 4 in the with and 4 in the height
TLBC2_Binning_8 = 8  # < Camera image is reduced by 8 in the with and 8 in the height
TLBC2_Binning_16 = 16  # < Camera image is reduced by 16 in the with and 16 in the height

class TLBC1_Calculations(Structure):
	_fields_ = [
		("isValid", c_int16),  # < \a VI_TRUE if scan analysis results are valid; \a VI_FALSE if an error occured during analysis and the calculations data is invalid.
		("baseLevel", c_double),  # < Mean noise of the sensor in [digits] (typically 47 digits for 12 bit images and 3 digits for 8 bit images)
		("lightShieldedPixelMeanIntensity", c_double),  # < mean intensity of the light shielded pixels ( if option is activated for TSI BC2xx cameras)
		("minIntensity", c_double),  # < Minimum intensity of the measurement
		("maxIntensity", c_double),  # < Pixel intensity value for maximum intensity / resoltution of the pixel intensities.
		("saturation", c_double),  # < Ratio of the highest intensity in the scan to the dynamic range of the sensor (value range 0.0 ... 1.0).
		("saturatedPixel", c_double),  # < Ratio of the amount of saturated pixels to amount of pixels inside the calculation area (value range 0.0 ... 1.0).
		("imageWidth", c_uint16),  # < Pixel per horizontal line.
		("imageHeight", c_uint16),  # < Pixel per vertical column.
		("peakPositionX", c_uint16),  # < Peak x pixel position.
		("peakPositionY", c_uint16),  # < Peak y pixel position.
		("peakIntensity", c_double),  # < Highest pixel intensity value inside the calculation area.
		("centroidPositionX", c_float),  # < Centroid x pixel position.
		("centroidPositionY", c_float),  # < Centroid y pixel position.
		("fourSigmaX", c_float),  # < Horizontal standard deviation in pixel.
		("fourSigmaY", c_float),  # < Vertical standard deviation in pixel.
		("fourSigmaR", c_float),  # < Radial standard deviation in pixel. ("generalized beam diameter" from ISO 11146-2)
		("fourSigmaXY", c_float),  # 
		("beamWidthIsoX", c_double),  # < beam with x measured by the ISO 11146-2 along one axis of the beam profile
		("beamWidthIsoY", c_double),  # < beam with y measured by the ISO 11146-2 along one axis of the beam profile prependicular to the beam width x
		("beamWidthIsoXSimple", c_double),  # < beam with x measured by the ISO 11146-2 for round profiles with ellipticity > 87%
		("beamWidthIsoYSimple", c_double),  # < beam with y measured by the ISO 11146-2 for round profiles with ellipticity > 87%
		("ellipticityIso", c_double),  # < ellipticity of the beam witdh by the ISO 11146-2
		("azimuthAngle", c_double),  # < azimuth angle measured clockwise by the ISO 11146-2. The angle i between the x axis of the laboratory system and that of the principal axis which is cloder to the x-axis
		("ellipseDiaMin", c_float),  # < Ellipse minor axis diameter in [pixel]
		("ellipseDiaMax", c_float),  # < Ellipse major axis diameter in [pixel]
		("ellipseDiaMean", c_float),  # < Ellipse diameter arithmetic mean value in [pixel]
		("ellipseOrientation", c_float),  # < Ellipse orientation angle in degree.
		("ellipseEllipticity", c_float),  # < The ellipse's ratio of minor axis diameter to major axis diameter.
		("ellipseEccentricity", c_float),  # < The ellipse's eccentricity.
		("ellipseCenterX", c_float),  # < Ellipse center x pixel position.
		("ellipseCenterY", c_float),  # < Ellipse center y pixel position.
		("ellipseFitAmplitude", c_float),  # < Ellipse amplitude in Fourier fit (in pixel).
		("rotAngleEllipseX", c_float),  # 
		("rotAngleEllipseY", c_float),  # 
		("ellipseWidthIsoX", c_float),  # 
		("ellipseWidthIsoY", c_float),  # 
		("totalPower", c_float),  # < Total power in dBm
		("peakPowerDensity", c_float),  # < Peak power density in mW/�m�
		("beamWidthClipX", c_float),  # < Horizontal beam width at clip level in pixel.
		("beamWidthClipY", c_float),  # < Vertical beam width at clip level in pixel.
		("gaussianFitCentroidPositionX", c_float),  # < Centroid x pixel position for the gaussian profile.
		("gaussianFitCentroidPositionY", c_float),  # < Centroid y pixel position for the gaussian profile.
		("gaussianFitRatingX", c_float),  # < Ratio of actual data to the gaussian fit of the x profile.
		("gaussianFitRatingY", c_float),  # < Ratio of actual data to the gaussian fit of the y profile.
		("gaussianFitDiameterX", c_float),  # < diameter for the profile X centroid
		("gaussianFitDiameterY", c_float),  # < diameter for the profile Y centroid
		("calcAreaCenterX", c_float),  # < Calculation area left border. The specified pixel colum is included to the calculation area.
		("calcAreaCenterY", c_float),  # < Calculation area right border. The specified pixel colum is included to the calculation area.
		("calcAreaWidth", c_float),  # < Calculation area width.
		("calcAreaHeight", c_float),  # < Calculation area height.
		("calcAreaAngle", c_double),  # < Calculation area rotation angle in degree. The rectangle/ellipse defined by \ref calcAreaLeft, \ref calcAreaTop, \ref calcAreaRight, and \ref calcAreaBottom will be rotated by this angle. Positive values rotate against the clock.
		("calcAreaLineOffset", c_double),  # < pixel inside the calculation area per line
		("profileValuesX", (c_float * (TLBC1_MAX_COLUMNS))), # < Intensity profile intensity values along the x axis of the whole image.
		("profileValuesY", (c_float * (TLBC1_MAX_ROWS))), # < Intensity profile intensity values along the y axis of the whole image.
		("profilePositionsX", (c_float * (TLBC1_MAX_COLUMNS))), # < Intensity profile position values along the x axis of the whole image.
		("profilePositionsY", (c_float * (TLBC1_MAX_ROWS))), # < Intensity profile position values along the y axis of the whole image.
		("profilePeakValueX", c_float),  # < Peak intensity value in the x profile inside the calculation area.
		("profilePeakValueY", c_float),  # < Peak intensity value in the y profile inside the calculation area.
		("profilePeakPosX", c_uint16),  # < Intensity profile peak intensity x pixel position inside the calculation area.
		("profilePeakPosY", c_uint16),  # < Intensity profile peak intensity y pixel position inside the calculation area.
		("effectiveArea", c_double),  # < Area of an ideal flat top beam with same peak intensity in �m�.
		("effectiveBeamDiameter", c_double),  # 
		("temperature", c_double),  # 
		("gaussianValuesX", (c_float * (TLBC1_MAX_COLUMNS))), # 
		("gaussianValuesY", (c_float * (TLBC1_MAX_ROWS))), # 
		("besselFitValuesX", (c_float * (TLBC1_MAX_COLUMNS))), # 
		("besselFitValuesY", (c_float * (TLBC1_MAX_ROWS))), # 
		("besselFitRatingX", c_float),  # 
		("besselFitRatingY", c_float),  # 
	]


class TLBC2:

	def __init__(self, resourceName = None, IDQuery = False, resetDevice = False):
		"""
		This function initializes the instrument driver session and performs the following initialization actions:
		
		(1) Opens a session to the Default Resource Manager resource and a session to the selected device using the Resource Name.
		(2) Performs an identification query on the Instrument.
		(3) Resets the instrument to a known state.
		(4) Sends initialization commands to the instrument.
		(5) Returns an instrument handle which is used to differentiate between different sessions of this instrument driver.
		
		Notes:
		(1) Each time this function is invoked an unique session is opened.  
		
		Args:
			resourceName (create_string_buffer)
			IDQuery (c_bool):This parameter specifies whether an identification query is performed during the initialization process.
			VI_OFF (0): Skip query.
			VI_ON  (1): Do query (default). 
			resetDevice (c_bool):Pass VI_TRUE to perform reset operation and put the instrument in a pre-defined reset state.
		"""
		if sizeof(c_voidp) == 4:
			dll_name = "TLBC2_32.dll"
		else:
			dll_name = "TLBC2_64.dll"
			
		self.dll = cdll.LoadLibrary(dll_name)	
		self.devSession = c_long()
		self.devSession.value = 0
		if resourceName!= None:
			pInvokeResult = self.dll.TLBC2_init(resourceName, IDQuery, resetDevice, byref(self.devSession))
			self.__testForError(pInvokeResult)


	def __testForError(self, status):
		if status < 0:
			self.__throwError(status)
		return status

	def __throwError(self, code):
		msg = create_string_buffer(1024)
		self.dll.TLBC2_error_message(self.devSession, c_int(code), msg)
		raise NameError(c_char_p(msg.raw).value)

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
		
		Args:
			resourceName (create_string_buffer)
			IDQuery (c_bool):This parameter specifies whether an identification query is performed during the initialization process.
			VI_OFF (0): Skip query.
			VI_ON  (1): Do query (default). 
			resetDevice (c_bool):Pass VI_TRUE to perform reset operation and put the instrument in a pre-defined reset state.
		Returns:
			int: The return value, 0 is for success
		"""
		self.dll.TLBC2_close(self.devSession)
		self.devSession.value = 0
		pInvokeResult = self.dll.TLBC2_init(resourceName, IDQuery, resetDevice, byref(self.devSession))
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def close(self):
		"""
		This function closes the instrument driver session.
		      
		Note: The instrument must be reinitialized to use it again.
		
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_close(self.devSession)
		return pInvokeResult

	def closeSDK(self):
		"""
		This function closes the sdk for the driver. Has to be called if the application is closing.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_closeSDK(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_device_count(self, deviceCount):
		"""
		Get the number of devices available in your system that can be controlled with this driver.
		
		Args:
			deviceCount(c_uint32 use with byref) : Receives the number of connected devices.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_device_count(self.devSession, deviceCount)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_device_information(self, deviceIndex, manufacturer, instrumentName, serialNumber, deviceAvailable, resourceName):
		"""
		Get identification information of a connected device.
		You don't have to open a session with the device with TLBC2_init() before you can use this function.
		
		
		Args:
			deviceIndex(c_uint32) : The device's index. Valid values range from 0 to (number of connected devices - 1) (see TLBC2_get_device_count()).
			manufacturer(create_string_buffer(1024)) : A 64 byte string buffer to receive the manufacturer name. You may pass VI_NULL if you don't need this value.
			instrumentName(create_string_buffer(1024)) : A 64 byte string buffer to receive the instrument/model name. You may pass VI_NULL if you don't need this value.
			serialNumber(create_string_buffer(1024)) : A 64 byte string buffer to receive the serial number. You may pass VI_NULL if you don't need this value.
			deviceAvailable(c_int16 use with byref) : true if the device is available (not used by another program). You may pass VI_NULL if you don't need this value.
			resourceName(create_string_buffer(1024)) : A 256 byte string buffer to receive the ressource identification string. Use this string in function TLBC2_init().You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_device_information(self.devSession, deviceIndex, manufacturer, instrumentName, serialNumber, deviceAvailable, resourceName)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def self_test(self, selfTestResult, selfTestMessage):
		"""
		This function runs the device self-test routine and returns the test result.
		
		Args:
			selfTestResult(c_int16 use with byref) : This parameter contains the value returned from the device self test routine. A retured zero value indicates a successful run, A value other than zero indicates failure.
			selfTestMessage(create_string_buffer(1024)) : This parameter returns the interpreted code as an user readable message string.
			          
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_self_test(self.devSession, selfTestResult, selfTestMessage)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def reset(self):
		"""
		This function resets the device to a default state.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_reset(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def revision_query(self, instrumentDriverRevision, firmwareRevision):
		"""
		This function returns the revision numbers of the instrument driver and the device firmware.
		
		Args:
			instrumentDriverRevision(create_string_buffer(1024)) : This parameter returns the Instrument Driver revision.
			          
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			firmwareRevision(create_string_buffer(1024)) : This parameter returns the device firmware revision.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass  VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_revision_query(self.devSession, instrumentDriverRevision, firmwareRevision)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def error_query(self, errorCode, errorMessage):
		"""
		This function queries the instrument's latest error code.
		
		Args:
			errorCode(c_int use with byref) : This parameter returns the instrument error number.
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value. 
			errorMessage(create_string_buffer(1024)) : This parameter returns the instrument error message.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you don't need this value. 
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_error_query(self.devSession, errorCode, errorMessage)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def error_message(self, errorCode, errorMessage):
		"""
		This function translates the error return value from a VXIplug&play instrument driver function to a user-readable string.
		
		Args:
			errorCode(c_int) : Instrument driver error code.
			errorMessage(create_string_buffer(1024)) : This parameter returns the interpreted code as an user readable message string.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_error_message(self.devSession, errorCode, errorMessage)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def identification_query(self, instrumentName, serialNumber):
		"""
		This function returns the device identification information.
		
		Args:
			instrumentName(create_string_buffer(1024)) : The instrument name (e.g. "BC207-VIS").
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass  VI_NULL if you don't need this value.
			serialNumber(create_string_buffer(1024)) : The instrument's serial number (e.g. "M01234567").
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass  VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_identification_query(self.devSession, instrumentName, serialNumber)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_gain_range(self, minGain, maxGain):
		"""
		Get the gain value range supported by the instrument.
		
		Args:
			minGain(c_double use with byref) : Minimum gain factor in dB.
			
			You may pass VI_NULL if you don't need this value.
			maxGain(c_double use with byref) : Maximum gain factor in dB.
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_gain_range(self.devSession, minGain, maxGain)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_gain(self, gain):
		"""
		Gets the gain value.
		
		Args:
			gain(c_double use with byref) : The gain value in dB.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_gain(self.devSession, gain)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_gain(self, gain):
		"""
		Sets the gain value.
		
		Note:
		(1) Setting the gain value will disable auto exposure mode.
		
		Args:
			gain(c_double) : Sets the gain in dB. Use <Get Gain Range> for the supported parameter value range.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_gain(self.devSession, gain)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_auto_exposure(self, autoExposure):
		"""
		Get the auto exposure mode.
		
		If auto exposure mode is enabled the data of the latest image is used to calculate improved exposure settings for the next scan. On fluctuating beam intensities it is still possible to scan dark or overexposed images as the new exposure parameters are only used for the next scan.
		If auto exposure mode is disabled the exposure parameters set with <Set Exposure Time> are used.
		
		Args:
			autoExposure(c_int16 use with byref) : Gets the auto exposure.
			VI_ON  = Auto exposure is active
			VI_OFF = Auto exposure is inactive
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_auto_exposure(self.devSession, autoExposure)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_auto_exposure(self, autoExposure):
		"""
		Set the auto exposure mode.
		
		If auto exposure mode is enabled the data of the latest image is used to calculate improved exposure settings for the next scan. On fluctuating beam intensities it is still possible to scan dark or overexposed images as the new exposure parameters are only used for the next scan.
		If auto exposure mode is disabled the exposure parameters set with TLBC2_set_exposure_time() are used.
		
		Args:
			autoExposure(c_int16) : Sets the auto exposure active or inactive.
			VI_ON  = Auto exposure is active
			VI_OFF = Auto exposure is inactive
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_auto_exposure(self.devSession, autoExposure)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_exposure_time_range(self, minExposureTime, maxExposureTime):
		"""
		Get the exposure time value range supported by the instrument.
		
		Args:
			minExposureTime(c_double use with byref) : Minimum exposure time in ms.
			
			You may pass VI_NULL if you don't need this value.
			maxExposureTime(c_double use with byref) : Maximum exposure time in ms.
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_exposure_time_range(self.devSession, minExposureTime, maxExposureTime)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_exposure_time(self, exposureTime):
		"""
		Gets the exposure time.
		
		Args:
			exposureTime(c_double use with byref) : The exposure time in ms.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_exposure_time(self.devSession, exposureTime)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_exposure_time(self, exposureTime):
		"""
		Sets the exposure time.
		
		Calling this function will disable auto exposure mode.
		
		Args:
			exposureTime(c_double) : The exposure time in ms. Use <Get Exposure Time Range> for the supported parameter value range.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_exposure_time(self.devSession, exposureTime)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_precision_mode(self, precisionMode):
		"""
		Get the precision mode.
		
		Args:
			precisionMode(c_uint8 use with byref) : Gets the Precision Mode.
			
			0 = Fast (with reduced intensity resolution)
			1 = Precise (with full intensity resolution)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_precision_mode(self.devSession, precisionMode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_precision_mode(self, precisionMode):
		"""
		Sets the precision mode.
		
		Args:
			precisionMode(c_uint8) : The precision mode.
			
			0 = Fast (with reduced intensity resolution)
			1 = Precise (with full intensity resolution)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_precision_mode(self.devSession, precisionMode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_binning(self, binning):
		"""
		Returns the binning for the camera. This reduces the resolution of the image.
		E.g. a binning of 2 will reduce the image by 2 in the with and 2 in the height
		
		Args:
			binning(c_uint8 use with byref) : The Binning Mode = binning factor in each dimension
			
			1 = No Binning
			2 = 2x2
			3 = 4x4
			4 = 8x8
			16 = 16x16
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_binning(self.devSession, binning)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_binning(self, binning):
		"""
		Sets the binning for the camera. This reduces the resolution of the image.
		E.g. a binning of 2 will reduce the image by 2 in the with and 2 in the height
		
		Args:
			binning(c_uint8) : The Binning Mode
			
			1 = No Binning
			2 = 2x2
			4 = 4x4
			8 = 8x8
			16 = 16x16
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_binning(self.devSession, binning)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_sensor_information(self, pixelCountX, pixelCountY, pixelPitchHorizontal, pixelPitchVertical):
		"""
		Get information about the sensor's dimensions.
		
		Args:
			pixelCountX(c_uint16 use with byref) : Count of horizontal pixel.
			
			You may pass VI_NULL if you don't need this value.
			pixelCountY(c_uint16 use with byref) : Count of vertical pixel.
			
			You may pass VI_NULL if you don't need this value.
			pixelPitchHorizontal(c_double use with byref) : Distance in µm between the left edge of each pixel to the left edge of the horizontally next pixel.
			
			You may pass VI_NULL if you don't need this value.
			pixelPitchVertical(c_double use with byref) : Distance in µm between the top edge of each pixel to the top edge of the vertically next pixel.
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_sensor_information(self.devSession, pixelCountX, pixelCountY, pixelPitchHorizontal, pixelPitchVertical)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_roi(self, left, top, width, height):
		"""
		Get the rectangle of the ROI.
		
		The ROI (Region Of Interest) defines a rectangular subarea of the sensor area whereas the maximum ROI is the full sensor size (see TLBC2_get_sensor_information()) and the smallest 32 x 32 pixel. Only image data of the selected ROI are transmitted from the device so that narrower ROI size reduces bandwidth and therefore increases measurement speed (frames per second).
		
		Args:
			left(c_uint16 use with byref) : Left border pixel index of the ROI rectangle.
			
			You may pass VI_NULL if you don't need this value.
			top(c_uint16 use with byref) : Top border pixel index of the ROI rectangle.
			
			You may pass VI_NULL if you don't need this value.
			width(c_uint16 use with byref) : Width of the ROI rectangle in pixel.
			
			You may pass VI_NULL if you don't need this value.
			height(c_uint16 use with byref) : Height of the ROI rectangle in pixel.
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_roi(self.devSession, left, top, width, height)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_roi(self, left, top, width, height):
		"""
		Set the rectangle of the ROI.
		
		The ROI (Region Of Interest) defines a rectangular subarea of the sensor area whereas the maximum ROI is the full sensor size (see TLBC2_get_sensor_information()) and the smallest 32 x 32 pixel. Only image data of the selected ROI are transmitted from the device so that narrower ROI size reduces bandwidth and therefore increases measurement speed (frames per second).
		
		Notes:
		(1) This function will coerce the passed set values to fitting values. Use TLBC2_get_roi() to read back the actual ROI rectangle after setting them.
		(2) This function tries to retain the currently set calculation area. In case that the current calculation area doesn't fit into the new ROI the calculation area will be reset to full ROI.
		
		Args:
			left(c_uint16) : Sets the left border of the ROI in pixels.
			top(c_uint16) : Sets the top border of the ROI in pixels.
			width(c_uint16) : Sets the width of the ROI in pixels.
			The width has to be a multiple of 4.
			height(c_uint16) : Sets the height of the ROI in pixels.
			The height has to be a multiple of 4.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_roi(self.devSession, left, top, width, height)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_trigger(self, triggerMode, triggerValue, triggerEdge):
		"""
		Get the currently set trigger parameters.
		
		The electrical TTL level trigger input can be used to synchronize laser pulses to the camera exposure time. By default 'No Trigger' is chosen for continuous caption of CW light sources.
		
		Args:
			triggerMode(c_uint16 use with byref) : The trigger mode:
			0 = No Trigger: The beam profiler continuously scans for images as fast as possible.
			2 = Hardware Trigger Pulse: The beam profiler triggers on a selected edge of a TTL signal at the device's BNC connector and starts exposure after a user defined delay time.
			
			You may pass VI_NULL if you don't need this value.
			triggerValue(c_double use with byref) : The meaning of this value depends on the trigger mode:
			- In trigger mode 'No Trigger': The value is not used.
			- In trigger mode 'Hardware Trigger Pulse': The delay in µs from trigger to start of exposure has no effect ( only for compability to the BC1 driver)
			
			You may pass VI_NULL if you don't need this value.
			triggerEdge(c_uint16 use with byref) : The trigger edge in the hardware trigger modes.
			0 = Rising Edge
			1 = Falling Edge
			
			The value is not used in No Trigger mode. You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_trigger(self.devSession, triggerMode, triggerValue, triggerEdge)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_trigger(self, triggerMode, triggerValue, triggerEdge):
		"""
		Set the trigger parameters.
		
		The electrical TTL level trigger input can be used to synchronize laser pulses to the camera exposure time. By default 'No Trigger' is chosen for continuous caption of CW light sources.
		
		Args:
			triggerMode(c_uint16) : The trigger mode:
			0 = No Trigger: The beam profiler continuously scans for images as fast as possible.
			2 = Hardware Trigger Pulse: The beam profiler triggers on a selected edge of a TTL signal at the device's BNC connector and starts exposure after a user defined delay time.
			triggerValue(c_double) : The meaning of this value depends on the trigger mode:
			- In trigger mode 'No Trigger': The value is ignored.
			- In trigger mode 'Hardware Trigger Pulse': The delay in µs from trigger to start of exposure (0 µs to 1000000 µs). THis parameter has no effect and only exists for compability to the BC1 driver
			triggerEdge(c_uint16) : The trigger edge in the hardware trigger modes.
			0 = Rising Edge
			1 = Falling Edge
			
			The value is ignored in No Trigger mode.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_trigger(self.devSession, triggerMode, triggerValue, triggerEdge)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_ambient_light_correction_mode(self, mode):
		"""
		Get the ambient light correction mode.
		
		Args:
			mode(c_uint8 use with byref) : The ambient light correction mode.
			
			0 = Ambient light correction disabled. A device specific base level is used.
			1 = Ambient light correction enabled. Measurement configuration specific base level measured by a special procedure will be used.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_ambient_light_correction_mode(self.devSession, mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_ambient_light_correction_mode(self, mode):
		"""
		Set the ambient light correction mode.
		
		The ambient light correction procedure must have been run successfully before ambient light correction can be enabled.
		See also <Run Ambient Light Correction> and <Get Ambient Light Correction Status>.
		
		Args:
			mode(c_uint8) : The ambient light correction mode.
			
			0 = Ambient light correction disabled. A device specific base level is used.
			1 = Ambient light correction enabled. Measurement configuration specific base level measured by a special procedure will be used.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_ambient_light_correction_mode(self.devSession, mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_ambient_light_correction_status(self, status):
		"""
		Get the ambient light correction data status.
		
		This status indicates the availability of valid ambient light correction data. The data is volatile and needs to be measured at least once after TLBC2_init(). Ambient light correction can't be enabled if there is no valid ALC data.
		
		Args:
			status(c_uint8 use with byref) : Ambient light correction status.
			
			0 = Ambient light correction data availabel. ALC can be enabled.
			1 = Ambient light correction measurement procedure was never run since TLBC2_init(). ALC can't be enabled.
			2 = The latest ambient light correction measurement procedure failed. ALC can't be enabled.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_ambient_light_correction_status(self.devSession, status)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def run_ambient_light_correction(self):
		"""
		Run the ambient light correction measurement.
		
		Block the laser beam while running this measurement. The function will block until the measurement is done. This can take up to 30 seconds.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_run_ambient_light_correction(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_bad_pixel_correction_support(self, supported):
		"""
		Get the bad pixel correction support information.
		
		Depending on the device's firmware the bad pixel correction feature is supported or not.
		
		Args:
			supported(c_int16 use with byref) : Support of the bad pixel correction feature.
			
			VI_FALSE (0) = Feature not supported.
			VI_TRUE  (1) = Feature supported.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_bad_pixel_correction_support(self.devSession, supported)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_bad_pixel_correction_threshold(self, threshold):
		"""
		Get the bad pixel correction threshold in percentage.
		
		Args:
			threshold(c_double use with byref) : Threshold of the bad pixel correction in percentage. 
			Range 0.0 - 1.0
			
			
			Notes:
			(1) If the bad pixel correction feature is not supported by the device this parameter will always receive VI_OFF. See <Get Bad Pixel Correction Support Information>.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_bad_pixel_correction_threshold(self.devSession, threshold)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_bad_pixel_correction_threshold(self, threshold):
		"""
		Set the bad pixel correction threshold in percentage.
		
		Args:
			threshold(c_double) : Threshold of the bad pixel correction in percentage. 
			Range 0.0 - 1.0
			
			
			Notes:
			(1) If the bad pixel correction feature is not supported by the device this parameter will always receive VI_OFF. See <Get Bad Pixel Correction Support Information>.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_bad_pixel_correction_threshold(self.devSession, threshold)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_cut_roi_from_fullsize(self, enable):
		"""
		With this function, the camera aquires full size images and cut off the roi from the image.
		
		With the function "get_fullsize_image" the full size will be returned
		
		Args:
			enable(c_int16 use with byref) : Returns the state if the roi is cut from the fullsize image
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_cut_roi_from_fullsize(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_cut_roi_from_fullsize(self, enable):
		"""
		With this function, the camera aquires full size images and cut off the roi from the image.
		
		With the function "get_fullsize_image" the full size will be returned
		
		Args:
			enable(c_int16) : Sets the state if the roi is cut from the fullsize image
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_cut_roi_from_fullsize(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def clearFrameQueue(self):
		"""
		The camera continuesly aquires image and hold them in a buffer. If you want to be sure that the next image is using the current settings, clear the queue before you request a new image.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_clearFrameQueue(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_wavelength_range(self, minWavelength, maxWavelength):
		"""
		Gets the wavelength range supported by the instrument.
		
		Typical values:
		VIS: 350 - 1100 nm
		UV:  190 - 350  nm.
		
		Args:
			minWavelength(c_double use with byref) : Minimum wavelength in nm.
			
			You may pass VI_NULL if you don't need this value.
			maxWavelength(c_double use with byref) : Maximum wavelength in nm.
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_wavelength_range(self.devSession, minWavelength, maxWavelength)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_wavelength(self, wavelength):
		"""
		Gets the current operating wavelength.
		
		Args:
			wavelength(c_double use with byref) : Wavelength in nm.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_wavelength(self.devSession, wavelength)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_wavelength(self, wavelength):
		"""
		Sets the current operating wavelength in nm.
		
		Args:
			wavelength(c_double) : Wavelength in nm.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_wavelength(self.devSession, wavelength)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_user_power_offset(self, powerOffset):
		"""
		Get the user power offset used in power calculation.
		
		Args:
			powerOffset(c_double use with byref) : Gets the power offset in dBm that is set by the user. The default value is 0.0 dBm.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_user_power_offset(self.devSession, powerOffset)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_user_power_offset(self, powerOffset):
		"""
		Sets the user power offset for power calculation.
		
		Args:
			powerOffset(c_double) : Sets the user power offset in dBm.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_user_power_offset(self.devSession, powerOffset)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_clip_level(self, clipLevel):
		"""
		Get the clip level where the clipped beam width is calulated.
		
		Args:
			clipLevel(c_double use with byref) : Clip level as fraction from the peak to the base line (value range 0.05 to 0.95).
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_clip_level(self.devSession, clipLevel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_clip_level(self, clipLevel):
		"""
		Set the clip level where the clipped beam width is calulated.
		
		Args:
			clipLevel(c_double) : Clip level as fraction from the peak to the base line (value range 0.05 to 0.95).
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_clip_level(self.devSession, clipLevel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_attenuation(self, attenuation):
		"""
		Get the attenuation of a filter placed in front of the beam profiler camera.
		
		This attenuation value is used to calculate a correct power measurement value.
		
		Args:
			attenuation(c_double use with byref) : The filter attenuation in dB.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_attenuation(self.devSession, attenuation)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_attenuation(self, attenuation):
		"""
		Set the attenuation of a filter placed in front of the beam profiler camera.
		
		This attenuation value is used to calculate a correct power measurement value.
		
		Args:
			attenuation(c_double) : The filter attenuation in dB.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_attenuation(self.devSession, attenuation)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_nd_filters(self, filterCount, filterValues):
		"""
		Get the attenuation of a filter placed in front of the beam profiler camera.
		
		This attenuation value is used to calculate a correct power measurement value.
		
		Args:
			filterCount(c_uint8 use with byref) : Amount of used filters in the filter wheel (maximum 4)
			filterValues( (c_double * arrayLength)()) : Array of filter attenuations in dB.
			Please provide an array with 6 entries.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_nd_filters(self.devSession, filterCount, filterValues)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_averaging(self, averagingMode, averagingValue):
		"""
		Get the averaging parameters.
		
		Args:
			averagingMode(c_uint8 use with byref) : The averaging mode:
			
			0 = Floating Averaging: The latest measurement data is added to the stored measurement data and weightend. E.g. if the 100th measurement data arrived, it is added to the 99 other measurement data with a weightend of 1/100.
			1 = Moving Averaging: The latest N measurement datas are summed up and averaged.
			
			You may pass VI_NULL if you don't need this value.
			averagingValue(c_uint16 use with byref) : The number of measurements to build the average.
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_averaging(self.devSession, averagingMode, averagingValue)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_averaging(self, averageMode, averageValue):
		"""
		Sets the average mode and the count of measurement data which build the average.
		
		Args:
			averageMode(c_uint8) : The averaging mode:
			
			0 = Floating Averaging: The latest measurement data is added to the stored measurement data and weightend. E.g. if the 100th measurement data arrived, it is added to the 99 other measurement data with a weightend of 1/100.
			1 = Moving Averaging: The latest N measurement datas are summed up and averaged.
			averageValue(c_uint16) : The number of measurements to build the average (value range 1 to 100).
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_averaging(self.devSession, averageMode, averageValue)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_profile_cut_position(self, positionPreset, xPosition, yPosition, rotationAngle):
		"""
		Get the position where x and y plots are taken.
		
		The position defines the intersection point of two right angled cut lines in the image rectangle. The gaussian fit x and y are calculated on the resulting cut profiles along those lines.
		
		Args:
			positionPreset(c_uint8 use with byref) : Profile position preset.
			
			0 = ROI Center: The center of the ROI is the position of the profile cut.
			1 = Peak Position: The position of the highest intensity inside the calculation area is the position of the profile cut.
			2 = Centroid Positin: The position of the centroid inside the calculation area is the position of the profile cut.
			3 = User Position: A user defined position inside the ROI is the position of the profile cut.
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			xPosition(c_uint16 use with byref) : The x pixel position of the intersection point.
			
			Notes:
			(1) This parameter is only used with preset 'User Position'.
			(2) You may pass VI_NULL if you don't need this value.
			yPosition(c_uint16 use with byref) : The y pixel position of the intersection point.
			
			Notes:
			(1) This parameter is only used with preset 'User Position'.
			(2) You may pass VI_NULL if you don't need this value.
			rotationAngle(c_double use with byref) : The rotation angle of the cut lines in degree. Postive values rotate against the clock.
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_profile_cut_position(self.devSession, positionPreset, xPosition, yPosition, rotationAngle)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_profile_cut_position(self, positionPresets, xPosition, yPosition, rotationAngle):
		"""
		Set the position where x and y plots are taken.
		
		The position defines the intersection point of two right angled cut lines in the image rectangle. The gaussian fit x and y are calculated on the resulting cut profiles along those lines.
		
		Args:
			positionPresets(c_uint8) : Profile position preset.
			
			0 = ROI Center: The center of the ROI is the position of the profile cut.
			1 = Peak Position: The position of the highest intensity inside the calculation area is the position of the profile cut.
			2 = Centroid Positin: The position of the centroid inside the calculation area is the position of the profile cut.
			3 = User Position: A user defined position inside the ROI is the position of the profile cut.
			xPosition(c_uint16) : The x pixel position of the intersection point.
			
			Notes:
			(1) This parameter is only used with preset 'User Position'.
			yPosition(c_uint16) : The y pixel position of the intersection point.
			
			Notes:
			(1) This parameter is only used with preset 'User Position'.
			rotationAngle(c_double) : The rotation angle of the cut lines in degree. Postive values rotate against the clock.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_profile_cut_position(self.devSession, positionPresets, xPosition, yPosition, rotationAngle)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_calculation_area_mode(self, automatic, form):
		"""
		Get the method for determining the calculation area.
		
		Args:
			automatic(c_int16 use with byref) : The calculation mode
			
			VI_ON  = Automatic - The driver tries to automatically find a good calculation area for each image. It uses the form     parameter and the clip level set in <Set Auto Calculation Area Clip Level> as 							parameters.
			
			
			VI_OFF = User defined - The user defined rectangle/ellipse (dimensions defined in <Set User Calculation Area>) according to <form> 							is used as calculation area.
			
			You may pass VI_NULL if you don't need this value.
			form(c_uint8 use with byref) : The form of the calculation area. 
			Rectangle = 0
			Ellipse   = 1
			IsoAuto   = 2
			
			You may pass  VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_calculation_area_mode(self.devSession, automatic, form)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_calculation_area_mode(self, automaticCalculation, form):
		"""
		Select the method for determining the calculation area.
		
		Args:
			automaticCalculation(c_int16) : The calculation mode
			
			VI_ON  = Automatic - The driver tries to automatically find a good calculation area for each image. It uses the form     parameter and the clip level set in <Set Auto Calculation Area Clip Level> as 							parameters.
			
			
			VI_OFF = User defined - The user defined rectangle/ellipse (dimensions defined in <Set User Calculation Area>) according to <form> is used as calculation area.
			form(c_uint8) : The form of the calculation area. 
			Rectangle = 0
			Ellipse   = 1
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_calculation_area_mode(self.devSession, automaticCalculation, form)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_user_calculation_area(self, centerXPosition, centerYPosition, width, height, angle):
		"""
		Get the geometry of the user defined calculation area.
		
		These parameters only have effect on the calculation results if the calculation area mode is set to user defined.
		
		Args:
			centerXPosition(c_double use with byref) : Horizontal calculation area center pixel position.
			
			You may pass VI_NULL if you don't need this value.
			centerYPosition(c_double use with byref) : Vertical calculation area center pixel position.
			
			You may pass VI_NULL if you don't need this value.
			width(c_double use with byref) : Width of the calculation area in pixels before rotating by the angle.
			
			You may pass VI_NULL if you don't need this value.
			height(c_double use with byref) : Height of the calculation area in pixels before rotating by angle.
			
			You may pass VI_NULL if you don't need this value.
			angle(c_double use with byref) : The calculation area rotation angle in degree.
			
			The rectangle/ellipse defined by centerX, centerY, width, and height will be rotated by this angle. Positive values rotate against the clock.
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_user_calculation_area(self.devSession, centerXPosition, centerYPosition, width, height, angle)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_user_calculation_area(self, centerXPosition, centerYPosition, width, height, angle):
		"""
		Set the geometry of the user defined calculation area.
		
		These parameters only have effect on the calculation results if the calculation area mode is set to user defined.
		
		Args:
			centerXPosition(c_double) : Horizontal calculation area center pixel position.
			centerYPosition(c_double) : Vertical calculation area center pixel position.
			width(c_double) : Width of the calculation area in pixels before rotating by the angle.
			height(c_double) : Height of the calculation area in pixels before rotating by the angle.
			angle(c_double) : The calculation area rotation angle in degree. The rectangle/ellipse defined by left, top, width, and height will be rotated by this angle. Positive values rotate against the clock.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_user_calculation_area(self.devSession, centerXPosition, centerYPosition, width, height, angle)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_auto_calculation_area_clip_level(self, automaticClipLevel):
		"""
		Get the automatic calculation area clip level.
		
		This clip level is used when automatically determining a calculation area. The parameter only has an effect on the calculation results if the calculation area mode is set to automatic.
		
		Args:
			automaticClipLevel(c_double use with byref) : The clip level as fraction of the current image's peak intensity.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_auto_calculation_area_clip_level(self.devSession, automaticClipLevel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_auto_calculation_area_clip_level(self, automaticClipLevel):
		"""
		Sets the geometry for the calculation area.
		
		Args:
			automaticClipLevel(c_double) : Sets the percentage of intensities that are inside the calculation area. Range 0.0 to 1.0.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_auto_calculation_area_clip_level(self.devSession, automaticClipLevel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_intensity_threshold(self, useThreshold, threshold):
		"""
		Get the threshold of the calculation area. 
		The threshold is a percentage value between the highest possible intensity value (100%) and the baseline.
		
		pixel intensities below this threshold are not taken into account in the calculation.
		
		Args:
			useThreshold(c_int16 use with byref) : Turn the use of the theshold on or off
			
			VI_ON = Threshold is used
			VI_OFF = Theshold is ignored
			threshold(c_double use with byref) : The threshold is a percentage value between the highest possible intensity value (100%) and the baseline.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_intensity_threshold(self.devSession, useThreshold, threshold)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_intensity_threshold(self, useThreshold, threshold):
		"""
		Set the threshold of the calculation area. 
		The threshold is a percentage value between the highest possible intensity value (100%) and the baseline.
		
		pixel intensities below this threshold are not taken into account in the calculation.
		
		Args:
			useThreshold(c_int16)
			threshold(c_double) : The threshold is a percentage value between the highest possible intensity value (100%) and the baseline.
			
			Range 0.0 ... 1.0
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_intensity_threshold(self.devSession, useThreshold, threshold)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_max_hold(self, maxHold):
		"""
		Returns the max hold status.
		The max hold function holds the highest intensities over all frames and you get a envelope.
		
		Args:
			maxHold(c_int16 use with byref) : Gets the status of max hold.
			VI_ON  = Max hold is active
			VI_OFF = Max hold is inactive
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_max_hold(self.devSession, maxHold)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_max_hold(self, maxHold):
		"""
		Sets the max hold function active or inactive.
		
		Args:
			maxHold(c_int16) : Enable or disable the max hold function.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_max_hold(self.devSession, maxHold)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_ellipse_mode(self, mode):
		"""
		Returns the method how the ellipse is calculated.
		
		Args:
			mode(c_uint8 use with byref) : Gets the status of approximate ellipse
			0 = Contour of the clip level intensities
			1 = Approximated countour
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_ellipse_mode(self.devSession, mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_ellipse_mode(self, mode):
		"""
		Set the method how to calculate the ellipse.
		
		Args:
			mode(c_uint8) : The method how the ellipse is calculated.
			
			0 = Clip level contour is directly used to determine length and orientation of the major and minor axis.
			1 = An ellipse approximation algorithm is used on the clip level contour.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_ellipse_mode(self.devSession, mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_rotation_angle(self, rotationAngle):
		"""
		Returns the rotation angle for the ellipse calculation area in the m2 measurement.
		
		Args:
			rotationAngle(c_double use with byref) : Gets the rotation angle in degree ( 0 ... 360)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_rotation_angle(self.devSession, rotationAngle)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_rotation_angle(self, rotationAngle):
		"""
		Sets the rotation angle for the ellipse calculation area in the m2 measurement.
		
		Args:
			rotationAngle(c_double) : Sets the rotation angle in degree ( 0 ... 360)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_rotation_angle(self.devSession, rotationAngle)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_measurement_method(self, method):
		"""
		Get the measurement method.
		
		Args:
			method(c_uint8 use with byref) : The measurement method.
			0 = Full image camera beam profiler
			1 = Emulated slit beam profiler
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_measurement_method(self.devSession, method)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_measurement_method(self, method):
		"""
		Set the measurement method.
		
		The camera beam profiler can emulate a slit beam profiler. This can be useful to compare slit beam profiler measurements with the camera beam profiler's measurements.
		
		Args:
			method(c_uint8) : The measurement method.
			0 = Full image camera beam profiler (default)
			1 = Emulated slit beam profiler
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_measurement_method(self.devSession, method)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_black_level(self, blackLevel):
		"""
		Returns the noise level of the camera
		
		Args:
			blackLevel(c_double use with byref) : Noise level of the camera in digits (0 ... 4095)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_black_level(self.devSession, blackLevel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_black_level(self, blackLevel):
		"""
		Sets the noise level of the camera in the range 0 to 4095 digits
		
		Args:
			blackLevel(c_double) : Noise level of the camera in digits.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_black_level(self.devSession, blackLevel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_auto_black_level(self, autoBlackLevel):
		"""
		Enables or disables the auto black level
		
		Args:
			autoBlackLevel(c_int16) : State of the auto black level
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_auto_black_level(self.devSession, autoBlackLevel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_light_shielded_pixels(self, lightShieldedPixels):
		"""
		The LSP can be seen as 8 rows of black pixels at the bottom or top of the sensor when the whole sensor area is evenly illuminated.
		
		Args:
			lightShieldedPixels(c_uint32 use with byref) : Get Light Shielded Pixels
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_light_shielded_pixels(self.devSession, lightShieldedPixels)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def set_light_shielded_pixels(self, lightShieldedPixels):
		"""
		The LSP can be seen as 8 rows of black pixels at the bottom or top of the sensor when the whole sensor area is evenly illuminated.
		
		Args:
			lightShieldedPixels(c_uint32) : Number of rows that are used for dark level calculation.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_set_light_shielded_pixels(self.devSession, lightShieldedPixels)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_scan_data(self, scanData):
		"""
		This function reads out one image from the beam profiler camera according to the current acquisition parameters (see configuration functions).
		That image is immediately analysed according to the current image analye parameters (see calculation functions).
		The image and all analyze results are saved into the ScanData passed by reference.
		
		Args:
			scanData(TLBC1_Calculations use with byref) : Receives the all in one scan data including analysis                         results.
			
			The structure is defined in 09199_BC1/src/TLBC1_Calculations.h
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_scan_data(self.devSession, scanData)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def request_new_measurement(self):
		"""
		This function reads out a new image from the camera and does the calculations. The calculations are internally stored and can be get with the get_XXXX functions. 
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_request_new_measurement(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_image(self, pixelData, imageWidth, imageHeight, bytesPerPixel):
		"""
		This function reads out the processed scan data. 
		
		Args:
			pixelData( (c_uint8 * arrayLength)()) : Buffer with a size of 2448*2048*2 bytes.
			The pixel data will be copied into this buffer.
			imageWidth(c_uint16 use with byref) : Vertical count of pixel. Maximal 2448
			imageHeight(c_uint16 use with byref) : Horizontal count of pixel. Maximal 2048
			bytesPerPixel(c_uint8 use with byref) : Bytes per pixel ( 1 byte in Fast Mode, 2 bytes in precision mode)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_image(self.devSession, pixelData, imageWidth, imageHeight, bytesPerPixel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_fullsize_image(self, pixelData, imageWidth, imageHeight, bytesPerPixel):
		"""
		This function reads out the processed scan data. 
		
		Args:
			pixelData( (c_uint8 * arrayLength)()) : Buffer with a size of 2448*2048*2 bytes.
			The pixel data will be copied into this buffer.
			imageWidth(c_uint16 use with byref) : Vertical count of pixel. Maximal 2448
			imageHeight(c_uint16 use with byref) : Horizontal count of pixel. Maximal 2048
			bytesPerPixel(c_uint8 use with byref) : Bytes per pixel ( 1 byte in Fast Mode, 2 bytes in precision mode)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_fullsize_image(self.devSession, pixelData, imageWidth, imageHeight, bytesPerPixel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_baseLevel(self, baseLevel):
		"""
		Returns the base level in digits
		
		Args:
			baseLevel(c_double use with byref) : Base Level in digits
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_baseLevel(self.devSession, baseLevel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_profiles(self, profileX, profileY):
		"""
		This function copies the profile data into the given buffer.
		
		Args:
			profileX( (c_double * arrayLength)()) : Buffer with a size of 2448*2 bytes.
			The pixel data will be copied into this buffer.
			profileY( (c_double * arrayLength)()) : Buffer with a size of 2048*2 bytes.
			The pixel data will be copied into this buffer.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_profiles(self.devSession, profileX, profileY)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_peak(self, peakIntensity, peakPositionX, peakPositionY):
		"""
		This function returns the peak intensity pixel position relative to the top left corner of the image (0; 0).
		The peak intensity pixel has the highest intensity of all pixels inside the calculation area.
		
		
		Args:
			peakIntensity(c_uint16 use with byref) : Intensity in digits of the pixel.
			Maximal 4096 in precision mode and 255 in fast mode.
			peakPositionX(c_uint16 use with byref) : Index of the highest pixel in vertical direction.
			peakPositionY(c_uint16 use with byref) : Index of the highest pixel in horizontal direction.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_peak(self.devSession, peakIntensity, peakPositionX, peakPositionY)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_saturation(self, saturation, saturatedPixel):
		"""
		Get the saturation level.
		
		Saturation level of the instrument's AD converter for the current image. For a good SNR (signal-to-noise ratio), the saturation level should be not below 40 % and not beyond 95 %.
		
		Args:
			saturation(c_double use with byref) : The saturation level is the ratio of the highest intensity in the scan to the dynamic range of the sensor. (Value range 0.0 ... 1.0)
			
			You may pass VI_NULL if you don't need this value.
			saturatedPixel(c_double use with byref) : Ratio of the amount of saturated pixels to amount of pixels inside the calculation area (value range 0.0 ... 1.0).
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_saturation(self.devSession, saturation, saturatedPixel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_centroid(self, centroidPositionX, centroidPositionY):
		"""
		This function returns the centroid pixel position relative to the top left corner of the image (0; 0).
		
		Args:
			centroidPositionX(c_double use with byref) : Index of the centroid pixel in vertical direction.
			centroidPositionY(c_double use with byref) : Index of the centroid pixel in horizontal direction.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_centroid(self.devSession, centroidPositionX, centroidPositionY)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_power(self, totalPower):
		"""
		This function returns the power value in dBm.
		
		Args:
			totalPower(c_double use with byref) : Returns the total power in dBm.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_power(self.devSession, totalPower)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_peak_power_density(self, peakPowerDensity):
		"""
		Get the measured peak power density. That is the power on the peak pixel divided by its area.
		
		Args:
			peakPowerDensity(c_double use with byref) : The peak power density in mW/µm².
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_peak_power_density(self.devSession, peakPowerDensity)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_beam_width(self, beamWidthClipX, beamWidthClipY, sigmaX, sigmaY):
		"""
		This function returns the measured beam width.
		
		Args:
			beamWidthClipX(c_double use with byref) : Beam Width Clip is measured from the peak down to the clip level .
			beamWidthClipY(c_double use with byref) : Beam Width Clip is measured from the peak down to the clip level .
			sigmaX(c_double use with byref) : Second Moment
			sigmaY(c_double use with byref) : Second Moment in y direction.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_beam_width(self.devSession, beamWidthClipX, beamWidthClipY, sigmaX, sigmaY)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_beam_width_4_sigma(self, beamWidth_4Sigma_X, beamWidth_4Sigma_Y, beamWidth_4Sigma_X_Norm, beamWidth_4Sigma_Y_Norm, azimuthAngle_4Sigma, ellipticity_4Sigma):
		"""
		This function returns the measured beam width 4 sigma values.
		
		Args:
			beamWidth_4Sigma_X(c_double use with byref) : Beam Width 4 sigma value (  = second moment multiplied by 4) in x direction
			
			beamWidth_4Sigma_Y(c_double use with byref) : Beam Width 4 sigma value (  = second moment multiplied by 4) in y direction
			
			beamWidth_4Sigma_X_Norm(c_double use with byref) : Beam Width 4 sigma value (= second moment multiplied by 4) in x' direction ( rotated and normalized coordinate system)
			
			beamWidth_4Sigma_Y_Norm(c_double use with byref) : Beam Width 4 sigma value (= second moment multiplied by 4) in y' direction ( rotated and normalized coordinate system)
			
			azimuthAngle_4Sigma(c_double use with byref) : Angle between the original coordinate system (x and y ) and the rotated coordinate system (x' and y')
			ellipticity_4Sigma(c_double use with byref) : Ellipticity of the beam calculated from the second moments
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_beam_width_4_sigma(self.devSession, beamWidth_4Sigma_X, beamWidth_4Sigma_Y, beamWidth_4Sigma_X_Norm, beamWidth_4Sigma_Y_Norm, azimuthAngle_4Sigma, ellipticity_4Sigma)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_gaussian(self, intensityX, intensityY, ratingX, ratingY, diameterX, diameterY):
		"""
		This function returns the gaussian fit parameter
		
		Args:
			intensityX(c_double use with byref) : Highest point of the gaussian fit in digits
			intensityY(c_double use with byref) : Highest point of the gaussian fit in digits
			ratingX(c_double use with byref) : Percentage ot the match between the gaussian fit and the measured profile.
			ratingY(c_double use with byref) : Percentage ot the match between the gaussian fit and the measured profile.
			diameterX(c_double use with byref) : Second Moment
			diameterY(c_double use with byref) : Second Moment in y direction.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_gaussian(self.devSession, intensityX, intensityY, ratingX, ratingY, diameterX, diameterY)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_actual_calculation_area(self, centerXPosition, centerYPosition, width, height, angle):
		"""
		Get the geometry of the actually used calculation area.
		
		If calculation area mode is 'user defined' this function will return the same data as was set in <Set User Calculation Area>.
		If calculation area mode is 'auto' this function will return the automatically found geometry. For the form see <Set Calculation Area Mode>.
		
		Args:
			centerXPosition(c_double use with byref) : Horizontal calculation area center pixel position.
			
			You may pass VI_NULL if you don't need this value.
			centerYPosition(c_double use with byref) : Vertical calculation area center pixel position.
			
			You may pass VI_NULL if you don't need this value.
			width(c_double use with byref) : Width of the calculation area in pixels before rotating by the angle.
			
			You may pass VI_NULL if you don't need this value.
			height(c_double use with byref) : Height of the calculation area in pixels before rotating by angle.
			
			You may pass VI_NULL if you don't need this value.
			angle(c_double use with byref) : The calculation area rotation angle in degree.
			
			The rectangle/ellipse defined by centerX, centerY, width, and height will be rotated by this angle. Positive values rotate against the clock.
			
			You may pass VI_NULL if you don't need this value.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_actual_calculation_area(self.devSession, centerXPosition, centerYPosition, width, height, angle)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_ellipse_diameters(self, minorAxisDiameter, majorAxisDiameter, meanDiameter):
		"""
		Get the calculated ellipse diameters.
		
		Args:
			minorAxisDiameter(c_double use with byref) : Ellipse minor axis diameter in [pixel].
			
			You may pass VI_NULL if this parameter is not required.
			majorAxisDiameter(c_double use with byref) : Ellipse major axis diameter in [pixel].
			
			You may pass VI_NULL if this parameter is not required.
			meanDiameter(c_double use with byref) : Ellipse diameter arithmetic mean value in [pixel].
			
			You may pass VI_NULL if this parameter is not required.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_ellipse_diameters(self.devSession, minorAxisDiameter, majorAxisDiameter, meanDiameter)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_ellipse_geometry(self, orientation, ellipticity, eccentricity, centerXPosition, centerYPosition):
		"""
		Get the calculated ellipse geometry.
		
		Args:
			orientation(c_double use with byref) : Ellipse orientation angle in degree.
			
			You may pass VI_NULL if this parameter is not required.
			ellipticity(c_double use with byref) : The ellipse's ratio of minor axis diameter to major axis diameter.
			
			You may pass VI_NULL if this parameter is not required.
			eccentricity(c_double use with byref) : The ellipse's eccentricity.
			
			You may pass VI_NULL if this parameter is not required.
			centerXPosition(c_double use with byref) : Ellipse center x pixel position.
			
			You may pass VI_NULL if this parameter is not required.
			centerYPosition(c_double use with byref) : Ellipse center y pixel position.
			
			You may pass VI_NULL if this parameter is not required.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_ellipse_geometry(self.devSession, orientation, ellipticity, eccentricity, centerXPosition, centerYPosition)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_effective_area(self, effectiveArea):
		"""
		Get the effective area.
		
		Args:
			effectiveArea(c_double use with byref) : Area of an ideal flat top beam with same peak intensity as the measured beam in µm².
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_effective_area(self.devSession, effectiveArea)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def get_temperature(self, temperature):
		"""
		Get the temperature near the camera sensor in Celsius Degrees.
		
		Args:
			temperature(c_double use with byref) : The camera sensor temperature in Celsius Degrees.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLBC2_get_temperature(self.devSession, temperature)
		self.__testForError(pInvokeResult)
		return pInvokeResult

