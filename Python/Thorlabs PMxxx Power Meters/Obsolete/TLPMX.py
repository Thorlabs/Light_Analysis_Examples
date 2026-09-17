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
TLPM_PID_PM6x_DFU = (0x80B4)  # PM6x on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM100Dx_DFU = (0x8099)  # PM100D2\D3 Generation on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODE _CODE==0x8070 || VI_ATTR_MODE _CODE==0x8078)}"
PM100A_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODE _CODE==0x8071 || VI_ATTR_MODE _CODE==0x8079)}"
PM100USB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODE _CODE==0x8072}"
PM160USB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODE _CODE==0x8073 || VI_ATTR_MODE _CODE==0x807B)}"
PM160TUSB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODE _CODE==0x8074 || VI_ATTR_MODE _CODE==0x807C)}"
PM200_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODE _CODE==0x80B0}"
PM400_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODE _CODE==0x8075 || VI_ATTR_MODE _CODE==0x807D)}"
PM101_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODE _CODE==0x8076)}"
PM102_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODE _CODE==0x8077)}"
PM103_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODE _CODE==0x807A}"
PMTest_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODE _CODE==0x807F}"
PM100_FIND_PATTERN = "USB?*::0x1313::0x807?::?*::INSTR"
PM5020_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODE _CODE==0x80BB}"
PM100D3rdGen_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODE _CODE==0x8099}"
PMxxx_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODE _CODE==0x8070 || VI_ATTR_MODE _CODE==0x8078 || " \
"VI_ATTR_MODEL_CODE==0x8071 || VI_ATTR_MODEL_CODE==0x8079 || " \
"VI_ATTR_MODEL_CODE==0x8072 || " \
"VI_ATTR_MODEL_CODE==0x8073 || VI_ATTR_MODEL_CODE==0x807B || " \
"VI_ATTR_MODEL_CODE==0x8074 || VI_ATTR_MODEL_CODE==0x807C || " \
"VI_ATTR_MODEL_CODE==0x8075 || VI_ATTR_MODEL_CODE==0x807D || " \
"VI_ATTR_MODEL_CODE==0x8076 || VI_ATTR_MODEL_CODE==0x807E || " \
"VI_ATTR_MODEL_CODE==0x8077 || VI_ATTR_MODEL_CODE==0x807F || " \
"VI_ATTR_MODEL_CODE==0x8099 ||" \
"VI_ATTR_MODEL_CODE==0x807A || VI_ATTR_MODEL_CODE==0x80BB ||" \
"VI_ATTR_MODEL_CODE==0x80B0 || VI_ATTR_MODEL_CODE==0x80B4)}"
PMBT_FIND_PATTERN = "ASR ?*::INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODE _CODE==0x807C || VI_ATTR_MODE _CODE==0x807B)}"
PMUART_FIND_PATTERN_VISA = "ASRL?*::INSTR"
PMUART_FIND_PATTERN_COM = "COM?*"
PMNET_FIND_PATTERN = "TCPIP?*::INSTR{(VI_ATTR_TCPIP_DEVICE_NAME==\"PM5020\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM103E\" || " \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM60\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM61\" || " \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM62\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM63\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM64\" ||" \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM400\" || " \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM100D3\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM100D2\" || " \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM103\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM103A\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM103R\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM103U\" || " \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM102\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM102A\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM102R\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM102U\" || " \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM101\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM101A\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM101R\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM101U\" || " \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM100USB\" || " \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM100D\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM100A\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM200\" || " \
"VI_ATTR_TCPIP_DEVICE_NAME==\"PM160\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM160T\")}"
PMBTH_FIND_PATTERN = "BTHLE?*"
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
TLPM_TRIGGER_SRC_CHANNEL_1 = (1)
TLPM_TRIGGER_SRC_CHANNEL_2 = (2)
TLPM_TRIGGER_SRC_FRONT_AUX = (3)
TLPM_TRIGGER_SRC_REAR = (4)
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
TLPM_STATBIT_OPER_TRIG = (0x0020)  # < The instrument is in a ?wait for trigger? state of the trigger model.
TLPM_STATBIT_OPER_ARM = (0x0040)  # < The instrument is in a ?wait for arm? state of the trigger model.
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
TLPM_AUTORANGE_ENERGY_OFF = (0)
TLPM_AUTORANGE_ENERGY_ON = (1)
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
TLPM_ANALOG_ROUTE_FUNC = (4)
TLPM_ANALOG_ROUTE_CUST = (5)
TLPM_ANALOG_ROUTE_GDBM = (6)
TLPM_MEAS_POWER = (0)
TLPM_MEAS_CURRENT = (1)
TLPM_MEAS_VOLTAGE = (2)
TLPM_MEAS_PDENSITY = (3)
TLPM_MEAS_ENERGY = (4)
TLPM_MEAS_EDENSITY = (5)
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
TLPM_SENS_FLAG_IS_UNDEFINED = 0x0000  # Undefined sensor
TLPM_SENS_FLAG_IS_POWER = 0x0001  # Power sensor
TLPM_SENS_FLAG_IS_ENERGY = 0x0002  # Energy sensor
TLPM_SENS_FLAG_IS_RESP_SET = 0x0010  # Responsivity settable
TLPM_SENS_FLAG_IS_WAVEL_SET = 0x0020  # Wavelength settable
TLPM_SENS_FLAG_IS_TAU_SET = 0x0040  # Time constant tau settable
TLPM_SENS_FLAG_HAS_TEMP = 0x0100  # Temperature sensor included
TLPM_SENS_XFLAG_AUTORANGE = 0x0001  # can auto range
TLPM_SENS_XFLAG_IS_ADAPTER = 0x0002  # is adapter
TLPM_SENS_XFLAG_IS_WAVEL_SET = 0x0004  # Energy sensor
TLPM_SENS_XFLAG_IS_RESP_SET = 0x0008  # Wavelength settable
TLPM_SENS_XFLAG_IS_ACC_SET = 0x0010  # can set acceleration
TLPM_SENS_XFLAG_IS_BW_SET = 0x0020  # can set bandwidth
TLPM_SENS_XFLAG_DECT_PEAK = 0x0040  # can detect peak
TLPM_SENS_XFLAG_MEAS_FREQ = 0x0080  # can meas frequency
TLPM_SENS_XFLAG_IS_ZERO_SET = 0x0100  # can start zeroing
TLPM_SENS_XFLAG_IS_TAU_SET = 0x0200  # can set tau
TLPM_SENS_XFLAG_MEAS_POS = 0x0400  # can meas position x,y
TLPM_SENS_XFLAG_PHOTOMETRIC = 0x0800  # can meas photometric
TLPM_SENS_XFLAG_HAS_TEMP = 0x1000  # Temperature sensor included

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
#			dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
			dllabspath = "C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\Bin\\" + dll_name
			self.dll = cdll.LoadLibrary(dllabspath)
		else:
			dll_name = "TLPMX_64.dll"
