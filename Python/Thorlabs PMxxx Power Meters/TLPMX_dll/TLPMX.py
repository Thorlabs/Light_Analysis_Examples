import os
from ctypes import cdll,c_long,c_uint32,c_uint16,c_uint8,byref,create_string_buffer,c_bool, c_char, c_char_p,c_int,c_int16,c_int8,c_double,c_float,sizeof,c_voidp, Structure

_VI_ERROR = (-2147483647-1)
VI_ON = 1
VI_OFF = 0
TLPM_VID_THORLABS = (0x1313)  # Thorlabs
TLPM_PID_TLPM_DFU = (0x8070)  # PM100D with DFU interface enabled
TLPM_PID_PM100A_DFU = (0x8071)  # PM100A with DFU interface enabled
TLPM_PID_PM100USB = (0x8072)  # PM100USB with DFU interface enabled
TLPM_PID_PM160USB_DFU = (0x8073)  # PM160 on USB with DFU interface enabled
TLPM_PID_PM160TUSB_DFU = (0x8074)  # PM160T on USB with DFU interface enabled
TLPM_PID_PM400_DFU = (0x8075)  # PM400 on USB with DFU interface enabled
TLPM_PID_PM101_DFU = (0x8076)  # PM101 on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM102_DFU = (0x8077)  # PM102 on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM103_DFU = (0x807A)  # PM103 on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM100D = (0x8078)  # PM100D w/o DFU interface
TLPM_PID_PM100A = (0x8079)  # PM100A w/o DFU interface
TLPM_PID_PM160USB = (0x807B)  # PM160 on USB w/o DFU interface
TLPM_PID_PM160TUSB = (0x807C)  # PM160T on USB w/o DFU interface
TLPM_PID_PM400 = (0x807D)  # PM400 on USB w/o DFU interface
TLPM_PID_PM101 = (0x807E)  # reserved
TLPM_PID_PMTest = (0x807F)  # PM Test Platform
TLPM_PID_PM200 = (0x80B0)  # PM200
TLPM_PID_PM5020 = (0x80BB)  # PM5020 1 channel benchtop powermeter (Interface 0 TMC, Interface 1 DFU)
TLPM_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8070 || VI_ATTR_MODEL_CODE==0x8078)}"
PM100A_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8071 || VI_ATTR_MODEL_CODE==0x8079)}"
PM100USB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x8072}"
PM160USB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8073 || VI_ATTR_MODEL_CODE==0x807B)}"
PM160TUSB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8074 || VI_ATTR_MODEL_CODE==0x807C)}"
PM200_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x80B0}"
PM400_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8075 || VI_ATTR_MODEL_CODE==0x807D)}"
PM101_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8076)}"
PM102_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8077)}"
PM103_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x807A}"
PMTest_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x807F}"
PM100_FIND_PATTERN = "USB?*::0x1313::0x807?::?*::INSTR"
PM5020_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x80BB}"
PMxxx_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8070 || VI_ATTR_MODEL_CODE==0x8078 || " \
"VI_ATTR_MODEL_CODE==0x8071 || VI_ATTR_MODEL_CODE==0x8079 || " \
"VI_ATTR_MODEL_CODE==0x8072 || " \
"VI_ATTR_MODEL_CODE==0x8073 || VI_ATTR_MODEL_CODE==0x807B || " \
"VI_ATTR_MODEL_CODE==0x8074 || VI_ATTR_MODEL_CODE==0x807C || " \
"VI_ATTR_MODEL_CODE==0x8075 || VI_ATTR_MODEL_CODE==0x807D || " \
"VI_ATTR_MODEL_CODE==0x8076 || VI_ATTR_MODEL_CODE==0x807E || " \
"VI_ATTR_MODEL_CODE==0x8077 || VI_ATTR_MODEL_CODE==0x807F || " \
"VI_ATTR_MODEL_CODE==0x807A || VI_ATTR_MODEL_CODE==0x80BB ||" \
"VI_ATTR_MODEL_CODE==0x80B0)}"
PMBT_FIND_PATTERN = "ASRL?*::INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x807C || VI_ATTR_MODEL_CODE==0x807B)}"
PMUART_FIND_PATTERN_VISA = "ASRL?*::INSTR"
PMUART_FIND_PATTERN_COM = "COM?*"
TLPM_BUFFER_SIZE = 256  # General buffer size
TLPM_ERR_DESCR_BUFFER_SIZE = 512  # Buffer size for error messages
VI_INSTR_WARNING_OFFSET = (0x3FFC0900 )
VI_INSTR_ERROR_OFFSET = (_VI_ERROR + 0x3FFC0900 )
VI_INSTR_ERROR_NOT_SUPP_INTF = (VI_INSTR_ERROR_OFFSET + 0x01 )
VI_INSTR_WARN_OVERFLOW = (VI_INSTR_WARNING_OFFSET + 0x01 )
VI_INSTR_WARN_UNDERRUN = (VI_INSTR_WARNING_OFFSET + 0x02 )
VI_INSTR_WARN_NAN = (VI_INSTR_WARNING_OFFSET + 0x03 )
TLPM_ATTR_SET_VAL = (0)
TLPM_ATTR_MIN_VAL = (1)
TLPM_ATTR_MAX_VAL = (2)
TLPM_ATTR_DFLT_VAL = (3)
TLPM_ATTR_AUTO_VAL = (9)
TLPM_DEFAULT_CHANNEL = (1)
TLPM_SENSOR_CHANNEL1 = (1)
TLPM_SENSOR_CHANNEL2 = (2)
TLPM_INDEX_1 = (1)
TLPM_INDEX_2 = (2)
TLPM_INDEX_3 = (3)
TLPM_INDEX_4 = (4)
TLPM_INDEX_5 = (5)
TLPM_PEAK_FILTER_NONE = (0)
TLPM_PEAK_FILTER_OVER = (1)
TLPM_REG_STB = (0)  # < Status Byte Register
TLPM_REG_SRE = (1)  # < Service Request Enable
TLPM_REG_ESB = (2)  # < Standard Event Status Register
TLPM_REG_ESE = (3)  # < Standard Event Enable
TLPM_REG_OPER_COND = (4)  # < Operation Condition Register
TLPM_REG_OPER_EVENT = (5)  # < Operation Event Register
TLPM_REG_OPER_ENAB = (6)  # < Operation Event Enable Register
TLPM_REG_OPER_PTR = (7)  # < Operation Positive Transition Filter
TLPM_REG_OPER_NTR = (8)  # < Operation Negative Transition Filter
TLPM_REG_QUES_COND = (9)  # < Questionable Condition Register
TLPM_REG_QUES_EVENT = (10)  # < Questionable Event Register
TLPM_REG_QUES_ENAB = (11)  # < Questionable Event Enable Reg.
TLPM_REG_QUES_PTR = (12)  # < Questionable Positive Transition Filter
TLPM_REG_QUES_NTR = (13)  # < Questionable Negative Transition Filter
TLPM_REG_MEAS_COND = (14)  # < Measurement Condition Register
TLPM_REG_MEAS_EVENT = (15)  # < Measurement Event Register
TLPM_REG_MEAS_ENAB = (16)  # < Measurement Event Enable Register
TLPM_REG_MEAS_PTR = (17)  # < Measurement Positive Transition Filter
TLPM_REG_MEAS_NTR = (18)  # < Measurement Negative Transition Filter
TLPM_REG_AUX_COND = (19)  # < Auxiliary Condition Register
TLPM_REG_AUX_EVENT = (20)  # < Auxiliary Event Register
TLPM_REG_AUX_ENAB = (21)  # < Auxiliary Event Enable Register
TLPM_REG_AUX_PTR = (22)  # < Auxiliary Positive Transition Filter
TLPM_REG_AUX_NTR = (23)  # < Auxiliary Negative Transition Filter
TLPM_REG_OPER_COND_1 = (24)  # < Operation Condition Register Channel 1
TLPM_REG_OPER_COND_2 = (25)  # < Operation Condition Register Channel 2
TLPM_REG_AUX_DET_COND = (26)  # < Auxiliary Condition Register DET
TLPM_STATBIT_STB_AUX = (0x01)  # < Auxiliary summary
TLPM_STATBIT_STB_MEAS = (0x02)  # < Device Measurement Summary
TLPM_STATBIT_STB_EAV = (0x04)  # < Error available
TLPM_STATBIT_STB_QUES = (0x08)  # < Questionable Status Summary
TLPM_STATBIT_STB_MAV = (0x10)  # < Message available
TLPM_STATBIT_STB_ESB = (0x20)  # < Event Status Bit
TLPM_STATBIT_STB_MSS = (0x40)  # < Master summary status
TLPM_STATBIT_STB_OPER = (0x80)  # < Operation Status Summary
TLPM_STATBIT_ESR_OPC = (0x01)  # < Operation complete
TLPM_STATBIT_ESR_RQC = (0x02)  # < Request control
TLPM_STATBIT_ESR_QYE = (0x04)  # < Query error
TLPM_STATBIT_ESR_DDE = (0x08)  # < Device-Specific error
TLPM_STATBIT_ESR_EXE = (0x10)  # < Execution error
TLPM_STATBIT_ESR_CME = (0x20)  # < Command error
TLPM_STATBIT_ESR_URQ = (0x40)  # < User request
TLPM_STATBIT_ESR_PON = (0x80)  # < Power on
TLPM_STATBIT_QUES_VOLT = (0x0001)  # < questionable voltage measurement
TLPM_STATBIT_QUES_CURR = (0x0002)  # < questionable current measurement
TLPM_STATBIT_QUES_TIME = (0x0004)  # < questionable time measurement
TLPM_STATBIT_QUES_POW = (0x0008)  # < questionable power measurement
TLPM_STATBIT_QUES_TEMP = (0x0010)  # < questionable temperature measurement
TLPM_STATBIT_QUES_FREQ = (0x0020)  # < questionable frequency measurement
TLPM_STATBIT_QUES_PHAS = (0x0040)  # < questionable phase measurement
TLPM_STATBIT_QUES_MOD = (0x0080)  # < questionable modulation measurement
TLPM_STATBIT_QUES_CAL = (0x0100)  # < questionable calibration
TLPM_STATBIT_QUES_ENER = (0x0200)  # < questionable energy measurement
TLPM_STATBIT_QUES_10 = (0x0400)  # < reserved
TLPM_STATBIT_QUES_11 = (0x0800)  # < reserved
TLPM_STATBIT_QUES_12 = (0x1000)  # < reserved
TLPM_STATBIT_QUES_INST = (0x2000)  # < instrument summary
TLPM_STATBIT_QUES_WARN = (0x4000)  # < command warning
TLPM_STATBIT_QUES_15 = (0x8000)  # < reserved
TLPM_STATBIT_OPER_CAL = (0x0001)  # < The instrument is currently performing a calibration.
TLPM_STATBIT_OPER_SETT = (0x0002)  # < The instrument is waiting for signals it controls to stabilize enough to begin measurements.
TLPM_STATBIT_OPER_RANG = (0x0004)  # < The instrument is currently changing its range.
TLPM_STATBIT_OPER_SWE = (0x0008)  # < A sweep is in progress.
TLPM_STATBIT_OPER_MEAS = (0x0010)  # < The instrument is actively measuring.
TLPM_STATBIT_OPER_TRIG = (0x0020)  # < The instrument is in a �wait for trigger� state of the trigger model.
TLPM_STATBIT_OPER_ARM = (0x0040)  # < The instrument is in a �wait for arm� state of the trigger model.
TLPM_STATBIT_OPER_CORR = (0x0080)  # < The instrument is currently performing a correction (Auto-PID tune).
TLPM_STATBIT_OPER_SENS = (0x0100)  # < Optical powermeter sensor connected and operable.
TLPM_STATBIT_OPER_DATA = (0x0200)  # < Measurement data ready for fetch.
TLPM_STATBIT_OPER_THAC = (0x0400)  # < Thermopile accelerator active.
TLPM_STATBIT_OPER_11 = (0x0800)  # < reserved
TLPM_STATBIT_OPER_12 = (0x1000)  # < reserved
TLPM_STATBIT_OPER_INST = (0x2000)  # < One of n multiple logical instruments is reporting OPERational status.
TLPM_STATBIT_OPER_PROG = (0x4000)  # < A user-defined programming is currently in the run state.
TLPM_STATBIT_OPER_15 = (0x8000)  # < reserved
TLPM_STATBIT_MEAS_0 = (0x0001)  # < reserved
TLPM_STATBIT_MEAS_1 = (0x0002)  # < reserved
TLPM_STATBIT_MEAS_2 = (0x0004)  # < reserved
TLPM_STATBIT_MEAS_3 = (0x0008)  # < reserved
TLPM_STATBIT_MEAS_4 = (0x0010)  # < reserved
TLPM_STATBIT_MEAS_5 = (0x0020)  # < reserved
TLPM_STATBIT_MEAS_6 = (0x0040)  # < reserved
TLPM_STATBIT_MEAS_7 = (0x0080)  # < reserved
TLPM_STATBIT_MEAS_8 = (0x0100)  # < reserved
TLPM_STATBIT_MEAS_9 = (0x0200)  # < reserved
TLPM_STATBIT_MEAS_10 = (0x0400)  # < reserved
TLPM_STATBIT_MEAS_11 = (0x0800)  # < reserved
TLPM_STATBIT_MEAS_12 = (0x1000)  # < reserved
TLPM_STATBIT_MEAS_13 = (0x2000)  # < reserved
TLPM_STATBIT_MEAS_14 = (0x4000)  # < reserved
TLPM_STATBIT_MEAS_15 = (0x8000)  # < reserved
TLPM_STATBIT_AUX_NTC = (0x0001)  # < Auxiliary NTC temperature sensor connected.
TLPM_STATBIT_AUX_EMM = (0x0002)  # < External measurement module connected.
TLPM_STATBIT_AUX_UPCS = (0x0004)  # < User Power Calibration supported by this instrument
TLPM_STATBIT_AUX_UPCA = (0x0008)  # < User Power Calibration active status
TLPM_STATBIT_AUX_EXPS = (0x0010)  # < External power supply connected
TLPM_STATBIT_AUX_BATC = (0x0020)  # < Battery charging
TLPM_STATBIT_AUX_BATL = (0x0040)  # < Battery low
TLPM_STATBIT_AUX_IPS = (0x0080)  # < Apple(tm) authentification supported. True if an authentification co-processor is installed.
TLPM_STATBIT_AUX_IPF = (0x0100)  # < Apple(tm) authentification failed. True if the authentification setup procedure failed.
TLPM_STATBIT_AUX_9 = (0x0200)  # < reserved
TLPM_STATBIT_AUX_10 = (0x0400)  # < reserved
TLPM_STATBIT_AUX_11 = (0x0800)  # < reserved
TLPM_STATBIT_AUX_12 = (0x1000)  # < reserved
TLPM_STATBIT_AUX_13 = (0x2000)  # < reserved
TLPM_STATBIT_AUX_14 = (0x4000)  # < reserved
TLPM_STATBIT_AUX_15 = (0x8000)  # < reserved
TLPM_WINTERTIME = (0)
TLPM_SUMMERTIME = (1)
TLPM_LINE_FREQ_50 = (50)  # < line frequency in Hz
TLPM_LINE_FREQ_60 = (60)  # < line frequency in Hz
TLPM_INPUT_FILTER_STATE_OFF = (0)
TLPM_INPUT_FILTER_STATE_ON = (1)
TLPM_ACCELERATION_STATE_OFF = (0)
TLPM_ACCELERATION_STATE_ON = (1)
TLPM_ACCELERATION_MANUAL = (0)
TLPM_ACCELERATION_AUTO = (1)
TLPM_STAT_DARK_ADJUST_FINISHED = (0)
TLPM_STAT_DARK_ADJUST_RUNNING = (1)
TLPM_AUTORANGE_CURRENT_OFF = (0)
TLPM_AUTORANGE_CURRENT_ON = (1)
TLPM_CURRENT_REF_OFF = (0)
TLPM_CURRENT_REF_ON = (1)
TLPM_ENERGY_REF_OFF = (0)
TLPM_ENERGY_REF_ON = (1)
TLPM_FREQ_MODE_CW = (0)
TLPM_FREQ_MODE_PEAK = (1)
TLPM_AUTORANGE_POWER_OFF = (0)
TLPM_AUTORANGE_POWER_ON = (1)
TLPM_POWER_REF_OFF = (0)
TLPM_POWER_REF_ON = (1)
TLPM_POWER_UNIT_WATT = (0)
TLPM_POWER_UNIT_DBM = (1)
SENSOR_SWITCH_POS_1 = (1)
SENSOR_SWITCH_POS_2 = (2)
TLPM_AUTORANGE_VOLTAGE_OFF = (0)
TLPM_AUTORANGE_VOLTAGE_ON = (1)
TLPM_VOLTAGE_REF_OFF = (0)
TLPM_VOLTAGE_REF_ON = (1)
TLPM_ANALOG_ROUTE_PUR = (0)
TLPM_ANALOG_ROUTE_CBA = (1)
TLPM_ANALOG_ROUTE_CMA = (2)
TLPM_ANALOG_ROUTE_GEN = (3)
TLPM_IODIR_INP = (VI_OFF)
TLPM_IODIR_OUTP = (VI_ON)
TLPM_IOLVL_LOW = (VI_OFF)
TLPM_IOLVL_HIGH = (VI_ON)
DIGITAL_IO_CONFIG_INPUT = (0)
DIGITAL_IO_CONFIG_OUTPUT = (1)
DIGITAL_IO_CONFIG_INPUT_ALT = (2)
DIGITAL_IO_CONFIG_OUTPUT_ALT = (3)
I2C_OPER_INTER = (0)
I2C_OPER_SLOW = (1)
I2C_OPER_FAST = (2)
FAN_OPER_OFF = (0)
FAN_OPER_FULL = (1)
FAN_OPER_OPEN_LOOP = (2)
FAN_OPER_CLOSED_LOOP = (3)
FAN_OPER_TEMPER_CTRL = (4)
FAN_TEMPER_SRC_HEAD = (0)
FAN_TEMPER_SRC_EXT_NTC = (1)
SENSOR_TYPE_NONE = 0x0  # No sensor. This value is used to mark sensor data for 'no sensor connected'.
SENSOR_TYPE_PD_SINGLE = 0x1  # Single photodiode sensor. Only one ipd input active at the same time.
SENSOR_TYPE_THERMO = 0x2  # Thermopile sensor
SENSOR_TYPE_PYRO = 0x3  # Pyroelectric sensor
SENSOR_TYPE_4Q = 0x4  # 4Q Sensor
SENSOR_SUBTYPE_NONE = 0x0  # No sensor. This value is used to mark RAM data structure for 'no sensor connected'. Do not write this value to the EEPROM.
SENSOR_SUBTYPE_PD_ADAPTER = 0x01  # Photodiode adapter (no temperature sensor)
SENSOR_SUBTYPE_PD_SINGLE_STD = 0x02  # Standard single photodiode sensor (no temperature sensor)
SENSOR_SUBTYPE_PD_SINGLE_FSR = 0x03  # One single photodiode. Filter position set by a slide on the sensor selects responsivity data set to use. (no temperature sensor)
SENSOR_SUBTYPE_PD_SINGLE_STD_T = 0x12  # Standard single photodiode sensor (with temperature sensor)
SENSOR_SUBTYPE_THERMO_ADAPTER = 0x01  # Thermopile adapter (no temperature sensor)
SENSOR_SUBTYPE_THERMO_STD = 0x02  # Standard thermopile sensor (no temperature sensor)
SENSOR_SUBTYPE_THERMO_STD_T = 0x12  # Standard thermopile sensor (with temperature sensor)
SENSOR_SUBTYPE_PYRO_ADAPTER = 0x01  # Pyroelectric adapter (no temperature sensor)
SENSOR_SUBTYPE_PYRO_STD = 0x02  # Standard pyroelectric sensor (no temperature sensor)
SENSOR_SUBTYPE_PYRO_STD_T = 0x12  # Standard pyroelectric sensor (with temperature sensor)
TLPM_SENS_FLAG_IS_POWER = 0x0001  # Power sensor
TLPM_SENS_FLAG_IS_ENERGY = 0x0002  # Energy sensor
TLPM_SENS_FLAG_IS_RESP_SET = 0x0010  # Responsivity settable
TLPM_SENS_FLAG_IS_WAVEL_SET = 0x0020  # Wavelength settable
TLPM_SENS_FLAG_IS_TAU_SET = 0x0040  # Time constant tau settable
TLPM_SENS_FLAG_HAS_TEMP = 0x0100  # Temperature sensor included

class TLPMX:

	def __init__(self, resourceName = None, IDQuery = False, resetDevice = False):
		"""
		This function initializes the instrument driver session and performs the following initialization actions:
		
		(1) Opens a session to the Default Resource Manager resource and a session to the specified device using the Resource Name.
		(2) Performs an identification query on the instrument.
		(3) Resets the instrument to a known state.
		(4) Sends initialization commands to the instrument.
		(5) Returns an instrument handle which is used to distinguish between different sessions of this instrument driver.
		
		Notes:
		(1) Each time this function is invoked a unique session is opened.  
		
		Args:
			resourceName (create_string_buffer)
			IDQuery (c_bool):This parameter specifies whether an identification query is performed during the initialization process.
			
			VI_TRUE  (1): Do query (default).
			VI_FALSE (0): Skip query.
			
			
			resetDevice (c_bool):This parameter specifies whether the instrument is reset during the initialization process.
			
			VI_TRUE  (1) - instrument is reset (default)
			VI_FALSE (0) - no reset 
			
			
		"""
		if sizeof(c_voidp) == 4:
			dll_name = "TLPMX_32.dll"
			dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
			self.dll = cdll.LoadLibrary(dllabspath)
		else:
			dll_name = "TLPMX_64.dll"
			dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
			self.dll = cdll.LoadLibrary(dllabspath)

		self.devSession = c_long()
		self.devSession.value = 0
		if resourceName!= None:
			pInvokeResult = self.dll.TLPMX_init(resourceName, IDQuery, resetDevice, byref(self.devSession))
			self.__testForError(pInvokeResult)


	def __testForError(self, status):
		if status < 0:
			self.__throwError(status)
		return status

	def __throwError(self, code):
		msg = create_string_buffer(1024)
		self.dll.TLPMX_errorMessage(self.devSession, c_int(code), msg)
		raise NameError(c_char_p(msg.raw).value)

	def open(self, resourceName, IDQuery, resetDevice):
		"""
		This function initializes the instrument driver session and performs the following initialization actions:
		
		(1) Opens a session to the Default Resource Manager resource and a session to the specified device using the Resource Name.
		(2) Performs an identification query on the instrument.
		(3) Resets the instrument to a known state.
		(4) Sends initialization commands to the instrument.
		(5) Returns an instrument handle which is used to distinguish between different sessions of this instrument driver.
		
		Notes:
		(1) Each time this function is invoked a unique session is opened.  
		
		Args:
			resourceName (create_string_buffer)
			IDQuery (c_bool):This parameter specifies whether an identification query is performed during the initialization process.
			
			VI_TRUE  (1): Do query (default).
			VI_FALSE (0): Skip query.
			
			
			resetDevice (c_bool):This parameter specifies whether the instrument is reset during the initialization process.
			
			VI_TRUE  (1) - instrument is reset (default)
			VI_FALSE (0) - no reset 
			
			
		Returns:
			int: The return value, 0 is for success
		"""
		self.dll.TLPMX_close(self.devSession)
		self.devSession.value = 0
		pInvokeResult = self.dll.TLPMX_init(resourceName, IDQuery, resetDevice, byref(self.devSession))
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def close(self):
		"""
		This function closes the instrument driver session.
		
		Note: The instrument must be reinitialized to use it again.
		
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_close(self.devSession)
		return pInvokeResult

	def findRsrc(self, resourceCount):
		"""
		This function finds all driver compatible devices attached to the PC and returns the number of found devices.
		
		Note:
		(1) The function additionally stores information like system name about the found resources internally. This information can be retrieved with further functions from the class, e.g. <Get Resource Description> and <Get Resource Information>.
		
		
		Args:
			resourceCount(c_uint32 use with byref) : The number of connected devices that are supported by this driver.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_findRsrc(self.devSession, resourceCount)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getRsrcName(self, index, resourceName):
		"""
		This function gets the resource name string needed to open a device with <Initialize>.
		
		Notes:
		(1) The data provided by this function was updated at the last call of <Find Resources>.
		
		Args:
			index(c_uint32) : This parameter accepts the index of the device to get the resource descriptor from.
			
			Notes: 
			(1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.
			
			resourceName(create_string_buffer(1024)) : This parameter returns the resource descriptor. Use this descriptor to specify the device in <Initialize>.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getRsrcName(self.devSession, index, resourceName)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getRsrcInfo(self, index, modelName, serialNumber, manufacturer, deviceAvailable):
		"""
		This function gets information about a connected resource.
		
		Notes:
		(1) The data provided by this function was updated at the last call of <Find Resources>.
		
		Args:
			index(c_uint32) : This parameter accepts the index of the device to get the resource descriptor from.
			
			Notes: 
			(1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.
			
			modelName(create_string_buffer(1024)) : This parameter returns the model name of the device.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) Serial interfaces over Bluetooth will return the interface name instead of the device model name.
			serialNumber(create_string_buffer(1024)) : This parameter returns the serial number of the device.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) The serial number is not available for serial interfaces over Bluetooth.
			manufacturer(create_string_buffer(1024)) : This parameter returns the manufacturer name of the device.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) The manufacturer name is not available for serial interfaces over Bluetooth.
			deviceAvailable(c_int16 use with byref) : Returns the information if the device is available.
			Devices that are not available are used by other applications.
			
			Notes:
			(1) You may pass VI_NULL if you do not need this parameter.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getRsrcInfo(self.devSession, index, modelName, serialNumber, manufacturer, deviceAvailable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def writeRegister(self, reg, value):
		"""
		This function writes the content of any writable instrument register. Refer to your instrument's user's manual for more details on status structure registers.
		
		
		Args:
			reg(c_int16) : Specifies the register to be used for operation. This parameter can be any of the following constants:
			
			  TLPM_REG_SRE         (1): Service Request Enable
			  TLPM_REG_ESE         (3): Standard Event Enable
			  TLPM_REG_OPER_ENAB   (6): Operation Event Enable Register
			  TLPM_REG_OPER_PTR    (7): Operation Positive Transition
			  TLPM_REG_OPER_NTR    (8): Operation Negative Transition
			  TLPM_REG_QUES_ENAB  (11): Questionable Event Enable Reg.
			  TLPM_REG_QUES_PTR   (12): Questionable Positive Transition
			  TLPM_REG_QUES_NTR   (13): Questionable Negative Transition
			  TLPM_REG_MEAS_ENAB  (16): Measurement Event Enable Register
			  TLPM_REG_MEAS_PTR   (17): Measurement Positive Transition
			  TLPM_REG_MEAS_NTR   (18): Measurement Negative Transition
			  TLPM_REG_AUX_ENAB   (21): Auxiliary Event Enable Register
			  TLPM_REG_AUX_PTR    (22): Auxiliary Positive Transition
			  TLPM_REG_AUX_NTR    (23): Auxiliary Negative Transition 
			
			value(c_int16) : This parameter specifies the new value of the selected register.
			
			These register bits are defined:
			
			STATUS BYTE bits (see IEEE488.2-1992 §11.2)
			TLPM_STATBIT_STB_AUX        (0x01): Auxiliary summary
			TLPM_STATBIT_STB_MEAS       (0x02): Device Measurement Summary
			TLPM_STATBIT_STB_EAV        (0x04): Error available
			TLPM_STATBIT_STB_QUES       (0x08): Questionable Status Summary
			TLPM_STATBIT_STB_MAV        (0x10): Message available
			TLPM_STATBIT_STB_ESB        (0x20): Event Status Bit
			TLPM_STATBIT_STB_MSS        (0x40): Master summary status
			TLPM_STATBIT_STB_OPER       (0x80): Operation Status Summary
			
			STANDARD EVENT STATUS REGISTER bits (see IEEE488.2-1992 §11.5.1)
			TLPM_STATBIT_ESR_OPC        (0x01): Operation complete
			TLPM_STATBIT_ESR_RQC        (0x02): Request control
			TLPM_STATBIT_ESR_QYE        (0x04): Query error
			TLPM_STATBIT_ESR_DDE        (0x08): Device-Specific error
			TLPM_STATBIT_ESR_EXE        (0x10): Execution error
			TLPM_STATBIT_ESR_CME        (0x20): Command error
			TLPM_STATBIT_ESR_URQ        (0x40): User request
			TLPM_STATBIT_ESR_PON        (0x80): Power on
			
			QUESTIONABLE STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_QUES_VOLT      (0x0001): Questionable voltage measurement
			TLPM_STATBIT_QUES_CURR      (0x0002): Questionable current measurement
			TLPM_STATBIT_QUES_TIME      (0x0004): Questionable time measurement
			TLPM_STATBIT_QUES_POW       (0x0008): Questionable power measurement
			TLPM_STATBIT_QUES_TEMP      (0x0010): Questionable temperature measurement
			TLPM_STATBIT_QUES_FREQ      (0x0020): Questionable frequency measurement
			TLPM_STATBIT_QUES_PHAS      (0x0040): Questionable phase measurement
			TLPM_STATBIT_QUES_MOD       (0x0080): Questionable modulation measurement
			TLPM_STATBIT_QUES_CAL       (0x0100): Questionable calibration
			TLPM_STATBIT_QUES_ENER      (0x0200): Questionable energy measurement
			TLPM_STATBIT_QUES_10        (0x0400): Reserved
			TLPM_STATBIT_QUES_11        (0x0800): Reserved
			TLPM_STATBIT_QUES_12        (0x1000): Reserved
			TLPM_STATBIT_QUES_INST      (0x2000): Instrument summary
			TLPM_STATBIT_QUES_WARN      (0x4000): Command warning
			TLPM_STATBIT_QUES_15        (0x8000): Reserved
			
			OPERATION STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_OPER_CAL       (0x0001): The instrument is currently performing a calibration.
			TLPM_STATBIT_OPER_SETT      (0x0002): The instrument is waiting for signals to stabilize for measurements.
			TLPM_STATBIT_OPER_RANG      (0x0004): The instrument is currently changing its range.
			TLPM_STATBIT_OPER_SWE       (0x0008): A sweep is in progress.
			TLPM_STATBIT_OPER_MEAS      (0x0010): The instrument is actively measuring.
			TLPM_STATBIT_OPER_TRIG      (0x0020): The instrument is in a “wait for trigger” state of the trigger model.
			TLPM_STATBIT_OPER_ARM       (0x0040): The instrument is in a “wait for arm” state of the trigger model.
			TLPM_STATBIT_OPER_CORR      (0x0080): The instrument is currently performing a correction (Auto-PID tune).
			TLPM_STATBIT_OPER_SENS      (0x0100): Optical powermeter sensor connected and operable.
			TLPM_STATBIT_OPER_DATA      (0x0200): Measurement data ready for fetch.
			TLPM_STATBIT_OPER_THAC      (0x0400): Thermopile accelerator active.
			TLPM_STATBIT_OPER_11        (0x0800): Reserved
			TLPM_STATBIT_OPER_12        (0x1000): Reserved
			TLPM_STATBIT_OPER_INST      (0x2000): One of n multiple logical instruments is reporting OPERational status.
			TLPM_STATBIT_OPER_PROG      (0x4000): A user-defined programming is currently in the run state.
			TLPM_STATBIT_OPER_15        (0x8000): Reserved
			
			Thorlabs defined MEASRUEMENT STATUS REGISTER bits
			TLPM_STATBIT_MEAS_0         (0x0001): Reserved
			TLPM_STATBIT_MEAS_1         (0x0002): Reserved
			TLPM_STATBIT_MEAS_2         (0x0004): Reserved
			TLPM_STATBIT_MEAS_3         (0x0008): Reserved
			TLPM_STATBIT_MEAS_4         (0x0010): Reserved
			TLPM_STATBIT_MEAS_5         (0x0020): Reserved
			TLPM_STATBIT_MEAS_6         (0x0040): Reserved
			TLPM_STATBIT_MEAS_7         (0x0080): Reserved
			TLPM_STATBIT_MEAS_8         (0x0100): Reserved
			TLPM_STATBIT_MEAS_9         (0x0200): Reserved
			TLPM_STATBIT_MEAS_10        (0x0400): Reserved
			TLPM_STATBIT_MEAS_11        (0x0800): Reserved
			TLPM_STATBIT_MEAS_12        (0x1000): Reserved
			TLPM_STATBIT_MEAS_13        (0x2000): Reserved
			TLPM_STATBIT_MEAS_14        (0x4000): Reserved
			TLPM_STATBIT_MEAS_15        (0x8000): Reserved
			
			Thorlabs defined Auxiliary STATUS REGISTER bits
			TLPM_STATBIT_AUX_NTC        (0x0001): Auxiliary NTC temperature sensor connected.
			TLPM_STATBIT_AUX_EMM        (0x0002): External measurement module connected.
			TLPM_STATBIT_AUX_2          (0x0004): Reserved
			TLPM_STATBIT_AUX_3          (0x0008): Reserved
			TLPM_STATBIT_AUX_EXPS       (0x0010): External power supply connected
			TLPM_STATBIT_AUX_BATC       (0x0020): Battery charging
			TLPM_STATBIT_AUX_BATL       (0x0040): Battery low
			TLPM_STATBIT_AUX_IPS        (0x0080): Apple(tm) authentification supported.
			TLPM_STATBIT_AUX_IPF        (0x0100): Apple(tm) authentification failed.
			TLPM_STATBIT_AUX_9          (0x0200): Reserved
			TLPM_STATBIT_AUX_10         (0x0400): Reserved
			TLPM_STATBIT_AUX_11         (0x0800): Reserved
			TLPM_STATBIT_AUX_12         (0x1000): Reserved
			TLPM_STATBIT_AUX_13         (0x2000): Reserved
			TLPM_STATBIT_AUX_14         (0x4000): Reserved
			TLPM_STATBIT_AUX_15         (0x8000): Reserved
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_writeRegister(self.devSession, reg, value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def readRegister(self, reg, value):
		"""
		This function reads the content of any readable instrument register. Refer to your instrument's user's manual for more details on status structure registers.
		
		
		Args:
			reg(c_int16) : Specifies the register to be used for operation. This parameter can be any of the following constants:
			
			  TLPM_REG_STB         (0): Status Byte Register
			  TLPM_REG_SRE         (1): Service Request Enable
			  TLPM_REG_ESB         (2): Standard Event Status Register
			  TLPM_REG_ESE         (3): Standard Event Enable
			  TLPM_REG_OPER_COND   (4): Operation Condition Register
			  TLPM_REG_OPER_EVENT  (5): Operation Event Register
			  TLPM_REG_OPER_ENAB   (6): Operation Event Enable Register
			  TLPM_REG_OPER_PTR    (7): Operation Positive Transition
			  TLPM_REG_OPER_NTR    (8): Operation Negative Transition
			  TLPM_REG_QUES_COND   (9): Questionable Condition Register
			  TLPM_REG_QUES_EVENT (10): Questionable Event Register
			  TLPM_REG_QUES_ENAB  (11): Questionable Event Enable Reg.
			  TLPM_REG_QUES_PTR   (12): Questionable Positive Transition
			  TLPM_REG_QUES_NTR   (13): Questionable Negative Transition
			  TLPM_REG_MEAS_COND  (14): Measurement Condition Register
			  TLPM_REG_MEAS_EVENT (15): Measurement Event Register
			  TLPM_REG_MEAS_ENAB  (16): Measurement Event Enable Register
			  TLPM_REG_MEAS_PTR   (17): Measurement Positive Transition
			  TLPM_REG_MEAS_NTR   (18): Measurement Negative Transition
			  TLPM_REG_AUX_COND   (19): Auxiliary Condition Register
			  TLPM_REG_AUX_EVENT  (20): Auxiliary Event Register
			  TLPM_REG_AUX_ENAB   (21): Auxiliary Event Enable Register
			  TLPM_REG_AUX_PTR    (22): Auxiliary Positive Transition
			  TLPM_REG_AUX_NTR    (23): Auxiliary Negative Transition 
			
			value(c_int16 use with byref) : This parameter returns the value of the selected register.
			
			These register bits are defined:
			
			STATUS BYTE bits (see IEEE488.2-1992 §11.2)
			TLPM_STATBIT_STB_AUX        (0x01): Auxiliary summary
			TLPM_STATBIT_STB_MEAS       (0x02): Device Measurement Summary
			TLPM_STATBIT_STB_EAV        (0x04): Error available
			TLPM_STATBIT_STB_QUES       (0x08): Questionable Status Summary
			TLPM_STATBIT_STB_MAV        (0x10): Message available
			TLPM_STATBIT_STB_ESB        (0x20): Event Status Bit
			TLPM_STATBIT_STB_MSS        (0x40): Master summary status
			TLPM_STATBIT_STB_OPER       (0x80): Operation Status Summary
			
			STANDARD EVENT STATUS REGISTER bits (see IEEE488.2-1992 §11.5.1)
			TLPM_STATBIT_ESR_OPC        (0x01): Operation complete
			TLPM_STATBIT_ESR_RQC        (0x02): Request control
			TLPM_STATBIT_ESR_QYE        (0x04): Query error
			TLPM_STATBIT_ESR_DDE        (0x08): Device-Specific error
			TLPM_STATBIT_ESR_EXE        (0x10): Execution error
			TLPM_STATBIT_ESR_CME        (0x20): Command error
			TLPM_STATBIT_ESR_URQ        (0x40): User request
			TLPM_STATBIT_ESR_PON        (0x80): Power on
			
			QUESTIONABLE STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_QUES_VOLT      (0x0001): Questionable voltage measurement
			TLPM_STATBIT_QUES_CURR      (0x0002): Questionable current measurement
			TLPM_STATBIT_QUES_TIME      (0x0004): Questionable time measurement
			TLPM_STATBIT_QUES_POW       (0x0008): Questionable power measurement
			TLPM_STATBIT_QUES_TEMP      (0x0010): Questionable temperature measurement
			TLPM_STATBIT_QUES_FREQ      (0x0020): Questionable frequency measurement
			TLPM_STATBIT_QUES_PHAS      (0x0040): Questionable phase measurement
			TLPM_STATBIT_QUES_MOD       (0x0080): Questionable modulation measurement
			TLPM_STATBIT_QUES_CAL       (0x0100): Questionable calibration
			TLPM_STATBIT_QUES_ENER      (0x0200): Questionable energy measurement
			TLPM_STATBIT_QUES_10        (0x0400): Reserved
			TLPM_STATBIT_QUES_11        (0x0800): Reserved
			TLPM_STATBIT_QUES_12        (0x1000): Reserved
			TLPM_STATBIT_QUES_INST      (0x2000): Instrument summary
			TLPM_STATBIT_QUES_WARN      (0x4000): Command warning
			TLPM_STATBIT_QUES_15        (0x8000): Reserved
			
			OPERATION STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_OPER_CAL       (0x0001): The instrument is currently performing a calibration.
			TLPM_STATBIT_OPER_SETT      (0x0002): The instrument is waiting for signals to stabilize for measurements.
			TLPM_STATBIT_OPER_RANG      (0x0004): The instrument is currently changing its range.
			TLPM_STATBIT_OPER_SWE       (0x0008): A sweep is in progress.
			TLPM_STATBIT_OPER_MEAS      (0x0010): The instrument is actively measuring.
			TLPM_STATBIT_OPER_TRIG      (0x0020): The instrument is in a “wait for trigger” state of the trigger model.
			TLPM_STATBIT_OPER_ARM       (0x0040): The instrument is in a “wait for arm” state of the trigger model.
			TLPM_STATBIT_OPER_CORR      (0x0080): The instrument is currently performing a correction (Auto-PID tune).
			TLPM_STATBIT_OPER_SENS      (0x0100): Optical powermeter sensor connected and operable.
			TLPM_STATBIT_OPER_DATA      (0x0200): Measurement data ready for fetch.
			TLPM_STATBIT_OPER_THAC      (0x0400): Thermopile accelerator active.
			TLPM_STATBIT_OPER_11        (0x0800): Reserved
			TLPM_STATBIT_OPER_12        (0x1000): Reserved
			TLPM_STATBIT_OPER_INST      (0x2000): One of n multiple logical instruments is reporting OPERational status.
			TLPM_STATBIT_OPER_PROG      (0x4000): A user-defined programming is currently in the run state.
			TLPM_STATBIT_OPER_15        (0x8000): Reserved
			
			Thorlabs defined MEASRUEMENT STATUS REGISTER bits
			TLPM_STATBIT_MEAS_0         (0x0001): Reserved
			TLPM_STATBIT_MEAS_1         (0x0002): Reserved
			TLPM_STATBIT_MEAS_2         (0x0004): Reserved
			TLPM_STATBIT_MEAS_3         (0x0008): Reserved
			TLPM_STATBIT_MEAS_4         (0x0010): Reserved
			TLPM_STATBIT_MEAS_5         (0x0020): Reserved
			TLPM_STATBIT_MEAS_6         (0x0040): Reserved
			TLPM_STATBIT_MEAS_7         (0x0080): Reserved
			TLPM_STATBIT_MEAS_8         (0x0100): Reserved
			TLPM_STATBIT_MEAS_9         (0x0200): Reserved
			TLPM_STATBIT_MEAS_10        (0x0400): Reserved
			TLPM_STATBIT_MEAS_11        (0x0800): Reserved
			TLPM_STATBIT_MEAS_12        (0x1000): Reserved
			TLPM_STATBIT_MEAS_13        (0x2000): Reserved
			TLPM_STATBIT_MEAS_14        (0x4000): Reserved
			TLPM_STATBIT_MEAS_15        (0x8000): Reserved
			
			Thorlabs defined Auxiliary STATUS REGISTER bits
			TLPM_STATBIT_AUX_NTC        (0x0001): Auxiliary NTC temperature sensor connected.
			TLPM_STATBIT_AUX_EMM        (0x0002): External measurement module connected.
			TLPM_STATBIT_AUX_2          (0x0004): Reserved
			TLPM_STATBIT_AUX_3          (0x0008): Reserved
			TLPM_STATBIT_AUX_EXPS       (0x0010): External power supply connected
			TLPM_STATBIT_AUX_BATC       (0x0020): Battery charging
			TLPM_STATBIT_AUX_BATL       (0x0040): Battery low
			TLPM_STATBIT_AUX_IPS        (0x0080): Apple(tm) authentification supported.
			TLPM_STATBIT_AUX_IPF        (0x0100): Apple(tm) authentification failed.
			TLPM_STATBIT_AUX_9          (0x0200): Reserved
			TLPM_STATBIT_AUX_10         (0x0400): Reserved
			TLPM_STATBIT_AUX_11         (0x0800): Reserved
			TLPM_STATBIT_AUX_12         (0x1000): Reserved
			TLPM_STATBIT_AUX_13         (0x2000): Reserved
			TLPM_STATBIT_AUX_14         (0x4000): Reserved
			TLPM_STATBIT_AUX_15         (0x8000): Reserved
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_readRegister(self.devSession, reg, value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def presetRegister(self):
		"""
		This function presets all status registers to default.
		
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_presetRegister(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def sendNTPRequest(self, timeMode, timeZone, IPAddress):
		"""
		This function sets the system date and time of the powermeter.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM100D, PM200, PM400.
		
		Args:
			timeMode(c_int16)
			timeZone(c_int16)
			IPAddress(create_string_buffer(1024))
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_sendNTPRequest(self.devSession, timeMode, timeZone, IPAddress)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setTime(self, year, month, day, hour, minute, second):
		"""
		This function sets the system date and time of the powermeter.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM100D, PM200, PM400.
		
		Args:
			year(c_int16) : This parameter specifies the actual year in the format yyyy e.g. 2009.
			month(c_int16) : This parameter specifies the actual month in the format mm e.g. 01.
			day(c_int16) : This parameter specifies the actual day in the format dd e.g. 15.
			
			hour(c_int16) : This parameter specifies the actual hour in the format hh e.g. 14.
			
			minute(c_int16) : This parameter specifies the actual minute in the format mm e.g. 43.
			
			second(c_int16) : This parameter specifies the actual second in the format ss e.g. 50.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setTime(self.devSession, year, month, day, hour, minute, second)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getTime(self, year, month, day, hour, minute, second):
		"""
		This function returns the system date and time of the powermeter.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM100D, PM200, PM400.
		
		Args:
			year(c_int16 use with byref) : This parameter specifies the actual year in the format yyyy.
			month(c_int16 use with byref) : This parameter specifies the actual month in the format mm.
			day(c_int16 use with byref) : This parameter specifies the actual day in the format dd.
			hour(c_int16 use with byref) : This parameter specifies the actual hour in the format hh.
			minute(c_int16 use with byref) : This parameter specifies the actual minute in the format mm.
			second(c_int16 use with byref) : This parameter specifies the actual second in the format ss.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getTime(self.devSession, year, month, day, hour, minute, second)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setSummertime(self, timeMode):
		"""
		This function sets the clock to summertime.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM5020
		
		Args:
			timeMode(c_int16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setSummertime(self.devSession, timeMode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getSummertime(self, timeMode):
		"""
		This function returns if the device uses the summertime.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM5020.
		
		Args:
			timeMode(c_int16 use with byref)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getSummertime(self.devSession, timeMode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setLineFrequency(self, lineFrequency):
		"""
		This function selects the line frequency.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200.
		
		
		Args:
			lineFrequency(c_int16) : This parameter specifies the line frequency.
			
			Accepted values:
			  TLPM_LINE_FREQ_50 (50): 50Hz
			  TLPM_LINE_FREQ_60 (60): 60Hz
			
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setLineFrequency(self.devSession, lineFrequency)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getLineFrequency(self, lineFrequency):
		"""
		This function returns the selected line frequency.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200.
		
		
		Args:
			lineFrequency(c_int16 use with byref) : This parameter returns the selected line frequency in Hz.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getLineFrequency(self.devSession, lineFrequency)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getBatteryVoltage(self, voltage):
		"""
		This function is used to obtain the battery voltage readings from the instrument.
		
		Remark:
		(1) This function is only supported with the PM160 and PM160T.
		(2) This function obtains the latest battery voltage measurement result.
		(3) With the USB cable connected this function will obtain the loading voltage. Only with USB cable disconnected (Bluetooth connection) the actual battery voltage can be read. 
		
		Args:
			voltage(c_double use with byref) : This parameter returns the battery voltage in volts [V].
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getBatteryVoltage(self.devSession, voltage)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDispBrightness(self, val):
		"""
		This function sets the display brightness.
		
		Args:
			val(c_double) : This parameter specifies the display brightness.
			
			Range   : 0.0 .. 1.0
			Default : 1.0
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDispBrightness(self.devSession, val)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDispBrightness(self, pVal):
		"""
		This function returns the display brightness.
		
		
		Args:
			pVal(c_double use with byref) : This parameter returns the display brightness. Value range is 0.0 to 1.0.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDispBrightness(self.devSession, pVal)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDispContrast(self, val):
		"""
		This function sets the display contrast of a PM100D.
		
		Note: The function is available on PM100D only.
		
		Args:
			val(c_double) : This parameter specifies the display contrast.
			
			Range   : 0.0 .. 1.0
			Default : 0.5
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDispContrast(self.devSession, val)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDispContrast(self, pVal):
		"""
		This function returns the display contrast of a PM100D.
		
		Note: This function is available on PM100D only
		
		Args:
			pVal(c_double use with byref) : This parameter returns the display contrast (0..1).
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDispContrast(self.devSession, pVal)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def beep(self):
		"""
		Plays a beep sound.
		
		Note: Only supported by PM5020.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_beep(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setInputFilterState(self, inputFilterState, channel):
		"""
		This function sets the instrument's photodiode input filter state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			inputFilterState(c_int16) : This parameter specifies the input filter mode.
			
			Acceptable values:
			  TLPM_INPUT_FILTER_STATE_OFF (0) input filter off
			  TLPM_INPUT_FILTER_STATE_ON  (1) input filter on
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setInputFilterState(self.devSession, inputFilterState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getInputFilterState(self, inputFilterState, channel):
		"""
		This function returns the instrument's photodiode input filter state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			inputFilterState(c_int16 use with byref) : This parameter returns the input filter state.
			
			Return values:
			  TLPM_INPUT_FILTER_STATE_OFF (0) input filter off
			  TLPM_INPUT_FILTER_STATE_ON  (1) input filter on
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getInputFilterState(self.devSession, inputFilterState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAccelState(self, accelState, channel):
		"""
		This function sets the thermopile acceleration state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200.
		
		
		Args:
			accelState(c_int16) : This parameter specifies the thermopile acceleration mode.
			
			Acceptable values:
			  TLPM_ACCELERATION_STATE_OFF (0): thermopile acceleration off
			  TLPM_ACCELERATION_STATE_ON  (1): thermopile acceleration on
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAccelState(self.devSession, accelState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAccelState(self, accelState, channel):
		"""
		This function returns the thermopile acceleration state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			accelState(c_int16 use with byref) : This parameter returns the thermopile acceleration mode.
			
			Return values:
			  TLPM_ACCELERATION_STATE_OFF (0): thermopile acceleration off
			  TLPM_ACCELERATION_STATE_ON  (1): thermopile acceleration on
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAccelState(self.devSession, accelState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAccelMode(self, accelMode, channel):
		"""
		This function sets the thermopile acceleration auto mode.
		
		While thermopile acceleration improves displaying changing measurement values it unfortunately adds extra noise which can become noticeable on constant values measurements. With acceleration mode set to AUTO the instrument enables the acceleration circuitry after big measurement value changes for five times of "Tau". See also functions <Set Thermopile Accelerator Tau> and <Set Thermopile Accelerator State>.
		
		With calling <Set Thermopile Accelerator State> the accelerator mode will always be reset to MANUAL.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			accelMode(c_int16) : This parameter specifies the thermopile acceleration mode.
			
			Acceptable values:
			  TLPM_ACCELERATION_MANUAL (0): auto acceleration off
			  TLPM_ACCELERATION_AUTO   (1): auto acceleration on
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAccelMode(self.devSession, accelMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAccelMode(self, accelMode, channel):
		"""
		This function returns the thermopile acceleration mode.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			accelMode(c_int16 use with byref) : This parameter returns the thermopile acceleration mode.
			
			Return values:
			  TLPM_ACCELERATION_MANUAL (0): auto acceleration off
			  TLPM_ACCELERATION_AUTO   (1): auto acceleration on
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAccelMode(self.devSession, accelMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAccelTau(self, accelTau, channel):
		"""
		This function sets the thermopile acceleration time constant in seconds [s].
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			accelTau(c_double) : This parameter specifies the thermopile acceleration time constant in seconds [s].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAccelTau(self.devSession, accelTau, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAccelTau(self, attribute, accelTau, channel):
		"""
		This function returns the thermopile acceleration time constant in seconds [s].
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			accelTau(c_double use with byref) : This parameter returns the thermopile acceleration time constant in seconds [s].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAccelTau(self.devSession, attribute, accelTau, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setInputAdapterType(self, type, channel):
		"""
		This function sets the sensor type to assume for custom sensors without calibration data memory connected to the instrument.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			type(c_int16) : This parameter specifies the custom sensor type.
			
			Acceptable values:
			 SENSOR_TYPE_PD_SINGLE (1): Photodiode sensor
			 SENSOR_TYPE_THERMO    (2): Thermopile sensor
			 SENSOR_TYPE_PYRO      (3): Pyroelectric sensor
			
			Value SENSOR_TYPE_PYRO is only available for energy meter instruments.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setInputAdapterType(self.devSession, type, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getInputAdapterType(self, type, channel):
		"""
		This function returns the assumed sensor type for custom sensors without calibration data memory connected to the instrument.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			type(c_int16 use with byref) : This parameter returns the custom sensor type.
			
			Remark:
			The meanings of the obtained sensor type are:
			
			Sensor Types:
			 SENSOR_TYPE_PD_SINGLE (1): Photodiode sensor
			 SENSOR_TYPE_THERMO    (2): Thermopile sensor
			 SENSOR_TYPE_PYRO      (3): Pyroelectric sensor
			 SENSOR_TYPE_4Q        (4): 4 Quadrant sensor
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getInputAdapterType(self.devSession, type, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAvgTime(self, avgTime, channel):
		"""
		This function sets the average time for measurement value generation.
		
		Args:
			avgTime(c_double) : This parameter specifies the average time in seconds.
			
			The value will be rounded to the closest multiple of the device's internal sampling rate.
			
			Remark: 
			To get an measurement value from the device the timeout in your application has to be longer than the average time.
			
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAvgTime(self.devSession, avgTime, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAvgTime(self, attribute, avgTime, channel):
		"""
		This function returns the average time for measurement value generation.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			avgTime(c_double use with byref) : This parameter returns the specified average time in seconds.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAvgTime(self.devSession, attribute, avgTime, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAvgCnt(self, averageCount, channel):
		"""
		This function sets the average count for measurement value generation.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		(2) The function is deprecated and kept for legacy reasons. Its recommended to use TLPM_setAvgTime() instead.
		
		
		Args:
			averageCount(c_int16) : This parameter specifies the average count.
			The default value is 1.
			
			Remark: 
			Depending on the powermeter model internal there are taken up to 3000 measurements per second.
			In this example   Average Time = Average Count / 3000 [s].
			To get an measurement value from the device the timeout in your application has to be longer than the calculated average time.
			
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAvgCnt(self.devSession, averageCount, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAvgCnt(self, averageCount, channel):
		"""
		This function returns the average count for measurement value generation.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		(2) The function is deprecated and kept for legacy reasons. Its recommended to use TLPM_getAvgTime() instead.
		
		
		Args:
			averageCount(c_int16 use with byref) : This parameter returns the actual Average Count.
			
			Remark: 
			Depending on the powermeter model internal there are taken up to 3000 measurements per second.
			In this example   Average Time = Average Count / 3000 [s].
			To get an measurement value from the device the timeout in your application has to be longer than the calculated average time.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAvgCnt(self.devSession, averageCount, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAttenuation(self, attenuation, channel):
		"""
		This function sets the input attenuation.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attenuation(c_double) : This parameter specifies the input attenuation in dezibel [dB].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAttenuation(self.devSession, attenuation, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAttenuation(self, attribute, attenuation, channel):
		"""
		This function returns the input attenuation.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			attenuation(c_double use with byref) : This parameter returns the specified input attenuation in dezibel [dB].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAttenuation(self.devSession, attribute, attenuation, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def startDarkAdjust(self, channel):
		"""
		This function starts the dark current/zero offset adjustment procedure.
		
		Remark: 
		(1) You have to darken the input before starting dark/zero adjustment.
		(2) You can get the state of dark/zero adjustment with <Get Dark Adjustment State>
		(3) You can stop dark/zero adjustment with <Cancel Dark Adjustment>
		(4) You get the dark/zero value with <Get Dark Offset>
		(5) Energy sensors do not support this function
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_startDarkAdjust(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def cancelDarkAdjust(self, channel):
		"""
		This function cancels a running dark current/zero offset adjustment procedure.
		
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_cancelDarkAdjust(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDarkAdjustState(self, state, channel):
		"""
		This function returns the state of a dark current/zero offset adjustment procedure previously initiated by <Start Dark Adjust>.
		
		
		Args:
			state(c_int16 use with byref) : This parameter returns the dark adjustment state.
			
			Possible return values are:
			TLPM_STAT_DARK_ADJUST_FINISHED (0) : no dark adjustment running
			TLPM_STAT_DARK_ADJUST_RUNNING  (1) : dark adjustment is running
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDarkAdjustState(self.devSession, state, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDarkOffset(self, darkOffset, channel):
		"""
		This function returns the dark/zero offset.
		
		The function is not supported with energy sensors.
		
		Args:
			darkOffset(c_double) : This parameter returns the dark/zero offset.
			
			The unit of the returned offset value depends on the sensor type. Photodiodes return the dark offset in ampere [A]. Thermal sensors return the dark offset in volt [V].
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDarkOffset(self.devSession, darkOffset, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDarkOffset(self, darkOffset, channel):
		"""
		This function returns the dark/zero offset.
		
		The function is not supported with energy sensors.
		
		Args:
			darkOffset(c_double use with byref) : This parameter returns the dark/zero offset.
			
			The unit of the returned offset value depends on the sensor type. Photodiodes return the dark offset in ampere [A]. Thermal sensors return the dark offset in volt [V].
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDarkOffset(self.devSession, darkOffset, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setBeamDia(self, beamDiameter, channel):
		"""
		This function sets the users beam diameter in millimeter [mm].
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		(2) Beam diameter set value is used for calculating power and energy density.
		
		
		Args:
			beamDiameter(c_double) : This parameter specifies the users beam diameter in millimeter [mm].
			
			Remark:
			Beam diameter set value is used for calculating power and energy density.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setBeamDia(self.devSession, beamDiameter, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getBeamDia(self, attribute, beamDiameter, channel):
		"""
		This function returns the users beam diameter in millimeter [mm].
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM101, PM102, PM400.
		(2) Beam diameter set value is used for calculating power and energy density.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			beamDiameter(c_double use with byref) : This parameter returns the specified beam diameter in millimeter [mm].
			
			Remark:
			Beam diameter set value is used for calculating power and energy density.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getBeamDia(self.devSession, attribute, beamDiameter, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setWavelength(self, wavelength, channel):
		"""
		This function sets the users wavelength in nanometer [nm].
		
		Remark:
		Wavelength set value is used for calculating power.
		
		
		Args:
			wavelength(c_double) : This parameter specifies the users wavelength in nanometer [nm].
			
			Remark:
			Wavelength set value is used for calculating power.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setWavelength(self.devSession, wavelength, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getWavelength(self, attribute, wavelength, channel):
		"""
		This function returns the users wavelength in nanometer [nm].
		
		Remark:
		Wavelength set value is used for calculating power.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			wavelength(c_double use with byref) : This parameter returns the specified wavelength in nanometer [nm].
			
			Remark:
			Wavelength set value is used for calculating power.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getWavelength(self.devSession, attribute, wavelength, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPhotodiodeResponsivity(self, response, channel):
		"""
		This function sets the photodiode responsivity in ampere per watt [A/W].
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			response(c_double) : This parameter specifies the photodiode responsivity in ampere per watt [A/W].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPhotodiodeResponsivity(self.devSession, response, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPhotodiodeResponsivity(self, attribute, responsivity, channel):
		"""
		This function returns the photodiode responsivity in ampere per watt [A/W].
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			responsivity(c_double use with byref) : This parameter returns the specified photodiode responsivity in ampere per watt [A/W].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPhotodiodeResponsivity(self.devSession, attribute, responsivity, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setThermopileResponsivity(self, response, channel):
		"""
		This function sets the thermopile responsivity in volt per watt [V/W]
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			response(c_double) : This parameter specifies the thermopile responsivity in volt per watt [V/W]
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setThermopileResponsivity(self.devSession, response, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getThermopileResponsivity(self, attribute, responsivity, channel):
		"""
		This function returns the thermopile responsivity in volt per watt [V/W]
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			responsivity(c_double use with byref) : This parameter returns the specified thermopile responsivity in volt per watt [V/W]
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getThermopileResponsivity(self.devSession, attribute, responsivity, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPyrosensorResponsivity(self, response, channel):
		"""
		This function sets the pyrosensor responsivity in volt per joule [V/J]
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			response(c_double) : This parameter specifies the pyrosensor responsivity in volt per joule [V/J]
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPyrosensorResponsivity(self.devSession, response, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPyrosensorResponsivity(self, attribute, responsivity, channel):
		"""
		This function returns the pyrosensor responsivity in volt per joule [V/J]
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			responsivity(c_double use with byref) : This parameter returns the specified pyrosensor responsivity in volt per joule [V/J]
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPyrosensorResponsivity(self.devSession, attribute, responsivity, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setCurrentAutoRange(self, currentAutorangeMode, channel):
		"""
		This function sets the current auto range mode.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			currentAutorangeMode(c_int16) : This parameter specifies the current auto range mode.
			
			Acceptable values:
			  TLPM_AUTORANGE_CURRENT_OFF (0): current auto range disabled
			  TLPM_AUTORANGE_CURRENT_ON  (1): current auto range enabled
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentAutoRange(self.devSession, currentAutorangeMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getCurrentAutorange(self, currentAutorangeMode, channel):
		"""
		This function returns the current auto range mode.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			currentAutorangeMode(c_int16 use with byref) : This parameter returns the current auto range mode.
			
			Return values:
			  TLPM_AUTORANGE_CURRENT_OFF (0): current auto range disabled
			  TLPM_AUTORANGE_CURRENT_ON  (1): current auto range enabled
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getCurrentAutorange(self.devSession, currentAutorangeMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setCurrentRange(self, current_to_Measure, channel):
		"""
		This function sets the sensor's current range.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			current_to_Measure(c_double) : This parameter specifies the current value to be measured in ampere [A].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentRange(self.devSession, current_to_Measure, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getCurrentRange(self, attribute, currentValue, channel):
		"""
		This function returns the actual current range value.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			currentValue(c_double use with byref) : This parameter returns the specified current range value in ampere [A].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getCurrentRange(self.devSession, attribute, currentValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getCurrentRanges(self, currentValues, rangeCount, channel):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			currentValues( (c_double * arrayLength)()) : This parameter returns the specified voltage range value in volts [V].
			
			rangeCount(c_uint16 use with byref)
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getCurrentRanges(self.devSession, currentValues, rangeCount, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setCurrentRangeSearch(self, channel):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentRangeSearch(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setCurrentRef(self, currentReferenceValue, channel):
		"""
		This function sets the current reference value.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			currentReferenceValue(c_double) : This parameter specifies the current reference value in amperes [A].
			
			Remark:
			This value is used for calculating differences between the actual current value and this current reference value if Current Reference State is ON.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentRef(self.devSession, currentReferenceValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getCurrentRef(self, attribute, currentReferenceValue, channel):
		"""
		This function returns the current reference value.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			currentReferenceValue(c_double use with byref) : This parameter returns the specified current reference value in amperes [A].
			
			Remark:
			This value is used for calculating differences between the actual current value and this current reference value if Current Reference State is ON.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getCurrentRef(self.devSession, attribute, currentReferenceValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setCurrentRefState(self, currentReferenceState, channel):
		"""
		This function sets the current reference state.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			currentReferenceState(c_int16) : This parameter specifies the current reference state.
			
			Acceptable values:
			  TLPM_CURRENT_REF_OFF (0): Current reference disabled. Absolute measurement.
			  TLPM_CURRENT_REF_ON  (1): Current reference enabled. Relative measurement.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentRefState(self.devSession, currentReferenceState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getCurrentRefState(self, currentReferenceState, channel):
		"""
		This function returns the current reference state.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			currentReferenceState(c_int16 use with byref) : This parameter returns the current reference state.
			
			Return values:
			  TLPM_CURRENT_REF_OFF (0): Current reference disabled. Absolute measurement.
			  TLPM_CURRENT_REF_ON  (1): Current reference enabled. Relative measurement.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getCurrentRefState(self.devSession, currentReferenceState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setEnergyRange(self, energyToMeasure, channel):
		"""
		This function sets the pyro sensor's energy range.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			energyToMeasure(c_double) : This parameter specifies the energy value in joule [J] to be measured.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setEnergyRange(self.devSession, energyToMeasure, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getEnergyRange(self, attribute, energyValue, channel):
		"""
		This function returns the pyro sensor's energy range.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			energyValue(c_double use with byref) : This parameter returns the specified pyro sensor's energy value in joule [J].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getEnergyRange(self.devSession, attribute, energyValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setEnergyRef(self, energyReferenceValue, channel):
		"""
		This function sets the pyro sensor's energy reference value
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		(2) This value is used for calculating differences between the actual energy value and this energy reference value.
		
		
		Args:
			energyReferenceValue(c_double) : This parameter specifies the pyro sensor's energy reference value in joule [J].
			
			Remark:
			This value is used for calculating differences between the actual energy value and this energy reference value if Energy Reference State is ON.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setEnergyRef(self.devSession, energyReferenceValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getEnergyRef(self, attribute, energyReferenceValue, channel):
		"""
		This function returns the specified pyro sensor's energy reference value.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		(2) The set value is used for calculating differences between the actual energy value and this energy reference value.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			energyReferenceValue(c_double use with byref) : This parameter returns the specified pyro sensor's energy reference value in joule [J].
			
			Remark:
			The set value is used for calculating differences between the actual energy value and this energy reference value if Energy Reference State is ON.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getEnergyRef(self.devSession, attribute, energyReferenceValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setEnergyRefState(self, energyReferenceState, channel):
		"""
		This function sets the instrument's energy reference state.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			energyReferenceState(c_int16) : This parameter specifies the energy reference state.
			
			Acceptable values:
			  TLPM_ENERGY_REF_OFF (0): Energy reference disabled. Absolute measurement.
			  TLPM_ENERGY_REF_ON  (1): Energy reference enabled. Relative measurement.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setEnergyRefState(self.devSession, energyReferenceState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getEnergyRefState(self, energyReferenceState, channel):
		"""
		This function returns the instrument's energy reference state.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			energyReferenceState(c_int16 use with byref) : This parameter returns the energy reference state.
			
			Return values:
			  TLPM_ENERGY_REF_OFF (0): Energy reference disabled. Absolute measurement.
			  TLPM_ENERGY_REF_ON  (1): Energy reference enabled. Relative measurement.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getEnergyRefState(self.devSession, energyReferenceState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFreqRange(self, lowerFrequency, upperFrequency, channel):
		"""
		This function returns the instruments frequency measurement range.
		
		Remark:
		The frequency of the input signal is calculated over at least 0.3s. So it takes at least 0.3s to get a new frequency value from the instrument.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, and PM100USB.
		
		
		Args:
			lowerFrequency(c_double use with byref) : This parameter returns the lower instruments frequency in [Hz].
			
			upperFrequency(c_double use with byref) : This parameter returns the upper instruments frequency in [Hz].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFreqRange(self.devSession, lowerFrequency, upperFrequency, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setFreqMode(self, frequencyMode, channel):
		"""
		This function sets the instruments frequency measurement mode. Only for photodiodes.
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			frequencyMode(c_uint16) : This parameter returns the frequency mode.
			
			CW (0)
			PEAK (1)
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setFreqMode(self.devSession, frequencyMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFreqMode(self, frequencyMode, channel):
		"""
		This function returns the instruments frequency measurement mode. 
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			frequencyMode(c_uint16 use with byref) : This parameter returns the frequency mode.
			
			CW (0)
			PEAK (1)
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFreqMode(self.devSession, frequencyMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerAutoRange(self, powerAutorangeMode, channel):
		"""
		This function sets the power auto range mode.
		
		
		Args:
			powerAutorangeMode(c_int16) : This parameter specifies the power auto range mode.
			
			Acceptable values:
			  TLPM_AUTORANGE_POWER_OFF (0): power auto range disabled
			  TLPM_AUTORANGE_POWER_ON  (1): power auto range enabled
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerAutoRange(self.devSession, powerAutorangeMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerAutorange(self, powerAutorangeMode, channel):
		"""
		This function returns the power auto range mode.
		
		
		Args:
			powerAutorangeMode(c_int16 use with byref) : This parameter returns the power auto range mode.
			
			Return values:
			  TLPM_AUTORANGE_POWER_OFF (0): power auto range disabled
			  TLPM_AUTORANGE_POWER_ON  (0): power auto range enabled
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerAutorange(self.devSession, powerAutorangeMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerRange(self, power_to_Measure, channel):
		"""
		This function sets the sensor's power range.
		
		
		Args:
			power_to_Measure(c_double) : This parameter specifies the most positive signal level expected for the sensor input in watt [W].
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerRange(self.devSession, power_to_Measure, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerRange(self, attribute, powerValue, channel):
		"""
		This function returns the actual power range value.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			powerValue(c_double use with byref) : This parameter returns the specified power range value in watt [W].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerRange(self.devSession, attribute, powerValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerRef(self, powerReferenceValue, channel):
		"""
		This function sets the power reference value.
		
		
		Args:
			powerReferenceValue(c_double) : This parameter specifies the power reference value.
			
			Remark:
			(1) The power reference value has the unit specified with <Set Power Unit>.
			(2) This value is used for calculating differences between the actual power value and this power reference value if Power Reference State is ON.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerRef(self.devSession, powerReferenceValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerRef(self, attribute, powerReferenceValue, channel):
		"""
		This function returns the power reference value.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			powerReferenceValue(c_double use with byref) : This parameter returns the specified power reference value.
			
			Remark:
			(1) The power reference value has the unit specified with <Set Power Unit>.
			(2) This value is used for calculating differences between the actual power value and this power reference value if Power Reference State is ON.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerRef(self.devSession, attribute, powerReferenceValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerRefState(self, powerReferenceState, channel):
		"""
		This function sets the power reference state.
		
		
		Args:
			powerReferenceState(c_int16) : This parameter specifies the power reference state.
			
			Acceptable values:
			  TLPM_POWER_REF_OFF (0): Power reference disabled. Absolute measurement.
			  TLPM_POWER_REF_ON  (1): Power reference enabled. Relative measurement.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerRefState(self.devSession, powerReferenceState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerRefState(self, powerReferenceState, channel):
		"""
		This function returns the power reference state.
		
		
		Args:
			powerReferenceState(c_int16 use with byref) : This parameter returns the power reference state.
			
			Return values:
			  TLPM_POWER_REF_OFF (0): Power reference disabled. Absolute measurement.
			  TLPM_POWER_REF_ON  (1): Power reference enabled. Relative measurement.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerRefState(self.devSession, powerReferenceState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerUnit(self, powerUnit, channel):
		"""
		This function sets the unit of the power value.
		
		
		Args:
			powerUnit(c_int16) : This parameter specifies the unit of the pover value.
			
			Acceptable values:
			  TLPM_POWER_UNIT_WATT (0): power in Watt
			  TLPM_POWER_UNIT_DBM  (1): power in dBm
			
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerUnit(self.devSession, powerUnit, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerUnit(self, powerUnit, channel):
		"""
		This function returns the unit of the power value.
		
		
		Args:
			powerUnit(c_int16 use with byref) : This parameter returns the unit of the power value.
			
			Return values:
			  TLPM_POWER_UNIT_WATT (0): power in Watt
			  TLPM_POWER_UNIT_DBM  (1): power in dBm
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerUnit(self.devSession, powerUnit, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerCalibrationPointsInformation(self, index, serialNumber, calibrationDate, calibrationPointsCount, author, sensorPosition, channel):
		"""
		Queries the customer adjustment header like serial nr, cal date, nr of points at given index
		
		
		Args:
			index(c_uint16) : Index of the power calibration (range 1...5)
			serialNumber(create_string_buffer(1024)) : Serial Number of the sensor.
			Please provide a buffer of 256 characters.
			calibrationDate(create_string_buffer(1024)) : Last calibration date of this sensor
			Please provide a buffer of 256 characters.
			calibrationPointsCount(c_uint16 use with byref) : Number of calibration points of the power calibration with this sensor
			author(create_string_buffer(1024))
			sensorPosition(c_uint16 use with byref) : The position of the sencor switch of a Thorlabs S130C
			1 = 5mW
			2 = 500mW
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerCalibrationPointsInformation(self.devSession, index, serialNumber, calibrationDate, calibrationPointsCount, author, sensorPosition, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerCalibrationPointsState(self, index, state, channel):
		"""
		Queries the state if the power calibration of this sensor is activated.
		
		
		Args:
			index(c_uint16)
			state(c_int16 use with byref) : State if the user power calibration is activated and used for the power measurements.
			
			VI_ON: The user power calibration is used
			VI_OFF: The user power calibration is ignored in the power measurements
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerCalibrationPointsState(self.devSession, index, state, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerCalibrationPointsState(self, index, state, channel):
		"""
		This function activates/inactivates the power calibration of this sensor.
		
		
		Args:
			index(c_uint16) : Index of the power calibration (range 1...5)
			state(c_int16) : State if the user power calibration is activated and used for the power measurements.
			
			VI_ON: The user power calibration is used
			VI_OFF: The user power calibration is ignored in the power measurements
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerCalibrationPointsState(self.devSession, index, state, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerCalibrationPoints(self, index, pointCounts, wavelengths, powerCorrectionFactors, channel):
		"""
		Returns a list of wavelength and the corresponding power correction factor.
		
		
		Args:
			index(c_uint16)
			pointCounts(c_uint16) : Number of points that are submitted in the wavelength and power correction factors arrays.
			Maximum of 8 wavelength - power correction factors pairs can be calibrated for each sensor.
			wavelengths( (c_double * arrayLength)()) : Array of wavelengths in nm. Requires ascending wavelength order.
			The array must contain <points counts> entries.
			powerCorrectionFactors( (c_double * arrayLength)()) : Array of power correction factorw that correspond to the wavelength array. 
			The array must contain <points counts> entries, same as wavelenght to build wavelength - power correction factors pairs.
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerCalibrationPoints(self.devSession, index, pointCounts, wavelengths, powerCorrectionFactors, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerCalibrationPoints(self, index, pointCounts, wavelengths, powerCorrectionFactors, author, sensorPosition, channel):
		"""
		Sumbits a list of wavelength and the corresponding measured power correction factors to calibrate the power measurement.
		
		
		Args:
			index(c_uint16) : Index of the power calibration (range 1...5)
			pointCounts(c_uint16) : Number of points that are submitted in the wavelength and power correction factors arrays.
			Maximum of 8 wavelength - power correction factors  pairs can be calibrated for each sensor.
			wavelengths( (c_double * arrayLength)()) : Array of wavelengths in nm. Requires ascending wavelength order.
			The array must contain <points counts> entries.
			powerCorrectionFactors( (c_double * arrayLength)()) : Array of powers correction factors that correspond to the wavelength array. 
			The array must contain <points counts> entries, same as wavelenght to build wavelength - power correction factors  pairs.
			author(create_string_buffer(1024)) : Buffer that contains the name of the editor of the calibration.
			Name of Author limited to 19 chars + ''
			sensorPosition(c_uint16) : The position of the sencor switch of a Thorlabs S130C
			1 = 5mW
			2 = 500mW
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerCalibrationPoints(self.devSession, index, pointCounts, wavelengths, powerCorrectionFactors, author, sensorPosition, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def reinitSensor(self, channel):
		"""
		To use the user power calibration, the sensor has to be reconnected.
		Either manually remove and reconnect the sensor to the instrument or use this funtion.
		
		This function will wait 2 seconds until the sensor has been reinitialized.
		
		Args:
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_reinitSensor(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setVoltageAutoRange(self, voltageAutorangeMode, channel):
		"""
		This function sets the voltage auto range mode.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageAutorangeMode(c_int16) : This parameter specifies the voltage auto range mode.
			
			Acceptable values:
			  TLPM_AUTORANGE_VOLTAGE_OFF (0): voltage auto range disabled
			  TLPM_AUTORANGE_VOLTAGE_ON  (1): voltage auto range enabled
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageAutoRange(self.devSession, voltageAutorangeMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getVoltageAutorange(self, voltageAutorangeMode, channel):
		"""
		This function returns the voltage auto range mode.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageAutorangeMode(c_int16 use with byref) : This parameter returns the voltage auto range mode.
			
			Return values:
			  TLPM_AUTORANGE_VOLTAGE_OFF (0): voltage auto range disabled
			  TLPM_AUTORANGE_VOLTAGE_ON  (1): voltage auto range enabled
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getVoltageAutorange(self.devSession, voltageAutorangeMode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setVoltageRange(self, voltage_to_Measure, channel):
		"""
		This function sets the sensor's voltage range.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltage_to_Measure(c_double) : This parameter specifies the voltage value to be measured in volts [V].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageRange(self.devSession, voltage_to_Measure, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getVoltageRange(self, attribute, voltageValue, channel):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			voltageValue(c_double use with byref) : This parameter returns the specified voltage range value in volts [V].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getVoltageRange(self.devSession, attribute, voltageValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getVoltageRanges(self, voltageValues, rangeCount, channel):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageValues( (c_double * arrayLength)()) : This parameter returns the specified voltage range value in volts [V].
			
			rangeCount(c_uint16 use with byref)
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getVoltageRanges(self.devSession, voltageValues, rangeCount, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setVoltageRangeSearch(self, channel):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageRangeSearch(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setVoltageRef(self, voltageReferenceValue, channel):
		"""
		This function sets the voltage reference value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageReferenceValue(c_double) : This parameter specifies the voltage reference value in volts [V].
			
			Remark:
			This value is used for calculating differences between the actual voltage value and this voltage reference value if Voltage Reference State is ON.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageRef(self.devSession, voltageReferenceValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getVoltageRef(self, attribute, voltageReferenceValue, channel):
		"""
		This function returns the voltage reference value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			voltageReferenceValue(c_double use with byref) : This parameter returns the specified voltage reference value in volts [V].
			
			Remark:
			This value is used for calculating differences between the actual voltage value and this voltage reference value if Voltage Reference State is ON.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getVoltageRef(self.devSession, attribute, voltageReferenceValue, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setVoltageRefState(self, voltageReferenceState, channel):
		"""
		This function sets the voltage reference state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageReferenceState(c_int16) : This parameter specifies the voltage reference state.
			
			Acceptable values:
			  TLPM_VOLTAGE_REF_OFF (0): Voltage reference disabled. Absolute measurement.
			  TLPM_VOLTAGE_REF_ON  (1): Voltage reference enabled. Relative measurement.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageRefState(self.devSession, voltageReferenceState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getVoltageRefState(self, voltageReferenceState, channel):
		"""
		This function returns the voltage reference state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageReferenceState(c_int16 use with byref) : This parameter returns the voltage reference state.
			
			Return values:
			  TLPM_VOLTAGE_REF_OFF (0): Voltage reference disabled. Absolute measurement.
			  TLPM_VOLTAGE_REF_ON  (1): Voltage reference enabled. Relative measurement.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getVoltageRefState(self.devSession, voltageReferenceState, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPeakThreshold(self, peakThreshold, channel):
		"""
		This function sets the peak detector threshold.
		
		Remark:
		Peak detector threshold is in percent [%] of the maximum from the actual measurements range.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			peakThreshold(c_double) : This parameter specifies the peak detector threshold.
			
			Remark:
			Peak detector threshold is in percent [%] of the maximum from the actual measurements range.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPeakThreshold(self.devSession, peakThreshold, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPeakThreshold(self, attribute, peakThreshold, channel):
		"""
		This function returns the peak detector threshold.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			peakThreshold(c_double use with byref) : This parameter returns the peak detector threshold.
			
			Remark:
			Peak detector threshold is in percent [%] of the maximum from the actual measurements range.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPeakThreshold(self.devSession, attribute, peakThreshold, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def startPeakDetector(self, channel):
		"""
		Starts peak finder. For pyro or photodiode in pulse mode.
		
		Notes:
		(1) The function is only available on PM103
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_startPeakDetector(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def isPeakDetectorRunning(self, isRunning, channel):
		"""
		Tests if peak finder is active at the moment. Same as polling status operation register of sensor and checking for bit 3.
		
		Notes:
		(1) The function is only available on PM103
		
		Args:
			isRunning(c_int16 use with byref) : returns the running state of the peak detector.
			
			VI_TRUE: peak detector is running
			VI_FALSE: peak detector is stopped.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_isPeakDetectorRunning(self.devSession, isRunning, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPeakFilter(self, filter, channel):
		"""
		
		Args:
			filter(c_int16) : Valid valus for this parameter are
			0 = NONE
			1 = OVER
			Use OVER if the signal measured is a rectangular signal.
			If it is a sinus or triangle signal use NONE.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPeakFilter(self.devSession, filter, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPeakFilter(self, filter, channel):
		"""
		
		Args:
			filter(c_int16 use with byref) : Valid valus for this parameter are
			0 = NONE
			1 = OVER
			Use OVER if the signal measured is a rectangular signal.
			If it is a sinus or triangle signal use NONE.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPeakFilter(self.devSession, filter, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setExtNtcParameter(self, r0Coefficient, betaCoefficient, channel):
		"""
		This function sets the temperature calculation coefficients for the NTC sensor externally connected to the instrument (NTC IN).
		
		Notes:
		(1) The function is only available on PM400.
		
		
		Args:
			r0Coefficient(c_double) : This parameter specifies the R0 coefficient in [Ohm] for calculating the temperature from the sensor's resistance by the beta parameter equation. R0 is the NTC's resistance at T0 (25 °C = 298.15 K).
			betaCoefficient(c_double) : This parameter specifies the B coefficient in [K] for calculating the temperature from the sensor's resistance by the beta parameter equation.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setExtNtcParameter(self.devSession, r0Coefficient, betaCoefficient, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getExtNtcParameter(self, attribute, r0Coefficient, betaCoefficient, channel):
		"""
		This function gets the temperature calculation coefficients for the NTC sensor externally connected to the instrument (NTC IN).
		
		Notes:
		(1) The function is only available on PM400.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the values to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			r0Coefficient(c_double use with byref) : This parameter returns the specified R0 coefficient in [Ohm].
			betaCoefficient(c_double use with byref) : This parameter returns the specified B coefficient in [K].
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getExtNtcParameter(self.devSession, attribute, r0Coefficient, betaCoefficient, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setFilterPosition(self, filterPosition):
		"""
		This function sets the current filter position
		
		Notes:
		(1) The function is only available on PM160 with firmware version 1.5.4 and higher
		
		
		Args:
			filterPosition(c_int16) : This parameter specifies the current filter position
			
			Acceptable values:
			  VI_OFF (0): Filter position OFF. The filter value will not be used in the power calculation
			  VI_ON  (1): Filter position ON, The filter value will be used in the power correction
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setFilterPosition(self.devSession, filterPosition)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFilterPosition(self, filterPosition):
		"""
		This function returns the current filter position
		
		Notes:
		(1) The function is only available on PM160 with firmware version 1.5.4 and higher
		
		
		Args:
			filterPosition(c_int16 use with byref) : This parameter returns the current filter position
			
			Acceptable values:
			  VI_OFF (0): Filter position OFF. The filter value will not be used in the power calculation
			  VI_ON  (1): Filter position ON, The filter value will be used in the power correction
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFilterPosition(self.devSession, filterPosition)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setFilterAutoMode(self, filterAutoPositionDetection):
		"""
		This function enables / disables the automatic filter position detection
		
		Notes:
		(1) The function is only available on PM160 with firmware version 1.5.4 and higher
		
		
		Args:
			filterAutoPositionDetection(c_int16) : This parameter specifies if the automatic filter position detection is enabled/disabled
			
			Acceptable values:
			  VI_OFF (0): Filter position detection is OFF. The manual set fitler position is used
			  VI_ON  (1): Filter position detection is ON, The filter position will be automatically detected
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setFilterAutoMode(self.devSession, filterAutoPositionDetection)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFilterAutoMode(self, filterAutoPositionDetection):
		"""
		This function returns if the automatic filter position detection is used
		
		Notes:
		(1) The function is only available on PM160 with firmware version 1.5.4 and higher
		
		
		Args:
			filterAutoPositionDetection(c_int16 use with byref) : This parameter returns if the automatic filter position detection is enabled/disabled
			
			Acceptable values:
			  VI_OFF (0): Filter position detection is OFF. The manual set fitler position is used
			  VI_ON  (1): Filter position detection is ON, The filter position will be automatically detected
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFilterAutoMode(self.devSession, filterAutoPositionDetection)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputSlopeRange(self, minSlope, maxSlope, channel):
		"""
		This function returns range of the responsivity in volts per watt [V/W] for the analog output.
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		
		Args:
			minSlope(c_double use with byref) : This parameter returns the minimum voltage in Volt [V/W] of the analog output.
			Lower voltage is clipped to the minimum.
			
			maxSlope(c_double use with byref) : This parameter returns the maximum voltage in Volt [V/W] of the analog output.
			Higher voltage values are clipped to the maximum.
			
			channel(c_uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputSlopeRange(self.devSession, minSlope, maxSlope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAnalogOutputSlope(self, slope, channel):
		"""
		This function sets the responsivity in volts per watt [V/W] for the analog output.
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		Args:
			slope(c_double) : This parameter specifies the responsivity in volts per watt [V/W].
			
			channel(c_uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputSlope(self.devSession, slope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputSlope(self, attribute, slope, channel):
		"""
		This function returns the responsivity in volts per watt [V/W] for the analog output.
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			slope(c_double use with byref) : This parameter returns the specified responsivity in volts per watt [V/W].
			
			channel(c_uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputSlope(self.devSession, attribute, slope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputVoltageRange(self, minVoltage, maxVoltage, channel):
		"""
		This function returns the range in Volt [V] of the analog output.
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		
		Args:
			minVoltage(c_double use with byref) : This parameter returns the minimum voltage in Volt [V] of the analog output.
			Lower voltage is clipped to the minimum.
			
			maxVoltage(c_double use with byref) : This parameter returns the maximum voltage in Volt [V] of the analog output.
			Higher voltage values are clipped to the maximum.
			
			channel(c_uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputVoltageRange(self.devSession, minVoltage, maxVoltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputVoltage(self, attribute, voltage, channel):
		"""
		This function returns the analog output in Volt [V].
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			voltage(c_double use with byref) : This parameter returns the analog output in Volt [V].
			
			channel(c_uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputVoltage(self.devSession, attribute, voltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputGainRange(self, gainRangeIndex, channel):
		"""
		This function returns the analog output hub in Volt [V].
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			gainRangeIndex(c_int16 use with byref)
			channel(c_uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputGainRange(self.devSession, gainRangeIndex, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAnalogOutputGainRange(self, gainRangeIndex, channel):
		"""
		This function returns the analog output hub in Volt [V].
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			gainRangeIndex(c_int16)
			channel(c_uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputGainRange(self.devSession, gainRangeIndex, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputRoute(self, routeName, channel):
		"""
		This function returns the analog output hub in Volt [V].
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			routeName(create_string_buffer(1024))
			channel(c_uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputRoute(self.devSession, routeName, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAnalogOutputRoute(self, routeStrategy, channel):
		"""
		This function returns the analog output hub in Volt [V].
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			routeStrategy(c_uint16) : TLPM_ANALOG_ROUTE_PUR  (0)  (Direct Route): The raw amplified signal is output. This signal is related to the photo current or voltage. It is not wavelength or zero compensated.
			TLPM_ANALOG_ROUTE_CBA  (1)  (Compensated Base Unit): The raw amplified signal is multiplied with a correction factor in hardware to compensate the dark current/voltage. The signal is the photo current or voltage and is not wavelength compensated.
			TLPM_ANALOG_ROUTE_CMA  (2) (Compensated Main Unit): The raw amplified signal is multiplied with a correction factor in hardware to output a analogue voltage related to power or energy. The signal is zero and wavelength compensated.
			channel(c_uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputRoute(self.devSession, routeStrategy, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPositionAnalogOutputSlopeRange(self, minSlope, maxSlope, channel):
		"""
		This function returns range of the responsivity in volts per µm [V/µm] for the analog output.
		
		Notes:
		(1) The function is only available on PM102
		
		
		
		Args:
			minSlope(c_double use with byref) : This parameter returns the minimum slope in [V/µm] of the analog output.
			
			maxSlope(c_double use with byref) : This parameter returns the maximum slope in [V/µm] of the analog output.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputSlopeRange(self.devSession, minSlope, maxSlope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPositionAnalogOutputSlope(self, slope, channel):
		"""
		This function sets the responsivity in volts per µm [V/µm] for the analog output.
		
		Notes:
		(1) The function is only available on PM102
		
		
		Args:
			slope(c_double) : This parameter specifies the responsivity in volts per µm [V/µm] for the AO2 and AO3 channel 
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPositionAnalogOutputSlope(self.devSession, slope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPositionAnalogOutputSlope(self, attribute, slope, channel):
		"""
		This function returns the responsivity in volts per µm [V/µm] for the analog output channels.
		
		Notes:
		(1) The function is only available on PM102
		
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			slope(c_double use with byref) : This parameter returns the specified responsivity in volts per µm [V/µm] for the AO2 and AO3 channel 
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputSlope(self.devSession, attribute, slope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPositionAnalogOutputVoltageRange(self, minVoltage, maxVoltage, channel):
		"""
		This function returns the range in Volt [V] of the analog output.
		
		Notes:
		(1) The function is only available on PM102
		
		
		
		Args:
			minVoltage(c_double use with byref) : This parameter returns the minimum voltage in Volt [V] of the analog output.
			Lower voltage is clipped to the minimum.
			
			maxVoltage(c_double use with byref) : This parameter returns the maximum voltage in Volt [V] of the analog output.
			Higher voltage values are clipped to the maximum.
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputVoltageRange(self.devSession, minVoltage, maxVoltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPositionAnalogOutputVoltage(self, attribute, voltageX, voltageY, channel):
		"""
		This function returns the analog output in Volt [V].
		
		Notes:
		(1) The function is only available on PM102
		
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			voltageX(c_double use with byref) : This parameter returns the analog output in Volt [V] for the AO2 channel ( x direction)
			
			voltageY(c_double use with byref) : This parameter returns the analog output in Volt [V] for the AO3 channel ( y direction)
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputVoltage(self.devSession, attribute, voltageX, voltageY, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getMeasPinMode(self, state, channel):
		"""
		This function returns the meas pin state
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			state(c_int16 use with byref) : This parameter returns the analog output hub in Volt [V].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getMeasPinMode(self.devSession, state, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getMeasPinPowerLevel(self, level, channel):
		"""
		This function returns the meas pin power level in [W]
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			level(c_double use with byref) : This parameter returns the measure pin output power level in Watt [W].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getMeasPinPowerLevel(self.devSession, level, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setMeasPinPowerLevel(self, level, channel):
		"""
		This function returns the meas pin state
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			level(c_double) : This parameter sets the measure pin output power level in Watt [W].
			
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setMeasPinPowerLevel(self.devSession, level, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getMeasPinEnergyLevel(self, level, channel):
		"""
		This function returns the meas pin energy level in [J]
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			level(c_double use with byref) : This parameter returns the measure pin output energy level in  [J].
			
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getMeasPinEnergyLevel(self.devSession, level, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setMeasPinEnergyLevel(self, level, channel):
		"""
		This function returns the meas pin state
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			level(c_double) : This parameter returns the measurement pin energy level in [J].
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setMeasPinEnergyLevel(self.devSession, level, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setNegativePulseWidth(self, pulseDuration, channel):
		"""
		This function sets the low pulse duration in Seconds
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			pulseDuration(c_double) : low pulse duration in Seconds
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setNegativePulseWidth(self.devSession, pulseDuration, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPositivePulseWidth(self, pulseDuration, channel):
		"""
		This function sets the high pulse duration in Seconds
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			pulseDuration(c_double) : high pulse duration in Seconds
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPositivePulseWidth(self.devSession, pulseDuration, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setNegativeDutyCycle(self, dutyCycle, channel):
		"""
		This function sets the low duty cycle in Percent
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			dutyCycle(c_double) : low pulse duty cycle in Percent
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setNegativeDutyCycle(self.devSession, dutyCycle, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPositiveDutyCycle(self, dutyCycle, channel):
		"""
		This function sets the high duty cycle in Percent
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			dutyCycle(c_double) : high pulse duty cycle in Percent
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPositiveDutyCycle(self.devSession, dutyCycle, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measCurrent(self, current, channel):
		"""
		This function is used to obtain current readings from the instrument. 
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			current(c_double use with byref) : This parameter returns the current in amperes [A].
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measCurrent(self.devSession, current, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measVoltage(self, voltage, channel):
		"""
		This function is used to obtain voltage readings from the instrument. 
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltage(c_double use with byref) : This parameter returns the voltage in volts [V].
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measVoltage(self.devSession, voltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measPower(self, power, channel):
		"""
		This function is used to obtain power readings from the instrument. 
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
		
		Args:
			power(c_double use with byref) : This parameter returns the power in the selected unit.
			
			Remark:
			(1) This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
			(2) Select the unit with <Set Power Unit>.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measPower(self.devSession, power, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measEnergy(self, energy, channel):
		"""
		This function is used to obtain energy readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			energy(c_double use with byref) : This parameter returns the actual measured energy value in joule [J].
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measEnergy(self.devSession, energy, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measFreq(self, frequency, channel):
		"""
		This function is used to obtain frequency readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			frequency(c_double use with byref) : This parameter returns the actual measured frequency of the input signal. 
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measFreq(self.devSession, frequency, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measPowerDens(self, powerDensity, channel):
		"""
		This function is used to obtain power density readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			powerDensity(c_double use with byref) : This parameter returns the actual measured power density in watt per square centimeter [W/cm²].
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measPowerDens(self.devSession, powerDensity, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measEnergyDens(self, energyDensity, channel):
		"""
		This function is used to obtain energy density readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			energyDensity(c_double use with byref) : This parameter returns the actual measured energy in joule per square centimeter [J/cm²].
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measEnergyDens(self.devSession, energyDensity, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measAuxAD0(self, voltage, channel):
		"""
		This function is used to obtain voltage readings from the instrument's auxiliary AD0 input. 
		
		Notes:
		(1) The function is only available on PM200, PM400.
		
		
		Args:
			voltage(c_double use with byref) : This parameter returns the voltage in volt.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measAuxAD0(self.devSession, voltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measAuxAD1(self, voltage, channel):
		"""
		This function is used to obtain voltage readings from the instrument's auxiliary AD1 input. 
		
		Notes:
		(1) The function is only available on PM200, PM400.
		
		
		Args:
			voltage(c_double use with byref) : This parameter returns the voltage in volt.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measAuxAD1(self.devSession, voltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measEmmHumidity(self, humidity, channel):
		"""
		This function is used to obtain relative humidity readings from the Environment Monitor Module (EMM) connected to the instrument. 
		
		Notes:
		(1) The function is only available on PM200, PM400.
		(2) The function will return an error when no EMM is connected.
		
		Args:
			humidity(c_double use with byref) : This parameter returns the relative humidity in %.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measEmmHumidity(self.devSession, humidity, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measEmmTemperature(self, temperature, channel):
		"""
		This function is used to obtain temperature readings from the Environment Monitor Module (EMM) connected to the instrument. 
		
		Notes:
		(1) The function is only available on PM200, PM400.
		(2) The function will return an error when no EMM is connected.
		
		Args:
			temperature(c_double use with byref) : This parameter returns the temperature in °C
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measEmmTemperature(self.devSession, temperature, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measExtNtcTemperature(self, temperature, channel):
		"""
		This function gets temperature readings from the external thermistor sensor connected to the instrument (NTC IN). 
		
		Notes:
		(1) The function is only available on PM400.
		(2) The function will return an error when no external sensor is connected.
		
		
		Args:
			temperature(c_double use with byref) : This parameter returns the temperature in °C
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measExtNtcTemperature(self.devSession, temperature, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measExtNtcResistance(self, resistance, channel):
		"""
		This function gets resistance readings from the external thermistor sensor connected to the instrument (NTC IN). 
		
		Notes:
		(1) The function is only available on PM400.
		(2) The function will return an error when no external sensor is connected.
		
		
		Args:
			resistance(c_double use with byref) : This parameter returns the resistance in Ohm
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measExtNtcResistance(self.devSession, resistance, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measHeadResistance(self, frequency, channel):
		"""
		This function is used to obtain frequency readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			frequency(c_double use with byref) : This parameter returns the resistance in Ohm
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measHeadResistance(self.devSession, frequency, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measHeadTemperature(self, frequency, channel):
		"""
		This function is used to obtain frequency readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			frequency(c_double use with byref) : This parameter returns the temperature in °C
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measHeadTemperature(self.devSession, frequency, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def meas4QPositions(self, xPosition, yPosition, channel):
		"""
		This function returns the x and position of a 4q sensor
		
		Notes:
		(1) The function is only available on PM101, PM102, PM400.
		
		
		Args:
			xPosition(c_double use with byref) : This parameter returns the actual measured x position in µm
			yPosition(c_double use with byref) : This parameter returns the actual measured y position in µm
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_meas4QPositions(self.devSession, xPosition, yPosition, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def meas4QVoltages(self, voltage1, voltage2, voltage3, voltage4, channel):
		"""
		This function returns the voltage of each sector of a 4q sensor
		
		Notes:
		(1) The function is only available on PM101, PM102, PM400.
		
		
		Args:
			voltage1(c_double use with byref) : This parameter returns the actual measured voltage of the upper left sector of a 4q sensor.
			voltage2(c_double use with byref)
			voltage3(c_double use with byref)
			voltage4(c_double use with byref)
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_meas4QVoltages(self.devSession, voltage1, voltage2, voltage3, voltage4, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measNegPulseWidth(self, negativePulseWidth, channel):
		"""
		This function returns the negative pulse width in µsec.
		Notes:
		(1) The function is only available on PM103.
		
		
		Args:
			negativePulseWidth(c_double use with byref) : Negative Pulse Width in µsec.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measNegPulseWidth(self.devSession, negativePulseWidth, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measPosPulseWidth(self, positivePulseWidth, channel):
		"""
		This function returns the positive pulse width in µsec.
		Notes:
		(1) The function is only available on PM103.
		
		
		Args:
			positivePulseWidth(c_double use with byref) : Positive Pulse Width in µsec.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measPosPulseWidth(self.devSession, positivePulseWidth, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measNegDutyCycle(self, negativeDutyCycle, channel):
		"""
		This function returns the negative duty cycle in percentage.
		Notes:
		(1) The function is only available on PM103.
		
		
		Args:
			negativeDutyCycle(c_double use with byref) : Negative Duty Cycle in percentage.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measNegDutyCycle(self.devSession, negativeDutyCycle, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measPosDutyCycle(self, positiveDutyCycle, channel):
		"""
		This function returns the positive duty cycle in percentage.
		Notes:
		(1) The function is only available on PM103.
		
		
		Args:
			positiveDutyCycle(c_double use with byref) : Positive Duty Cycle in percentage.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measPosDutyCycle(self.devSession, positiveDutyCycle, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measPowerMeasurementSequence(self, baseTime, channel):
		"""
		This function send the SCPI Command "CONF:ARR:POW" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		
		Duration of measurement in µsec = Count * Interval
		The maximum capture time is 1 sec regardless of the used interval
		
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM103.
		
		
		Args:
			baseTime(c_uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is 100µsec without averaging
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measPowerMeasurementSequence(self.devSession, baseTime, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measPowerMeasurementSequenceHWTrigger(self, baseTime, hPos, channel):
		"""
		PM103:
		This function send the SCPI Command "CONF:ARR:HWTrig:POW" to the device.
		Then is possible to call the methods 'startMeasurementSequence' and  'getMeasurementSequenceHWTrigger' to get the power data.
		 
		Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging (setPowerAutoRange to OFF)
		
		PM101 special:
		This function send the SCPI Command "CONF:ARR" to the device.
		Then is possible to call the methods 'startMeasurementSequence' and 'getMeasurementSequenceHWTrigger' to get the power data.
		
		Note: The function is only available on PM103 and PM101 special.
		
		
		Args:
			baseTime(c_uint32) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is 100 µsec without averaging.
			
			PM101 special:
			time to collect measurements.
			hPos(c_uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measPowerMeasurementSequenceHWTrigger(self.devSession, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measureCurrentMeasurementSequence(self, baseTime, channel):
		"""
		This function send the SCPI Command "CONF:ARR:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		 
		Duration of measurement in µsec = Count* Interval
		The maximum capture time is 1 sec regardless of the used interval
		
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM103.
		
		
		Args:
			baseTime(c_uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is 100µsec without averaging
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measureCurrentMeasurementSequence(self.devSession, baseTime, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measureCurrentMeasurementSequenceHWTrigger(self, baseTime, hPos, channel):
		"""
		This function send the SCPI Command "CONF:ARR:HWTrig:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequenceHWTrigger' to get the current data.
		 
		Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging ( setPowerAutoRange to OFF)
		
		PM101 special:
		This function send the SCPI Command "CONF:ARR:CURR" to the device.
		Then is possible to call the methods 'startMeasurementSequence' and 'getMeasurementSequenceHWTrigger' to get the current data.
		
		Note: The function is only available on PM103 and PM101 special.
		
		
		Args:
			baseTime(c_uint32) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is 100 µsec without averaging.
			
			PM101 special:
			time to collect measurements.
			hPos(c_uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measureCurrentMeasurementSequenceHWTrigger(self.devSession, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measureVoltageMeasurementSequence(self, baseTime, channel):
		"""
		This function send the SCPI Command "CONF:ARR:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		 
		Duration of measurement in µsec = Count* Interval
		The maximum capture time is 1 sec regardless of the used interval
		
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM5020.
		
		
		Args:
			baseTime(c_uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is 100µsec without averaging
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measureVoltageMeasurementSequence(self.devSession, baseTime, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measureVoltageMeasurementSequenceHWTrigger(self, baseTime, hPos, channel):
		"""
		This function send the SCPI Command "CONF:ARR:HWTrig:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequenceHWTrigger' to get the current data.
		 
		Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging ( setPowerAutoRange to OFF)
		
		Note: The function is only available on PM5020.
		
		
		Args:
			baseTime(c_uint32) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is 100 µsec without averaging.
			
			PM101 special:
			time to collect measurements.
			hPos(c_uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measureVoltageMeasurementSequenceHWTrigger(self.devSession, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFetchState(self, state, channel):
		"""
		This function can be used to get the measurement state information before doing a fetch.
		
		Notes:
		(1) The function is only available on PM5020.
		
		
		Args:
			state(c_int16 use with byref) : This parameter returns the fetch state
			
			VI_FALSE = no new measurement is ready
			VI_TRUE  = a new measurement is ready and can be get by "FETCH#?" ( replace # with the number of the channel)
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFetchState(self.devSession, state, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def resetFastArrayMeasurement(self, channel):
		"""
		This function resets the array measurement.
		
		Note: The function is only available on PM103.
		
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_resetFastArrayMeasurement(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confPowerFastArrayMeasurement(self, channel):
		"""
		This function is used to conffiure the fast array measurement of power values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds.   
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confPowerFastArrayMeasurement(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confCurrentFastArrayMeasurement(self, channel):
		"""
		This function is used to conffiure the fast array measurement of current values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. 
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confCurrentFastArrayMeasurement(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confVoltageFastArrayMeasurement(self, channel):
		"""
		This function is used to conffiure the fast array measurement of voltage values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds.  
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confVoltageFastArrayMeasurement(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confPDensityFastArrayMeasurement(self, channel):
		"""
		This function is used to conffiure the fast array measurement of P density values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. 
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confPDensityFastArrayMeasurement(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confEnergyFastArrayMeasurement(self, channel):
		"""
		This function is used to configure the fast array measurement of energy values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. 
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confEnergyFastArrayMeasurement(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confEDensityFastArrayMeasurement(self, channel):
		"""
		This function is used to configure the fast array measurement of E density values.
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. 
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confEDensityFastArrayMeasurement(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getNextFastArrayMeasurement(self, count, timestamps, values, values2, channel):
		"""
		This function is used to obtain measurements from the instrument. 
		The result are timestamp - value pairs.
		
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds.
		
		Args:
			count(c_uint16 use with byref) : The count of timestamp - measurement value pairs
			The value will be 200
			timestamps( (c_uint32 * arrayLength)()) : Buffer containing up to 200 timestamps.
			This are raw timestamps and are NOT in ms.
			values( (c_float * arrayLength)()) : Buffer containing up to 200 measurement values.
			values2( (c_float * arrayLength)()) : Array of power/current measurements. The size of this array is 100 * baseTime.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getNextFastArrayMeasurement(self.devSession, count, timestamps, values, values2, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFastMaxSamplerate(self, pVal, channel):
		"""
		This function is used to obtain the maximal possible sample rate (Hz) 
		
		Args:
			pVal(c_uint32 use with byref) : Max possible sample rate (Hz)
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFastMaxSamplerate(self.devSession, pVal, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confPowerMeasurementSequence(self, baseTime, channel):
		"""
		This function send the SCPI Command "CONF:ARR:POW" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		
		Duration of measurement in µsec = Count * Interval
		The maximum capture time is 1 sec regardless of the used interval
		
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM103.
		
		
		Args:
			baseTime(c_uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is 100µsec without averaging
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confPowerMeasurementSequence(self.devSession, baseTime, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confPowerMeasurementSequenceHWTrigger(self, trigSrc, baseTime, hPos, channel):
		"""
		PM103:
		This function send the SCPI Command "CONF:ARR:HWTrig:POW" to the device.
		Then is possible to call the methods 'startMeasurementSequence' and  'getMeasurementSequenceHWTrigger' to get the power data.
		 
		Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging (setPowerAutoRange to OFF)
		
		PM101 special:
		This function send the SCPI Command "CONF:ARR" to the device.
		Then is possible to call the methods 'startMeasurementSequence' and 'getMeasurementSequenceHWTrigger' to get the power data.
		
		Note: The function is only available on PM103 and PM101 special.
		
		
		Args:
			trigSrc(c_uint16) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is 100 µsec without averaging.
			
			PM101 special:
			time to collect measurements.
			baseTime(c_uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			hPos(c_uint32) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confPowerMeasurementSequenceHWTrigger(self.devSession, trigSrc, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confCurrentMeasurementSequence(self, baseTime, channel):
		"""
		This function send the SCPI Command "CONF:ARR:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		 
		Duration of measurement in µsec = Count* Interval
		The maximum capture time is 1 sec regardless of the used interval
		
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM103.
		
		
		Args:
			baseTime(c_uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is 100µsec without averaging
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confCurrentMeasurementSequence(self.devSession, baseTime, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confCurrentMeasurementSequenceHWTrigger(self, trigSrc, baseTime, hPos, channel):
		"""
		This function send the SCPI Command "CONF:ARR:HWTrig:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequenceHWTrigger' to get the current data.
		 
		Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging ( setPowerAutoRange to OFF)
		
		PM101 special:
		This function send the SCPI Command "CONF:ARR:CURR" to the device.
		Then is possible to call the methods 'startMeasurementSequence' and 'getMeasurementSequenceHWTrigger' to get the current data.
		
		Note: The function is only available on PM103 and PM101 special.
		
		
		Args:
			trigSrc(c_uint16) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is 100 µsec without averaging.
			
			PM101 special:
			time to collect measurements.
			baseTime(c_uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			hPos(c_uint32) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confCurrentMeasurementSequenceHWTrigger(self.devSession, trigSrc, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confVolatgeMeasurementSequence(self, baseTime, channel):
		"""
		
		Args:
			baseTime(c_uint32)
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confVolatgeMeasurementSequence(self.devSession, baseTime, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confVolatgeMeasurementSequenceHWTrigger(self, trigSrc, baseTime, hPos, channel):
		"""
		
		Args:
			trigSrc(c_uint16)
			baseTime(c_uint32)
			hPos(c_uint32)
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confVolatgeMeasurementSequenceHWTrigger(self.devSession, trigSrc, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def startMeasurementSequence(self, autoTriggerDelay, triggerForced, channel):
		"""
		This function send the SCPI Command "INIT" to the device.
		
		PM103:
		Then it calls TLPM_readRegister for the register TLPM_REG_OPER_COND if there is new data to read
		
		If this method is successfull you can call getMeasurementSequence or getMeasurementSequenceHWTrigger
		
		PM101 special:
		Just the INIT command is send to the device.
		
		
		Note: The function is only available on PM103 and PM101 special. 
		
		
		
		Args:
			autoTriggerDelay(c_uint32) : PM103:
			The unit of this parameter is milliseconds.
			If this parameter bigger then zero, the method will
			wait the time in milliseconds to send the SCPI command:"TRIGer:ARRay:FORce".
			
			This command will force the measurement. 
			
			PM101 special:
			Not used.
			triggerForced(c_int16 use with byref) : PM103:
			Return parameter is TRUE if the command:"TRIGer:ARRay:FORce". was internally send to the device. See parameter "AutoTriggerDelay".
			
			PM101 special:
			Not used.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_startMeasurementSequence(self.devSession, autoTriggerDelay, triggerForced, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getMeasurementSequence(self, baseTime, timeStamps, values, values2, channel):
		"""
		 Should be called if the methods confPowerMeasurementSequence and startMeasurementSequence were called first.
		 
		This function filles the given array with (100 * baseTime) measurements from the device.
		
		Duration of measurement in µsec = Count* Interval
		The maximum capture time is 1 sec regardless of the used inteval
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM103.
		
		
		Args:
			baseTime(c_uint32) : The amount of samples to collect in the internal interation of the method.
			The value can be from 1 to 100.
			
			Every sample is 10µs for PM5020.
			timeStamps( (c_float * arrayLength)()) : Array of time stamps in ms. The size of this array is 100 * baseTime.
			values( (c_float * arrayLength)()) : Array of power/current measurements. The size of this array is 100 * baseTime.
			values2( (c_float * arrayLength)()) : Array of power/current measurements. The size of this array is 100 * baseTime.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getMeasurementSequence(self.devSession, baseTime, timeStamps, values, values2, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getMeasurementSequenceHWTrigger(self, baseTime, timeStamps, values, values2, channel):
		"""
		Should be called if the method confPowerMeasurementSequenceHWTrigger and startMeasurementSequence were called first, (or confCurrentMeasurementSequenceHWTrigger and startMeasurementSequence)
		
		PM103: 
		 This function fills the given array with (100 * baseTime) measurements from the device, external triggered.
		 Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		 
		PM101 special:
		This function fills the Values array with measurements from the device, external triggered.
		The size of measurements to set in the array is in the parameter Base Time. Base Time is equal to the time of measurement through the intervall between each measurement. These parameters are set in the method confPowerMeasurementSequenceHWTrigger. 
		 
		
		 Note: The function is only available on PM103 and PM101 special (Not HWT). 
		
		
		Args:
			baseTime(c_uint32) : PM103:
			The amount of samples to collect in the internal interation of the method. The value can be from 1 to 100.
			PM101:
			Size of measuremnts to collect from the PM101. Time of measurement / intervall.
			timeStamps( (c_float * arrayLength)()) : PM103:
			Array of time stamps in ms. The size of this array is 100 * baseTime.
			
			PM101 special:
			Not used.
			values( (c_float * arrayLength)()) : PM103:
			Array of power/current measurements. The size of this array is 100 * baseTime.
			
			PM101:
			Array of power/current measurements. The size of this array is the time of measurement through the interval.
			
			values2( (c_float * arrayLength)()) : Array of power/current measurements. The size of this array is 100 * baseTime.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getMeasurementSequenceHWTrigger(self.devSession, baseTime, timeStamps, values, values2, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confBurstArrayMeasurementChannel(self, channel):
		"""
		This function is used to configure the burst array measurement of each channel.
		
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasurementChannel(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confBurstArrayMeasPowerTrigger(self, initDelay, burstCount, averaging):
		"""
		
		Args:
			initDelay(c_uint32)
			burstCount(c_uint32)
			averaging(c_uint32)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasPowerTrigger(self.devSession, initDelay, burstCount, averaging)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confBurstArrayMeasCurrentTrigger(self, initDelay, burstCount, averaging):
		"""
		
		Args:
			initDelay(c_uint32)
			burstCount(c_uint32)
			averaging(c_uint32)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasCurrentTrigger(self.devSession, initDelay, burstCount, averaging)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def startBurstArrayMeasurement(self):
		"""
		Starts a burst array measurement
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_startBurstArrayMeasurement(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getBurstArraySamplesCount(self, samplesCount):
		"""
		Read the amount of samples in the burst array buffer
		
		Args:
			samplesCount(c_uint32 use with byref) : Amount of samples measure in burst mode.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getBurstArraySamplesCount(self.devSession, samplesCount)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getBurstArraySamples(self, startIndex, sampleCount, timeStamps, values, values2):
		"""
		Read scope buffer content at index 
		
		Args:
			startIndex(c_uint32)
			sampleCount(c_uint32)
			timeStamps( (c_float * arrayLength)()) : Buffer containing the samples.
			
			Buffer size: Samples Count * 2
			values( (c_float * arrayLength)())
			values2( (c_float * arrayLength)())
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getBurstArraySamples(self.devSession, startIndex, sampleCount, timeStamps, values, values2)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDigIoDirection(self, IO0, IO1, IO2, IO3):
		"""
		This function sets the digital I/O port direction.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			IO0(c_int16) : This parameter specifies the I/O port #0 direction.
			
			Input:  VI_OFF (0)
			Output: VI_ON  (1)
			
			IO1(c_int16) : This parameter specifies the I/O port #1 direction.
			
			Input:  VI_OFF (0)
			Output: VI_ON  (1)
			
			IO2(c_int16) : This parameter specifies the I/O port #2 direction.
			
			Input:  VI_OFF (0)
			Output: VI_ON  (1)
			
			IO3(c_int16) : This parameter specifies the I/O port #3 direction.
			
			Input:  VI_OFF (0)
			Output: VI_ON  (1)
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDigIoDirection(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDigIoDirection(self, IO0, IO1, IO2, IO3):
		"""
		This function returns the digital I/O port direction.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			IO0(c_int16 use with byref) : This parameter returns the I/O port #0 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO1(c_int16 use with byref) : This parameter returns the I/O port #1 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO2(c_int16 use with byref) : This parameter returns the I/O port #2 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO3(c_int16 use with byref) : This parameter returns the I/O port #3 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDigIoDirection(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDigIoOutput(self, IO0, IO1, IO2, IO3):
		"""
		This function sets the digital I/O outputs.
		
		Notes:
		(1) Only ports configured as outputs are affected by this function. Use <Set Digital I/O Direction> to configure ports as outputs.
		(2) The function is only available on PM200 and PM400.
		
		Args:
			IO0(c_int16) : This parameter specifies the I/O port #0 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
			IO1(c_int16) : This parameter specifies the I/O port #1 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
			IO2(c_int16) : This parameter specifies the I/O port #2 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
			IO3(c_int16) : This parameter specifies the I/O port #3 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDigIoOutput(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDigIoOutput(self, IO0, IO1, IO2, IO3):
		"""
		This function returns the digital I/O output settings.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			IO0(c_int16 use with byref) : This parameter returns the I/O port #0 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO1(c_int16 use with byref) : This parameter returns the I/O port #1 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO2(c_int16 use with byref) : This parameter returns the I/O port #2 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO3(c_int16 use with byref) : This parameter returns the I/O port #3 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDigIoOutput(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDigIoPort(self, IO0, IO1, IO2, IO3):
		"""
		This function returns the actual digital I/O port level.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			IO0(c_int16 use with byref) : This parameter returns the I/O port #0 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO1(c_int16 use with byref) : This parameter returns the I/O port #1 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO2(c_int16 use with byref) : This parameter returns the I/O port #2 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO3(c_int16 use with byref) : This parameter returns the I/O port #3 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDigIoPort(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDigIoPinMode(self, pinNumber, pinMode):
		"""
		This function sets the digital I/O port direction.
		
		Note: The function is only available on PM200, PM400 and PM103
		
		Args:
			pinNumber(c_int16) : Number of the Pin.
			
			Range: 1-7
			pinMode(c_uint16) : This parameter specifies the I/O port direction.
			
			Input:       DIGITAL_IO_CONFIG_INPUT   (0)
			Output:      DIGITAL_IO_CONFIG_OUTPUT  (1)
			Alternative: DIGITAL_IO_CONFIG_ALT     (2)
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDigIoPinMode(self.devSession, pinNumber, pinMode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDigIoPinMode(self, pinNumber, pinMode):
		"""
		This function returns the digital I/O port direction.
		
		Note: The function is only available on PM200, PM400 and PM103
		
		Args:
			pinNumber(c_int16) : Number of the Pin.
			
			Range: 1-7
			pinMode(c_uint16 use with byref) : This parameter returns the I/O port #0 direction.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			Input:              DIGITAL_IO_CONFIG_INPUT      (0)
			Output:             DIGITAL_IO_CONFIG_OUTPUT     (1)
			Input Alternative:  DIGITAL_IO_CONFIG_INPUT_ALT  (2)
			Output Alternative: DIGITAL_IO_CONFIG_OUTPUT_ALT (3)
			
			
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDigIoPinMode(self.devSession, pinNumber, pinMode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDigIoOutput2(self, IO0, IO1, IO2, IO3):
		"""
		
		Args:
			IO0(c_int16)
			IO1(c_int16)
			IO2(c_int16)
			IO3(c_int16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDigIoOutput(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDigIoOutput2(self, IO0, IO1, IO2, IO3):
		"""
		
		Args:
			IO0(c_int16 use with byref)
			IO1(c_int16 use with byref)
			IO2(c_int16 use with byref)
			IO3(c_int16 use with byref)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDigIoOutput(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDigIoPinInput(self, IO0, IO1, IO2, IO3):
		"""
		This function returns the actual digital I/O port level.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			IO0(c_int16 use with byref) : This parameter returns the I/O port #0 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO1(c_int16 use with byref) : This parameter returns the I/O port #1 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO2(c_int16 use with byref) : This parameter returns the I/O port #2 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO3(c_int16 use with byref) : This parameter returns the I/O port #3 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDigIoPinInput(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getShutterInterlock(self, interlockState):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			interlockState(c_int16 use with byref)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getShutterInterlock(self.devSession, interlockState)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setShutterPosition(self, position):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			position(c_int16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setShutterPosition(self.devSession, position)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getShutterPosition(self, position):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			position(c_int16 use with byref)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getShutterPosition(self.devSession, position)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setI2CMode(self, mode):
		"""
		This setter changes the I2C speed and operating mode. By dafault I2C is controlled by the powermeter and SCPI I2C commands are disabled. It is mandatory to select a manual mode before SCPI I2C commands are enabled. The configuraiton is not stored for next boot. Be aware in manual mode the optional external environmental sensor will not longer be queried by the powermeter. The following modes are supported
		INTER: I2C controlled by powermeter. SCPI I2C disabled.
		SLOW: I2C controlled by SCPI commands in 100k standard speed. Powermeter does not access bus.
		FAST: I2C controlled by SCPI commands in 400k fast speed. Powermeter does not access bus.
		
		Note: The function is only available on PM5020
		
		Args:
			mode(c_uint16) : INTER,SLOW,FASTnew I2C operating mode and speed. See list in detail section.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setI2CMode(self.devSession, mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getI2CMode(self, mode):
		"""
		The command queries the I2C speed and operating mode. 
		INTER: I2C controlled by powermeter. SCPI I2C disabled.
		SLOW: I2C controlled by SCPI commands in 100k standard speed. Powermeter does not access bus.
		FAST: I2C controlled by SCPI commands in 400k fast speed. Powermeter does not access bus.
		
		Note: The function is only available on PM5020
		
		Args:
			mode(c_int16 use with byref) : INTER,SLOW,FASTI2C operating mode and speed
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getI2CMode(self.devSession, mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def I2CRead(self, address, count, dataRead):
		"""
		The command receives data from slave with given address. The function requires TLPMX_setI2CMode to be called once previously. The command returns data as integer. Data is read synchronously with the SCPI command.
		
		Note: The function is only available on PM5020
		
		Args:
			address(c_uint32) : I2C slave address. Address are bit 7 to bit 1. Bit 0 is ignored.
			count(c_uint32) : amount of bytes to read from address. Needs to be less than 128.
			dataRead(c_uint32 use with byref) : received data.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_I2CRead(self.devSession, address, count, dataRead)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def I2CWrite(self, address, hexData):
		"""
		The command transmits given data to slave with given address. The function requires TLPMX_setI2CMode  to be called once previously. The transmission data is given as hexadecimal string parameter. The length needs to be a multiple of two as two hex digits encode a single byte. Leading zeros are mandatory. So to transfer byte 2 and 75 use string 024B. Hex digits are support upper or lowercase letters. The maximal length are 128 Bytes. Data is transferred synchronously with the SCPI command. If you want to read after writing some data you may use TLPMX_I2CWriteRead.
		
		Note: The function is only available on PM5020
		
		Args:
			address(c_uint32) : I2C slave address. Address are bit 7 to bit 1. Bit 0 is ignored.
			hexData(c_char_p) : transmission data as hexadecimal string without byte separator. Length always multiple of 2.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_I2CWrite(self.devSession, address, hexData)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def I2CWriteRead(self, address, hexSendData, count, dataRead):
		"""
		The command transmits given data to slave with given address following a bus reception from same device if transmission was successful. This command is a convenience function for a CON:I2C#:WRIT followed by a CON:I2C#:READ? command sequence. The maximal transmission and reception byte count is 128. For closer details of hexString format read TLPMX_I2CWrite command description.
		
		Note: The function is only available on PM5020
		
		Args:
			address(c_uint32) : I2C slave address. Address are bit 7 to bit 1. Bit 0 is ignored.
			hexSendData(c_char_p) : transmission data as hexadecimal string without byte separator. Length always multiple of 2.
			count(c_uint32) : amount of bytes to read from address.
			dataRead(c_uint32 use with byref) : received data.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_I2CWriteRead(self.devSession, address, hexSendData, count, dataRead)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFanState(self, isRunning, channel):
		"""
		This function returns if the fan is running
		
		Note: The function is only available on PM5020
		
		Args:
			isRunning(c_int16 use with byref) : Returns the fan running state
			
			VI_OFF (0) Fan is still
			VI_ON  (1) Fan is running
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFanState(self.devSession, isRunning, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setFanMode(self, mode, channel):
		"""
		This function sets the state of the fan to 
		
		FAN_OPER_OFF         (0)
		FAN_OPER_FULL        (1)
		FAN_OPER_OPEN_LOOP   (2)
		FAN_OPER_CLOSED_LOOP (3)
		FAN_OPER_TEMPER_CTRL (4)
		
		Note: The function is only available on PM5020
		
		Args:
			mode(c_uint16)
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setFanMode(self.devSession, mode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFanMode(self, mode, channel):
		"""
		This function gets the state of the fan of
		
		FAN_OPER_OFF         (0)
		FAN_OPER_FULL        (1)
		FAN_OPER_OPEN_LOOP   (2)
		FAN_OPER_CLOSED_LOOP (3)
		FAN_OPER_TEMPER_CTRL (4)
		
		Note: The function is only available on PM5020
		
		Args:
			mode(c_uint16 use with byref)
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFanMode(self.devSession, mode, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setFanVoltage(self, voltage, channel):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			voltage(c_double)
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setFanVoltage(self.devSession, voltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFanVoltage(self, voltage, channel):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			voltage(c_double use with byref)
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFanVoltage(self.devSession, voltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setFanRpm(self, maxRPM, targetRPM, channel):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			maxRPM(c_double) : Max RPM of the Fan
			targetRPM(c_double) : Target RPM of the Fan
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setFanRpm(self.devSession, maxRPM, targetRPM, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFanRpm(self, maxRPM, targetRPM, channel):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			maxRPM(c_double use with byref) : Max RPM of the fan
			targetRPM(c_double use with byref) : Target RPM of the fan
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFanRpm(self.devSession, maxRPM, targetRPM, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getActFanRpm(self, RPM, channel):
		"""
		Gets the current rpm of the fan
		
		Note: The function is only available on PM5020
		
		Args:
			RPM(c_double use with byref) : Current RPM of the fan
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getActFanRpm(self.devSession, RPM, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setFanTemperatureSource(self, source, channel):
		"""
		This function sets the source for the temperature control
		
		FAN_TEMPER_SRC_HEAD (0)    ///< Sensor head temper source
		FAN_TEMPER_SRC_EXT_NTC (1) ///< External NTC temper source
		
		Note: The function is only available on PM5020
		
		Args:
			source(c_uint16) : Source for the temperature control
			
			FAN_TEMPER_SRC_HEAD (0)    ///< Sensor head temper source
			FAN_TEMPER_SRC_EXT_NTC (1) ///< External NTC temper source
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setFanTemperatureSource(self.devSession, source, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFanTemperatureSource(self, source, channel):
		"""
		This function gets the source for the temperature control
		
		FAN_TEMPER_SRC_HEAD (0)    ///< Sensor head temper source
		FAN_TEMPER_SRC_EXT_NTC (1) ///< External NTC temper source
		
		Note: The function is only available on PM5020
		
		Args:
			source(c_uint16 use with byref) : Source for the temperature control
			
			FAN_TEMPER_SRC_HEAD (0)    ///< Sensor head temper source
			FAN_TEMPER_SRC_EXT_NTC (1) ///< External NTC temper source
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFanTemperatureSource(self.devSession, source, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setFanAdjustParameters(self, voltageMin, voltageMax, temperatureMin, temperatureMax, channel):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			voltageMin(c_double)
			voltageMax(c_double)
			temperatureMin(c_double)
			temperatureMax(c_double)
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setFanAdjustParameters(self.devSession, voltageMin, voltageMax, temperatureMin, temperatureMax, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFanAdjustParameters(self, voltageMin, voltageMax, temperatureMin, temperatureMax, channel):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			voltageMin(c_double use with byref)
			voltageMax(c_double use with byref)
			temperatureMin(c_double use with byref)
			temperatureMax(c_double use with byref)
			channel(c_uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getFanAdjustParameters(self.devSession, voltageMin, voltageMax, temperatureMin, temperatureMax, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def errorMessage(self, statusCode, description):
		"""
		This function takes the error code returned by the instrument driver functions interprets it and returns it as an user readable string. 
		
		Status/error codes and description:
		
		--- Instrument Driver Errors and Warnings ---
		Status      Description
		-------------------------------------------------
		         0  No error (the call was successful).
		0x3FFF0085  Unknown Status Code     - VI_WARN_UNKNOWN_STATUS
		0x3FFC0901  WARNING: Value overflow - VI_INSTR_WARN_OVERFLOW
		0x3FFC0902  WARNING: Value underrun - VI_INSTR_WARN_UNDERRUN
		0x3FFC0903  WARNING: Value is NaN   - VI_INSTR_WARN_NAN
		0xBFFC0001  Parameter 1 out of range. 
		0xBFFC0002  Parameter 2 out of range.
		0xBFFC0003  Parameter 3 out of range.
		0xBFFC0004  Parameter 4 out of range.
		0xBFFC0005  Parameter 5 out of range.
		0xBFFC0006  Parameter 6 out of range.
		0xBFFC0007  Parameter 7 out of range.
		0xBFFC0008  Parameter 8 out of range.
		0xBFFC0012  Error Interpreting instrument response.
		
		--- Instrument Errors --- 
		Range: 0xBFFC0700 .. 0xBFFC0CFF.
		Calculation: Device error code + 0xBFFC0900.
		Please see your device documentation for details.
		
		--- VISA Errors ---
		Please see your VISA documentation for details.
		
		
		Args:
			statusCode(c_int) : This parameter accepts the error codes returned from the instrument driver functions.
			
			Default Value: 0 - VI_SUCCESS
			description(create_string_buffer(1024)) : This parameter returns the interpreted code as an user readable message string.
			
			Notes:
			(1) The message buffer has to be initalized with 256 bytes.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_errorMessage(self.devSession, statusCode, description)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def errorQuery(self, errorNumber, errorMessage):
		"""
		This function queries the instrument's error queue manually. 
		Use this function to query the instrument's error queue if the driver's error query mode is set to manual query. 
		
		Notes:
		(1) The returned values are stored in the drivers error store. You may use <Error Message> to get a descriptive text at a later point of time.
		
		Args:
			errorNumber(c_int use with byref) : This parameter returns the instrument error number.
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			
			errorMessage(create_string_buffer(1024)) : This parameter returns the instrument error message.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256] including the null byte.
			(2) You may pass VI_NULL if you do not need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_errorQuery(self.devSession, errorNumber, errorMessage)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def errorQueryMode(self, mode):
		"""
		This function selects the driver's error query mode.
		
		Args:
			mode(c_int16) : This parameter specifies the driver's error query mode. 
			
			If set to Automatic each driver function queries the instrument's error queue and in case an error occured returns the error number.
			
			If set to Manual the driver does not query the instrument for errors and therefore a driver function does not return instrument errors. You should use <Error Query> to manually query the instrument's error queue.
			
			VI_OFF (0): Manual error query.
			VI_ON  (1): Automatic error query (default).
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_errorQueryMode(self.devSession, mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def errorCount(self, count):
		"""
		This function returns the number of errors in the queue.
		
		Args:
			count(c_uint32 use with byref) : This parameter returns the instrument error number.
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_errorCount(self.devSession, count)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def reset(self):
		"""
		Places the instrument in a default state.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_reset(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def selfTest(self, selfTestResult, description):
		"""
		This function runs the device self test routine and returns the test result.
		
		Args:
			selfTestResult(c_int16 use with byref) : This parameter contains the value returned from the device self test routine. A retured zero value indicates a successful run, a value other than zero indicates failure.
			description(create_string_buffer(1024)) : This parameter returns the interpreted code as an user readable message string.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_selfTest(self.devSession, selfTestResult, description)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def revisionQuery(self, instrumentDriverRevision, firmwareRevision):
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
			(2) You may pass VI_NULL if you do not need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_revisionQuery(self.devSession, instrumentDriverRevision, firmwareRevision)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def identificationQuery(self, manufacturerName, deviceName, serialNumber, firmwareRevision):
		"""
		This function returns the device identification information.
		
		Args:
			manufacturerName(create_string_buffer(1024)) : This parameter returns the manufacturer name.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			deviceName(create_string_buffer(1024)) : This parameter returns the device name.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			serialNumber(create_string_buffer(1024)) : This parameter returns the device serial number.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			firmwareRevision(create_string_buffer(1024)) : This parameter returns the device firmware revision.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_identificationQuery(self.devSession, manufacturerName, deviceName, serialNumber, firmwareRevision)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getCalibrationMsg(self, message, channel):
		"""
		This function returns a human readable calibration message.
		
		
		Args:
			message(create_string_buffer(1024)) : This parameter returns the calibration message.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			channel(c_uint16) : Number if the channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getCalibrationMsg(self.devSession, message, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDisplayName(self, name):
		"""
		This method send the SCPI command SYST:COMM:NET:HOST %S
		This name is used by the PM400 as custom display name
		and by the PM103E as network hostname.
		
		Args:
			name(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDisplayName(self.devSession, name)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDisplayName(self, name):
		"""
		This method send the SCPI command SYST:COMM:NET:HOST?
		This name is used by the PM400 as custom display name
		and by the PM103E as network hostname.
		
		Args:
			name(create_string_buffer(1024))
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDisplayName(self.devSession, name)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getChannels(self, channelCount):
		"""
		This function returns the number of supported sensor channels.
		
		Args:
			channelCount(c_uint16 use with byref) : Number of supported sensor channels.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getChannels(self.devSession, channelCount)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getSensorInfo(self, name, snr, message, pType, pStype, pFlags, channel):
		"""
		This function is used to obtain informations from the connected sensor like sensor name, serial number, calibration message, sensor type, sensor subtype and sensor flags.  
		
		Remark:
		The meanings of the obtained sensor type, subtype and flags are:
		
		Sensor Types:
		 SENSOR_TYPE_NONE               0x00 // No sensor
		 SENSOR_TYPE_PD_SINGLE          0x01 // Photodiode sensor
		 SENSOR_TYPE_THERMO             0x02 // Thermopile sensor
		 SENSOR_TYPE_PYRO               0x03 // Pyroelectric sensor
		
		Sensor Subtypes:
		 SENSOR_SUBTYPE_NONE            0x00 // No sensor
		 
		Sensor Subtypes Photodiode:
		 SENSOR_SUBTYPE_PD_ADAPTER      0x01 // Photodiode adapter
		 SENSOR_SUBTYPE_PD_SINGLE_STD   0x02 // Photodiode sensor
		 SENSOR_SUBTYPE_PD_SINGLE_FSR   0x03 // Photodiode sensor with 
		                                        integrated filter
		                                        identified by position 
		 SENSOR_SUBTYPE_PD_SINGLE_STD_T 0x12 // Photodiode sensor with
		                                        temperature sensor
		Sensor Subtypes Thermopile:
		 SENSOR_SUBTYPE_THERMO_ADAPTER  0x01 // Thermopile adapter
		 SENSOR_SUBTYPE_THERMO_STD      0x02 // Thermopile sensor
		 SENSOR_SUBTYPE_THERMO_STD_T    0x12 // Thermopile sensor with 
		                                        temperature sensor
		Sensor Subtypes Pyroelectric Sensor:
		 SENSOR_SUBTYPE_PYRO_ADAPTER    0x01 // Pyroelectric adapter
		 SENSOR_SUBTYPE_PYRO_STD        0x02 // Pyroelectric sensor
		 SENSOR_SUBTYPE_PYRO_STD_T      0x12 // Pyroelectric sensor with
		                                        temperature sensor
		Sensor Flags:
		 TLPM_SENS_FLAG_IS_POWER     0x0001 // Power sensor
		 TLPM_SENS_FLAG_IS_ENERGY    0x0002 // Energy sensor
		 TLPM_SENS_FLAG_IS_RESP_SET  0x0010 // Responsivity settable
		 TLPM_SENS_FLAG_IS_WAVEL_SET 0x0020 // Wavelength settable
		 TLPM_SENS_FLAG_IS_TAU_SET   0x0040 // Time constant settable
		 TLPM_SENS_FLAG_HAS_TEMP     0x0100 // With Temperature sensor 
		
		Args:
			name(create_string_buffer(1024)) : This parameter returns the name of the connected sensor.
			
			snr(create_string_buffer(1024)) : This parameter returns the serial number of the connected sensor.
			message(create_string_buffer(1024)) : This parameter returns the calibration message of the connected sensor.
			
			pType(c_int16 use with byref) : This parameter returns the sensor type of the connected sensor.
			
			Remark:
			The meanings of the obtained sensor type are:
			
			Sensor Types:
			 SENSOR_TYPE_NONE               0x00 // No sensor
			 SENSOR_TYPE_PD_SINGLE          0x01 // Photodiode sensor
			 SENSOR_TYPE_THERMO             0x02 // Thermopile sensor
			 SENSOR_TYPE_PYRO               0x03 // Pyroelectric sensor
			pStype(c_int16 use with byref) : This parameter returns the subtype of the connected sensor.
			
			Remark:
			The meanings of the obtained sensor subtype are:
			
			Sensor Subtypes:
			 SENSOR_SUBTYPE_NONE            0x00 // No sensor
			 
			Sensor Subtypes Photodiode:
			 SENSOR_SUBTYPE_PD_ADAPTER      0x01 // Photodiode adapter
			 SENSOR_SUBTYPE_PD_SINGLE_STD   0x02 // Photodiode sensor
			 SENSOR_SUBTYPE_PD_SINGLE_FSR   0x03 // Photodiode sensor with 
			                                        integrated filter
			                                        identified by position 
			 SENSOR_SUBTYPE_PD_SINGLE_STD_T 0x12 // Photodiode sensor with
			                                        temperature sensor
			Sensor Subtypes Thermopile:
			 SENSOR_SUBTYPE_THERMO_ADAPTER  0x01 // Thermopile adapter
			 SENSOR_SUBTYPE_THERMO_STD      0x02 // Thermopile sensor
			 SENSOR_SUBTYPE_THERMO_STD_T    0x12 // Thermopile sensor with 
			                                        temperature sensor
			Sensor Subtypes Pyroelectric Sensor:
			 SENSOR_SUBTYPE_PYRO_ADAPTER    0x01 // Pyroelectric adapter
			 SENSOR_SUBTYPE_PYRO_STD        0x02 // Pyroelectric sensor
			 SENSOR_SUBTYPE_PYRO_STD_T      0x12 // Pyroelectric sensor with
			                                        temperature sensor
			pFlags(c_int16 use with byref) : This parameter returns the flags of the connected sensor.
			
			Remark:
			The meanings of the obtained sensor flags are:
			
			Sensor Flags:
			 TLPM_SENS_FLAG_IS_POWER     0x0001 // Power sensor
			 TLPM_SENS_FLAG_IS_ENERGY    0x0002 // Energy sensor
			 TLPM_SENS_FLAG_IS_RESP_SET  0x0010 // Responsivity settable
			 TLPM_SENS_FLAG_IS_WAVEL_SET 0x0020 // Wavelength settable
			 TLPM_SENS_FLAG_IS_TAU_SET   0x0040 // Time constant settable
			 TLPM_SENS_FLAG_HAS_TEMP     0x0100 // With Temperature sensor
			channel(c_uint16) : Number if the channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getSensorInfo(self.devSession, name, snr, message, pType, pStype, pFlags, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def writeRaw(self, command):
		"""
		This function writes directly to the instrument.
		
		Args:
			command(c_char_p) : Null terminated command string to send to the instrument.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_writeRaw(self.devSession, command)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def readRaw(self, buffer, size, returnCount):
		"""
		This function reads directly from the instrument.
		
		
		Args:
			buffer(create_string_buffer(1024)) : Byte buffer that receives the data read from the instrument.
			
			Notes:
			(1) If received data is less than buffer size, the buffer is additionaly terminated with a '' character.
			(2) If received data is same as buffer size no '' character is appended. Its the caller's responsibility to make sure a buffer is '' terminated if the caller wants to interprete the buffer as string.
			size(c_uint32) : This parameter specifies the buffer size.
			
			returnCount(c_uint32 use with byref) : Number of bytes actually transferred and filled into Buffer. This number doesn't count the additional termination '' character. If Return Count == size the buffer content will not be '' terminated.
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_readRaw(self.devSession, buffer, size, returnCount)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setTimeoutValue(self, value):
		"""
		This function sets the interface communication timeout value.
		
		Args:
			value(c_uint32) : This parameter specifies the communication timeout value in ms.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setTimeoutValue(self.devSession, value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getTimeoutValue(self, value):
		"""
		This function gets the interface communication timeout value.
		
		
		Args:
			value(c_uint32 use with byref) : This parameter returns the communication timeout value in ms.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getTimeoutValue(self.devSession, value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setIPAddress(self, IPAddress):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			IPAddress(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setIPAddress(self.devSession, IPAddress)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getIPAddress(self, IPAddress):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			IPAddress(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getIPAddress(self.devSession, IPAddress)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setIPMask(self, IPMask):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			IPMask(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setIPMask(self.devSession, IPMask)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getIPMask(self, IPMask):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			IPMask(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getIPMask(self.devSession, IPMask)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getMACAddress(self, MACAddress):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			MACAddress(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getMACAddress(self.devSession, MACAddress)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDHCP(self, DHCP):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			DHCP(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDHCP(self.devSession, DHCP)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDHCP(self, DHCP):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			DHCP(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDHCP(self.devSession, DHCP)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setHostname(self, hostname):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			hostname(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setHostname(self.devSession, hostname)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getHostname(self, hostname):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			hostname(create_string_buffer(1024)) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getHostname(self.devSession, hostname)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setWebPort(self, port):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			port(c_uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setWebPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getWebPort(self, port):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			port(c_uint32 use with byref) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getWebPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setSCPIPort(self, port):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			port(c_uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setSCPIPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getSCPIPort(self, port):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			port(c_uint32 use with byref) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getSCPIPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDFUPort(self, port):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			port(c_uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDFUPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDFUPort(self, port):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			port(c_uint32 use with byref) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDFUPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDeviceBaudrate(self, baudrate):
		"""
		Tell the instrument which baudrate has to be used for the serial communication.
		This value is stored inside the instrument. 
		
		If the RS232 interface is currently used for the communication, call the function setDriverBaudrate to adapt to the new baudrate.
		
		Args:
			baudrate(c_uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDeviceBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDeviceBaudrate(self, baudrate):
		"""
		This function returns the baudrate that is used for the serial communication inside the instrument
		
		
		Args:
			baudrate(c_uint32 use with byref) : This parameter returns the baudrate in bist/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDeviceBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDriverBaudrate(self, baudrate):
		"""
		This function sets the baudrate for the serial interface on the PC side
		
		Args:
			baudrate(c_uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDriverBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDriverBaudrate(self, baudrate):
		"""
		This function returns the baudrate that is used for the serial communication on the PC side
		
		
		Args:
			baudrate(c_uint32 use with byref) : This parameter returns the baudrate in bist/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDriverBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