#			dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
			dllabspath = "C:\\Program Files\\IVI Foundation\\VISA\\Win64\\Bin\\" + dll_name
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

	def initWithEncryption(self, IDQuery, reset, password, pInstr):
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
			IDQuery(c_int16) : This parameter specifies whether an identification query is performed during the initialization process.
			
			VI_TRUE  (1): Do query (default).
			VI_FALSE (0): Skip query.
			
			
			reset(c_int16) : This parameter specifies whether the instrument is reset during the initialization process.
			
			VI_TRUE  (1) - instrument is reset (default)
			VI_FALSE (0) - no reset 
			
			
			password(c_char_p) : Password for encryption over ethernet communication.
			pInstr(ViPSession use with byref) : This parameter returns an instrument handle that is used in all subsequent calls to distinguish between different sessions of this instrument driver.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_initWithEncryption(self.devSession, IDQuery, reset, password, pInstr)
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
		(1) The function additionally stores information like system name about the found resources internally. This information can be retrieved with further functions from the class, e.g. <Get Resource Description> and :func:`getRsrcInfo`.
		
		(2) To list Ethernet and Bluetooth devices, enable the search for these devices with functions setEnableNetSearch and setEnableBthSearch.
		
		
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
		This function gets the resource name string needed to open a device with :func:`init`.
		
		Notes:
		(1) The data provided by this function was updated at the last call of :func:`findRsrc`.
		
		Args:
			index(c_uint32) : This parameter accepts the index of the device to get the resource descriptor from.
			
			Notes: 
			(1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.
			
			resourceName(create_string_buffer(1024) use with byref) : This parameter returns the resource descriptor. Use this descriptor to specify the device in <Initialize>.
			
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
		(1) The data provided by this function was updated at the last call of :func:`findRsrc`.
		
		Args:
			index(c_uint32) : This parameter accepts the index of the device to get the resource descriptor from.
			
			Notes: 
			(1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.
			
			modelName(create_string_buffer(1024) use with byref) : This parameter returns the model name of the device.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) Serial interfaces over Bluetooth will return the interface name instead of the device model name.
			serialNumber(create_string_buffer(1024) use with byref) : This parameter returns the serial number of the device.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) The serial number is not available for serial interfaces over Bluetooth.
			manufacturer(create_string_buffer(1024) use with byref) : This parameter returns the manufacturer name of the device.
			
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
		
		Remarks:
		(1) Be aware the condition and the event registers are read only!
		
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
		
		Remarks:
		(1) Reading the event register will clear the event bitmask
		
		
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
		This function sends a (Network Time Protocol) NTP - Request to given IP address to update date and time of the powermeter automatically using an external time server. 
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM5020
		(3) Requires an active Ethernet connection with the route to the requested server.
		
		Args:
			timeMode(c_int16) : 0 for wintertime. 1 for summertime
			timeZone(c_int16) : Local time zone offset for GMT. Berlin is +1
			IPAddress(c_char_p) :  IP address of used NTP server. By default PTB server is used.
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
		(2) The function is available on PM5020, PM6x, PM100Dx
		
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
		(2) The function is available on PM5020, PM6x and PM100Dx
		
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
		This function is used to obtain the battery voltage readings from the instrument. It optains the latest battery voltage measurement result.
		
		Remarks:
		(1) Supported for PM160, PM160T, PM6x, PM100Dx
		(2) if USB cable connected: this function will obtain the loading voltage. Only with USB cable disconnected (Bluetooth connection) the actual battery voltage can be read. 
		
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
		
		Note: Supported by PM5020, PM400, PM60, PM100Dx
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_beep(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setInputFilterState(self, inputFilterState, channel):
		"""
		This functionto enables or disables the bandwidth limitation of the photodiode sensor signal amplifier. This command is useful for CW signals to suppress noise. For modulated signals ensure bandwidth is set to high. 
		
		Remarks:
		(1) When active bandwidth is limited to approximately 3 Hz.
		(2) Photodiode only!
		
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
		This function tests if the bandwidth limitation of the photodiode sensor signal amplifier is enabled or disabled. This command is useful for CW signals to suppress noise. For modulated signals ensure bandwidth is set to high. 
		
		Remarks:
		(1) When active bandwidth is limited to approximately 3 Hz.
		(2) Photodiode only!
		
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
		Enables or disables the thermopile sensor value prediction algorithm. Thermopile sensors can respond slowly to rapid changes in light intensity. The prediction algorithm automatically calculates the resulting power, following a logarithmic function during positive jumps and a 1/e function during negative jumps. The sensor behaves like a capacitor, and in both scenarios, the signal reaches 99% of its final level after a time period of 5 Tau, at which point the prediction is automatically halted. Tau is a sensor-specific constant stored in the head's EEPROM.
		
		Notes:
		(1) The function is only available on powermeters withThermopile sensor support.
		(2) For adapter sensors (Without EEPROM), Tau can be modified using the setAccelTau function
		
		
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
		(1) The function is only available on powermeters withThermopile sensor support.
		
		
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
		(1) Applies only for Thermopile adapter sensors without EEPROM
		
		
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
		(1) Note: The function is only available on powermeters with Thermopile sensor support.
		(2) Tau is stored in the sensor head EEPROM
		
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
		Changes the default adapter sensor type. Adapters are sensors that do not have a head EEPROM. If no sensor is currently connected, this function will update the default adapter sensor type. If an adapter is connected, the function will re-enumerate the new adapter type on the Powermeter. The adapter type is stored persistently and will be automatically reused after a reboot.
		
		Remarks:
		(1) For every Powermeter only the specified sensor types are supported. 
		
		Args:
			type(c_int16) : This parameter specifies the custom sensor type.
			
			Acceptable values:
			 SENSOR_TYPE_PD_SINGLE (1): Photodiode sensor
			 SENSOR_TYPE_THERMO    (2): Thermopile sensor
			 SENSOR_TYPE_PYRO      (3): Pyroelectric sensor
			 SENSOR_TYPE_4Q        (4): 4 Quadrant sensor
			
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

	def getThermopilePulseIntegrator(self, enable, channel):
		"""
		Tests if thermopile pulse energy measurement is enabled or disabled. This mode is suitable for measuring the energy in joules from single thermopile pulses with a slow repetition rate. The algorithm integrates the power measurement over a duration of 8 * Tau, where Tau is a sensor-specific time constant stored in the head's EEPROM.
		
		Args:
			enable(c_int16 use with byref) : True when thermopile pulse integrator is enabled. False when disabled.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getThermopilePulseIntegrator(self.devSession, enable, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setThermopilePulseIntegrator(self, enable, channel):
		"""
		Enables or disables thermopile pulse energy measurement. This mode is suitable for measuring the energy in joules from single thermopile pulses with a slow repetition rate. The algorithm integrates the power measurement over a duration of 8 * Tau, where Tau is a sensor-specific time constant stored in the head's EEPROM.
		
		Notes:
		(1) Note: The function is only available on powermeters with Thermopile sensor support.
		(2) For adapter sensors Tau must be specified by setAcclTau function previously
		
		Args:
			enable(c_int16) : True to enable the pulse energy measurement. False to disable it.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setThermopilePulseIntegrator(self.devSession, enable, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAvgTime(self, avgTime, channel):
		"""
		This function sets the average time for measurement value generation. The value will be rounded to the closest multiple of the device's internal sampling rate. Averaging applies for the device slow measurement system of light sensor related CW measurements. 
		
		Remarks:
		(1) To get an measurement value from the device the timeout in your application has to be longer than the average time.
		(2) All non light related measurements like temperature and frequenency measurements are not affected by this prescaler
		(3) Affected only continuous wave (CW) measurements of light signals.
		
		Args:
			avgTime(c_double) : This parameter specifies the average time in seconds.
			
			
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
		This function returns the average time for measurement value generation. The value has beenrounded to the closest multiple of the device's internal sampling rate. Averaging applies for the device slow measurement system of light sensor related CW measurements. 
		
		Remarks:
		(1) To get an measurement value from the device the timeout in your application has to be longer than the average time.
		(2) All non light related measurements like temperature and frequenency measurements are not affected by this prescaler
		(3) Affected only continuous wave (CW) measurements of light signals.
		
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
		Configures the averaging prescaler for slow light signal measurements. The prescaler value, which must be a whole number, reduces the measurement rate derived from the powermeter specific measurement frequency. 
		
		For example, the powermeter measurement frequency is 1 kHz and the prescaler is set to 2, the Powermeter will average two slow measurements, resulting in an update rate of 500 Hz.
		
		Notes:
		(1) The function is DEBRECATED and kept for legacy reasons. Its recommended to use setAvgTime() instead.
		(2) To get an measurement value from the device the timeout in your application has to be longer than the average time.
		(3) All non light related measurements like temperature and frequenency measurements are not affected by this prescaler
		(4) Affected only continuous wave (CW) measurements of light signals.
		
		Args:
			averageCount(c_int16) : This parameter specifies the average count. The default value is 1.
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
		Returns the average count prescaler for the slow measurement system. The prescaler value, which is a whole number, reduces the measurement rate derived from the powermeter specific measurement frequency. 
		
		For example, the powermeter measurement frequency is 1 kHz and the prescaler is set to 2, the Powermeter will average two slow measurements, resulting in an update rate of 500 Hz.
		
		Notes:
		(1) The function is DEBRECATED and kept for legacy reasons. Its recommended to use getAvgTime() instead.
		(2) To get an measurement value from the device the timeout in your application has to be longer than the average time.
		(3) All non light related measurements like temperature and frequenency measurements are not affected by this prescaler
		(4) Affected only continuous wave (CW) measurements of light signals.
		
		Args:
			averageCount(c_int16 use with byref) : This parameter returns the actual Average Count.
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
		Sets the attenuation of light in dBm. If your setup includes a filter in front of the sensor, this attenuation ensures that the Powermeter displays corrected values. The attenuation parameter is stored persistently and will be restored after a reboot. If the connected sensor is changed, the parameter will be reset to 0.
		
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
		Querys the attenuation of light in dB. If your setup includes a filter in front of the sensor, this attenuation ensures that the Powermeter displays corrected values. The attenuation parameter is stored persistently and will be restored after a reboot. If the connected sensor is changed, the parameter will be reset to 0.
		
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
		Initiates a dark current or voltage correction for the sensor. Before starting the correction, ensure that the light source is not illuminating the sensor area and that the sensor is completely covered. This command only begins the zeroing procedure, which runs in the background. During the zeroing process, measurements cannot be taken. 
		
		Remarks:
		(1) You have to darken the input before starting dark/zero adjustment.
		(2) For relative measurements in relation to ambient light, utilize delta mode functions as the maximum zero correction is limited and exceeding this limit will result in an error.
		(3) Uero parameter is not stored persistently and will be lost after a reboot
		(4) You can get the state of dark/zero adjustment with :func:`getDarkAdjustState`.
		(5) You can stop dark/zero adjustment with :func:`cancelDarkAdjust`.
		(6) You get the dark/zero value with :func:`getDarkOffset`.
		(7) Energy sensors do not support this function.
		(8) Photodiode sensors in peak mode do not support this function.
		
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
		command to abort a previously initiated zeroing process. The zeroing of the sensor operates as an asynchronous background task. Aborting the sequence will terminate the background operation and allow measurements to continue using the previous zero value. 
		
		Remarks:
		(1) You can get the state of dark/zero adjustment with :func:`getDarkAdjustState`.
		(2) You can start dark/zero adjustment with :func:`startDarkAdjust`.
		(3) Energy sensors do not support this function.
		(4) Photodiode sensors in peak mode do not support this function.
		
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
		Checks if the previously initiated zeroing procedure is currently running in the background. The zeroing process for the sensor operates asynchronously. It will automatically terminate upon encountering an error or upon successful completion. Once the procedure has ended, this function will return 0. If no zeroing process has been initiated, the command will also return 0. 
		
		Remarks:
		(1) You can get the state of dark/zero adjustment with :func:`getDarkAdjustState`.
		(2) You can start dark/zero adjustment with :func:`startDarkAdjust`.
		(3) You can stop dark/zero adjustment with :func:`cancelDarkAdjust`.
		(4) You get the dark/zero value with :func:`getDarkOffset`.
		(5) Energy sensors do not support this function.
		(6) Photodiode sensors in peak mode do not support this function.
		
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
		Establishes the zero correction value in Amperes for the Photodiode sensor, or in Volts for the Thermopile and 4-Quadrant Thermopile sensors. Directly setting the zero value will not initiate the asynchronous zeroing procedure.
		
		Remarks:
		(1) Typically, you should allow the Powermeter to determine the zero value itself by using the :func:`startDarkAdjust`.
		(2) Set to 0 to disable zero correction of sensor.
		(3) For relative measurements in relation to ambient light, utilize delta mode functions as the maximum zero correction is limited and exceeding this limit will result in an error.
		(4) Zero parameter is not stored persistently and will be lost after a reboot
		(5) Energy sensors do not support this function.
		(6) Photodiode sensors in peak mode do not support this function.
		
		
		Args:
			darkOffset(c_double) : This parameter returns the dark/zero offset. The unit of the returned offset value depends on the sensor type. Photodiodes return the dark offset in ampere [A]. Thermal sensors return the dark offset in volt [V].
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
		Retrieve the zero correction value in Amperes for the Photodiode sensor, or in Volts for the Thermopile and 4-Quadrant Thermopile sensors. 
		
		Remarks:
		(1) Typically, you should allow the Powermeter to determine the zero value itself by using :func:`startDarkAdjust` 
		(2) To specify a fixed zero offset use :func:`setDarkOffset`
		(3) Zero parameter is not stored persistently and will be lost after a reboot
		(4) Energy sensors do not support this function.
		(5) Photodiode sensors in peak mode do not support this function.
		
		Args:
			darkOffset(c_double use with byref) : This parameter returns the dark/zero offset. The unit of the returned offset value depends on the sensor type. Photodiodes return the dark offset in ampere [A]. Thermal sensors return the dark offset in volt [V].
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDarkOffset(self.devSession, darkOffset, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def startZeroPos(self, channel):
		"""
		Starts a background task to measure the actual beam position and use it as position correction in the future. Before starting the correction ensure light source is hitting the sensor area. Position is floating if no beam is hitting the sensor. This command only starts the zeroing procedure running in background for at least one second. During zero procedure, measuring is not possible. 
		
		Remarks:
		(1) Only available for 4 quadrant thermopile sensors.
		(2) You have to ensure light source is hitting the sensor for this procedure.
		(3) Beam zero parameter is not stored persistently and will be lost after a reboot.
		(4) You can stop beam zeroing with :func:`cancelZeroPos`.
		(5) You get the beam zero coordinate with :func:`getZeroPos`.
		(6) For PM400 firmware needs to be >= 1.5.0 
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_startZeroPos(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def cancelZeroPos(self, channel):
		"""
		Aborts a previously started position zero correction. The zeroing of position is running as asynchronous background operation. Aborting the sequence will end the background operation and enables measuring with the old zero value.
		
		Remarks:
		(1) Only available for 4 quadrant thermopile sensors.
		(4) You can restart beam zeroing with :func:`startZeroPos`.
		(6) For PM400 firmware needs to be >= 1.5.0 
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_cancelZeroPos(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setZeroPos(self, zeroX, zeroY, channel):
		"""
		Use this command to set beam position zero correction coordinate in µm. Zero parameter is not stored persistently. It will be lost after reboot!
		
		Remarks:
		(1) Only available for 4 quadrant thermopile sensors.
		(2) In most cases, you will want the Powermeter to automatically measure the delta reference using :func:`startZeroPos`.
		(3) You get the beam zero coordinate with :func:`getZeroPos`.
		(4) Beam zero parameter is not stored persistently and will be lost after a reboot.
		(5) For PM400 firmware needs to be >= 1.5.0 
		
		Args:
			zeroX(c_double) : This parameter set the zero x in µm.
			zeroY(c_double) : This parameter set the zero y in µm.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setZeroPos(self.devSession, zeroX, zeroY, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getZeroPos(self, pZeroX, pZeroY, channel):
		"""
		Use this command to get beam position zero correction coordinate in µm.
		
		Remarks:
		(1) Only available for 4 quadrant thermopile sensors.
		(2)  In most cases, you will want the Powermeter to automatically measure the delta reference using :func:`startZeroPos`.
		(3) To specify a fixed zero offset use :func:`setZeroPos`.
		(4) Beam zero parameter is not stored persistently and will be lost after a reboot.
		(5) For PM400 firmware needs to be >= 1.5.0
		
		
		Args:
			pZeroX(c_double use with byref) : This parameter returns the zero x value in µm.
			pZeroY(c_double use with byref) : This parameter returns the zero y value in µm.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getZeroPos(self.devSession, pZeroX, pZeroY, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setBeamDia(self, beamDiameter, channel):
		"""
		Sets the circular beam diameter in millimeter hitting the sensor[mm]. If you are working with different beam shapes, you will need to manually calculate the corresponding diameter for a circle with the same area. 
		
		Notes:
		(1) Beam diameter set value is used for calculating power and energy density.
		(2) Beam diameter is stored persistently and will be restored after a reboot. 
		(3) If the connected sensor type is changed, default values will be applied. If the sensor type remains the same, the parameter will be automatically coerced.
		
		Args:
			beamDiameter(c_double) : This parameter specifies circular beam diameter in millimeter [mm].
			
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
		Returns the circular beam diameter in millimeter [mm]. If you are working with different beam shapes, you will need to manually calculate the corresponding diameter for a circle with the same area. 
		
		Notes:
		(1) Beam diameter set value is used for calculating power and energy density.
		(2) Beam diameter is stored persistently and will be restored after a reboot. 
		(3) If the connected sensor type is changed, default values will be applied. If the sensor type remains the same, the parameter will be automatically coerced.
		
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
		Sets the wavelength of light in nanometers (nm). The configured wavelength is used to determine the sensor's responsivity for calculating light power. For adapter sensors, set the responsivity directly instead.
		
		Remarks:
		(1) Only supported for sensor heads with EEPROM. 
		(2) Adapter types have to set responsivity directly by e.g. :func:`setPhotodiodeResponsivity`
		(3) The wavelength parameter is stored persistently and will be restored after a reboot.
		(4) If the connected sensor type is changed, default values will be applied. If the sensor type remains the same, the parameter will be automatically coerced.
		
		Args:
			wavelength(c_double) : This parameter specifies the users wavelength in nanometer [nm].
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
		Returns the light wavelength in nanometer [nm]. The configured wavelength is used to determine the sensor's responsivity for calculating light power. For adapter sensors, get the responsivity directly instead.
		
		Remarks:
		(1) Only supported for sensor heads with EEPROM. 
		(2) Adapter types have to get responsivity directly by e.g. :func:`getPhotodiodeResponsivity`
		(3) The wavelength parameter is stored persistently and will be restored after a reboot.
		(4) If the connected sensor type is changed, default values will be applied. If the sensor type remains the same, the parameter will be automatically coerced.
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			wavelength(c_double use with byref) : This parameter returns the specified wavelength in nanometer [nm].
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
		Sets the photodiode responsivity in A/W for photodiode sensor adapters. This responsivity is used to calculate power based on the photodiode current, and the correct value depends on the wavelength of the light. Adapters are sensors that do not have head EEPROM. 
		
		Remarks:
		(1) Photodiode adapter sensors only
		(2) For sensor with EEPROM use :func:`setWavelength` to change responsivity
		(3) Set adapter type by calling :func:`setInputAdapterType`
		
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
		Queries the photodiode responsivity in A/W for photodiode sensor. This responsivity is used to calculate power based on the photodiode current, and the correct value depends on the wavelength of the light.
		
		Remarks:
		(1) Photodiode only!
		(2) For sensor with EEPROM use :func:`setWavelength` to change responsivity
		(3) For adapter sensor without EEPROM use :func:`setPhotodiodeResponsivity` to change responsivity
		
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
		Sets the thermopile responsivity in V/W for thermopile sensor adapters. This responsivity is used to calculate power based on the thermopile voltage, and the correct value depends on the wavelength of the light. Adapters are sensors that do not have head EEPROM. 
		
		Remarks:
		(1) Thermopile adapter sensors only
		(2) For sensor with EEPROM use :func:`setWavelength` to change responsivity
		(3) Set adapter type by calling :func:`setInputAdapterType`
		
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
		Queries the thermopile responsivity in V/W for thermopile sensor. This responsivity is used to calculate power based on the thermopile voltage, and the correct value depends on the wavelength of the light.
		
		Remarks:
		(1) Thermopile only!
		(2) For sensor with EEPROM use :func:`setWavelength` to change responsivity
		(3) For adapter sensor without EEPROM use :func:`setThermopileResponsivity` to change responsivity
		
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
		Sets the pyrosensor responsivity in V/J for pyroelectric sensor adapters. This responsivity is used to calculate energy based on the pyrosensor voltage, and the correct value depends on the wavelength of the light. Adapters are sensors that do not have head EEPROM. 
		
		Remarks:
		(1) Pyrosensor adapter only
		(2) For sensor with EEPROM use :func:`setWavelength` to change responsivity
		(3) Set adapter type by calling :func:`setInputAdapterType`
		
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
		
		Queries the pyrosensor responsivity in volt per joule [V/J] for pyroelectric sensor. This responsivity is used to calculate energy based on the pyrosensor voltage, and the correct value depends on the wavelength of the light.
		
		Remarks:
		(1) Pyrosensor only!
		(2) For sensor with EEPROM use :func:`setWavelength` to change responsivity
		(3) For adapter sensor without EEPROM use :func:`setPyrosensorResponsivity` to change responsivity
		
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
		Enables or disables the auto-ranging feature for current measurement. When auto-ranging is active, the Powermeter compares the measured signal to the currently used measurement range. If the signal falls outside the optimal range, the Powermeter automatically adjusts the measurement range. Changing the measurement range will temporarily interrupt the measurement for up to 10 milliseconds to allow the analog hardware to stabilize. After this period, measurement will automatically resume.
		
		For continuous wave (CW) signals, the current auto-ranging feature automatically selects the optimal range for measuring your signal effectively. You can use call :func:`getCurrentRange` to check the currently selected measurement range. When measuring modulated signals in CW mode, it is advisable to manually set the range using :func:`setCurrentRange` to avoid the meter from permanently switching ranges.
		
		When using auto-ranging in peak mode, the input signal must consist of repetitive pulses with a pulse-to-pulse voltage difference of less than 5 percent. In this mode, the Powermeter automatically selects the appropriate range and adjusts the threshold for peak detection. If the signal is lost, the algorithm will initiate a peak-finding procedure after a timeout of 500 ms. For all other types of pulse signals, you will need to manually set the range using :func:`setCurrentRange`  and adjust the threshold with :func:`setPeakThreshold`
		
		The state of auto-ranging is stored persistently and will be restored after a reboot. If you change the sensor type, auto-ranging is enabled by default. You can check the ranging status by looking for flag bit 2 in the Operation Status register using :func:`readRegister` to determine if the ranging pause is currenly active.
		
		Remarks:
		(1) Auto-ranging is enabled by default
		(2) By default auto-ranging is supported for CW signals only
		(3) Auto-ranging is not useful for fast measurements like scope, burst or fast measurement stream due to the ranging measurement pauses
		(4) Auto-ranging should be disabled for modulated input signals in CW measurement mode.
		(5) Not all powermeter support auto-ranging in peak mode. Ensure you installed the recent firmware for your Powermeter.  
		
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
		Tests if auto-ranging is enabled for current [A] measurement. For closer details read :func:`setCurrentAutoRange`. You can query the currently used range by using :func:`getCurrentRange`. Auto range enable state is stored persistently and restored after reboot.
		
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
		Sets a manual range for the specified current in amperes [A]. Activating a manual range will automatically disable auto-ranging (see :func:`setCurrentAutoRange`). Changing the measurement range will temporarily interrupt the measurement for up to 10 milliseconds to allow the analog hardware to stabilize. After this period, measurement will automatically resume. The manual range is stored persistently and will be restored after a reboot. You can check the ranging status by looking for flag bit 2 in the Operation Status register using :func:`readRegister` to determine if the ranging pause is currenly active.
		
		Remarks:
		(1) Select a manual range for fast measurements like scope, burst or fast measurement stream
		(2) Select a manual range for modulated light input measurements in CW mode to prevent the meter from interrupting measurements due to range switching.
		
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
		This function returns the actual current [A] range value. The range gets changed either by auto-ranging :func:`setCurrentAutoRange` or manually by :func:`setCurrentRange`. A manually selected range is stored persistently and will be restored after a reboot.
		
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
		This function returns a list of all  photodiode current measurement ragnes of the Powermeter. 
		
		Notes:
		(1) The function is NOT available on PM100D, PM100A, PM160, PM160T, PM16, PM200
		
		Args:
			currentValues( (c_double * arrayLength)()) : List of all photodiode current measurement ranges for the power-meter. At least 25 entries long. All entries have the unit Ampere. Check the <Range Count> parameter to get the entry count.  
			rangeCount(c_uint16 use with byref) : Amount of current ranges for this Powermeter
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
		This command activates auto-ranging until a stable range is detected, at which point auto-ranging is disabled again. Use this command to automatically find the best-fitting range after altering the input signal. If auto-ranging was previously enabled, it will be turned off afterward. The command requires a stable continuous wave (CW) signal during the search process. You can check the currently used range by using the :func:`getCurrentAutorange` function. 
		
		A similar function is available for Pyro and Photodiode in peak measurement mode; refer to the :func:`startPeakDetector` function. The resulting range is stored persistently and will be restored after a reboot.
		
		Remarks:
		(1) Not supported for PM100D, PM100A, PM160, PM160T, PM16, PM200, PM400, PM101, PM102
		
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
		Sets a current offset in amperes [A] for delta measurement mode. To switch to relative measurements, make sure that delta mode is enabled using the :func:`setCurrentRefState` fucntion. Any non-zero parameter value will result in a relative measurement. To obtain relative measurement results, call :func:`measCurrent` afterwards. The relative current offset parameter is not stored persistently and will be reset to zero after a reboot!
		
		Args:
			currentReferenceValue(c_double) : This parameter specifies the current reference value in amperes [A]. This value is used for calculating differences between the actual current value and this current reference value.
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
		Retrieves the currently used current offset in amperes [A] for delta measurement mode. Even if a non-zero offset has been set, it will not be applied until delta mode is enabled using the :func:`setCurrentRefState` command. Please note that the relative current offset parameter is not stored persistently and will be reset to zero after a reboot!
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			currentReferenceValue(c_double use with byref) : This parameter returns the specified current reference value in amperes [A]. This value is used for calculating differences between the actual current value and this current reference value.
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
		Enables current [A] delta measurement mode. When delta mode is activated and a non-zero offset has been previously set using :func:`setCurrentRef`, the :func:`measCurrent` function will return relative measurements. If delta mode is subsequently disabled, the measurement command will revert to returning absolute measurements, even if a non-zero offset was set earlier. Please note that delta mode is automatically disabled after a reboot or when the sensor is changed.
		
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
		Checks if current [A] delta measurement mode is enabled. When delta mode is active and a non-zero offset has been previously set using:func:`setCurrentRef`, the :func:`measCurrent` function will return relative measurements.
		
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

	def setEnergyAutoRange(self, val, channel):
		"""
		This command enables or disables the auto-ranging feature for energy measurement. When auto-ranging is active, the Powermeter compares the measured peak values to the currently used measurement range. If the signal falls outside the optimal range, the Powermeter automatically adjusts the measurement range. Additionally, the meter modifies the peak detection threshold when auto-ranging is enabled. Changing the measurement range will temporarily interrupt the measurement for up to 10 milliseconds to allow the analog hardware to stabilize. After this period, measurement will automatically resume.
		Auto-ranging for energy measurement requires a repetitive pulsed input signal with a repetition rate greater than 5 Hz. It also relies on small changes (<5%) between the pulses. If auto-ranging loses peaks due to an incorrect threshold, it will automatically initiate the peak finder algorithm after a timeout of 500 milliseconds.
		You can inquire about the current range using the :func:`getEnergyRange` function. If you set a manual range using the :func:`setEnergyRange` command, auto-ranging will be disabled automatically. The state of auto-ranging is stored persistently and will be restored after a reboot. If you change the sensor type, auto-ranging is enabled by default. You can check the ranging status by looking for flag bit 2 in the Operation Status register using the :func:`readRegister` command to determine if the ranging process was completed successfully.
		
		Remarks:
		(1) Not all powermeter support auto-ranging in peak mode. Ensure you installed the recent firmware for your Powermeter. 
		
		Args:
			val(c_int16) : This parameter specifies the energy auto range mode. 
			
			Acceptable values:
			  TLPM_AUTORANGE_ENERY_OFF (0):  energy auto range disabled
			  TLPM_AUTORANGE_ENERGY_ON  (1): energy auto range enabled
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setEnergyAutoRange(self.devSession, val, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getEnergyAutorange(self, pVal, channel):
		"""
		Tests if auto-ranging is enabled for energy measurement. For closer details read :func:`setEnergyAutoRange`. You can query the currently used range by using :func:`getEnergyRange`. Auto range enable state is stored persistently and restored after reboot.
		
		Args:
			pVal(c_int16 use with byref) : This parameter returns the energy auto range mode.
			Works only for PM103, PM103E and PM5020 with the newest firmware.
			
			Return values:
			  TLPM_AUTORANGE_ENERGY_OFF (0): energy auto range disabled
			  TLPM_AUTORANGE_ENERGY_ON  (1): energy auto range enabled
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getEnergyAutorange(self.devSession, pVal, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setEnergyRange(self, energyToMeasure, channel):
		"""
		Sets a manual range for the specified energy in Joules[J]. Activating a manual range will automatically disable auto-ranging (see :func:`setEnergyAutoRange`). Changing the measurement range will temporarily interrupt the measurement for up to 10 milliseconds to allow the analog hardware to stabilize. After this period, measurement will automatically resume. The manual range is stored persistently and will be restored after a reboot. You can check the ranging status by looking for flag bit 2 in the Operation Status register using :func:`readRegister` to determine if the ranging pause is currenly active.
		
		Remarks:
		(1) Select a manual range for slow (<5 Hz) and single pulse input signals
		(2) Select a manual range for input signals with an unstable pulse-to-pulse ratio (>5%)
		
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
		This function returns the actual energy [J] range value. The range gets changed either by auto-ranging :func:`setEnergyAutoRange` or manually by :func:`setEnergyRange`. A manually selected range is stored persistently and will be restored after a reboot.
		
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
		Sets a energy offset in joules [J] for delta measurement mode. To switch to relative measurements, make sure that delta mode is enabled using the :func:`setEnergyRefState` fucntion. Any non-zero parameter value will result in a relative measurement. To obtain relative measurement results, call :func:`measEnergy` afterwards. The relative energy offset parameter is not stored persistently and will be reset to zero after a reboot!
		
		Args:
			energyReferenceValue(c_double) : This parameter specifies the pyro sensor's energy reference value in joule [J]. This value is used for calculating differences between the actual energy value and this energy reference value.
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
		Retrieves the currently used energy offset in joules [J] for delta measurement mode. Even if a non-zero offset has been set, it will not be applied until delta mode is enabled using the :func:`setEnergyRefState` command. Please note that the relative energy offset parameter is not stored persistently and will be reset to zero after a reboot!
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			energyReferenceValue(c_double use with byref) : This parameter returns the specified pyro sensor's energy reference value in joule [J]. The set value is used for calculating differences between the actual energy value and this energy reference value.
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
		Enables energy [J] delta measurement mode. When delta mode is activated and a non-zero offset has been previously set using :func:`setEnergyRef`, the :func:`measEnergy` function will return relative measurements. If delta mode is subsequently disabled, the measurement command will revert to returning absolute measurements, even if a non-zero offset was set earlier. Please note that delta mode is automatically disabled after a reboot or when the sensor is changed.
		
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
		Checks if energy [J] delta measurement mode is enabled. When delta mode is active and a non-zero offset has been previously set using:func:`setEnergyRef`, the :func:`measEnergy` function will return relative measurements.
		
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
		Changes the measurement mode of the photodiode sensor. The Powermeter can measure photodiode sensors in continuous wave (CW) mode, which is suitable for CW input signals. When measuring modulated signals such as sinusoidal, triangular, or square waves in CW mode, you will obtain the average power. If you need to measure peak power, you must switch to peak mode, which will return a single measurement result for each detected peak. In CW mode, the Powermeter continuously outputs measurement results, while in peak mode, the output is dependent on the modulation frequency of the input signal. 
		
		Remarks:
		(1) This command only applies for Photodiode sensors
		(2) Pyroelectric sensor always measure in peak mode
		(3) Thermoeletric sensors always measure in CW mode
		(4) Measurement averaging is applied in CW mode only
		(5) NOT available for PM100D, PM100A, PM160, PM160T, PM16, PM200, PM400
		
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
		retrieve the measurement method of the connected sensor. Photodiode sensors support both continuous wave (CW) and peak modes, while pyro sensors support peak mode only, and thermopile sensors support CW mode exclusively. 
		
		Remarks:
		(1) NOT available for PM100D, PM100A, PM160, PM160T, PM16, PM200, PM400
		
		
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
		Enables or disables the auto-ranging feature for power[W,dBm] measurement. When auto-ranging is active, the Powermeter compares the measured signal to the currently used measurement range. If the signal falls outside the optimal range, the Powermeter automatically adjusts the measurement range. Changing the measurement range will temporarily interrupt the measurement for up to 10 milliseconds to allow the analog hardware to stabilize. After this period, measurement will automatically resume.
		
		For continuous wave (CW) signals, the power auto-ranging feature automatically selects the optimal range for measuring your signal effectively. You can use call :func:`getPowerRange` to check the currently selected measurement range. When measuring modulated signals in CW mode, it is advisable to manually set the range using :func:`setPowerRange` to avoid the meter from permanently switching ranges.
		
		When using auto-ranging in peak mode, the input signal must consist of repetitive pulses with a pulse-to-pulse voltage difference of less than 5 percent. In this mode, the Powermeter automatically selects the appropriate range and adjusts the threshold for peak detection. If the signal is lost, the algorithm will initiate a peak-finding procedure after a timeout of 500 ms. For all other types of pulse signals, you will need to manually set the range using :func:`setPowerRange`  and adjust the threshold with :func:`setPeakThreshold`
		
		The state of auto-ranging is stored persistently and will be restored after a reboot. If you change the sensor type, auto-ranging is enabled by default. You can check the ranging status by looking for flag bit 2 in the Operation Status register using :func:`readRegister` to determine if the ranging pause is currenly active.
		
		Remarks:
		(1) Auto-ranging is enabled by default
		(1) By default auto-ranging is supported for CW signals only
		(2) Auto-ranging is not useful for fast measurements like scope, burst or fast measurement stream due to the ranging measurement pauses
		(3) Auto-ranging should be disabled for modulated input signals in CW measurement mode.
		(2) Not all powermeter support auto-ranging in peak mode. Ensure you installed the recent firmware for your Powermeter.  
		
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
		Tests if auto-ranging is enabled for power [W, dBm] measurement. For closer details read :func:`setPowerAutoRange`. You can query the currently used range by using :func:`getPowerRange`. Auto-range enable state is stored persistently and restored after reboot.
		
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
		Sets a manual range for the specified power in watts [W]. Activating a manual range will automatically disable auto-ranging (see :func:`setPowerAutoRange`). Changing the measurement range will temporarily interrupt the measurement for up to 10 milliseconds to allow the analog hardware to stabilize. After this period, measurement will automatically resume. The manual range is stored persistently and will be restored after a reboot. You can check the ranging status by looking for flag bit 2 in the Operation Status register using :func:`readRegister` to determine if the ranging pause is currenly active.
		
		Remarks:
		(1) Select a manual range for fast measurements like scope, burst or fast measurement stream
		(2) Select a manual range for modulated light input measurements in CW mode to prevent the meter from interrupting measurements due to range switching.
		
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
		This function returns the actual power [W] range value. The range gets changed either by auto-ranging :func:`setPowerAutoRange` or manually by :func:`setPowerRange`. A manually selected range is stored persistently and will be restored after a reboot.
		
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

	def setPowerRangeSearch(self, channel):
		"""
		This command activates auto-ranging until a stable range is detected, at which point auto-ranging is disabled again. Use this command to automatically find the best-fitting range after altering the input signal. If auto-ranging was previously enabled, it will be turned off afterward. The command requires a stable continuous wave (CW) signal during the search process. You can check the currently used range by using the :func:`getPowerAutorange` function. 
		
		A similar function is available for Pyro and Photodiode in peak measurement mode; refer to the :func:`startPeakDetector` function. The resulting range is stored persistently and will be restored after a reboot.
		
		Remarks:
		(1) Not supported for PM100D, PM100A, PM160, PM160T, PM16, PM200, PM400, PM101, PM102
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerRangeSearch(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerRef(self, powerReferenceValue, channel):
		"""
		Sets a power offset in watts [W] for delta measurement mode. To switch to relative measurements, make sure that delta mode is enabled using the :func:`setPowerRefState` fucntion. Any non-zero parameter value will result in a relative measurement. To obtain relative measurement results, call :func:`measPower` afterwards. The relative power offset parameter is not stored persistently and will be reset to zero after a reboot!
		
		Args:
			powerReferenceValue(c_double) : Specifies the power reference value. This value is used for calculating differences between the actual power value and this power reference value.
			
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
		Retrieves the currently used power offset in watts [W] for delta measurement mode. Even if a non-zero offset has been set, it will not be applied until delta mode is enabled using the :func:`setPowerRefState` command. Please note that the relative power offset parameter is not stored persistently and will be reset to zero after a reboot!
		
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
		Enables power [W] delta measurement mode. When delta mode is activated and a non-zero offset has been previously set using :func:`setPowerRef`, the :func:`measPower` function will return relative measurements. If delta mode is subsequently disabled, the measurement command will revert to returning absolute measurements, even if a non-zero offset was set earlier. Please note that delta mode is automatically disabled after a reboot or when the sensor is changed.
		
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
		Checks if power [W] delta measurement mode is enabled. When delta mode is active and a non-zero offset has been previously set using:func:`setPowerRef`, the :func:`measPower` function will return relative measurements.
		
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
		Changes the power unit between Watt and dBm. The unit affects the results of the :func:`measPower` command. The default unit is Watt.
		
		Remarks:
		(1) This does not affect the units of the fast measurement stream, scope or burst measurements
		(2) This does not affect the power related parameters in the setters like e.g. :func:`setCurrentRef`
		
		Args:
			powerUnit(c_int16) : This parameter specifies the unit of the pover value.
			
			Acceptable values:
			  TLPM_POWER_UNIT_WATT (0): power in Watt
			  TLPM_POWER_UNIT_DBM  (1): power in dBm
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
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
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerUnit(self.devSession, powerUnit, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerCalibrationPointsInformation(self, index, serialNumber, calibrationDate, calibrationPointsCount, author, sensorPosition, channel):
		"""
		Retrieve the customer calibration meta information like serial nr, cal date, nr of points at given index. After calling this function use :func:`getPowerCalibrationPoints` to query the correction set points until you reach the Calibration Points Count Parameter limit. 
		The customer calibrations allows customers to modify sensor corrections at fixed wavelength set points. Each calibration is stored within the Powermeter and is associated with a single sensor identified by its serial number. The factory calibration of both the Powermeter and the sensor remains unaffected by the customer calibration. The Powermeter automatically applies the customer calibration when the corresponding sensor is connected and the calibration is enabled by function  :func:`setPowerCalibrationPointsState`. To check if a customer calibration is currently active for sensor call  :func:`readRegister` for Auxilary register. Then check for UseCustomerCalibration flag bit 3 in the result. 
		
		Remarks:
		(1) Even if customer calibration is stored it might be disabled by :func:`setPowerCalibrationPointsState`
		(2) Only PM400, PM101,PM102, PM103 support customer calibration slot index 5. All other powermeters have only 4 slots. 
		(3) The customer calibration correction point list ist limited to 10 entries
		(4) Customer calibrations are only applied during sensor initialization.
		(5) Sensor adapters(Sensors without EEPROM) do not support customer calibration
		
		Args:
			index(c_uint16) : Memory slot where to store customer calibration. For PM400, PM101, PM102 last index is 5 otherwise last index is 4!
			serialNumber(create_string_buffer(1024) use with byref) : Serial Number of the sensor. Please provide a buffer of 20 characters.
			calibrationDate(create_string_buffer(1024) use with byref) : Last calibration date of this sensor. Please provide a buffer of 20 characters.
			calibrationPointsCount(c_uint16 use with byref) : Number of calibration points of the power calibration with this sensor
			author(create_string_buffer(1024) use with byref) : Author of calibration. Max 19 characters.
			sensorPosition(c_uint16 use with byref) : The position of the sencor switch of a Thorlabs S130C. For all sensor with a single head position has to be 1.
			1 = 5mW
			2 = 500mW
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerCalibrationPointsInformation(self.devSession, index, serialNumber, calibrationDate, calibrationPointsCount, author, sensorPosition, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerCalibrationPointsState(self, index, state, channel):
		"""
		Queries the state if the customer calibration at given slot is enabled. When slot is enabled and the sensor serial matches the customer calibration the sensor gets initiaialized with the customer calibration. If the slot is disabled the sensor initializes only with the factory calibration. For closer details refer to :func:`setPowerCalibrationPointsState`.
		
		Args:
			index(c_uint16) : Memory slot where to store customer calibration. For PM400, PM101, PM102 last index is 5 otherwise last index is 4!
			state(c_int16 use with byref) : State if the customer calibration is activated and used for the measurements.
			
			VI_ON: The user power calibration is used
			VI_OFF: The user power calibration is ignored
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerCalibrationPointsState(self.devSession, index, state, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerCalibrationPointsState(self, index, state, channel):
		"""
		Enable or disable a customer calibration for a specified slot. When a slot is enabled and the sensor serial matches the customer calibration the sensor gets initiaialized with the customer calibration. If the slot is disabled the sensor initializes only with the factory calibration. 
		
		The customer calibrations allows customers to modify sensor corrections at fixed wavelength set points. Each calibration is stored within the Powermeter and is associated with a single sensor identified by its serial number. The factory calibration of both the Powermeter and the sensor remains unaffected by the customer calibration. The Powermeter automatically applies the customer calibration when the corresponding sensor is connected and the calibration is enabled by this function. To check if a customer calibration is currently active for sensor call  :func:`readRegister` for Auxilary register. Then check for UseCustomerCalibration flag bit 3 in the result. 
		
		Remarks:
		(1) Even if customer calibration is stored it might be disabled by :func:`setPowerCalibrationPointsState`
		(2) Only PM400, PM101,PM102, PM103 support customer calibration slot index 5. All other powermeters have only 4 slots. 
		(3) Customer calibrations are only applied during sensor initialization.
		(4) Sensor adapters(Sensors without EEPROM) do not support customer calibration
		
		Args:
			index(c_uint16) : Memory slot where to store customer calibration. For PM400, PM101, PM102 last index is 5 otherwise last index is 4!
			state(c_int16) : State if the user power calibration is activated and used for the power measurements.
			
			VI_ON: The user power calibration is used
			VI_OFF: The user power calibration is ignored in the power measurements
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerCalibrationPointsState(self.devSession, index, state, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerCalibrationPoints(self, index, pointCounts, wavelengths, powerCorrectionFactors, channel):
		"""
		Retrieve the customer calibration set point tuple list at given memory slot index. Every set point tuple is a point for wavelength and a correction factor. The length of the resulting tuple list is variable from 1 to 10.  Call :func:`getPowerCalibrationPointsInformation` previously to get the amount of tuples available for this memory slot. Ensure the both list parameters are large enough to store at least the amount of requested data. 
		For closer information refer to :func:`setPowerCalibrationPoints`
		
		Remarks:
		(1) Even if customer calibration is stored it might be disabled by :func:`setPowerCalibrationPointsState`
		(2) Only PM400, PM101,PM102, PM103 support customer calibration slot index 5. All other powermeters have only 4 slots. 
		(3) The customer calibration correction point list ist limited to 10 entries
		
		Args:
			index(c_uint16) : Memory slot where to store customer calibration. For PM400, PM101, PM102 last index is 5 otherwise last index is 4!
			pointCounts(c_uint16) : Amount of set points to query. Ensure Wavelength and Correction Factor list length are equal or larger than this count. Query more than available will result in an error. 
			wavelengths( (c_double * arrayLength)()) : Result list of wavelength in nm. Together with Correction Factors this specifies the correction set point tuples. Ensure length matches Point Counts. 
			powerCorrectionFactors( (c_double * arrayLength)()) : Result list of correction factors Together with Wavelengts this specifies the correction set point tuples. Ensure length matches Point Counts. 
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPowerCalibrationPoints(self.devSession, index, pointCounts, wavelengths, powerCorrectionFactors, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerCalibrationPoints(self, index, pointCounts, wavelengths, powerCorrectionFactors, author, sensorPosition, channel):
		"""
		Writes a customer calibration for the currently connected sensor to memory at the specified index.
		
		Calibration Process:
		Before writing the customer calibration, use a specified light source with a known wavelength and light power or energy. Perform reference measurements with the power meter, then calculate the correction factor using the formula: factor = measured power or energy / reference power or energy for that wavelength. Repeat this process with up to 10 different wavelength light sources.
		
		Once all correction factors are calculated, call this function to persist the calibration for the connected sensor. It is mandatory to provide the wavelength-factor tuples in ascending wavelength order. After successfully writing the customer calibration, use :func:`setPowerCalibrationPointsState` to enable it. Then invoke the :func:`reinitSensor` function in a final step to reinit the sensor head if the calibration should become active without a reboot.
		
		Remarks:
		(1) Even if customer calibration is stored it might be disabled by :func:`setPowerCalibrationPointsState`
		(2) Only PM400, PM101,PM102, PM103 support customer calibration slot index 5. All other powermeters have only 4 slots. 
		(3) The customer calibration correction point list ist limited to 10 entries
		(4) Customer calibrations are only applied during sensor initialization.
		(5) Sensor adapters(Sensors without EEPROM) do not support customer calibration
		
		Args:
			index(c_uint16) : Memory slot where to store customer calibration. For PM400, PM101, PM102 last index is 5 otherwise last index is 4!
			pointCounts(c_uint16) : Number of tuples that are submitted in the wavelength and power correction factors lists. Maximum of 10 wavelength - correction factors tuples can be calibrated for each sensor.
			wavelengths( (c_double * arrayLength)()) : Array of wavelengths in nm. Requires ascending wavelength order. The array must contain <points counts> entries. Together with Correction Factor list this specifies the correction tuple list. 
			powerCorrectionFactors( (c_double * arrayLength)()) : List of correction factors. Where every factor is between 0.80 and 1.2. The array must contain <Points Counts> entries.  Together with Wavelength list this specifies the correction tuple list. 
			author(c_char_p) : Buffer that contains the name of the editor of the calibration. Name of Author limited to 20 chars including zero termination. 
			sensorPosition(c_uint16) : The position of the sencor switch of a Thorlabs S130C(1 = 5mW, 2 = 500mW). For all sensor with a single head position use index 1.
			
			
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPowerCalibrationPoints(self.devSession, index, pointCounts, wavelengths, powerCorrectionFactors, author, sensorPosition, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def reinitSensor(self, channel):
		"""
		Simulates unplugging and then plugging in the sensor connector. This final step is essential after modifying the customer calibration for the currently connected sensor. Please note that executing this command will interrupt any ongoing measurements. This function will wait 2 seconds until the sensor has been reinitialized.
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_reinitSensor(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setVoltageAutoRange(self, voltageAutorangeMode, channel):
		"""
		Enables or disables the auto-ranging feature for voltage [V] measurement. When auto-ranging is active, the Powermeter compares the measured signal to the currently used measurement range. If the signal falls outside the optimal range, the Powermeter automatically adjusts the measurement range. Changing the measurement range will temporarily interrupt the measurement for up to 10 milliseconds to allow the analog hardware to stabilize. After this period, measurement will automatically resume.
		
		For continuous wave (CW) signals of thermopile sensors, the current auto-ranging feature automatically selects the optimal range for measuring your signal effectively. You can use call :func:`getVoltageRange` to check the currently selected measurement range. When measuring modulated signals in CW mode, it is advisable to manually set the range using :func:`setVoltageRange` to avoid the meter from permanently switching ranges.
		
		When using auto-ranging in peak mode for pyroelectric sensors, the input signal must consist of repetitive pulses with a pulse-to-pulse voltage difference of less than 5 percent. In this mode, the Powermeter automatically selects the appropriate range and adjusts the threshold for peak detection. If the signal is lost, the algorithm will initiate a peak-finding procedure after a timeout of 500 ms. For all other types of pulse signals, you will need to manually set the range using :func:`setVoltageRange`  and adjust the threshold with :func:`setPeakThreshold`
		
		The state of auto-ranging is stored persistently and will be restored after a reboot. If you change the sensor type, auto-ranging is enabled by default. You can check the ranging status by looking for flag bit 2 in the Operation Status register using :func:`readRegister` to determine if the ranging pause is currenly active.
		
		Remarks:
		(1) Auto-ranging is enabled by default
		(2) By default auto-ranging is supported for CW signals only
		(3) Auto-ranging is not useful for fast measurements like scope, burst or fast measurement stream due to the ranging measurement pauses
		(4) Auto-ranging should be disabled for modulated input signals in CW measurement mode.
		(5) Not all powermeter support auto-ranging in peak mode. Ensure you installed the recent firmware for your Powermeter.  
		
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
		Tests if auto-ranging is enabled for voltage [V] measurement. For closer details read :func:`setVoltageAutoRange`. You can query the currently used range by using :func:`getVoltageRange`. Auto range enable state is stored persistently and restored after reboot.
		
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
		Sets a manual range for the specified voltage in Volt [V]. Activating a manual range will automatically disable auto-ranging (see :func:`setVoltageAutoRange`). Changing the measurement range will temporarily interrupt the measurement for up to 10 milliseconds to allow the analog hardware to stabilize. After this period, measurement will automatically resume. The manual range is stored persistently and will be restored after a reboot. You can check the ranging status by looking for flag bit 2 in the Operation Status register using :func:`readRegister` to determine if the ranging pause is currenly active.
		
		Remarks:
		(1) Select a manual range for fast measurements like scope, burst or fast measurement stream
		(2) Select a manual range for modulated light input measurements in CW mode to prevent the meter from interrupting measurements due to range switching.
		
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
		This function returns a list of all thermopile or pyro voltage measurement ragnes of the Powermeter. 
		
		Notes:
		(1) The function is NOT available on PM100D, PM100A, PM160, PM160T, PM16, PM200
		(2) The result depends on the connected sensor type
		
		Args:
			voltageValues( (c_double * arrayLength)()) : List of all pyro or thermopile voltage measurement ranges for the power-meter. At least 25 entries long. All entries have the unit Volt [V]. Check the <Range Count> parameter to get the entry count. 
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
		This command activates auto-ranging until a stable range is detected, at which point auto-ranging is disabled again. Use this command to automatically find the best-fitting range after altering the input signal. If auto-ranging was previously enabled, it will be turned off afterward. The command requires a stable continuous wave (CW) signal during the search process. You can check the currently used range by using the :func:`getCurrentAutorange` function. 
		
		A similar function is available for Pyro and Photodiode in peak measurement mode; refer to the :func:`startPeakDetector` function. The resulting range is stored persistently and will be restored after a reboot.
		
		Remarks:
		(1) Not supported for PM100D, PM100A, PM160, PM160T, PM16, PM200, PM400, PM101, PM102
		(1) For thermopile sensors only
		
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
		Sets a voltage offset in Volts [V] for delta measurement mode. To switch to relative measurements, make sure that delta mode is enabled using the :func:`setVoltageRefState` fucntion. Any non-zero parameter value will result in a relative measurement. To obtain relative measurement results, call :func:`measVoltage` afterwards. The relative current offset parameter is not stored persistently and will be reset to zero after a reboot!
		
		Args:
			voltageReferenceValue(c_double) : This parameter specifies the voltage reference value in volts [V]. This value is used for calculating differences between the actual voltage value and this voltage reference value.
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
		Retrieves the currently used voltage offset in volts [V] for delta measurement mode. Even if a non-zero offset has been set, it will not be applied until delta mode is enabled using the :func:`setVoltageRefState` command. Please note that the relative current offset parameter is not stored persistently and will be reset to zero after a reboot!
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			voltageReferenceValue(c_double use with byref) : This parameter returns the specified voltage reference value in volts [V]. This value is used for calculating differences between the actual voltage value and this voltage reference value.
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
		Enables voltage [V] delta measurement mode. When delta mode is activated and a non-zero offset has been previously set using :func:`setVoltageRef`, the :func:`measVoltage` function will return relative measurements. If delta mode is subsequently disabled, the measurement command will revert to returning absolute measurements, even if a non-zero offset was set earlier. Please note that delta mode is automatically disabled after a reboot or when the sensor is changed.
		
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
		Checks if voltage [V] delta measurement mode is enabled. When delta mode is active and a non-zero offset has been previously set using:func:`setVoltageRef`, the :func:`measVoltage` function will return relative measurements.
		
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
		Sets the peak detection threshold in percent [%]. The percentage is relatively compared to the actually used measurement range maximum value. For Pyro or modulated Photodiode signals the Powermeter compares sensor signal to a threshold to decide if a new pulse has been found. If the threshold is too low noise floor may be detected as peak signals. If the threshold is too high the Powermeter will not measure a single pulse. 
		You might also use the peak finder algorithm :func:`startPeakDetector` to set the threshold once automatically. For repetive pulsed input signals you might also want to use auto-ranging algorithm e.g. :func:`setCurrentAutoRange` to let the device control the threshold level automatically. 
		The threshold is also used for light modulation frequency measurement :func:`measFreq`.
		
		Remarks:
		(1) Threshold is relative to the maximum measurement value for the currently selected range
		(2) For pyro sensors this threshold have to be 10-15% below the expected peak otherwise the deteced energy pulses are read to low.
		(3) Used for pyro or photodiode sensor signal peak detection in peak mode
		(4) Used for frequency measurement. See :func:`measFreq`
		
		Args:
			peakThreshold(c_double) : This parameter specifies the peak detector threshold in percent [%] of the maximum from the actual measurements range.
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
		Use this command to query the peak detection threshold in percent. For closer details about the threshold read :func:`setPeakThreshold` description.
		
		Remarks:
		(1) Threshold is relative to the maximum measurement value for the currently selected range
		(2) For pyro sensors this threshold have to be 10-15% below the expected peak otherwise the deteced energy pulses are read to low.
		(3) Used for pyro or photodiode sensor signal peak detection in peak mode
		(4) Used for frequency measurement. See :func:`measFreq`
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			peakThreshold(c_double use with byref) : This parameter specifies the peak detector threshold in percent [%] of the maximum from the actual measurements range.
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
		Initiates or aborts the peak-finder background algorithm. When the Powermeter receives this command, it will halt normal measurements and attempt to asynchronously determine the optimal measurement range and peak-detection threshold for the pulsed input signal. Please note that auto-ranging will be disabled once the peak-finder algorithm is started.
		You can check the status of the background operation by using the :func:`isPeakDetectorRunning` function or by polling the StatusPeakFinder flag in the Operation Status register with :func:`readRegister`. 
		The peak-finder algorithm will always terminate, even if no pulses are detected. This algorithm is specifically designed for repetitive pulsed input signals measured with photodiodes in peak mode or pyro sensors. To switch the photodiode to peak mode, use the :func:`setFreqMode` command.
		If you wish to abort a previously initiated procedure, simply send the same command while the peak-finder is active. To retrieve the new parameters call functions :func:`getPeakThreshold` and  e.g. :func:`getPowerRange` to retrieve the automatically set parameters later.
		
		Remarks:
		(1) Only available for repetitive pulsed input signals with a stable pulse-to-pulse ratio in peak mode measured by Photodiode or Pyro sensors.
		(2) The function is NOT available on PM100D, PM100A, PM100USB, PM160, PM160T, PM16, PM200, PM400, PM101, PM102
		
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
		Use this command to query the peak detection threshold in percent. For closer details about the threshold read :func:`startPeakDetector` description.
		
		Remarks:
		(1) The function is NOT available on PM100D, PM100A, PM100USB, PM160, PM160T, PM16, PM200, PM400, PM101, PM102
		
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
		Enables or disables peak overshoot filter. If the filter is enabled, the Powermeter will filter Over- and Undershoots on the sensor signal during peak measurement. This is useful for Photodiode when measuring TTL signals. For any other modulation like sinus or triangle disable the filter.
		
		Remarks:
		(1) Note: The function is NOT available on PM100D, PM100A, PM100USB, PM160, PM160T, PM16, PM200, PM400, PM101, PM102
		
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
		Test if peak overshoot filter is enabled. If the filter is enabled, the Powermeter will filter over- and undershoots on the sensor signal during peak measurement. This is useful for Photodiode when measuring TTL signals. For any other modulation like sinus or triangle disable the filter. 
		
		Remarks:
		(1) Note: The function is NOT available on PM100D, PM100A, PM100USB, PM160, PM160T, PM16, PM200, PM400, PM101, PM102
		
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
		This function sets the temperature calculation coefficients for the NTC sensor externally connected to the instrument (NTC IN). Call :func:`measExtNtcTemperature` function to get the temperature measurement of external NTC or call :func:`measExtNtcResistance` function to query the NTC resistance. 
		
		Notes:
		(1) A wrong parameter value results in a wrong temperature measurements
		(2) Only available when Powermeter has an external NTC resistor input
		
		
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
		(1) Only available when Powermeter has an external NTC resistor input
		
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
		Returns value range (min and max) of the slope prameter for given light power or energy analog output channel. For closer details refer to :func:`setAnalogOutputSlope`. 
		To query the voltage range of the selcted analog output channel call :func:`getAnalogOutputVoltageRange`. 
		To query the slope range for the position output call :func:`getPositionAnalogOutputSlopeRange`.
		
		Remarks:
		(1) Available only on powermeters equipped with a generated light power or energy analog output
		
		Args:
			minSlope(c_double use with byref) : Minimum allowed slope. Unit depends on connected sensor.
			maxSlope(c_double use with byref) : Maximum allowed slope. Unit depends on connected sensor.
			
			channel(c_uint16) : 2 - Generated power/energy output for measurement channel 1: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor.
			3 - Reserved
			4 - Reserved
			5 - Reserved
			6 - Generated power/energy output for measurement channel 2: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor
			7 - Reserved
			8 - Reserved
			9 - Reserved
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputSlopeRange(self.devSession, minSlope, maxSlope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAnalogOutputSlope(self, slope, channel):
		"""
		This function sets the slope parameter for the specified light power or energy analog output channel. The powermeter computes the DAC output voltage as follows: DAC_V = Power or Energy *  slope. The unit of the slope varies depending on the connected sensor. For the generated main output, it is volts per watt [V/W] for photodiode and thermopile sensors, or volts per joule [V/J] for pyroelectric sensors. The voltage for the light power or energy is updated only when :func:`setAnalogOutputRoute` is configured appropriatly.
		To determine an appropriate slope value, first call :func:`getAnalogOutputVoltageRange` to retrieve the voltage range for the selected channel, or consult the product manual for details. To set the slope for the position output call :func:`setPositionAnalogOutputSlope`.
		You can use :func:`getAnalogOutputVoltage` to query the actual applied DAC output voltage, for example, to verify or test the slope setting. The slope value is stored persistently and will be automatically applied after a powermeter reboot. 
		      
		The following example illustrates how to select a suitable slope for a given application: Assume the maximum output voltage of the selected channel is 2V and the expected power to be measured is 3mW. The ratio of maximum voltage to expectedpower is 2V / 0.003W = 666.66. To generate an output voltage of 1.5V at 3mW, a slope of 500 can be selected. Alternatively, a slope of 100 could be chosen to generate 0.3V at 3mW.
		
		Remarks:
		(1) Available only on powermeters equipped with a generated light power or energy analog output.
		(2) Slope does not apply to the raw ampliefied analog sensor output.
		(3) DAC depends on measurement mode is updated at max 1 kHz.
		(4) The voltage will clip to the analog output physical voltage limits.
		
		Args:
			slope(c_double) : Analog output conversion slope parameter. Unit depends on connected sensor.
			channel(c_uint16) : 2 - Generated power/energy output for measurement channel 1: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor.
			3 - Reserved
			4 - Reserved
			5 - Reserved
			6 - Generated power/energy output for measurement channel 2: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor
			7 - Reserved
			8 - Reserved
			9 - Reserved
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputSlope(self.devSession, slope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputSlope(self, attribute, slope, channel):
		"""
		Returns the slope parameter for given light power or energy analog output channel. The powermeter calculates DAC_V = Power or Energy * slope. The unit of the slope depends on the connected sensor. For closer details refer to :func:`setAnalogOutputSlope`. 
		To query the currenlty output voltage call :func:`getAnalogOutputVoltage`. 
		To query the position output related slope call :func:`getPositionAnalogOutputSlope`. 
		
		Remarks:
		(1) Available only on powermeters equipped with a generated light power or energy analog output
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			slope(c_double use with byref) : Analog output conversion slope parameter. Unit depends on connected sensor.
			channel(c_uint16) : 2 - Generated power/energy output for measurement channel 1: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor.
			3 - Reserved
			4 - Reserved
			5 - Reserved
			6 - Generated power/energy output for measurement channel 2: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor
			7 - Reserved
			8 - Reserved
			9 - Reserved
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputSlope(self.devSession, attribute, slope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputVoltageRange(self, minVoltage, maxVoltage, channel):
		"""
		Returns the analog output voltage [V] range (min and max) for given light power or energy channel. This is especially useful to calculate and later set the channel slope by calling :func:`setAnalogOutputSlope`. To query the actually output voltage call :func:`getAnalogOutputVoltage`. To query the beam position analog output voltage range call :func:`getPositionAnalogOutputVoltageRange`. 
		On the PM5020 you can configure the voltage range by calling <Set Analog Output Gain Range>.
		
		Remarks:
		(1) Available only on powermeters equipped with a generated light power or energy analog output
		
		Args:
			minVoltage(c_double use with byref) : This parameter returns the minimum voltage in Volt [V] of the given analog output channel.
			
			maxVoltage(c_double use with byref) : This parameter returns the maximum voltage in Volt [V] of the given analog output channel.
			channel(c_uint16) : 2 - Generated power/energy output for measurement channel 1: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor.
			3 - Reserved
			4 - Reserved
			5 - Reserved
			6 - Generated power/energy output for measurement channel 2: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor
			7 - Reserved
			8 - Reserved
			9 - Reserved
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputVoltageRange(self.devSession, minVoltage, maxVoltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputVoltage(self, attribute, voltage, channel):
		"""
		Returns the currently output voltage in volts [V] for the specified light power or energy analog output channel. The powermeter computes the DAC output voltage as follows: DAC_V = power or energy *  slope. Call :func:`setAnalogOutputSlope` to modify the slope parameter. The voltage for the light power or energy is updated only when :func:`setAnalogOutputRoute` is configured appropriatly.
		To query the currenlty used analog output voltage for the position output call :func:`getPositionAnalogOutputVoltage`.
		
		Remarks:
		(1) Available only on powermeters equipped with a generated light power or energy analog output.
		(2) DAC depends on measurement mode is updated at max 1 kHz. Reading voltage faster results in duplicate readings.
		(3) The voltage will clip to the analog output physical voltage limits.
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			voltage(c_double use with byref) : This parameter returns the analog output in Volt [V].
			channel(c_uint16) : 2 - Generated power/energy output for measurement channel 1: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor.
			3 - Reserved
			4 - Reserved
			5 - Reserved
			6 - Generated power/energy output for measurement channel 2: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor
			7 - Reserved
			8 - Reserved
			9 - Reserved
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputVoltage(self.devSession, attribute, voltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputGainRange(self, gainRangeIndex, channel):
		"""
		
		Args:
			gainRangeIndex(c_int16 use with byref)
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputGainRange(self.devSession, gainRangeIndex, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAnalogOutputGainRange(self, gainRangeIndex, channel):
		"""
		
		Args:
			gainRangeIndex(c_int16)
			channel(c_uint16)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputGainRange(self.devSession, gainRangeIndex, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputConfig(self, configIdx, channel):
		"""
		This function queries the voltage range for the specified analog output channel. The configured voltage range is stored persistently and automatically restored after a powermeter reboot. To retrieve the actual output voltage for the channel, call :func:`getAnalogOutputVoltage`.
		
		The following provides an overview of the available voltage ranges, mapped by channel:
		
		    Channels 2 & 6 (Generated power/energy output): Ranges 0, 1, 2, 3
		    Channels 3 & 7 (Beam X position output): Ranges 0, 1, 4, 5
		    Channels 4 & 8 (Beam Y position output): Ranges 0, 1, 4, 5
		    Channels 5 & 9: Reserved
		    Channels 10 & 11 (Real analog output): Ranges 0, 1, 2, 3
		
		Remarks:
		(1) This function is available only on the PM5020 model.
		(2) Generated output voltages will clip to the configured limits if they exceed the selected range.
		
		Args:
			configIdx(c_int16 use with byref) : 0: 0 up to 10V
			1: 0 up to 4V
			2: 0 up to 2V
			3: 0 up to 1V
			4: -5 up to 5V
			5: -2 up to 2V
			
			channel(c_uint16) : 2 - Generated power/energy output for measurement channel 1: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor.
			3 - Beam X position output on measurement channel 1: [V/µm]
			4 - Beam Y position output on measurement channel 1: [V/µm]
			5 - Reserved
			6 - Generated power/energy output for measurement channel 2: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor
			7 - Beam X position output on measurement channel 2: [V/µm]
			8 - Beam Y position output on measurement channel 2: [V/µm]
			9 - Reserved
			10 - Raw analog output measurement channel 1
			11 - Raw analog output measurement channel 2
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputConfig(self.devSession, configIdx, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAnalogOutputConfig(self, configIdx, channel):
		"""
		The function changes the voltage range for given analogue output channel. The configured voltage range is stored persistently and automatically restored after a powermeter reboot. Changing the voltage range might require to update slope of channel by function :func:`setAnalogOutputSlope`. 
		
		The following provides an overview of the available voltage ranges, mapped by channel:
		
		    Channels 2 & 6 (Generated power/energy output): Ranges 0, 1, 2, 3
		    Channels 3 & 7 (Beam X position output): Ranges 0, 1, 4, 5
		    Channels 4 & 8 (Beam Y position output): Ranges 0, 1, 4, 5
		    Channels 5 & 9: Reserved
		    Channels 10 & 11 (Real analog output): Ranges 0, 1, 2, 3
		
		Remarks:
		(1) This function is available only on the PM5020 model.
		(2) Generated output voltages will clip to the configured limits if they exceed the selected range.
		
		Args:
			configIdx(c_int16) : 0: 0 up to 10V
			1: 0 up to 4V
			2: 0 up to 2V
			3: 0 up to 1V
			4: -5 up to 5V
			5: -2 up to 2V
			
			channel(c_uint16) : 2 - Generated power/energy output for measurement channel 1: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor.
			3 - Beam X position output on measurement channel 1: [V/µm]
			4 - Beam Y position output on measurement channel 1: [V/µm]
			5 - Reserved
			6 - Generated power/energy output for measurement channel 2: [V/W] for photodiode sensors, [V/W] for thermopile sensors or [V/J] for pyroelectric sensor
			7 - Beam X position output on measurement channel 2: [V/µm]
			8 - Beam Y position output on measurement channel 2: [V/µm]
			9 - Reserved
			10 - Raw analog output measurement channel 1
			11 - Raw analog output measurement channel 2
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputConfig(self.devSession, configIdx, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAnalogLogConf(self, max, dynRange, channel):
		"""
		Call this function to configure the logarithmic power output in dBm. The analog signal is generated by a DAC and is wavelength- and zero-corrected. The maximum parameter specifies the power level at which the analog output reaches its maximum value. The dynamic range parameter determines how the analog voltage range is scaled to the dB range. During ranging pauses, the power meter uses linear interpolation to maintain the signals. After setting the configuration, use :func:`getAnalogOutputRoute` to modify the analog output strategy to Generated dBm. 
		
		Remarks:
		(1) Available only on powermeters equipped with a generated light power or energy analog output
		(2) Not all Powermeter support all kind of output strategies.
		(3) Note that this mode is not available for photodiodes in peak measurement mode
		(4) To smooth the output signal, the generated power or energy mode employs a low pass filter with a cutoff frequency of 10 kHz.
		
		Args:
			max(c_double) : This parameter defines the maximum dBm reference value. This value is utilized by the dBm output route to determine the dBm level at which the DAC produces its maximum voltage. In conjunction with the dBm dynamic range parameter, it scales the dBm range to the DAC output voltage range.
			dynRange(c_double) : This parameter defines the dynamic range of the DAC output in decibels (dB). The dynamic range represents the difference between the maximum and minimum dBm values, which determines how the DAC output voltage range is scaled.
			channel(c_uint16) :  2  - for a single channel powermeters
			11 - for measurement channel 1 (PM5020)
			12 - for measurement channel 2 (PM5020)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogLogConf(self.devSession, max, dynRange, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogLogConf(self, max, dynRange, channel):
		"""
		Use this function to retrieve the current configuration (maximum power level and dynamic range scaling) set by :func:`setAnalogLogConf` for the DAC-generated logarithmic power output in dBm. 
		
		Remarks:
		(1) Available only on powermeters equipped with a generated light power or energy analog output
		(2) Not all Powermeter support all kind of output strategies.
		(3) Note that this mode is not available for photodiodes in peak measurement mode
		(4) To smooth the output signal, the generated power or energy mode employs a low pass filter with a cutoff frequency of 10 kHz.
		
		Args:
			max(c_double) :  2  - for a single channel powermeters
			11 - for measurement channel 1 (PM5020)
			12 - for measurement channel 2 (PM5020)
			dynRange(c_double use with byref) : This parameter defines the maximum dBm reference value. This value is utilized by the dBm output route to determine the dBm level at which the DAC produces its maximum voltage. In conjunction with the dBm dynamic range parameter, it scales the dBm range to the DAC output voltage range.
			channel(c_uint16 use with byref) : This parameter defines the dynamic range of the DAC output in decibels (dB). The dynamic range represents the difference between the maximum and minimum dBm values, which determines how the DAC output voltage range is scaled.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogLogConf(self.devSession, max, dynRange, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getAnalogOutputRoute(self, routeName, channel):
		"""
		This function queries the analog output strategy of the light sensor related anlog output channel. The Powermeter can output different signals on this channel. For PM5020 the <Channel> is 11 or 12. For all other Powermeters the <Channel> is 2. 
		
		Remarks:
		(1) Available only on powermeters equipped with a generated light power or energy analog output
		(2) Not all Powermeter support all kind of output strategies
		(3) The function is available when Powermeter has at least one generated analog output signal.
		
		Args:
			routeName(create_string_buffer(1024) use with byref) : PURe (Direct Route):           The raw amplified signal is output. This signal is related to the photo current or voltage and is not wavelength or zero compensated.
			CBA (Compensated Base Unit):   The raw amplified signal is multiplied with a correction factor in hardware to compensate the dark current/voltage. The signal is the photo current or voltage and is not wavelength compensated.
			CMA (Compensated Main Unit):   The raw amplified signal is multiplied with a correction factor in hardware to output a analogue voltage related to power or energy. The signal is zero and wavelength compensated.
			GENer (Generated Main Unit):   A DAC outputs the most recently measured main unit in Watts (W) or Joules (J).
			GDBM (Generated dBm):          A DAC outputs the most recently measured logarithmic power in (dBm)
			FUNCtion (Function generator): A DAC acts as analog function generator.
			CUSTom (Custom usage):         A DAC output a customer defined voltage.
			channel(c_uint16) :  2  - for a single channel powermeters
			11 - for measurement channel 1 (PM5020)
			12 - for measurement channel 2 (PM5020)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getAnalogOutputRoute(self.devSession, routeName, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setAnalogOutputRoute(self, routeStrategy, channel):
		"""
		This function selects the analog output strategy of the light sensor related anlog output channel. The Powermeter can output different signals on this channel. For PM5020 the <Channel> is 11 or 12. For all other Powermeters the <Channel> is 2. 
		
		PM100D2,PM100D3
		- Pure Analog, Generated Main Unit, Function Generator, Custom usage
		PM5020
		- Pure Analog, Compensated Analog Base, Compensated Analog Main
		
		Remarks:
		(1) Available only on powermeters equipped with a generated light power or energy analog output
		(2) Not all Powermeter support all kind of output strategies.
		(3) The function is available when Powermeter has at least one generated analog output signal.
		(4) Depending on selected output strategy you have to call one ore multiple other functions to use the mode.
		
		Args:
			routeStrategy(c_uint16) : TLPM_ANALOG_ROUTE_PUR  (0)  (Direct Route): The raw amplified signal is output. This signal is related to the photo current or voltage. It is not wavelength or zero compensated.
			TLPM_ANALOG_ROUTE_CBA  (1)  (Compensated Base Unit): The raw amplified signal is multiplied with a correction factor in hardware to compensate the dark current/voltage. The signal is the photo current or voltage and is not wavelength compensated.
			TLPM_ANALOG_ROUTE_CMA  (2) (Compensated Main Unit): The raw amplified signal is multiplied with a correction factor in hardware to output a analogue voltage related to power or energy. The signal is zero and wavelength compensated.
			TLPM_ANALOG_ROUT_GEN   (3) (Generated Main Unit) A DAC outputs the most recently measured main unit in Watts (W) or Joules (J)
			TLPM_ANALOG_ROUTE_FUNC (4) (Function generator) A DAC outputs a previously defined function out of a lookup table like a function generator
			TLPM_ANALOG_ROUTE_CUST (5) (Custom usage) A DAC outputs a customer defined voltage
			TLPM_ANALOG_ROUTE_GDBM (6) (Generated dBm) A DAC outputs the most recently measured power in dBm (dBm)
			channel(c_uint16) :  2  - for a single channel powermeters
			11 - for measurement channel 1 (PM5020)
			12 - for measurement channel 2 (PM5020)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputRoute(self.devSession, routeStrategy, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPositionAnalogOutputSlopeRange(self, minSlope, maxSlope, channel):
		"""
		Returns value range of the slope prameter for given beam position analog output channel. The unit is [V/µm]. For closer details refer to :func:`setPositionAnalogOutputSlope`. 
		To query the voltage range of the selcted analog output channel call :func:`getPositionAnalogOutputVoltageRange`. 
		To query the slope range for the analog light output call :func:`getAnalogOutputSlopeRange`.
		
		Remarks:
		(1) Available only on powermeters equipped with beam position analog outputs for the X and Y coordinates.
		
		Args:
			minSlope(c_double use with byref) : This parameter returns the minimum slope in [V/µm] of the analog output.
			
			maxSlope(c_double use with byref) : This parameter returns the maximum slope in [V/µm] of the analog output.
			
			channel(c_uint16) : 2 - Reserved
			3 - Beam X position output on measurement channel 1: [V/µm]
			4 - Beam Y position output on measurement channel 1: [V/µm]
			5 - Reserved
			6 - Reserved
			7 - Beam X position output on measurement channel 2: [V/µm]
			8 - Beam Y position output on measurement channel 2: [V/µm]
			9 - Reserved
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputSlopeRange(self.devSession, minSlope, maxSlope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPositionAnalogOutputSlope(self, slope, channel):
		"""
		This function sets the slope parameter for the specified position output analog output channel. The powermeter computes the DAC output voltage as follows: DAC_V = Position *  slope. The unit of the slope is V/µm.
		To determine an appropriate slope value, first call :func:`getPositionAnalogOutputVoltageRange` to retrieve the voltage range for the selected channel, or consult the product manual for details. To set the slope for the light signal analog output call :func:`setAnalogOutputSlope`.
		You can use :func:`getPositionAnalogOutputVoltage` to query the actual applied DAC output voltage, for example, to verify or test the slope setting. The slope value is stored persistently and will be automatically applied after a powermeter reboot. 
		      
		The following example illustrates how to select a suitable slope for a given application: Assume the maximum output voltage of the selected channel is 2 V and the expected maximal position to be measured is 25 µm. The ratio of maximum voltage to expectedpower is 2 V / 25 µm = 0.08. To generate an output voltage of 1.25 V at  25 µm, a slope of 0.05 can be selected. Alternatively, a slope of 0.01 could be chosen to generate 0.25V at 25 µm.
		
		Remarks:
		(1) Available only on powermeters equipped with beam position analog outputs for the X and Y coordinates.
		(3) DAC is updated at max 1 kHz.
		(4) The voltage will clip to the analog output physical voltage limits.
		
		Args:
			slope(c_double) : This parameter specifies the responsivity in volts per µm [V/µm]
			channel(c_uint16) : 2 - Reserved
			3 - Beam X position output on measurement channel 1: [V/µm]
			4 - Beam Y position output on measurement channel 1: [V/µm]
			5 - Reserved
			6 - Reserved
			7 - Beam X position output on measurement channel 2: [V/µm]
			8 - Beam Y position output on measurement channel 2: [V/µm]
			9 - Reserved
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPositionAnalogOutputSlope(self.devSession, slope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPositionAnalogOutputSlope(self, attribute, slope, channel):
		"""
		Returns the analog output slope parameter for given beam position analog channel. The powermeter calculates DAC_V = Position * slope. The unit of the slope is [V/µm]. For closer details refer to  :func:`setPositionAnalogOutputSlope`. 
		To query the currenlty output voltage call :func:`getPositionAnalogOutputVoltage`. 
		To query the analog light signal related slope call :func:`getAnalogOutputSlope`. 
		
		Remarks:
		(1) Allowed when Powermeter has at least one generated analog output signalGet Position Analog Output Voltage
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			slope(c_double use with byref) : This parameter returns the specified responsivity in volts per µm [V/µm]
			
			channel(c_uint16) : 2 - Reserved
			3 - Beam X position output on measurement channel 1: [V/µm]
			4 - Beam Y position output on measurement channel 1: [V/µm]
			5 - Reserved
			6 - Reserved
			7 - Beam X position output on measurement channel 2: [V/µm]
			8 - Beam Y position output on measurement channel 2: [V/µm]
			9 - Reserved
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputSlope(self.devSession, attribute, slope, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPositionAnalogOutputVoltageRange(self, minVoltage, maxVoltage, channel):
		"""
		Returns the analog output voltage [V] range (min and max) for given beam position channel. This is especially useful to calculate and later set the channel slope by calling :func:`setPositionAnalogOutputSlope`. To query the actually output voltage call :func:`getPositionAnalogOutputVoltage`. To query the light power or energy analog output voltage range call :func:`getAnalogOutputVoltageRange`. 
		On the PM5020 you can configure the voltage range by calling <Set Analog Output Gain Range>.
		
		Remarks:
		(1) Available only on powermeters equipped with beam position analog outputs for the X and Y coordinates.
		
		Args:
			minVoltage(c_double use with byref) : This parameter returns the minimum voltage in Volt [V] of the analog output. Lower voltage is clipped to the minimum.
			maxVoltage(c_double use with byref) : This parameter returns the maximum voltage in Volt [V] of the analog output. Higher voltage values are clipped to the maximum.
			
			channel(c_uint16) : 2 - Reserved
			3 - Beam X position output on measurement channel 1: [V/µm]
			4 - Beam Y position output on measurement channel 1: [V/µm]
			5 - Reserved
			6 - Reserved
			7 - Beam X position output on measurement channel 2: [V/µm]
			8 - Beam Y position output on measurement channel 2: [V/µm]
			9 - Reserved
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputVoltageRange(self.devSession, minVoltage, maxVoltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPositionAnalogOutputVoltage(self, attribute, voltageX, voltageY, channel):
		"""
		Returns the recent output voltage in volts [V] for the specified beam position analog output channel. The powermeter computes the DAC output voltage as follows: DAC_V = position *  slope. Call :func:`setPositionAnalogOutputSlope` to modify the slope parameter. 
		To query the recent output voltage for the light power or energy analog output call :func:`getAnalogOutputVoltage`.
		
		Remarks:
		(1) Available only on powermeters equipped with beam position analog outputs for the X and Y coordinates.
		(2) DAC depends on measurement mode is updated at max 1 kHz. Reading voltage faster results in duplicate readings.
		(3) The voltage will clip to the analog output physical voltage limits.
		
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

	def getPassFailState(self, state, channel):
		"""
		This function checks if the current sensor signal remains within a previously defined window. To modify the window, use the function :func:`setPassFailPowerWindow` for power or :func:`setPassFailEnergyWindow` for energy sensors. 
		Additionally, you can link an DIO pin to indicate this status using the function :func:`setDigIoPinMode`. 
		The state is also monitored in the Auxiliary register, specifically in bit 10 of <Read register>.
		
		Remarks:
		(1) Using the DIO pin is optional
		(2) Available only on powermeters equipped with Pass/Fail support
		
		Args:
			state(c_int16 use with byref) : True(1) if signals is within the defined window. False(0) otherwise.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPassFailState(self.devSession, state, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPassFailPowerWindow(self, minPower, maxPower, channel):
		"""
		This function queries the photodiode or thermopile sensor  power value window within which the measured sensor power readings are considered valid. The Powermeter employs a 5 % hysteresis if the window has been exited, allowing it to indicate valid status again. For closer details refer to function :func:`setPassFailPowerWindow`.
		
		Remarks:
		(1) Using the DIO pin is optional.
		(2) This only applies to thermopile or photodiode sensors.
		(2) Available only on powermeters equipped with Pass/Fail support.
		
		Args:
			minPower(c_double use with byref) : This parameter returns the pass/fail window lower limit in Watt [W]. Power readings below this value are defined as invalid.
			maxPower(c_double use with byref) : This parameter returns the pass/fail window upper limit in Watt [W]. Power readings above this value are defined as invalid.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPassFailPowerWindow(self.devSession, minPower, maxPower, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPassFailPowerWindow(self, minPower, maxPower, channel):
		"""
		This function establishes the photodiode or thermopile sensor power value window within which the measured sensor power readings are considered valid. The Powermeter employs a 5 % hysteresis if the window has been exited, allowing it to indicate valid status again. 
		Additionally, you can link an DIO pin to indicate this status using the function :func:`setDigIoPinMode`. 
		The state is also monitored in the Auxiliary register, specifically in bit 10 of <Read register>.
		
		Remarks:
		(1) Using the DIO pin is optional.
		(2) This only applies to thermopile or photodiode sensors.
		(2) Available only on powermeters equipped with Pass/Fail support.
		
		Args:
			minPower(c_double) : This parameter returns the pass/fail window lower limit in Watt [W]. Power readings below this value are defined as invalid.
			maxPower(c_double) : This parameter returns the pass/fail window upper limit in Watt [W]. Power readings above this value are defined as invalid.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPassFailPowerWindow(self.devSession, minPower, maxPower, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPassFailEnergyWindow(self, minEnergy, maxEnergy, channel):
		"""
		This function queries the pyroelectric sensor energy value window within which the measured sensor power readings are considered valid. The Powermeter employs a 5 % hysteresis if the window has been exited, allowing it to indicate valid status again. For closer details refer to function
		:func:`setPassFailEnergyWindow`.
		
		Remarks:
		(1) Using the DIO pin is optional.
		(2) This only applies to pyroelectric sensors.
		(2) Available only on powermeters equipped with Pass/Fail support.
		
		Args:
			minEnergy(c_double use with byref) : This parameter returns the pass/fail window lower limit in Joules [J]. Energy readings below this value are defined as invalid.
			maxEnergy(c_double use with byref) : This parameter returns the pass/fail window upper limit in Joules [J]. Energy readings above this value are defined as invalid.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getPassFailEnergyWindow(self.devSession, minEnergy, maxEnergy, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPassFailEnergyWindow(self, minEnergy, maxEnergy, channel):
		"""
		This function establishes the Pyro sensor energy value window within which the measured sensor power readings are considered valid. The Powermeter employs a 5 % hysteresis if the window has been exited, allowing it to indicate valid status again. 
		Additionally, you can link an DIO pin to indicate this status using the function :func:`setDigIoPinMode`. 
		The state is also monitored in the Auxiliary register, specifically in bit 10 of <Read register>.
		
		Remarks:
		(1) Using the DIO pin is optional.
		(2) This only applies to pyroelectric sensors.
		(2) Available only on powermeters equipped with Pass/Fail support.
		
		Args:
			minEnergy(c_double) : This parameter sets the pass/fail window lower limit in Joules [J]. Energy readings below this value are defined as invalid.
			maxEnergy(c_double) : This parameter sets the pass/fail window upper limit in Joules [J]. Energy readings above this value are defined as invalid.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setPassFailEnergyWindow(self.devSession, minEnergy, maxEnergy, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measCurrent(self, current, channel):
		"""
		This function measure the average current in ampere [A] for Photodiode sensors. The powermeter will start a new measurement and return the result once enough data has been averaged. The maximum frequency for command depends on the Powermeter but will be limited at 1 kHz (with averaging set to 1), and all measurement results within a 1-millisecond window are averaged. The result of this function may be either absolute or relative, depending on the delta mode offset and its enabled state. For more information, refer to the :func:`setCurrentRef` and :func:`setCurrentRefState` functions. By default, delta mode is disabled. You can also check the Questionable Status register :func:`readRegister` to confirm the validity of the measurement results and ensure they are not infinite.
		In CW measurement mode, the averaging process can be adjusted using the :func:`setAvgTime` function. You can either set the range manually using :func:`setCurrentRange` or enable auto-ranging with :func:`setCurrentAutoRange`.
		For Photodiode in peak-mode (see :func:`setFreqMode`), averaging is not applied in this sensor measurement mode. The Powermeter utilizes an internal threshold for peak detection. You can manually set the threshold level using :func:`setPeakThreshold` or enable autoranging with :func:`setCurrentAutoRange` for repetitive pulsed input signals with a repetition rate greater than 5 Hz. For such repetitive input signals, you can also use the peak-finder background operation :func:`startPeakDetector` to automatically set the range and threshold parameters once. The peak-finder is a one-time autoranging operation. 
		For non-repetitive pulse signals (such as single pulse measurements or low repetition rates), you will need to manually select the range and threshold.
		Certain powermeters support fast data acquisition. To access this functionality, refer to the following functions: :func:`confCurrentMeasurementSequence`, :func:`confCurrentFastArrayMeasurement`, or :func:`startBurstArrayMeasurement`.
		
		Remarks:
		(1) Photodiode sensors only. Be careful when measuring single pulse events. Read details carefully.
		(2) Maximum call frequency depends on the connected Powermeter but is limited at 1 kHz
		(3) Scope and Burst measurements are not supported for Photodiode peak-mode measurements. 
		(4) For PM5020 you might want to measure current for both channels simultaniously by calling :func:`measDualChannelSimultaneous`
		
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
		This function measures the average voltage in volts [V]  for Pyro, Thermopile, or 4-Quadrant Thermopile sensors. The powermeter will start a new measurement and return the result once enough data has been averaged. The maximum frequency for command depends on the Powermeter but will be limited at 1 kHz (with averaging set to 1), and all measurement results within a 1-millisecond window are averaged. The result of this function may be either absolute or relative, depending on the delta mode offset and its enabled state. For more information, refer to the :func:`setVoltageRef` and :func:`setVoltageRefState` functions. By default, delta mode is disabled. You can also check the Questionable Status register :func:`readRegister` to confirm the validity of the measurement results and ensure they are not infinite.
		In CW measurement mode, the averaging process can be adjusted using the :func:`setAvgTime` function. You can either set the range manually using :func:`setVoltageRange` or enable autoranging with :func:`setVoltageAutoRange`.
		For Pyro measurements, averaging is not applied in this sensor measurement mode. The Powermeter utilizes an internal threshold for peak detection. You can manually set the threshold level using:func:`setPeakThreshold` or enable autoranging with :func:`setVoltageAutoRange` for repetitive pulsed input signals with a repetition rate greater than 5 Hz. For such repetitive input signals, you can also use the peak-finder background operation :func:`startPeakDetector` to automatically set the range and threshold parameters once. The peak-finder is a one-time autoranging operation. 
		For non-repetitive pulse signals (such as single pulse measurements or low repetition rates), you will need to manually select the range and threshold.
		Certain powermeters support fast data acquisition for Thermopile sensors. To access this functionality, refer to the following functions: :func:`confVoltageMeasurementSequence`, :func:`confVoltageFastArrayMeasurement`, or :func:`startBurstArrayMeasurement`.
		
		Remarks:
		(1) Pyroelectric, Thermopile and 4-Quadrant Thermopile only. Be careful when measuring single pulse events. Read details carefully.
		(2) Maximum call frequency depends on the connected Powermeter but is limited at 1 kHz
		(3) Scope and Burst measurements are not supported for Pyroelectric sensor energy measurements. 
		(4) For the PM5020, you can measure voltage on both channels simultaneously by calling :func:`measDualChannelSimultaneous`.
		
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
		This function measures the average power in watts [W] for Photodiode, Thermopile, or 4-Quadrant Thermopile sensors.  The powermeter will start a new measurement and return the result once enough data has been averaged. The maximum frequency for command depends on the Powermeter but will be limited at 1 kHz (with averaging set to 1), and all measurement results within a 1-millisecond window are averaged. The result of this command may be either absolute or relative, depending on the delta mode offset and its enabled state. For more information, refer to the :func:`setPowerRef` and :func:`setPowerRefState` functions. By default, delta mode is disabled. You can also check the Questionable Status register :func:`readRegister` to confirm the validity of the measurement results and ensure they are not infinite.
		In CW measurement mode, the averaging process can be adjusted using the :func:`setAvgTime` function.  You can either set the range manually using :func:`setPowerRange` or enable auto-ranging with :func:`setPowerAutoRange`.
		For Photodiode in peak-mode (see :func:`setFreqMode`), averaging is not applied in this sensor measurement mode. The Powermeter utilizes an internal threshold for peak detection. You can manually set the threshold level using  :func:`setPeakThreshold` or enable autoranging with :func:`setPowerAutoRange` for repetitive pulsed input signals with a repetition rate greater than 5 Hz. For such repetitive input signals, you can also use the peak-finder background operation :func:`startPeakDetector` to automatically set the range and threshold parameters once. The peak-finder is a one-time autoranging operation.
		For non-repetitive pulse signals (such as single pulse measurements or low repetition rates), you will need to manually select the range and threshold.
		Certain powermeters support fast data acquisition. To access this functionality, refer to the following functions: :func:`confPowerMeasurementSequence`, :func:`confPowerFastArrayMeasurement`, or :func:`startBurstArrayMeasurement`.
		
		Remarks:
		(1) Photodiode Thermopile and 4-Quadrant Thermopile only. Be careful when measuring single pulse events. Read details carefully.
		(2) Maximum call frequency depends on the connected Powermeter but is limited at 1 kHz
		(3) Scope and Burst measurements are not supported for Photodiode peak-mode  measurements. 
		(4) For the PM5020, you can measure power on both channels simultaneously by calling :func:`measDualChannelSimultaneous`.
		
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
		This function measures the average energy in joules [J] for Pyro sensors. The powermeter will start a new measurement and return when the next peak has been deteced.The maximum frequency for command depends on the Powermeter but will be limited at 1 kHz. All peaks within a 1-millisecond window are averaged.
		The result of this function may be either absolute or relative, depending on the delta mode offset and its enabled state. For more information, refer to the :func:`setEnergyRef` and :func:`setEnergyRefState` functions. By default, delta mode is disabled. You can also check the Questionable Status register :func:`readRegister` to confirm the validity of the measurement results and ensure they are not infinite.
		For Pyro measurements, averaging is not applied in this sensor measurement mode. The Powermeter utilizes an internal threshold for peak detection. You can manually set the threshold level using :func:`setPeakThreshold` or enable autoranging with :func:`setEnergyAutoRange` for repetitive pulsed input signals with a repetition rate greater than 5 Hz. For such repetitive input signals, you can also use the peak-finder background operation :func:`startPeakDetector` to automatically set the range and threshold parameters once. The peak-finder is a one-time autoranging operation.
		For non-repetitive pulse signals (such as single pulse measurements or low repetition rates), you will need to manually select the range and threshold.
		Certain powermeters support fast data acquisition. To access this functionality, refer to the following functions: :func:`confEnergyFastArrayMeasurement`.
		
		Remarks:
		(1) Pyroelectric sensor only. Be careful when measuring single pulse events. Read details carefully.
		(2) Maximum call frequency depends on the connected Powermeter but is limited at 1 kHz
		(3) Scope and Burst measurements are not supported for Pyroelectric sensor energy measurements. 
		
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
		This function measures the modulation frequency of the input signal in Hz. The Powermeter updates the frequency reading at intervals of 2 Hz or less, depending on the input frequency. For frequency measurement, the input signal is compared to a threshold level, which can be set using the :func:`setPeakThreshold` command. If the input signal exceeds the threshold, it is detected as high; otherwise, the Powermeter identifies it as low.
		The accuracy of the frequency measurement depends on the input signal frequency. The Powermeter employs edge counting for input signals above approximately 500 Hz and uses period measurement for slower signal frequencies. Edge counting always yields a whole number frequency. If a continuous wave (CW) signal is input, the frequency will be reported as 0.
		
		Notes:
		(1) Check different bandwidth of amplification stages for high frequencies.
		(2) Averaging :func:`setAvgTime` is not applicable for frequency measurements.
		(3) For photodiodes, ensure that you select the high bandwidth limit using :func:`setInputFilterState` for accurate frequency measurements.
		(4) For modulated signals with a low frequency < 1Hz the frequency measurement might be corrupted depending on the signal shape. It is mandatory that the slope on the detection threshold is strighly ascending even with noise floor.
		
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
		This function measures the average power density in watts per square cm [W/cm²] for Photodiode, Thermopile, or 4-Quadrant Thermopile sensors.  The powermeter will start a new measurement and return the result once enough data has been averaged. The maximum frequency for command depends on the Powermeter but will be limited at 1 kHz (with averaging set to 1), and all measurement results within a 1-millisecond window are averaged. To change the density reference beam size, use the :func:`setBeamDia` function.
		The result of this command may be either absolute or relative, depending on the delta mode offset and its enabled state. For more information, refer to the :func:`setPowerRef` and :func:`setPowerRefState` functions. By default, delta mode is disabled. You can also check the Questionable Status register :func:`readRegister` to confirm the validity of the measurement results and ensure they are not infinite.
		In CW measurement mode, the averaging process can be adjusted using the :func:`setAvgTime` function.  You can either set the range manually using :func:`setPowerRange` or enable auto-ranging with :func:`setPowerAutoRange`.
		For Photodiode in peak-mode (see :func:`setFreqMode`), averaging is not applied in this sensor measurement mode. The Powermeter utilizes an internal threshold for peak detection. You can manually set the threshold level using  :func:`setPeakThreshold` or enable autoranging with :func:`setPowerAutoRange` for repetitive pulsed input signals with a repetition rate greater than 5 Hz. For such repetitive input signals, you can also use the peak-finder background operation :func:`startPeakDetector` to automatically set the range and threshold parameters once. The peak-finder is a one-time autoranging operation.
		Certain powermeters support fast data acquisition. To access this functionality, refer to the following functions: :func:`confPDensityFastArrayMeasurement`.
		
		Remarks:
		(1) Photodiode Thermopile and 4-Quadrant Thermopile only. Be careful when measuring single pulse events. Read details carefully.
		(2) Maximum call frequency depends on the connected Powermeter but is limited at 1 kHz
		(3) The Scope, Burst or Fast Measure Stream does not support power density measurements. 
		(4) For the PM5020, you can measure power density on both channels simultaneously by calling :func:`measDualChannelSimultaneous`.
		
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
		This function measures the average energy density in joules per square cm [J/cm²] for Pyro sensors. The powermeter will start a new measurement and return when the next peak has been deteced.The maximum frequency for command depends on the Powermeter but will be limited at 1 kHz. All peaks within a 1-millisecond window are averaged. To change the density reference beam size, use the :func:`setBeamDia` function.
		The result of this function may be either absolute or relative, depending on the delta mode offset and its enabled state. For more information, refer to the :func:`setEnergyRef` and :func:`setEnergyRefState` functions. By default, delta mode is disabled. You can also check the Questionable Status register :func:`readRegister` to confirm the validity of the measurement results and ensure they are not infinite.
		For Pyro measurements, averaging is not applied in this sensor measurement mode. The Powermeter utilizes an internal threshold for peak detection. You can manually set the threshold level using :func:`setPeakThreshold` or enable autoranging with :func:`setEnergyAutoRange` for repetitive pulsed input signals with a repetition rate greater than 5 Hz. For such repetitive input signals, you can also use the peak-finder background operation :func:`startPeakDetector` to automatically set the range and threshold parameters once. The peak-finder is a one-time autoranging operation.
		For non-repetitive pulse signals (such as single pulse measurements or low repetition rates), you will need to manually select the range and threshold.
		Certain powermeters support fast data acquisition. To access this functionality, refer to the following functions: :func:`confEDensityFastArrayMeasurement`.
		
		Remarks:
		(1) Pyroelectric sensor only. Be careful when measuring single pulse events. Read details carefully.
		(2) Maximum call frequency depends on the connected Powermeter but is limited at 1 kHz
		(3) Scope and Burst measurements are not supported for Pyroelectric sensor energy density measurements. 
		
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

	def measDualChannelSimultaneous(self, measurement, resultChannel1, resultChannel2):
		"""
		This function is used to obtain frequency readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			measurement(c_uint16)
			resultChannel1(c_double use with byref) : Measurement result of channel 1. Unit depends on <Unit> parameter. 
			resultChannel2(c_double use with byref) : Measurement result of channel 2. Unit depends on <Unit> parameter. 
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measDualChannelSimultaneous(self.devSession, measurement, resultChannel1, resultChannel2)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measAuxAnalogInput(self, voltage, channel):
		"""
		This function is used to obtain voltage readings from the instrument's auxiliary AD1 and AD2 input. 
		
		Notes:
		(1) The function is only available on PM200, PM400.
		
		
		Args:
			voltage(c_double use with byref) : This parameter returns the voltage in volt [V].
			channel(c_uint16) : 2 for AD1, 3 for AD2
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measAuxAnalogInput(self.devSession, voltage, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def isEmmConnected(self, isConnected):
		"""
		This function checks if an external environemental sensor is connected to the powermeter. A environmental sensor supports measuring temperature and humidity. To read the sensor call :func:`measEmmHumidity` or :func:`measEmmTemperature`.
		
		Args:
			isConnected(c_int16 use with byref) : Flag set to true if external environmental sensor is connected. False otherwise.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_isEmmConnected(self.devSession, isConnected)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measEmmHumidity(self, humidity):
		"""
		This function obtains the most recent measured humidity from the external digital environmental sensor, expressed in percent [%]. The Powermeter updates the humidity reading at a rate of 10 Hz or less. To read the temperature of the sensor call :func:`measEmmTemperature`. Before calling this function you might want to check if environmental sensor is connected by calling :func:`isEmmConnected`. 
		
		Notes:
		(1) Only available on PM400 and on all Powermeters with I²C fieldbus on auxilary connector
		(2) On I²C Texas Instruments HDC1080 and HDC3020 sensors are supported
		(3) Return an error when no digital environment sensor is connected
		(4) Averaging :func:`setAvgTime` does not apply to this measurements. 
		
		Args:
			humidity(c_double use with byref) : This parameter returns the relative humidity in %.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measEmmHumidity(self.devSession, humidity)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measEmmTemperature(self, temperature):
		"""
		This function queries the most recently measured temperature from external digital environmental sensor, reported in degrees Celsius [°C]. The powermeter updates the temperature reading at a rate of 10 Hz or less. For environmental humidity, call :func:`measEmmHumidity`. For sensor head temperature, call :func:`measHeadTemperature`. For external NTC temperature, call :func:`measExtNtcTemperature`. Before calling this function you might want to check if environmental sensor is connected by calling :func:`isEmmConnected`. 
		
		Notes:
		(1) Only available on PM400 and on all Powermeters with I²C fieldbus on auxilary connector
		(2) On I²C Texas Instruments HDC1080 and HDC3020 sensors are supported
		(3) Return an error when no digital environment sensor is connected
		(4) Averaging :func:`setAvgTime` does not apply to this measurements. 
		
		Args:
			temperature(c_double use with byref)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measEmmTemperature(self.devSession, temperature)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def isExtNtcConnected(self, isConnected, channel):
		"""
		This function checks if an external NTC temperature sensor on given channel is connected to the powermeter. To read the sensor call :func:`measExtNtcTemperature` or :func:`measExtNtcResistance`.
		
		Args:
			isConnected(c_int16 use with byref) : Flag set to true if external NTC sensor is connected. False otherwise.
			channel(c_uint16) : Temperature measurement channel. 
			5 for NTC on channel 1 (Default for all devices with single NTC input)
			6 for NTC on channel 2
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_isExtNtcConnected(self.devSession, isConnected, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measExtNtcTemperature(self, temperature, channel):
		"""
		This function queries the recent measured temperature of the external NTC in degree Celsius. The Powermeter updates the NTC temperature below 10 Hz. If you use a special NTC temperature sensor ensure NTC parameters :func:`setExtNtcParameter` are correct. To get the external NTC resistance use :func:`measExtNtcResistance`. Before calling this function you may check if the NTC is connected by calling :func:`isExtNtcConnected`. 
		For sensor head temperature, call :func:`measHeadTemperature`. For digital environmental temperature, call :func:`measEmmTemperature`.
		
		Remarks:
		(1) Available if Powermeter has an 2,5 mm sound jack or NTC pin on the auxilary connector
		(2) Return an error when no NTC sensor is connected
		(3) Averaging :func:`setAvgTime` does not apply to this measurements. 
		
		Args:
			temperature(c_double use with byref) : This parameter returns the temperature in °C
			channel(c_uint16) : 5 for NTC 1 (default)
			6 for NTC 2
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measExtNtcTemperature(self.devSession, temperature, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measExtNtcResistance(self, resistance, channel):
		"""
		This function queries the recent measured resistance of the external NTC in Ohm. The Powermeter updates the NTC resistance below 10 Hz. To get the external NTC temperature use :func:`measExtNtcTemperature`. Before calling this function you may check if the NTC is connected by calling :func:`isExtNtcConnected`. 
		For sensor head NTC resistance, call :func:`measHeadResistance`.
		
		Remarks:
		(1) Available if Powermeter has an 2,5 mm sound jack or NTC pin on the auxilary connector.
		(2) Return an error when no NTC sensor is connected.
		(3) Averaging :func:`setAvgTime` does not apply to this measurements.
		
		Args:
			resistance(c_double use with byref) : This parameter returns the resistance in Ohm
			channel(c_uint16) : 5 for NTC 1 (default)
			6 for NTC 2
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measExtNtcResistance(self.devSession, resistance, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measHeadResistance(self, frequency, channel):
		"""
		The function measures the light sensor head NTC resistance in Ohm. The powermter updates the resistance below 10 Hz. 
		To measure the light sensor temperature instead use :func:`measHeadTemperature`. 
		If you want to measure the external NTC resistance call :func:`measExtNtcResistance`. 
		
		Remarks:
		(1) Not all light sensor heads support head resistance measurements. Call :func:`getSensorInfoExt` and check the flags.
		(2) Averaging :func:`setAvgTime` does not apply to this measurements. 
		
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
		The function measures the light sensor head emperature in °C. The powermter updates the temperature below 10 Hz. 
		To measure the light sensor NTC resistance use :func:`measHeadResistance`. 
		If you want to measure the external NTC temperature call :func:`measExtNtcTemperature`. If you want to measure the external digital environemental sensor temperature call :func:`measEmmTemperature`.
		
		Remarks:
		(1) Not all light sensor heads support head temperature measurements. Call :func:`getSensorInfoExt` and check the flags.
		(2) Averaging :func:`setAvgTime` does not apply to this measurements. 
		
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
		This function measures the average beam position coordinate on the sensor in um for 4-Quadrant Thermopile sensors. The powermeter will start a new measurement and return the result once enough data has been averaged. The maximum frequency for command calls is 1 kHz (with averaging set to 1), and all measurement results within a 1-millisecond window are averaged.
		The result of this function may be either absolute or relative, depending on the beam zero position :func:`startZeroPos`.
		The averaging process can be adjusted using the :func:`setAvgTime` function. You can either set the range manually using :func:`setVoltageRange`  or enable autoranging with :func:`setVoltageAutoRange`.
		
		Remarks:
		(1) 4-Quadrant Thermopile only.
		(2) Maximum call frequency depends on the connected Powermeter but is limited at 1 kHz
		(3) Scope and Burst measurements are not supported for beam position measurements.
		
		Args:
			xPosition(c_double use with byref) : This parameter returns the actual measured x position in µm
			yPosition(c_double use with byref) : This parameter returns the actual measured y position in µm
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_meas4QPositions(self.devSession, xPosition, yPosition, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def meas4QVoltages(self, voltage1, voltage2, voltage3, voltage4, channel):
		"""
		This command measures the single quadrant voltages of 4-quadrant thermopile sensors in volts [V]. All measreuemnts are quadrupels. The powermeter will start a new measurement and return the result once sufficient data has been averaged. The maximum frequency for this measurement is 1 kHz (with averaging set to 1). You can adjust the averaging settings using the :func:`setAvgTime` function.
		
		Remarks:
		(1) 4-Quadrant Thermopile only.
		(2) Maximum call frequency depends on the connected Powermeter but is limited at 1 kHz
		(3) Scope and Burst measurements are not supported for 4-Quadrant Voltage measurements.
		
		Args:
			voltage1(c_double use with byref) : This parameter returns the actual measured voltage of the upper right sector of a 4-Quadrant Thermopile sensor.
			voltage2(c_double use with byref) : This parameter returns the actual measured voltage of the upper left sector of a 4-Quadrant Thermopile sensor.
			voltage3(c_double use with byref) : This parameter returns the actual measured voltage of the lower right sector of a 4-Quadrant Thermopile sensor.
			voltage4(c_double use with byref) : This parameter returns the actual measured voltage of the lower left sector of a 4-Quadrant Thermopile sensor.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_meas4QVoltages(self.devSession, voltage1, voltage2, voltage3, voltage4, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measNegPulseWidth(self, negativePulseWidth, channel):
		"""
		This command measures the negative or low pulse-width in seconds [s] for a photodiode sensor operating in peak-mode. Refer to :func:`setFreqMode`for more details. The low and high levels are determined by the peak detection threshold, which can be set using :func:`setPeakThreshold`. When the analog signal from the sensor exceeds the threshold, the time measurement begins and continues until the signal drops below the threshold again. To measure the low time of the pulse, you can use :func:`measNegPulseWidth`. For measurements of the relative positive duty-cycle, call :func:`measNegDutyCycle`.
		
		Remarks:
		(1) Only for Photodiode sensors in peak measurement mode. Not available for Pyro sensors.
		(2) Measurement is applicable only for rectangular input signals.
		
		Args:
			negativePulseWidth(c_double use with byref) : Negative pulse-width in Seconds [s].
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
		This command measures the positive or high pulse-width in seconds [s] for a photodiode sensor operating in peak-mode. Refer to :func:`setFreqMode`for more details. The low and high levels are determined by the peak detection threshold, which can be set using :func:`setPeakThreshold`. When the analog signal from the sensor drops below the threshold, the time measurement begins and continues until the  signal rises back to the threshold. To measure the low time of the pulse, you can use :func:`measNegPulseWidth`. For measurements of the relative positive duty-cycle, call :func:`measPosDutyCycle`.
		
		Remarks:
		(1) Only for Photodiode sensors in peak measurement mode. Not available for Pyro sensors.
		(2) Measurement is applicable only for rectangular input signals.
		
		Args:
			positivePulseWidth(c_double use with byref) : Positive pulse-width in Seconds [s].
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
		This fucntion measures the negative pulse duty-cycle in percent [%] for a photodiode sensor operating in peak-mode. Refer to :func:`setFreqMode`for more details. The negative duty-cycle represents the ratio of the pulse low time to the total pulse period. The low and high levels are determined by the peak detection threshold, which can be set using :func:`setPeakThreshold`. To measure the absolute negative pulse time, use :func:`measNegPulseWidth`. 
		
		Remarks:
		(1) Only for Photodiode sensors in peak measurement mode. Not available for Pyro sensors.
		(2) Measurement is applicable only for rectangular input signals.
		(3) Measuring the duty-cycle is not supported for single pulse measurements.
		
		Args:
			negativeDutyCycle(c_double use with byref) : Negative Duty Cycle in percentage [%]. Value betweeen 0 and 100.
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
		This fucntion measures the positive pulse duty-cycle in percent [%] for a photodiode sensor operating in peak-mode. Refer to :func:`setFreqMode`for more details. The positive duty-cycle represents the ratio of the pulse high time to the total pulse period. The low and high levels are determined by the peak detection threshold, which can be set using :func:`setPeakThreshold`. To measure the absolute positive pulse time, use :func:`measPosPulseWidth`. 
		
		Remarks:
		(1) Only for Photodiode sensors in peak measurement mode. Not available for Pyro sensors.
		(2) Measurement is applicable only for rectangular input signals.
		(3) Measuring the duty-cycle is not supported for single pulse measurements.
		
		Args:
			positiveDutyCycle(c_double use with byref) : Positive Duty Cycle in percentage [%]. Value betweeen 0 and 100.
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
		This function initiates a software-triggered oscilloscope (scope) like power measurement in watts [W] and wait for its completion, for continuous wave (CW) measurement mode. Upon receiving the command, the powermeter begins rapid data acquisition and accumulates samples in an internal device buffer until it reaches capacity. The sampling rate and buffer size vary by device but are guaranteed to be at least 10,000 samples per second and 10,000 elements, respectively. When the buffer is full, the measurement halts, and the stored data can then be retrieved at any desired speed or in any order. The function will block the remote interface until the buffer is completely filled.
		The captured data remains valid until a subsequent scope or burst measurement is initiated. During the active measurement phase, the device cannot be retriggered. To access the measurement data, invoke the :func:`getMeasurementSequence` command multiple times, specifying different offsets each time.
		This function serves as a convenient shortcut for the typical workflow, which involves calling :func:`confPowerMeasurementSequence`, followed by :func:`startMeasurementSequence`, and then the final :func:`getMeasurementSequence` to wait for completion.
		
		Remarks:
		(1) Scope mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM102
		(2) Supported for photodiode, thermopile and 4-Quadrant Thermopile sensors in CW measurement mode.
		(3) Do NOT use this function for long lasting scope measurements for more than 3 seconds capture time to prevent read timeouts.
		(4) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Relative samples are not supported in scope mode e.g. :func:`setPowerRef`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(8) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(9) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed. 
			For PM400 and PM101 time in us between the samples. Needs to be >= 100.
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
		This function initiates a hardware-triggered oscilloscope (scope) like power measurement in watts [W] and waits for its completion, specifically for continuous wave (CW) measurement mode. Upon sending the command, the hardware trigger is armed. On the next rising edge of the trigger signal, the powermeter begins high-speed data acquisition, accumulating samples in an internal device buffer until it reaches full capacity. The sampling rate and buffer size are device-dependent but guaranteed to be at least 10,000 samples per second and 10,000 elements, respectively. Once the buffer is full, the measurement stops, and the stored data can be retrieved at any desired speed or in any order. The function blocks the remote interface until the buffer is completely filled.
		The captured data remains valid until a subsequent scope or burst measurement is started. Retriggering is not possible during the active measurement phase. When the buffer is entirely filled, the trigger is disarmed. To retrieve the measurement data, invoke the :func:`getMeasurementSequence` command multiple times, specifying different offsets each time.
		This function provides a convenient shortcut for the standard workflow, combining :func:`confPowerMeasurementSequenceHWTrigger`, :func:`startMeasurementSequence`, and the final :func:`getMeasurementSequence` call to ensure completion before proceeding.
		
		PM103/PM103E: For external trigger on digial IO1 pin. Use :func:`setDigIoPinMode` function to configure pin. This is not required for the other Powermeters.
		
		Remarks:
		(1) Hardware-triggered scop mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM400, PM101, PM102
		(2) Not all hardware trigger sources are available for on every powermeter.
		(3) Supported for photodiode, thermopile and 4-Quadrant Thermopile sensors in CW measurement mode.
		(4) Do NOT use this function for long lasting scope measurements for more than 3 seconds capture time to prevent read timeouts.
		(5) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(6) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(7) Relative samples are not supported in scope mode e.g. :func:`setPowerRef`.
		(8) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(9) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(10) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed. 
			For PM400 and PM101 time in us between the samples. Needs to be >= 100.
			hPos(c_uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(c_uint16) : external trigger source.
			PM5020: 1(default) signal of channel 1, 2 signal of channel 2, 3 signal of front AUX, 4 signal of rear trigger.
			PM100D3: 1(default) signal of channel 1, 2 for DIO1
			PM6x: 1(default) signal of channel 1, 2 for DIO1
			PM103/PM103E: 1(default)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measPowerMeasurementSequenceHWTrigger(self.devSession, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measureCurrentMeasurementSequence(self, baseTime, channel):
		"""
		This function initiates a software-triggered oscilloscope (scope) like current measurement in amperes [A] and wait for its completion, for continuous wave (CW) measurement mode. Upon receiving the command, the powermeter begins rapid data acquisition and accumulates samples in an internal device buffer until it reaches capacity. The sampling rate and buffer size vary by device but are guaranteed to be at least 10,000 samples per second and 10,000 elements, respectively. When the buffer is full, the measurement halts, and the stored data can then be retrieved at any desired speed or in any order. The function will block the remote interface until the buffer is completely filled.
		The captured data remains valid until a subsequent scope or burst measurement is initiated. During the active measurement phase, the device cannot be retriggered. To access the measurement data, invoke the :func:`getMeasurementSequence` command multiple times, specifying different offsets each time.
		This function serves as a convenient shortcut for the typical workflow, which involves calling :func:`confCurrentMeasurementSequence`, followed by :func:`startMeasurementSequence`, and then the final :func:`getMeasurementSequence` to wait for completion.
		
		Remarks:
		(1) Scope mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM102
		(2) Supported for photodiode sensors in CW measurement mode.
		(3) Do NOT use this function for long lasting scope measurements for more than 3 seconds capture time to prevent read timeouts.
		(4) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Relative samples are not supported in scope mode e.g. :func:`setCurrentRef`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setCurrentAutoRange`.
		(8) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(9) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed. 
			For PM400 and PM101 time in us between the samples. Needs to be >= 100.
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
		This function initiates a hardware-triggered oscilloscope (scope) like current measurement in amperes [A] and waits for its completion, specifically for continuous wave (CW) signals. Upon sending the command, the hardware trigger is armed. On the next rising edge of the trigger signal, the powermeter begins high-speed data acquisition, accumulating samples in an internal device buffer until it reaches full capacity. The sampling rate and buffer size are device-dependent but guaranteed to be at least 10,000 samples per second and 10,000 elements, respectively. Once the buffer is full, the measurement stops, and the stored data can be retrieved at any desired speed or in any order. The function blocks the remote interface until the buffer is completely filled.
		The captured data remains valid until a subsequent scope or burst measurement is started. Retriggering is not possible during the active measurement phase. When the buffer is entirely filled, the trigger is disarmed. To retrieve the measurement data, invoke the :func:`getMeasurementSequence` command multiple times, specifying different offsets each time.
		This function provides a convenient shortcut for the standard workflow, combining :func:`confCurrentMeasurementSequenceHWTrigger`, :func:`startMeasurementSequence`, and the final :func:`getMeasurementSequence` call to ensure completion before proceeding.
		
		PM103/PM103E: For external trigger on digial IO1 pin. Use :func:`setDigIoPinMode` function to configure pin. This is not required for the other Powermeters.
		
		Remarks:
		(1) Hardware-triggered scop mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM400, PM101, PM102
		(2) Not all hardware trigger sources are available for on every powermeter.
		(3) Supported for photodiode sensors in CW measurement mode.
		(4) Do NOT use this function for long lasting scope measurements for more than 3 seconds capture time to prevent read timeouts.
		(5) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(6) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(7) Relative samples are not supported in scope mode e.g. :func:`setCurrentRef`.
		(8) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setCurrentAutoRange`.
		(9) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(10) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed. 
			For PM400 and PM101 time in us between the samples. Needs to be >= 100.
			hPos(c_uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(c_uint16) : external trigger source.
			PM5020: 1(default) signal of channel 1, 2 signal of channel 2, 3 signal of front AUX, 4 signal of rear trigger.
			PM100D3: 1(default) signal of channel 1, 2 for DIO1
			PM6x: 1(default) signal of channel 1, 2 for DIO1
			PM103/PM103E: 1(default)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measureCurrentMeasurementSequenceHWTrigger(self.devSession, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measureVoltageMeasurementSequence(self, baseTime, channel):
		"""
		This function initiates a software-triggered oscilloscope (scope) like voltage measurement in volts [V] and wait for its completion, for continuous wave (CW) measurement mode. Upon receiving the command, the powermeter begins rapid data acquisition and accumulates samples in an internal device buffer until it reaches capacity. The sampling rate and buffer size vary by device but are guaranteed to be at least 10,000 samples per second and 10,000 elements, respectively. When the buffer is full, the measurement halts, and the stored data can then be retrieved at any desired speed or in any order. The function will block the remote interface until the buffer is completely filled.
		The captured data remains valid until a subsequent scope or burst measurement is initiated. During the active measurement phase, the device cannot be retriggered. To access the measurement data, invoke the :func:`getMeasurementSequence` command multiple times, specifying different offsets each time.
		This function serves as a convenient shortcut for the typical workflow, which involves calling :func:`confVoltageMeasurementSequence`, followed by :func:`startMeasurementSequence`, and then the final :func:`getMeasurementSequence` to wait for completion.
		
		Remarks:
		(1) Scope mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM400, PM101, PM102
		(2) Supported for thermopile and 4-quadrant thermopile sensors.
		(3) Do NOT use this function for long lasting scope measurements for more than 3 seconds capture time to prevent read timeouts.
		(4) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(5) Disable the Thermopile accelerator :func:`setAccelState`.
		(6) Relative samples are not supported in scope mode e.g. :func:`setVoltageRef`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setVoltageAutoRange`.
		(8) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed. 
			For PM400 and PM101 time in us between the samples. Needs to be >= 100.
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
		This function initiates a hardware-triggered oscilloscope (scope) like voltage measurement in volts [V] and waits for its completion, specifically for continuous wave (CW) measurement mode. Upon sending the command, the hardware trigger is armed. On the next rising edge of the trigger signal, the powermeter begins high-speed data acquisition, accumulating samples in an internal device buffer until it reaches full capacity. The sampling rate and buffer size are device-dependent but guaranteed to be at least 10,000 samples per second and 10,000 elements, respectively. Once the buffer is full, the measurement stops, and the stored data can be retrieved at any desired speed or in any order. The function blocks the remote interface until the buffer is completely filled.
		The captured data remains valid until a subsequent scope or burst measurement is started. Retriggering is not possible during the active measurement phase. When the buffer is entirely filled, the trigger is disarmed. To retrieve the measurement data, invoke the :func:`getMeasurementSequence` command multiple times, specifying different offsets each time.
		This function provides a convenient shortcut for the standard workflow, combining :func:`confVoltageMeasurementSequenceHWTrigger`, :func:`startMeasurementSequence`, and the final :func:`getMeasurementSequence` call to ensure completion before proceeding.
		
		Remarks:
		(1) Hardware-triggered scop mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM400, PM101, PM102.
		(2) Not all hardware trigger sources are available for on every powermeter.
		(3) Supported for thermopile and 4-quadrant thermopile sensors in CW measurement mode.
		(4) Do NOT use this function for long lasting scope measurements for more than 3 seconds capture time to prevent read timeouts.
		(5) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(6) Disable the Thermopile accelerator :func:`setAccelState`.
		(7) Relative samples are not supported in scope mode e.g. :func:`setVoltageRef`.
		(8) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setVoltageAutoRange`.
		(9) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed. 
			For PM400 and PM101 time in us between the samples. Needs to be >= 100.
			hPos(c_uint32) : Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999). Value has not uni as it is a counter.
			
			channel(c_uint16) : external trigger source. 1(default) signal of channel 1, 2 signal of channel 2, 3 signal of front AUX, 4 signal of rear trigger.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_measureVoltageMeasurementSequenceHWTrigger(self.devSession, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getFetchState(self, state, channel):
		"""
		This function checks if there is measurement data available to fetch. If the function returns 1.
		
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
		Call this function once initially before starting a new measurement stream for the currently configured unit to ensure Powermeter stream buffer contains only data following the start condition. When unit gets changed reset is performed internally already.
		
		Remarks:
		(1) Note: Supported if Powermeter has Ethernet or USB High Speed
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_resetFastArrayMeasurement(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confFastArrayMeasurement(self, measurement, channel):
		"""
		This function configures the fast measurement stream for the configured unit. If the connected sensor or the powermeter does not support the request unit, an error will be generated. Changing the fast measure unit resets the measurement stream automatically see :func:`resetFastArrayMeasurement` as the buffer would contain measure results for another unit. 
		The stream data rate is constant and device dependent. Use :func:`getFastMaxSamplerate` to query device sampling rate. The stream supports CW and peak-mode measurements. To reduce the risk of data loss the Powermeter buffers the stream of the recent 10 ms. In case of buffer overflow new data is truncated until there is free space in the buffer. 
		
		Remarks:
		(1) Supported if Powermeter has Ethernet or USB High Speed.
		(2) Not supported on serial interface or bluetooth due to low bandwidth.
		(3) Averaging :func:`setAvgTime` is not considered for fast data stream.
		(4) Measuing power in dBm :func:`setPowerUnit` is not supported by fast measurement stream. 
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(7) The powermeter data stream is updated internally at 1 kHz.
		
		Args:
			measurement(c_uint16) : Fast measurement stream unit. 
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confFastArrayMeasurement(self.devSession, measurement, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confPowerFastArrayMeasurement(self, channel):
		"""
		This function configures the fast measurement stream for power measurements in watts [W]. If the connected sensor or the powermeter does not support the request unit, an error will be generated. Changing the fast measure unit resets the measurement stream automatically see :func:`resetFastArrayMeasurement` as the buffer would contain measure results for another unit. 
		The stream data rate is constant and device dependent. Use :func:`getFastMaxSamplerate` to query device sampling rate. The stream supports CW and peak-mode measurements. To reduce the risk of data loss the Powermeter buffers the stream of the recent 10 ms. In case of buffer overflow new data is truncated until there is free space in the buffer. 
		
		Remarks:
		(1) Supported if Powermeter has Ethernet or USB High Speed.
		(2) Supported for photodiode, thermopile and 4-Quadrant Thermopile sensors
		(2) Not supported on serial interface or bluetooth due to low bandwidth.
		(3) Averaging :func:`setAvgTime` is not considered for fast data stream.
		(4) Measuing power in dBm :func:`setPowerUnit` is not supported by fast measurement stream. 
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(7) The powermeter data stream is updated internally at 1 kHz.
		
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
		This function configures the fast measurement stream for current measurements in amperes [A]. If the connected sensor or the powermeter does not support the request unit, an error will be generated. Changing the fast measure unit resets the measurement stream automatically see :func:`resetFastArrayMeasurement` as the buffer would contain measure results for another unit. 
		The stream data rate is constant and device dependent. Use :func:`getFastMaxSamplerate` to query device sampling rate. The stream supports CW and peak-mode measurements. To reduce the risk of data loss the Powermeter buffers the stream of the recent 10 ms. In case of buffer overflow new data is truncated until there is free space in the buffer. 
		
		Remarks:
		(1) Supported if Powermeter has Ethernet or USB High Speed.
		(2) Supported for photodiode sensors
		(3) Not supported on serial interface or bluetooth due to low bandwidth.
		(4) Averaging :func:`setAvgTime` is not considered for fast data stream.
		(5) Measuing power in dBm :func:`setPowerUnit` is not supported by fast measurement stream. 
		(6) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(8) The powermeter data stream is updated internally at 1 kHz.
		
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
		This function configures the fast measurement stream for voltage measurements in volts [V]. If the connected sensor or the powermeter does not support the request unit, an error will be generated. Changing the fast measure unit resets the measurement stream automatically see :func:`resetFastArrayMeasurement` as the buffer would contain measure results for another unit. 
		The stream data rate is constant and device dependent. Use :func:`getFastMaxSamplerate` to query device sampling rate. The stream supports CW and peak-mode measurements. To reduce the risk of data loss the Powermeter buffers the stream of the recent 10 ms. In case of buffer overflow new data is truncated until there is free space in the buffer. 
		
		Remarks:
		(1) Supported if Powermeter has Ethernet or USB High Speed.
		(2) Supported for thermopile, 4Q Thermopile and pyroelectric sensors
		(3) Not supported on serial interface or bluetooth due to low bandwidth.
		(4) Averaging :func:`setAvgTime` is not considered for fast data stream.
		(5) Measuing power in dBm :func:`setPowerUnit` is not supported by fast measurement stream. 
		(6) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(8) The powermeter data stream is updated internally at 1 kHz.
		
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
		This function configures the fast measurement stream for power densitiy measurements in watts per square cm[W / cm²]. If the connected sensor or the powermeter does not support the request unit, an error will be generated. Changing the fast measure unit resets the measurement stream automatically see :func:`resetFastArrayMeasurement` as the buffer would contain measure results for another unit. 
		The stream data rate is constant and device dependent. Use :func:`getFastMaxSamplerate` to query device sampling rate. The stream supports CW and peak-mode measurements. To reduce the risk of data loss the Powermeter buffers the stream of the recent 10 ms. In case of buffer overflow new data is truncated until there is free space in the buffer. 
		
		Remarks:
		(1) Supported if Powermeter has Ethernet or USB High Speed.
		(2) Supported for photodiode, thermopile and 4-Quadrant Thermopile sensors
		(2) Not supported on serial interface or bluetooth due to low bandwidth.
		(3) Averaging :func:`setAvgTime` is not considered for fast data stream.
		(4) Measuing power in dBm :func:`setPowerUnit` is not supported by fast measurement stream. 
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(7) The powermeter data stream is updated internally at 1 kHz.
		
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
		This function configures the fast measurement stream for energy measurements in joules [J]. If the connected sensor or the powermeter does not support the request unit, an error will be generated. Changing the fast measure unit resets the measurement stream automatically see :func:`resetFastArrayMeasurement` as the buffer would contain measure results for another unit. 
		The stream data rate is constant and device dependent. Use :func:`getFastMaxSamplerate` to query device sampling rate. The stream supports peak-mode measurements. To reduce the risk of data loss the Powermeter buffers the stream of the recent 10 ms. In case of buffer overflow new data is truncated until there is free space in the buffer. 
		
		Remarks:
		(1) Supported if Powermeter has Ethernet or USB High Speed.
		(2) Supported for pyroelectric sensors
		(2) Not supported on serial interface or bluetooth due to low bandwidth.
		(3) Averaging :func:`setAvgTime` is not considered for fast data stream.
		(4) Measuing power in dBm :func:`setPowerUnit` is not supported by fast measurement stream. 
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(7) The powermeter data stream is updated internally at 1 kHz.
		
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
		This function configures the fast measurement stream for energy density measurements in joules per square cm [J / cm²]. If the connected sensor or the powermeter does not support the request unit, an error will be generated. Changing the fast measure unit resets the measurement stream automatically see :func:`resetFastArrayMeasurement` as the buffer would contain measure results for another unit. 
		The stream data rate is constant and device dependent. Use :func:`getFastMaxSamplerate` to query device sampling rate. The stream supports peak-mode measurements. To reduce the risk of data loss the Powermeter buffers the stream of the recent 10 ms. In case of buffer overflow new data is truncated until there is free space in the buffer. 
		
		Remarks:
		(1) Supported if Powermeter has Ethernet or USB High Speed.
		(2) Supported for pyroelectric sensors
		(2) Not supported on serial interface or bluetooth due to low bandwidth.
		(3) Averaging :func:`setAvgTime` is not considered for fast data stream.
		(4) Measuing power in dBm :func:`setPowerUnit` is not supported by fast measurement stream. 
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(7) The powermeter data stream is updated internally at 1 kHz.
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confEDensityFastArrayMeasurement(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getNextFastArrayMeasurement(self, count, timestamps, values, channel):
		"""
		This function retrieves the oldest measurements from the device's internal fast measurement stream buffer. It returns multiple tuples, each consisting of a relative wrapping microsecond counter (timestamp) and the corresponding measurement value. The relative timestamp enables calculation of time differences between samples, with the unit determined by the stream's unit configuration (e.g., :func:`confPowerFastArrayMeasurement`). The timestamp is provided in the format used by the device firmware. For an alternative that delivers timestamps already in relative time, use the convenience function :func:`getNextFastArrayMeasurementRelativeTime`.
		Prior to initiating fast measurement streaming, clear the device's internal buffer to remove any outdated measurements by invoking :func:`resetFastArrayMeasurement`. Then, call this function as frequently as possible to prevent the buffer from filling up. The stream operates at a constant, device-specific data rate; query the sampling rate using :func:`getFastMaxSamplerate`. The stream accommodates both CW and peak-mode measurements. To minimize the risk of data loss, the powermeter retains a buffer of the most recent 10 ms of stream data. If the buffer overflows, incoming data is discarded until space becomes available.
		
		Remarks:
		(1) Supported if Powermeter has Ethernet or USB High Speed.
		(2) Not supported on serial interface or bluetooth due to low bandwidth.
		(3) Averaging :func:`setAvgTime` is not considered for fast data stream.
		(4) Measuing power in dBm :func:`setPowerUnit` is not supported by fast measurement stream. 
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(7) The powermeter data stream is updated internally at 1 kHz.
		
		Args:
			count(c_uint32 use with byref) : The count of timestamp - measurement value pairs.
			timestamps( (c_uint32 * arrayLength)()) : Buffer containing up to 200 timestamps. This are raw timestamps and are NOT in ms.
			values( (c_float * arrayLength)()) : Buffer containing up to 200 measurement values.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getNextFastArrayMeasurement(self.devSession, count, timestamps, values, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getNextFastArrayMeasurementRelativeTime(self, count, timestamps, values, channel):
		"""
		This function retrieves the oldest measurements from the device's internal fast measurement stream buffer and calculates the relative time between the samples. It returns multiple tuples, each consisting of a relative wrapping microsecond counter (timestamp) and the corresponding measurement value. The relative timestamp enables calculation of time differences between samples, with the unit determined by the stream's unit configuration (e.g., :func:`confPowerFastArrayMeasurement`). To retrieve the timestamp in the raw microseconds refer to function :func:`getNextFastArrayMeasurement`.
		Prior to initiating fast measurement streaming, clear the device's internal buffer to remove any outdated measurements by invoking :func:`resetFastArrayMeasurement`. Then, call this function as frequently as possible to prevent the buffer from filling up. The stream operates at a constant, device-specific data rate; query the sampling rate using :func:`getFastMaxSamplerate`. The stream accommodates both CW and peak-mode measurements. To minimize the risk of data loss, the powermeter retains a buffer of the most recent 10 ms of stream data. If the buffer overflows, incoming data is discarded until space becomes available.
		
		Remarks:
		(1) Supported if Powermeter has Ethernet or USB High Speed.
		(2) Not supported on serial interface or bluetooth due to low bandwidth.
		(3) Averaging :func:`setAvgTime` is not considered for fast data stream.
		(4) Measuing power in dBm :func:`setPowerUnit` is not supported by fast measurement stream. 
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(7) The powermeter data stream is updated internally at 1 kHz.
		
		Args:
			count(c_uint32 use with byref) : The count of timestamp - measurement value pairs
			The value will be 200
			timestamps( (c_uint32 * arrayLength)()) : Buffer containing up to 200 timestamps.
			This are timestamps in µsec relative to the first timestamp.
			
			e.g.
			timestamp [0] = 0
			timestamp [1] = 10
			timestamp [2] = 20
			
			means that the time difference between the samples are 10 µsec.
			
			values( (c_float * arrayLength)()) : Buffer containing up to 200 measurement values.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getNextFastArrayMeasurementRelativeTime(self.devSession, count, timestamps, values, channel)
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
		This function sets up a software-triggered oscilloscope (scope) like power measurement in watts (W) specifically for continuous wave (CW) measurement mode. It configures the necessary scope mode parameters but does not initiate the measurement itself.
		The configuration remains active until the system is rebooted or the parameters are explicitly modified. In most applications, this function needs to be invoked only once.
		
		It serves as the initial step in a standard measurement workflow:
		1. Call this function to configure the power measurement sequence.
		2. Follow with :func:`startMeasurementSequence` to begin the acquisition to wait for completion.
		3. Invoke :func:`getMeasurementSequence` to retrieve data from the sample buffer.
		
		Remarks:
		(1) Scope mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM102
		(2) Supported for photodiode, thermopile and 4-Quadrant Thermopile sensors in CW measurement mode. (See :func:`setFreqMode`). 
		(3) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(4) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(5) Relative samples are not supported in scope mode e.g. :func:`setPowerRef`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(7) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(8) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed default is 1.
			For PM400 and PM101 time in us between the samples. Needs to be >= 100.
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
		This function sets up a hardware-triggered oscilloscope (scope) like power measurement in watts (W) specifically for continuous wave (CW) measurement mode. It configures the necessary scope mode parameters but does not initiate the measurement itself or arms the external trigger.
		The configuration remains active until the system is rebooted or the parameters are explicitly modified. In most applications, this function needs to be invoked only once.
		
		It serves as the initial step in a standard measurement workflow:
		1. Call this function to configure the power measurement sequence.
		2. Follow with :func:`startMeasurementSequence` to begin the acquisition to wait for completion.
		3. Invoke :func:`getMeasurementSequence` to retrieve data from the sample buffer.
		
		PM103/PM103E: For external trigger on digial IO1 pin. Use :func:`setDigIoPinMode` function to configure pin. This is not required for the other Powermeters.
		
		Remarks:
		(1) Hardware-triggered scop mode mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM400, PM101, PM102
		(2) Not all hardware trigger sources are available for on every powermeter.
		(3) Supported for photodiode, thermopile and 4-Quadrant Thermopile sensors in CW measurement mode. (See :func:`setFreqMode`). 
		(4) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Relative samples are not supported in scope mode e.g. :func:`setPowerRef`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		(8) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(9) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			trigSrc(c_uint16) : external trigger source.
			PM5020: 1(default) signal of channel 1, 2 signal of channel 2, 3 signal of front AUX, 4 signal of rear trigger.
			PM100D3: 1(default) signal of channel 1, 2 for DIO1
			PM6x: 1(default) signal of channel 1, 2 for DIO1
			PM103/PM103E: 1(default)
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed default is 1.
			hPos(c_uint32) : Sets the horizontal position of trigger condition in the scope catpure (Between 0 and 2500). The parameter has no unit as it is an index. 
			channel(c_uint16) : Number of the sensor channel. Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confPowerMeasurementSequenceHWTrigger(self.devSession, trigSrc, baseTime, hPos, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confCurrentMeasurementSequence(self, baseTime, channel):
		"""
		This function sets up a software-triggered oscilloscope (scope) like current measurement in ampere (A) specifically for continuous wave (CW) measurement mode. It configures the necessary scope mode parameters but does not initiate the measurement itself.
		The configuration remains active until the system is rebooted or the parameters are explicitly modified. In most applications, this function needs to be invoked only once.
		
		It serves as the initial step in a standard measurement workflow:
		1. Call this function to configure the current measurement sequence.
		2. Follow with :func:`startMeasurementSequence` to begin the acquisition to wait for completion.
		3. Invoke :func:`getMeasurementSequence` to retrieve data from the sample buffer.
		
		Remarks:
		(1) Scope mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM102
		(2) Supported for photodiode in CW measurement mode. (See :func:`setFreqMode`). 
		(3) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(4) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(5) Relative samples are not supported in scope mode e.g. :func:`setCurrentRef`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setCurrentAutoRange`.
		(7) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(8) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed default is 1.
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
		This function sets up a hardware-triggered oscilloscope (scope) like current measurement in ampere (A) specifically for continuous wave (CW) measurement mode. It configures the necessary scope mode parameters but does not initiate the measurement itself or arms the external trigger.
		The configuration remains active until the system is rebooted or the parameters are explicitly modified. In most applications, this function needs to be invoked only once.
		
		It serves as the initial step in a standard measurement workflow:
		1. Call this function to configure the current measurement sequence.
		2. Follow with :func:`startMeasurementSequence` to begin the acquisition to wait for completion.
		3. Invoke :func:`getMeasurementSequence` to retrieve data from the sample buffer.
		
		PM103/PM103E: For external trigger on digial IO1 pin. Use :func:`setDigIoPinMode` function to configure pin. This is not required for the other Powermeters.
		
		Remarks:
		(1) Hardware-triggered scop mode mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM400, PM101, PM102
		(2) Not all hardware trigger sources are available for on every powermeter.
		(3) Supported for photodiode sensors in CW measurement mode. (See :func:`setFreqMode`). 
		(4) Averaging :func:`setAvgTime` is not considered for scope measurements.
		(5) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(6) Relative samples are not supported in scope mode e.g. :func:`setCurrentRef`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setCurrentAutoRange`.
		(8) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(9) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			trigSrc(c_uint16) : external trigger source.
			PM5020: 1(default) signal of channel 1, 2 signal of channel 2, 3 signal of front AUX, 4 signal of rear trigger.
			PM100D3: 1(default) signal of channel 1, 2 for DIO1
			PM6x: 1(default) signal of channel 1, 2 for DIO1
			PM103/PM103E: 1(default)
			baseTime(c_uint32) : Scope averaging for fast sample rate <Get Fast Max Samplerate>. 0 is not allowed default is 1.
			hPos(c_uint32) : Sets the horizontal position of trigger condition in the scope catpure (Between 0 and 2500). The parameter has no unit as it is an index. 
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
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

	def confPDENMeasurementSequence(self, baseTime, channel):
		"""
		Configures power density array measurement.
		
		Use this command to configure the measure system for array power density measurement in W/cm^2. The command does not start the measurement. The configuration is only required once. Afterwards you control the measure system by using ABOR, INIT and FETC:ARR? finally.
		The array mode always stores 10000 power values in W or dBm with 10 kHz in an internal buffer. So max time resolution between the samples is 100 us. Ensure the product of delta_t / 100 * samples is always smaller or equal 10000. Also keep delta_t a multiple of 100. Normally it makes sense to disable bandwidth limitation for this measurement mode by using DIAG#:INP:PDI:BWID. SENS#:AVER is not applied for array mode. Also relative power measurements (See SENS#:POW:REF) are not supported in array mode.
		
		Note: The function is only available on PM101, PM400.
		
		
		Args:
			baseTime(c_uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is defined in the device specifications.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confPDENMeasurementSequence(self.devSession, baseTime, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def startMeasurementSequence(self, autoTriggerDelay, triggerForced):
		"""
		This function initiates a new scope measurement and requires the scope to be previously configured, for example, by calling :func:`confPowerMeasurementSequence`. Starting a measurement will invalidate any existing data and arm the hardware trigger if required by configuration. For software-triggered measurements, the trigger is activated immediately upon initialization.
		
		The function waits until the measurement data is ready to be retrieved. If a timeout is configured, it will force a trigger condition upon timeout and then wait for the measurement to complete. If no timeout is set, the measurement is aborted and a warning is issued in case of a timeout.
		
		This function acts as the intermediate step in a typical measurement workflow:
		1. Configure the measurement sequence once by calling, for example, :func:`confPowerMeasurementSequence`.
		2. Call this function to start the acquisition and to wait for completion.
		3. Use :func:`getMeasurementSequence` to retrieve data from the device internal sample buffer.
		
		Remarks:
		(1) Scope mode is not available for PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200
		(2) Supported for photodiode, thermopile and 4-quadrant thermopile sensors.
		(3) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(4) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			autoTriggerDelay(c_uint32) : Time to wait before forcing trigger condition by software if not triggered externally already. The unit of this parameter is milliseconds. Set 0 to disable this feature. 
			
			Special for PM400, PM101: Not used
			triggerForced(c_int16 use with byref) : Flag set to true if trigger condition was forced by timeout. False for real trigger. 
			Special for PM400, PM101: Not used
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_startMeasurementSequence(self.devSession, autoTriggerDelay, triggerForced)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getMeasurementSequence(self, baseTime, timeStamps, values, values2):
		"""
		This function retrieves the scope measurement results out of the device internal buffer. The function expects a oscilloscope (scope) like measurement to be initiated previsouly by calling :func:`startMeasurementSequence`. Ensure the provided list parameters length is at least 100 * <Base Time>. For the PM101 and PM400 devices ensure the list length is at least <Base Time> parameter. 
		
		This function acts as the intermediate step in a typical measurement workflow:
		1. Configure the measurement sequence once by calling, for example, :func:`confPowerMeasurementSequence`.
		2. Initiate the measurement and wait for completion by calling :func:`startMeasurementSequence`.
		3. Call this function to retrieve data from the device internal sample buffer.
		
		Remarks:
		(1) Scope mode is not available for PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200
		(2) Supported for photodiode, thermopile and 4-quadrant thermopile sensors.
		(3) PM101, PM400: Scope mode always stores 10000 samples with 10 kHz. So max time resolution between the samples is 100 us.
		(4) PM103, PM103E, PM6x, PM100D3, PM5020: Scope mode stores 10000 samples with given averaging at max 100 kHz. So max time resolution between the samples is 10 us.
		
		Args:
			baseTime(c_uint32) : The number of samples to collect during the internal iteration of the method.
			
			For PM5020, PM103, PM103E, PM6x, and PM100D3 models: The value can range from 1 to 100. Setting the value to 1 corresponds to collecting the first 100 samples, while a value of 100 will return 10,000 samples. Ensure that the lengths of the <Time Stamps> and <Values> parameter lists are at least 100 times the <Base Time>.
			
			For PM400 and PM101 models: This value specifies the number of samples to collect. In this case, the <Time Stamps> and <Values> parameter lists must have lengths of at least <Base Time> elements.
			timeStamps( (c_float * arrayLength)()) : Array of time stamps in ms. The size of this array is 100 * baseTime.
			values( (c_float * arrayLength)()) : Array of measurements. The size of this array is 100 * baseTime. Unit depends on scope configuration. 
			values2( (c_float * arrayLength)()) : Array of measurements for the second channel (PM5020 only). The size of this array is 100 * baseTime. Unit depends on scope configuration.  Set to NULL for single channel powermeters.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getMeasurementSequence(self.devSession, baseTime, timeStamps, values, values2)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confBurstArrayMeasPowerChannel(self, channel):
		"""
		This function configures a hardware-triggered burst power measurement in watts (W) for continuous wave (CW) measurement mode. It sets up the necessary burst mode parameters but does not start the measurement.
		
		The configuration persists until the system is rebooted or the parameters are explicitly changed. In most applications, this function needs to be called only once.
		
		In burst mode, each hardware trigger (rising edge) initiates one or more measurements after an optional initial delay, storing the results in the device's internal buffer. The buffer size is device-dependent but supports at least 10,000 samples. Use <Get Burst Array Length> to query the exact size. Once sufficient data is acquired, burst mode needs to be disabled manually before fetching the results. Once a trigger fires and starts the burst measurement sequence, the trigger is disabled until the measurement sequence has been taken.
		
		It serves as the initial step in a standard measurement workflow:
		1. Call this function to configure burst mode for power measurements in W (dBm is not supported).
		2. Follow with :func:`confBurstArrayMeasTrigger` to set up the trigger parameters.
		3. Follow with :func:`startBurstArrayMeasurement` to initiate acquisition and arm the trigger.
		4. Invoke :func:`getBurstArraySamples` to abort measurement and retrieve data from the sample buffer.
		
		Remarks:
		(1) Burst mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM101, PM102, PM400
		(2) Supported for photodiode, thermopile and 4-Quadrant Thermopile sensors in CW measurement mode. (See :func:`setFreqMode`). 
		(3) Averaging :func:`setAvgTime` is not considered for burst measurements.
		(4) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(5) Disable the Thermopile accelerator :func:`setAccelState`.
		(6) Relative samples are not supported in burst mode e.g. :func:`setPowerRef`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasPowerChannel(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confBurstArrayMeasCurrentChannel(self, channel):
		"""
		This function configures a hardware-triggered burst current measurement in amperes (A) for continuous wave (CW) measurement mode. It sets up the necessary burst mode parameters but does not start the measurement.
		
		The configuration persists until the system is rebooted or the parameters are explicitly changed. In most applications, this function needs to be called only once.
		
		In burst mode, each hardware trigger (rising edge) initiates one or more measurements after an optional initial delay, storing the results in the device's internal buffer. The buffer size is device-dependent but supports at least 10,000 samples. Use <Get Burst Array Length> to query the exact size. Once sufficient data is acquired, burst mode needs to be disabled manually before fetching the results. Once a trigger fires and starts the burst measurement sequence, the trigger is disabled until the measurement sequence has been taken.
		
		It serves as the initial step in a standard measurement workflow:
		1. Call this function to configure burst mode for current measurements in A.
		2. Follow with :func:`confBurstArrayMeasTrigger` to set up the trigger.
		3. Follow with :func:`startBurstArrayMeasurement` to initiate acquisition and wait for completion.
		4. Invoke :func:`getBurstArraySamples` to retrieve data from the sample buffer.
		
		Remarks:
		(1) Burst mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM101, PM102, PM400
		(2) Supported for photodiode
		(3) Averaging :func:`setAvgTime` is not considered for burst measurements.
		(4) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(5) Relative samples are not supported in burst mode e.g. :func:`setCurrentRef`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setCurrentAutoRange`.
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasCurrentChannel(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confBurstArrayMeasVoltageChannel(self, channel):
		"""
		This function configures a hardware-triggered burst voltage measurement in volts (V) for continuous wave (CW) measurement mode. It sets up the necessary burst mode parameters but does not start the measurement.
		
		The configuration persists until the system is rebooted or the parameters are explicitly changed. In most applications, this function needs to be called only once.
		
		In burst mode, each hardware trigger (rising edge) initiates one or more measurements after an optional initial delay, storing the results in the device's internal buffer. The buffer size is device-dependent but supports at least 10,000 samples. Use <Get Burst Array Length> to query the exact size. Once sufficient data is acquired, burst mode needs to be disabled manually before fetching the results. Once a trigger fires and starts the burst measurement sequence, the trigger is disabled until the measurement sequence has been taken.
		
		It serves as the initial step in a standard measurement workflow:
		1. Call this function to configure burst mode for voltage measurements in V.
		2. Follow with :func:`confBurstArrayMeasTrigger` to set up the trigger.
		3. Follow with :func:`startBurstArrayMeasurement` to initiate acquisition and wait for completion.
		4. Invoke :func:`getBurstArraySamples` to retrieve data from the sample buffer.
		
		Remarks:
		(1) Burst mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM101, PM102, PM400, PM103
		(2) Supported for thermopile and 4-Quadrant Thermopile sensors
		(3) Averaging :func:`setAvgTime` is not considered for burst measurements.
		(4) Disable the Thermopile accelerator :func:`setAccelState`.
		(5) Relative samples are not supported in burst mode e.g. :func:`setVoltageRef`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setVoltageAutoRange`.
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasVoltageChannel(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def confBurstArrayMeasTrigger(self, trgSource, initDelay, burstCount, averaging):
		"""
		This function configures a hardware-triggered burst measurement parameters for continuous wave (CW) measurement mode. It sets up the necessary burst mode parameters but does not start the measurement.
		
		The configuration persists until the system is rebooted or the parameters are explicitly changed. In most applications, this function needs to be called only once.
		
		In burst mode, each hardware trigger (rising edge) initiates one or more measurements after an optional initial delay, storing the results in the device's internal buffer. The buffer size is device-dependent but supports at least 10,000 samples. Use <Get Burst Array Length> to query the exact size. Once sufficient data is acquired, burst mode needs to be disabled manually before fetching the results. Once a trigger fires and starts the burst measurement sequence, the trigger is disabled until the measurement sequence has been taken.
		
		It serves as the second step in a standard measurement workflow:
		1. Configure the unit of the burst measurement mode using e.g. function :func:`confBurstArrayMeasPowerChannel` 
		2. Call this function to configure the trigger for the burst mode.
		3. Follow with :func:`startBurstArrayMeasurement` to initiate acquisition and arm the trigger.
		4. Invoke :func:`getBurstArraySamples` to abort measurement and retrieve data from the sample buffer.
		
		The parameter units are counts so the unit depends on the device sample rate. For PM5020 this is 10µs.
		The sum of all values is the burst sequence time. E.g. Init Delay = 5; Burst Count = 2; Averaging = 3
		=> Burst Sequence time = (InitDelay + (Burst Count * Averaging)) * 10µs = (5 + 2  * 3) * 10µs = 110µs
		
		Remarks:
		(1) Burst mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM101, PM102, PM400
		(2) Supported for CW measurement mode. (See :func:`setFreqMode`). 
		(3) Averaging :func:`setAvgTime` is not considered for burst measurements.
		(4) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(5) Disable the Thermopile accelerator :func:`setAccelState`.
		(6) Relative samples are not supported in burst mode e.g. :func:`setPowerRef`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		
		Args:
			trgSource(c_uint32) : Trigger source. 
			
			1(default) signal of channel 1
			2 signal of channel 2
			3 signal of front AUX 
			4 signal of rear trigger
			initDelay(c_uint32) : Init Delay time in 10µs. E.g. 5 means 5 * 10µs = 50µs 
			burstCount(c_uint32) : Amount of measurements for every trigger condition.
			averaging(c_uint32) : Average time in 10µ. Use to change the time between the measurements. E.g. Entered 3 means averaging of 30µs
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasTrigger(self.devSession, trgSource, initDelay, burstCount, averaging)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def startBurstArrayMeasurement(self):
		"""
		This function initiates a hardware-triggered burst measurement for continuous wave (CW) measurement mode and arms the trigger. It requires that the burst unit and trigger parameters have been configured initially (e.g., via <Conf Burst Power Unit>). Each triggered event stores the measurement results in the device's internal buffer. The mode remains active until the :func:`getBurstArraySamples` function disarms the trigger and retrieves the results. If the buffer becomes full, new measurement results are discarded.
		
		In burst mode, each hardware trigger (rising edge) initiates one or more measurements after an optional initial delay, storing the results in the device's internal buffer. The buffer size is device-dependent but supports at least 10,000 samples. Use <Get Burst Array Length> to query the exact size. Once sufficient data is acquired, burst mode needs to be disabled manually before fetching the results. Once a trigger fires and starts the burst measurement sequence, the trigger is disabled until the measurement sequence has been taken.
		
		It serves as the third step in a standard measurement workflow:
		1. Configure the unit of the burst measurement mode using e.g. function :func:`confBurstArrayMeasPowerChannel` 
		2. Follow with :func:`confBurstArrayMeasTrigger` to set up the trigger parameters.
		3. Call this function to start the measurement. 
		4. Invoke :func:`getBurstArraySamples` to abort measurement and retrieve data from the sample buffer.
		
		Remarks:
		(1) Burst mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM101, PM102, PM400
		(2) Supported for CW measurement mode. (See :func:`setFreqMode`). 
		(3) Averaging :func:`setAvgTime` is not considered for burst measurements.
		(4) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(5) Disable the Thermopile accelerator :func:`setAccelState`.
		(6) Relative samples are not supported in burst mode e.g. :func:`setPowerRef`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_startBurstArrayMeasurement(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getBurstArraySamplesCount(self, samplesCount):
		"""
		This function reads the amount of samples that have been measured during active burst mode. You can call this function regardless if burst mode is active or inactive to test if there is already measurement data to fetch. 
		
		In burst mode, each hardware trigger (rising edge) initiates one or more measurements after an optional initial delay, storing the results in the device's internal buffer. The buffer size is device-dependent but supports at least 10,000 samples. Use <Get Burst Array Length> to query the exact size. Once sufficient data is acquired, burst mode needs to be disabled manually before fetching the results. Once a trigger fires and starts the burst measurement sequence, the trigger is disabled until the measurement sequence has been taken.
		
		Remarks:
		(1) Burst mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM101, PM102, PM400
		(2) Supported for CW measurement mode. (See :func:`setFreqMode`). 
		(3) Averaging :func:`setAvgTime` is not considered for burst measurements.
		(4) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(5) Relative samples are not supported in burst mode e.g. :func:`setCurrentRef`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setCurrentAutoRange`.
		
		Args:
			samplesCount(c_uint32 use with byref) : Amount of samples taken during burst measurements.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getBurstArraySamplesCount(self.devSession, samplesCount)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getBurstArraySize(self, size):
		"""
		This function reads the device internal burst buffer size. If the buffer becomes full, new measurement results are discarded. Use the function :func:`getBurstArraySamplesCount` to query the amount of samples currenlty stored. 
		
		In burst mode, each hardware trigger (rising edge) initiates one or more measurements after an optional initial delay, storing the results in the device's internal buffer. The buffer size is device-dependent but supports at least 10,000 samples. Use <Get Burst Array Length> to query the exact size. Once sufficient data is acquired, burst mode needs to be disabled manually before fetching the results. Once a trigger fires and starts the burst measurement sequence, the trigger is disabled until the measurement sequence has been taken.
		
		Remarks:
		(1) Burst mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM101, PM102, PM400
		(2) Supported for CW measurement mode. (See :func:`setFreqMode`). 
		(3) Averaging :func:`setAvgTime` is not considered for burst measurements.
		(4) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(5) Relative samples are not supported in burst mode e.g. :func:`setCurrentRef`.
		(6) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setCurrentAutoRange`.
		
		Args:
			size(c_uint32 use with byref) : Amount of samples measure in burst mode.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getBurstArraySize(self.devSession, size)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getBurstArraySamples(self, startIndex, sampleCount, timeStamps, values, values2):
		"""
		This function aborts the burst measurement for continuous wave (CW) measurement mode, disarms the trigger, and retrieves the measurement results from the internal buffer. It requires that the measurement has been previously initiated by :func:`startBurstArrayMeasurement`. Ensure the provided arrays are large enough to store the specified <sample Count> samples. Use :func:`getBurstArraySamplesCount` to query the number of measurements in the buffer. This function can be called multiple times with different <Start Index> values to retrieve data in smaller chunks. 
		
		In burst mode, each hardware trigger (rising edge) initiates one or more measurements after an optional initial delay, storing the results in the device's internal buffer. The buffer size is device-dependent but supports at least 10,000 samples. Use <Get Burst Array Length> to query the exact size. Once sufficient data is acquired, burst mode needs to be disabled manually before fetching the results. Once a trigger fires and starts the burst measurement sequence, the trigger is disabled until the measurement sequence has been taken.
		
		It serves as the final step in a standard measurement workflow:
		1. Configure the unit of the burst measurement mode using e.g. function :func:`confBurstArrayMeasPowerChannel` 
		2. Follow with :func:`confBurstArrayMeasTrigger` to set up the trigger parameters.
		3. Follow with :func:`startBurstArrayMeasurement` to initiate acquisition and arm the trigger.
		4. Call this function to abort measurement and retrieve data from the sample buffer.
		
		Remarks:
		(1) Burst mode is NOT supported on PM100D, PM100A, PM100USB, PM16, PM160, PM160T, PM200, PM101, PM102, PM400
		(2) Supported for CW measurement mode. (See :func:`setFreqMode`). 
		(3) Averaging :func:`setAvgTime` is not considered for burst measurements.
		(4) Measure photodiode with high bandwidth filter :func:`setInputFilterState`.
		(5) Disable the Thermopile accelerator :func:`setAccelState`.
		(6) Relative samples are not supported in burst mode e.g. :func:`setPowerRef`.
		(7) Disable auto-ranging to prevent the Powermeter to interuppt the measurement due to ranging hardware settling pauses. For closer details read :func:`setPowerAutoRange`.
		
		Args:
			startIndex(c_uint32) : Start offset in device internal buffer where to start reading from. Starts at index 0.
			sampleCount(c_uint32) : Amount of measurements to read from device internal buffer. Ensure that <Timestamp>, <Channel 1> and <Channel 2> array fits at least the requested size.
			timeStamps( (c_uint32 * arrayLength)()) : Array for sample timestamps. Ensure array length is at least <Sample Count> parameter elements long.
			values( (c_float * arrayLength)()) : Array for feasrement results of channel 1 (default for single channel powermeters). Unit depends on burst mode unit configuration. Ensure array length is at least <Sample Count> parameter elements long.
			values2( (c_float * arrayLength)()) : Array for measrement results of channel 2 (PM5020 only, set to VI_NULL otherwise). Unit depends on burst mode unit configuration. Ensure array length is at least <Sample Count> parameter elements long.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getBurstArraySamples(self.devSession, startIndex, sampleCount, timeStamps, values, values2)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def disableArrayMeasurementChannel(self, channel):
		"""
		Use this command during scope or burst mode configuration to exclude measurement channel from scope or burst measurement. If the channel is excluded it will continue measuring in normal mode but does not contribute the scope or array measurement buffer.
		
		Remarks:
		(1) Only useful on PM5020
		
		Args:
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_disableArrayMeasurementChannel(self.devSession, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDigIoDirection(self, IO0, IO1, IO2, IO3):
		"""
		This function sets the digital I/O port direction.
		
		Note: The DEBRECATED function is only available on PM200 and PM400.
		
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
		
		Note: The DEBRECATED function is only available on PM200 and PM400.
		
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
		(1) Only ports configured as outputs are affected by this function. Use :func:`setDigIoDirection` to configure ports as outputs.
		(2) The DEBRECATED function is only available on PM200 and PM400.
		
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
		
		Note: The DEBRECATED function is only available on PM200 and PM400.
		
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
		
		Note: The DEBRECATED function is only available on PM200 and PM400.
		
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
		Configures the functionality of a single given digitial I/O pin. Each I/O pin has multiple potential uses. The selected usage is stored in the device and is automatically restored after a reboot. 
		
		Remarks:
		(1) Please note that changing the usage may affect the signal level.
		(2) Not all pins support all pin functions. Refer to product manual for details.
		(3) The amount of digital I/O pins depends on the connected powermeter. Refer to product manual for details. 
		(4) Depending on the function the pin might be connected to a pullup resistor internally. 
		(5) When used as output the pin should not driver more than 10 mA. 
		(6) The function is NOT available for PM200 and PM400
		
		Args:
			pinNumber(c_int16) : Number of the Pin. Refer to the powermeter manual to get the amount of pins available. 
			pinMode(c_uint16) : This parameter specifies the I/O port direction. Refer to the powermeter manual for the alternate functions. 
			
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
		Reads the current configuration of a single DIO pin. For closer details read :func:`setDigIoPinMode` comment.
		
		Remarks:
		(1) The function is NOT available for PM200 and PM400
		
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

	def setDigIoPinOutput(self, IO0, IO1, IO2, IO3):
		"""
		This function sets the digital I/O outputs simultaneously. If the powermeter has less digital I/O pins, the values are ignored.
		
		Notes:
		(1) Only ports configured as outputs are affected by this function. Use :func:`setDigIoDirection` to configure ports as outputs.
		(2) The amount of digital I/O pins depends on the connected powermeter. Refer to product manual for details. 
		(3) When used as output the pin should not driver more than 10 mA. 
		(4) The function is NOT available for PM200 and PM400
		
		Args:
			IO0(c_int16) : This parameter specifies the I/O port #1 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
			IO1(c_int16) : This parameter specifies the I/O port #2 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
			IO2(c_int16) : This parameter specifies the I/O port #3 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
			IO3(c_int16) : This parameter specifies the I/O port #4 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDigIoPinOutput(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDigIoPinOutput(self, IO0, IO1, IO2, IO3):
		"""
		This function returns the signal levels of the digital I/O pins configured in output direction. If a pin is configured for a different function, the corresponding bit will always be read back as low (0). 
		
		Remarks:
		(1) The amount of digital I/O pins depends on the connected powermeter. Refer to product manual for details. 
		(2) When used as output the pin should not driver more than 10 mA. 
		(3) The function is NOT available for PM200 and PM400
		
		Args:
			IO0(c_int16 use with byref) : This parameter returns the I/O port #1 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO1(c_int16 use with byref) : This parameter returns the I/O port #2 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO2(c_int16 use with byref) : This parameter returns the I/O port #3 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO3(c_int16 use with byref) : This parameter returns the I/O port #4 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDigIoPinOutput(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDigIoPinInput(self, IO0, IO1, IO2, IO3):
		"""
		This function returns the signal levels of the digital I/O pins configured in input direction. If a pin is configured for a different function, the corresponding bit will always be read back as low (0). 
		
		Remarks:
		(1) The amount of digital I/O pins depends on the connected powermeter. Refer to product manual for details. 
		(2) The function is NOT available for PM200 and PM400
		
		Args:
			IO0(c_int16 use with byref) : This parameter returns the I/O port #1 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO1(c_int16 use with byref) : This parameter returns the I/O port #2 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO2(c_int16 use with byref) : This parameter returns the I/O port #3 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
			IO3(c_int16 use with byref) : This parameter returns the I/O port #4 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDigIoPinInput(self.devSession, IO0, IO1, IO2, IO3)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getShutterInterlock(self, interlockState):
		"""
		This method checks if the interlock is closed or not. Only with an plugged in interlock the shutter can be opened. If the interlock is removed the shutter will close immediately. The interlock state is also masked in the SCPI Auxiliary Detail register bit 10. 
		
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
		This method sets the shutter set state. If the interlock is closed this method results in an change of the shutter state. If the interlock is open the method only changes the set value without a mechanically effect. If the interlock is plugged in later the shutter will open then. It is not possible to read back the set value. 
		
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
		This method checks if the shutter is currently open or closed. The shutter state is monitored by a internal light barrier. So even if it is mechanically blocked this method returns the real state. The actual shutter state is also masked in the SCPI Auxiliary Detail register bit 11.
		
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
		
		Note: The function is only available on PM5020 and PM100D3
		
		Args:
			mode(c_uint16) : I2C operating mode and bus speed. INTER,SLOW,FAST. More details in function description.
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
		
		Note: The function is only available on PM5020 and PM100D3
		
		Args:
			mode(c_int16 use with byref) : I2C operating mode and bus speed (INTER,SLOW,FAST)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getI2CMode(self.devSession, mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def I2CRead(self, address, count, dataRead):
		"""
		The command receives data from slave with given address. The function requires :func:`setI2CMode` to be called once previously. The command returns data as integer. Data is read synchronously with the SCPI command.
		
		Note: The function is available on PM5020, PM100D3
		
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
		The command transmits given data to slave with given address. The function requires :func:`setI2CMode`  to be called once previously. The transmission data is given as hexadecimal string parameter. The length needs to be a multiple of two as two hex digits encode a single byte. Leading zeros are mandatory. So to transfer byte 2 and 75 use string 024B. Hex digits are support upper or lowercase letters. The maximal length are 128 Bytes. Data is transferred synchronously with the function. If you want to read after writing some data you may use :func:`I2CWriteRead` function.
		
		Note: The function is available on PM5020, PM100D3
		
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
		The command transmits given data to slave with given address following a bus reception from same device if transmission was successful. The function requires :func:`setI2CMode`  to be called once previously. The function is a convenience function for a :func:`I2CWrite` followed by a :func:`I2CRead` command sequence. The maximal transmission and reception byte count is 128. For closer details of hexString format read :func:`I2CWrite` command description.
		
		Note: The function is available on PM5020, PM100D3
		
		Args:
			address(c_uint32) : I2C slave address. Address are bit 7 to bit 1. Bit 0 is ignored.
			hexSendData(c_char_p) : transmission data as hexadecimal string without byte separator. Length always multiple of 2.
			count(c_uint32) : amount of bytes to read from address.
			dataRead(c_uint32 use with byref) : received data as hexstring without seperator. Char count is always a multiple of 2. 
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
		Calling this method sets the fix voltage parameter for fan open loop operating mode. In open mode the fan speed is not controlled. The fan controller simply outputs a fixed voltage. This modus allows to operate 12V or 5V fans. If another operating mode is selected this function simply sets voltage parameter. If open loop mode is currently selected the function will set the parameter and update the fan controller output voltage simultaneously.
		
		Outputing more than 5V for a 5V fan can cause damage.
		If the given voltage is to low the fan might not start spinning.
		
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
		Use this method to read back the output voltage of fan. 
		
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
		Use this method to update the fan closed loop speed parameters. If fan controller is currently configured for another mode this function simply updates the parameters. If the fan controller is configured for closed loop mode the function updates the parameters and changes the fan speed set point simultaneously. To change the operating mode use SetFanMode. This mode is only possible to operate 12V fans. To calculate the internal RPM count registers it is mandatory to set the maximal expected speed out of fan. The implemented fan speed control is reacting slowly.
		
		Only available for 12V fans with 3 wire tacho signal.
		Control of fan speed is slow and can take several seconds.
		
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
		Use this method to read the closed loop fan speed set parameters. 
		
		Only available for 12V fans with 3 wire tacho signal.
		Control of fan speed is slow and can take several seconds.
		
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
		This method sets the temperature fan voltage adjustment points used by Powermeter to control the fan speed based on temperature measurement. This function will simply update the adjustment points. If fan controller operates in control mode the new parameters are used immediately. Use the method SetFanMode to change the operating mode and GetFanTemperatureSource to select the temperature measure source. The fan speed control is updated at 2 Hz and implements a 3% hysteresis when head or external NTC is chilling. Between the given points a logarithmic curve is fitted to calculate fan speed at measured temperature. The control parameters are stored persistently and are used at restart automatically.
		
		The control uses 3 Kelvin hysteresis before disabling fan again.
		
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
		This command reads back the automatically fan speed control adjustment parameters.
		
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

	def setLaserState(self, state, frequency, duration):
		"""
		Use this command to enable or disable the fibre laser in CW or TTL modulated mode. The function allows to enable the timer for a defined period or endless for CW and TTL mode. The time resolution is limited by the modulation frequency in TTL mode. The maximal duration is 10 seconds. Modulation is limited to 100 Hz. Use frequency 0 for CW mode. The laser might be disabled in any case.
		
		Note: The function is only available on PM61.
		
		Args:
			state(c_int16) : 1 to enable. 0 for disable.
			frequency(c_uint32) : Optional modulation frequency <= 100Hz. 0 for CW.
			duration(c_uint32) : Optional duration of laser sequence in ms. Resolution depends on frequ. Set to 65535 for endless.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setLaserState(self.devSession, state, frequency, duration)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getLaserState(self, state):
		"""
		Use this command to enable or disable the fibre laser in CW or TTL modulated mode. The function allows to enable the timer for a defined period or endless for CW and TTL mode. The time resolution is limited by the modulation frequency in TTL mode. The maximal duration is 10 seconds. Modulation is limited to 100 Hz. Use frequency 0 for CW mode. The laser might be disabled in any case.
		
		Note: The function is only available on PM61.
		
		Args:
			state(c_int16 use with byref) : 1 if enabled. 0 for disabled.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getLaserState(self.devSession, state)
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
			description(create_string_buffer(1024) use with byref) : This parameter returns the interpreted code as an user readable message string.
			
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
		(1) The returned values are stored in the drivers error store. You may use :func:`errorMessage` to get a descriptive text at a later point of time.
		
		Args:
			errorNumber(c_int use with byref) : This parameter returns the instrument error number.
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			
			errorMessage(create_string_buffer(1024) use with byref) : This parameter returns the instrument error message.
			
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
			description(create_string_buffer(1024) use with byref) : This parameter returns the interpreted code as an user readable message string.
			
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
			instrumentDriverRevision(create_string_buffer(1024) use with byref) : This parameter returns the Instrument Driver revision.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			firmwareRevision(create_string_buffer(1024) use with byref) : This parameter returns the device firmware revision. 
			
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
			manufacturerName(create_string_buffer(1024) use with byref) : This parameter returns the manufacturer name.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			deviceName(create_string_buffer(1024) use with byref) : This parameter returns the device name.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			serialNumber(create_string_buffer(1024) use with byref) : This parameter returns the device serial number.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			firmwareRevision(create_string_buffer(1024) use with byref) : This parameter returns the device firmware revision.
			
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
			message(create_string_buffer(1024) use with byref) : This parameter returns the calibration message.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			channel(c_uint16) : Number of the sensor channel. 
			
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
			name(c_char_p) : This parameter specifies the baudrate in bits/sec.
			
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
			name(create_string_buffer(1024) use with byref)
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDisplayName(self.devSession, name)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def isSensorConnected(self, isConnected, channel):
		"""
		This function checks if a light sensor is connected to the powermeter. 
		
		Args:
			isConnected(c_int16 use with byref) : Flag set to true if light sensor is connected. False otherwise.
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_isSensorConnected(self.devSession, isConnected, channel)
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
		This debrecated function is used to obtain informations from the connected sensor like sensor name, serial number, calibration message, sensor type, sensor subtype and sensor flags.  
		
		Remarks:
		This function is DEBRECATED. Use <Sensor Information Exteded> instead. 
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
		 SENSOR_SUBTYPE_PD_SINGLE_FSR   0x03 // Photodiode sensor with integrated filter identified by position 
		 SENSOR_SUBTYPE_PD_SINGLE_STD_T 0x12 // Photodiode sensor with temperature sensor
		
		Sensor Subtypes Thermopile:
		 SENSOR_SUBTYPE_THERMO_ADAPTER  0x01 // Thermopile adapter
		 SENSOR_SUBTYPE_THERMO_STD      0x02 // Thermopile sensor
		 SENSOR_SUBTYPE_THERMO_STD_T    0x12 // Thermopile sensor with temperature sensor
		
		Sensor Subtypes Pyroelectric Sensor:
		 SENSOR_SUBTYPE_PYRO_ADAPTER    0x01 // Pyroelectric adapter
		 SENSOR_SUBTYPE_PYRO_STD        0x02 // Pyroelectric sensor
		 SENSOR_SUBTYPE_PYRO_STD_T      0x12 // Pyroelectric sensor with temperature sensor
		
		Sensor Flags:
		 TLPM_SENS_FLAG_IS_POWER     0x0001 // Power sensor
		 TLPM_SENS_FLAG_IS_ENERGY    0x0002 // Energy sensor
		 TLPM_SENS_FLAG_IS_RESP_SET  0x0010 // Responsivity settable
		 TLPM_SENS_FLAG_IS_WAVEL_SET 0x0020 // Wavelength settable
		 TLPM_SENS_FLAG_IS_TAU_SET   0x0040 // Time constant settable
		 TLPM_SENS_FLAG_HAS_TEMP     0x0100 // With Temperature sensor 
		
		Args:
			name(create_string_buffer(1024) use with byref) : This parameter returns the name of the connected sensor. Provide at least buffer for 128 characters.
			
			snr(create_string_buffer(1024) use with byref) : This parameter returns the serial number of the connected sensor. Provide at least buffer for 128 characters.
			message(create_string_buffer(1024) use with byref) : This parameter returns the calibration message of the connected sensor. Provide at least buffer for 128 characters.
			
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
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getSensorInfo(self.devSession, name, snr, message, pType, pStype, pFlags, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getSensorInfoExt(self, name, snr, message, pType, pStype, pFlags, channel):
		"""
		This function is used to obtain informations from the connected sensor like sensor name, serial number, calibration message, sensor type, sensor subtype and sensor flags.  
		With this method you get more information about the sensor with the flags parameter.
		It will work with the power meters PM103, PM103E, PM5020, PM60 Series with the newest firmware.
		
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
		TLPM_SENS_XFLAG_AUTORANGE     0x0001 // can auto range
		TLPM_SENS_XFLAG_IS_ADAPTER    0x0002 // is adapter
		TLPM_SENS_XFLAG_ IS_WAVEL_SET 0x0004 // Energy sensor
		TLPM_SENS_XFLAG_IS_RESP_SET   0x0008 // Wavelength settable
		TLPM_SENS_XFLAG_IS_ACC_SET    0x0010 // can set acceleration
		TLPM_SENS_XFLAG_IS_BW_SET     0x0020 // can set bandwidth
		TLPM_SENS_XFLAG_DECT_PEAK     0x0040 // can detect peak
		TLPM_SENS_XFLAG_MEAS_FREQ     0x0080 // can meas frequency 
		TLPM_SENS_XFLAG_IS_ZERO_SET   0x0100 // can start zeroing
		TLPM_SENS_XFLAG_IS_TAU_SET    0x0200 // can set tau
		TLPM_SENS_XFLAG_MEAS_POS      0x0400 // can meas position x,y
		TLPM_SENS_XFLAG_PHOTOMETRIC   0x0800 // can meas photometric
		TLPM_SENS_XFLAG_HAS_TEMP      0x1000 // Temperature sensor included
		
		Args:
			name(create_string_buffer(1024) use with byref) : This parameter returns the name of the connected sensor. Provide at least buffer for 128 characters.
			snr(create_string_buffer(1024) use with byref) : This parameter returns the serial number of the connected sensor. Provide at least buffer for 128 characters.
			message(create_string_buffer(1024) use with byref) : This parameter returns the calibration message of the connected sensor. Provide at least buffer for 128 characters.
			
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
			pFlags(c_int use with byref) : This parameter returns the flags of the connected sensor.
			
			Remark:
			The meanings of the obtained sensor flags are:
			
			Sensor Flags:
			TLPM_SENS_XFLAG_AUTORANGE     0x0001 // can auto range
			TLPM_SENS_XFLAG_IS_ADAPTER    0x0002 // is adapter
			TLPM_SENS_XFLAG_ IS_WAVEL_SET 0x0004 // Energy sensor
			TLPM_SENS_XFLAG_IS_RESP_SET   0x0008 // Wavelength settable
			TLPM_SENS_XFLAG_IS_ACC_SET    0x0010 // can set acceleration
			TLPM_SENS_XFLAG_IS_BW_SET     0x0020 // can set bandwidth
			TLPM_SENS_XFLAG_DECT_PEAK     0x0040 // can detect peak
			TLPM_SENS_XFLAG_MEAS_FREQ     0x0080 // can meas frequency 
			TLPM_SENS_XFLAG_IS_ZERO_SET   0x0100 // can start zeroing
			TLPM_SENS_XFLAG_IS_TAU_SET    0x0200 // can set tau
			TLPM_SENS_XFLAG_MEAS_POS      0x0400 // can meas position x,y
			TLPM_SENS_XFLAG_PHOTOMETRIC   0x0800 // can meas photometric
			TLPM_SENS_XFLAG_HAS_TEMP      0x1000 // Temperature sensor included
			channel(c_uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getSensorInfoExt(self.devSession, name, snr, message, pType, pStype, pFlags, channel)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def importSettingsFromJson(self, adapt, settings):
		"""
		Use this function to import a previously stored parameter set again. The command will parse the JSON input and apply the parameter value. To export use the function :func:`exportSettingsAsJson`. It is possible to import parameters within a sensor family. For example you might import parameters exported for a photodiode when another photodiode is currenlty connected. Use the <Adapt> parameter to allow the command to change the parameters when out of range.
		
		Args:
			adapt(c_int16) : true to adapt parameters to ranges. False to generate error when out of range. 
			settings(c_char_p) :  device parameters as single line JSON format string. May be a substring of json line if larger 240 chars.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_importSettingsFromJson(self.devSession, adapt, settings)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def exportSettingsAsJson(self, settings, settingsSize):
		"""
		Use this command to export the persistently stored device parameters as single line JSON string. Some parameters like zeroing are not exported as the value is not valid for future imports. Use :func:`importSettingsFromJson` to import the parameter set again.
		
		
		Args:
			settings(create_string_buffer(1024) use with byref) : Device parameters as single line JSON string 
			settingsSize(c_uint32) : Size of buffer used to get the parameters
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_exportSettingsAsJson(self.devSession, settings, settingsSize)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def writeRaw(self, command):
		"""
		This function writes SCPI commands directly to the instrument.
		
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
			buffer(create_string_buffer(1024) use with byref) : Byte buffer that receives the data read from the instrument.
			
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
		Updates the IPv5 address the device has to commuicate with. If DHCP is enabled the function simply updates the static IPv4 netmask without applying configuration to the network interface. If DHCP is disabled, the command also applies configuration to the network interface. The configuration is stored in the device memory and restored after reboot.
		
		Args:
			IPAddress(c_char_p) : IPv4 address string. Bytes separated by fullstop.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setIPAddress(self.devSession, IPAddress)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getIPAddress(self, IPAddress):
		"""
		Use this command to query IPv4 address of device. If DHCP is enabled and no IP has been assigned yet the result might be "0.0.0.0". If DHCP is disabled the static IPv4 netmask will be returned.
		
		Args:
			IPAddress(create_string_buffer(1024) use with byref) : IPv4 address gateway string. Bytes separated by fullstop.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getIPAddress(self.devSession, IPAddress)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setIPMask(self, IPMask):
		"""
		Use this command to change IPv4 netmask of device. If DHCP is enabled the function simply updates the static IPv4 netmask without applying configuration to the network interface. If DHCP is disabled the command also applies configuration to the network interface. The configuration is stored in the device memory and restored after reboot.
		
		Args:
			IPMask(c_char_p) : IPv4 netmask string. Bytes separated by fullstop.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setIPMask(self.devSession, IPMask)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getIPMask(self, IPMask):
		"""
		Use this command to query IPv4 netmask of device. If DHCP is enabled and no IP has been assigned yet the result might be "0.0.0.0". If DHCP is disabled the static IPv4 netmask will be returned.
		
		
		
		Args:
			IPMask(create_string_buffer(1024) use with byref) : IPv4 netmask string. Bytes separated by fullstop.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getIPMask(self.devSession, IPMask)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getMACAddress(self, MACAddress):
		"""
		Returns the MAC address of the powermeter ethernet adapter.
		
		Args:
			MACAddress(create_string_buffer(1024) use with byref) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getMACAddress(self.devSession, MACAddress)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDHCP(self, enabled):
		"""
		Enables or disables the DHCP client on the device. When enabled the IP address is assigned at runtime by any Dynamic Host Configuration Protocol (DHCP) Server in LAN. When DHCP is disabled the static IP configuration is used. The configuration is stored in the device memory and restored after reboot.
		
		Args:
			enabled(c_int16) : This parameter accepts the instrument handle returned by <Initialize> to select the desired instrument driver session.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDHCP(self.devSession, enabled)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDHCP(self, enabled):
		"""
		Checks the DHCP client on the device is enabled or disabled. When enabled the IP address is assigned at runtime by any Dynamic Host Configuration Protocol (DHCP) Server in LAN. When DHCP is disabled the static IP configuration is used. 
		
		Args:
			enabled(c_int16 use with byref) : True when DHCP is enabled. False for static IP configuration. 
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDHCP(self.devSession, enabled)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setGateway(self, Gateway):
		"""
		Use this method to change IPv4 gateway of device. If DHCP is enabled the function simply updates the static IPv4 gateway without applying configuration to the network interface. If DHCP is disabled the command also applies configuration to the network interface. You can use 0.0.0.0 if gateway is not required.
		The configuration is stored in the device memory and restored after reboot.
		
		Args:
			Gateway(c_char_p) : IPv4 address gateway string. Bytes separated by fullstop.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setGateway(self.devSession, Gateway)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getGateway(self, Gateway):
		"""
		Use this method to query IPv4 gateway of device. If DHCP is enabled and no IP has been assigned yet the result might be "0.0.0.0". If DHCP is disabled the static IPv4 gateway will be returned. 
		
		
		
		Args:
			Gateway(create_string_buffer(1024) use with byref) : IPv4 address gateway string. Bytes separated by fullstop.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getGateway(self.devSession, Gateway)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setHostname(self, hostname):
		"""
		Changes the hostname for the device. The hostname can be used to customize the device name. It is displayed during boot to identify device if powermeter features a display. It may also be used in network as alias for IP address. This feature requires NetBIOS protocol to be enabled in LAN.  The configuration is stored in the device memory and restored after reboot. 
		
		Be aware not all characters are allowed in hostname string. DO NOT USE "space, slash, backslash, colon, semicolon, question mark, asterisk, smaller, bigger, pipe".
		
		Remark
		(1) Available for PM400, PM103E, PM5020, PM100Dx
		
		Args:
			hostname(c_char_p) : Hostname for the device. Changes the hostname for the device. The hostname can be used to customize the device name.
			DO NOT USE "space, slash, backslash, colon, semicolon, question mark, asterisk, smaller, bigger, pipe".
			
			Remark
			(1) Available for PM400, PM103E, PM5020, PM100Dx
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setHostname(self.devSession, hostname)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getHostname(self, hostname):
		"""
		Reads the hostname for the device. It is displayed during boot to identify device if powermeter features a display. It may also be used in networks as alias for IP address. This feature requires NetBIOS protocol to be enabled in LAN.
		
		Remark
		(1) Available for PM400, PM103E, PM5020, PM100Dx
		
		Args:
			hostname(create_string_buffer(1024) use with byref) : Queries device hostname. Used as device alias name and for ethernet devices as NETBIOS network hostname. 
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getHostname(self.devSession, hostname)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setWebPort(self, port):
		"""
		Changes the ethernet port number of the Web - Server. Set port number to 0 to disable the service. Once the port number is changed a reboot of the device is mandatory to apply new server settings.  The configuration is stored in the device memory and restored after reboot.
		
		Remark
		(1) Available on PM5020, PM103E
		
		Args:
			port(c_uint32) : new Web-Server port number. 0 to disable service. Default it 80.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setWebPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getWebPort(self, port):
		"""
		Reads the ethernet port number of the Web - Server.
		
		Remark
		(1) Available on PM5020, PM103E
		
		Args:
			port(c_uint32 use with byref) : Web - Server port number. 0 if service is disabled. Default is 80.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getWebPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setSCPIPort(self, port):
		"""
		Changes the ethernet port number of the SCPI - Server. Set port number to 0 to disable the service. Once the port number is changed a reboot of the device is mandatory to apply new server settings.  The configuration is stored in the device memory and restored after reboot.
		
		Remark
		(1) Available on PM5020, PM103E
		
		Args:
			port(c_uint32) : New port number. 0 to disable service. Default it 2001
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setSCPIPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getSCPIPort(self, port):
		"""
		Reads the ethernet port number of the SCPI - Server. When 0 service is disabled.
		
		Remark
		(1) Available on PM5020, PM103E
		
		Args:
			port(c_uint32 use with byref) : SCPI Server port number. 0 if service is disabled. Default is 2000.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getSCPIPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDFUPort(self, port):
		"""
		Changes the ethernet port number of the Device Firmware Update (DFU) - Server. Set port number to 0 to disable the service. Once the port number is changed a reboot of the device is mandatory to apply new server settings. The configuration is stored in the device memory and restored after reboot.
		
		Remark
		(1) Available on PM5020, PM103E
		
		Args:
			port(c_uint32) : new port number. 0 to disable service. Default it 27007
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDFUPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDFUPort(self, port):
		"""
		Reads the ethernet port number of the Device Firmware Update (DFU) - Server. When 0 service is disabed. 
		
		Remark
		(1) Available on PM5020, PM103E
		
		Args:
			port(c_uint32 use with byref) : DFU Server port number. 0 if service is disabled. Default is 27007.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDFUPort(self.devSession, port)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setEncryption(self, oldPassword, newPassword, encryption):
		"""
		Overwrites the system password used for authentication, Default password ist THORlabs. If changing the password via ethernet ensure to reinit communication channel after this command. The configuration is stored in the device memory and restored after reboot.
		
		Remarks:
		(1) Available on PM5020, PM103E
		
		
		Args:
			oldPassword(c_char_p) : old ASCII passwort string. Max length is 25. Min length is 5
			
			newPassword(c_char_p) : new ASCII passwort string. Max length is 25. Min length is 5
			
			encryption(c_int16) : True if SCPI LAN interface should be crypted.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setEncryption(self.devSession, oldPassword, newPassword, encryption)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getEncryption(self, password, encryption):
		"""
		Queries password used for authentication. Default password ist THORlabs. Only supported by local interface like USB or serial.
		
		Remarks:
		(1) Available on PM5020, PM103E
		
		
		Args:
			password(create_string_buffer(1024) use with byref) : used password
			
			encryption(c_int16 use with byref) : True if SCPI LAN interface should be crypted
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getEncryption(self.devSession, password, encryption)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setLANPropagation(self, enable):
		"""
		Use this command to enable or disable LAN service propagation server. If the server is disabled the device will not be found by ethernet network device discovery. The device discovery is based on UDP broadcast on port 27078. The configuration is stored in the device memory and restored after reboot.
		
		Remarks:
		(1) Available on PM103E, PM5020
		
		Args:
			enable(c_int16) : True to enable service propagation server. False to stop and disable the server.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setLANPropagation(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getLANPropagation(self, enable):
		"""
		Use this command to test if LAN service propagation is enabled. When enabled a UDP server listens on port 27078 to answer ethernet network disocvery requests. When disbaled the device can not be found by the network device search. 
		
		Remarks:
		(1) Available on PM103E, PM5020
		
		Args:
			enable(c_int16 use with byref) : 1 to enable service propagation. False to disable
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getLANPropagation(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setEnableNetSearch(self, enable):
		"""
		Enables searching for Ethernet devices on the current instance. To accelerate the device discovery process, Ethernet scanning is disabled by default. To include devices connected via Ethernet in the search results, invoke this setter prior to initiating the connected devices scan.
		The configuration is not stored and needs to be set for every new device search.
		
		Remarks:
		(1) Particularly useful for PM103E and PM5020 devices.
		
		Args:
			enable(c_int16) : True to enable the ethnet network search. False to disable searching for ethernet devices on local LAN to speed up the search routine. 
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setEnableNetSearch(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getEnableNetSearch(self, enable):
		"""
		Tests if the ethernet devices search for the actual instance is enabled or disabled. Ethernet searching is disabled by default to speed up search routine. When enabled the device search routine will also search the local LAN.
		
		Remarks:
		(1) Useful for PM103E and PM5020
		
		Args:
			enable(c_int16 use with byref) : True if ethnet network search is enabled. False if searching for ethernet devices on local LAN is disabled to speed up the search routine. 
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getEnableNetSearch(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setLookForInfoOnSearch(self, enable):
		"""
		Enables or disables the posibility to get information on TLPMX_findRsrc.
		If this is set to false the method TLPMX_getRsrcInfo will not retrive any information after TLPMX_findRsrc.
		
		
		
		
		Args:
			enable(c_int16) : Enables or disables the posibility to get information on TLPMX_findRsrc.
			If this is set to false the method TLPMX_getRsrcInfo will not retrive any information after TLPMX_findRsrc.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setLookForInfoOnSearch(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getLookForInfoOnSearch(self, enable):
		"""
		Get if the posibility to get information on TLPMX_findRsrc is enabled.
		If this is set to false the method TLPMX_getRsrcInfo will not retrive any information after TLPMX_findRsrc.
		
		
		Args:
			enable(c_int16 use with byref) : Get if the posibility to get information on TLPMX_findRsrc is enabled.
			If this is set to false the method TLPMX_getRsrcInfo will not retrive any information after TLPMX_findRsrc.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getLookForInfoOnSearch(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setNetSearchMask(self, netMask):
		"""
		Sets the default network mask for searching Ethernet devices on the computer. If the local PC has multiple networks, call this function prior to the network search to specify the network used for device discovery. Configure the network broadcast address for the network to which the power meters are connected. For example, on a subnet with IP addresses in the range 192.168.1.0/24, the broadcast address would typically be 192.168.1.255. If this command is not invoked before the search command, the local operating system decides where to send the broadcast messages. The configuration is not stored and needs to be set for every new device search.
		
		Remarks:
		(1) Particulary useful for PM103E and PM5020 devices
		
		Args:
			netMask(c_char_p) : Network broadcast address used for the device search.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setNetSearchMask(self.devSession, netMask)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setEnableBthSearch(self, enable):
		"""
		Enables searching for Ethernet devices on the current instance. To accelerate the device discovery process, Bluetooth Low Energy (BLE) scanning is disabled by default. To include devices connected via BLE in the search results, invoke this setter prior to initiating the connected devices scan. 
		The configuration is not stored and needs to be set for every new device search.
		
		Remarks:
		(1) Particularly useful for PM61 and PM100D3 devices.
		
		Args:
			enable(c_int16) : 1 to enable the Bluetooth search during device discovery. 0 to exclude Bluetooth device discovery. 
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setEnableBthSearch(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getEnableBthSearch(self, enable):
		"""
		Tests if searching for Ethernet devices is enabled or disabled on the current instance. To accelerate the device discovery process, Bluetooth Low Energy (BLE) scanning is disabled by default. 
		
		Remarks:
		(1) Particularly useful for PM61 and PM100D3 devices.
		
		Args:
			enable(c_int16 use with byref) : True(1) when BLE device search is enabled for current instance. False(0) when BLE device search is excluded from search routine.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getEnableBthSearch(self.devSession, enable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDeviceBaudrate(self, baudrate):
		"""
		Configures the baudrate of the device serial interface. To configure the baudrate of the instrument driver (PC) call function :func:`setDriverBaudrate`. The new baudrate is stored in the device memory and restored after reboot.
		
		Default Serial Configuration: 115200 8N1
		
		Remarks:
		(1) It is mandatory that device baudrate configuration matches the instrument driver (PC) one. 
		(2) Requires a serial interface on the connected powermeter
		
		Args:
			baudrate(c_uint32) : Device serial interface baudrate in Baud.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDeviceBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDeviceBaudrate(self, baudrate):
		"""
		Reads the baudrate used by the device for the serial interface. To read the baudrate used by the instrument driver (PC) use :func:`getDriverBaudrate` function.
		
		Default Serial Configuration: 115200 8N1
		
		Remarks:
		(2) Requires a serial interface (RS232 or UART) on the connected powermeter
		
		Args:
			baudrate(c_uint32 use with byref) : Device serial interface baudrate in Baud.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDeviceBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDriverBaudrate(self, baudrate):
		"""
		Sets the baud rate for the serial interface on the PC side. This does not affect the device itself. Call setDeviceBaudrate prior to this function. The baud rate configuration is not stored persistently and must be reconfigured before opening a connection to the device.
		
		Default Serial Configuration: 115200 8N1
		
		Remarks:
		(1) It is mandatory that device baudrate configuration matches the instrument driver (PC) one. 
		
		Args:
			baudrate(c_uint32) : Device driver (PC) serial interface baudrate in Baud.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_setDriverBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDriverBaudrate(self, baudrate):
		"""
		This function returns the baudrate that is used for the serial communication on the PC side. To query the baudrate of the device use :func:`getDeviceBaudrate` function. 
		
		
		Args:
			baudrate(c_uint32 use with byref) : Device driver (PC) baudrate in Baud
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_getDriverBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

