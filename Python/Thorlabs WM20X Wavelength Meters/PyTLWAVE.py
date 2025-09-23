import os
import ctypes

class TLWAVE:

    def __init__(self, resourceName = None, IDQuery = True, resetDevice = False):
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
            resourceName
            IDQuery (bool):This parameter specifies whether an identification query is performed during the initialization process.
            
            VI_TRUE  (1): Do query (default).
            VI_FALSE (0): Skip query.
            
            
            resetDevice (bool):This parameter specifies whether the instrument is reset during the initialization process.
            
            VI_TRUE  (1): instrument is reset 
            VI_FALSE (0): no reset (default)
            
            
        """
        possiblepaths = [os.path.dirname(os.path.abspath(__file__)),
                         r"C:\Program Files (x86)\Thorlabs\OPM"]

        if ctypes.sizeof(ctypes.c_voidp) == 4:
            dll_name = "TLWAVE_32.dll"
        else:
            dll_name = "TLWAVE_64.dll"
        
        self.dll = None
        last_err = None
        for path in possiblepaths:
            fullpath = os.path.join(path,dll_name)
            if os.path.isfile(fullpath):
                try:
                    self.dll = ctypes.cdll.LoadLibrary(fullpath)
                    break
                except OSError as e:
                    print(e)
                    last_err = e

        if self.dll is None:
            print(last_err)
            raise RuntimeError(f"Could not find {dll_name} in {" or ".join(possiblepaths)}")

        self.devSession = ctypes.c_long()
        self.devSession.value = 0
        if resourceName is not None:
            pInvokeResult = self.dll.TLWAVE_init( ctypes.create_string_buffer(resourceName), ctypes.c_bool(IDQuery), ctypes.c_bool(resetDevice), ctypes.byref(self.devSession))
            self.__testForError(pInvokeResult)


    def __testForError(self, status):
        if status < 0:
            self.__throwError(status)
        return status

    def __throwError(self, code):
        msg = ctypes.create_string_buffer(1024)
        self.dll.TLWAVE_error_message(self.devSession, ctypes.c_int(code), msg)
        raise NameError(ctypes.c_char_p(msg.raw).value)
    
    def getRsrcName(self, index):
        """
        This function gets the resource name string needed to open a device.
        
        Notes:
        (1) The data provided by this function was updated at the last call of <Find Resources>.
        
        Args:
            index(uint32) : This parameter accepts the index of the device to get the resource descriptor from.
            
            Notes: 
            (2) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.
            
        Returns:
            resourceName(string) : This parameter returns the resource descriptor. Use this descriptor to specify the device.
        """
        pyresourceName = ctypes.create_string_buffer(1024)
        pInvokeResult = self.dll.TLWAVE_getRsrcName(self.devSession, ctypes.c_uint32(index), pyresourceName)
        self.__testForError(pInvokeResult)
        return ctypes.c_char_p(pyresourceName.raw).value

    def findRsrc(self):
        """
        This function finds all driver compatible devices attached to the PC and returns the number of found devices.

        Note:
        (1) The function additionally stores information like system name about the found resources internally. This information can be retrieved with further functions from the class, e.g. <Get Resource Description> and <Get Resource Information>.


        Args:
            
        Returns:
            resourceCount(uint32) : The number of connected devices that are supported by this driver.
        """
        pyresourceCount = ctypes.c_uint32(0)
        pInvokeResult = self.dll.TLWAVE_findRsrc(self.devSession, ctypes.byref(pyresourceCount))
        self.__testForError(pInvokeResult)
        return  pyresourceCount.value
    
    def __del__(self):
        #destructor
        if self.dll is not None:
            self.close()

    def close(self):
        """
        This function closes the instrument driver session.
        
        Note: The instrument must be reinitialized to use it again.
        
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLWAVE_close(self.devSession)
        return pInvokeResult
    
    def writeRaw(self, command):
        """
        This function writes directly to the instrument.
        
        Args:
            command(char_p) : Null terminated command string to send to the instrument.
            
        Returns:
        """
        pInvokeResult = self.dll.TLWAVE_writeRaw(self.devSession, ctypes.c_char_p(command.encode('utf-8')))
        self.__testForError(pInvokeResult)

    def readRaw(self, size):
        """
        This function reads directly from the instrument.
        
        Args:

            size(uint32) : This parameter specifies the buffer size.

            Notes:
            (1) If received data is less than buffer size, the buffer is additionally terminated with a '' character.
            (2) If received data is same as buffer size no '' character is appended. It's the caller's responsibility to make sure a buffer is '' terminated if the caller wants to interpret the buffer as string.
            (3) You may pass VI_NULL if you don't need this value.
            
        Returns:
            buffer(string) : Byte buffer that receives the data read from the instrument.
            returnCount(uint32) : Number of bytes actually transferred and filled into Buffer. This number doesn't count the additional termination '' character. If Return Count == size of the buffer, the content will not be '' terminated.
        """
        pybuffer = ctypes.create_string_buffer(1024)
        pyreturnCount = ctypes.c_uint32(0)
        pInvokeResult = self.dll.TLWAVE_readRaw(self.devSession, pybuffer, ctypes.c_uint32(size), ctypes.byref(pyreturnCount))
        self.__testForError(pInvokeResult)
        return ctypes.c_char_p(pybuffer.raw).value, pyreturnCount.value

    def readRegister(self, registerID:int) -> int:
        registervalue = ctypes.c_int16(-1)
        pInvokeResult = self.dll.TLWAVE_readRegister(self.devSession, registerID, ctypes.byref(registervalue))
        self.__testForError(pInvokeResult)
        return registervalue.value

    def getID(self) -> str:
        self.writeRaw("*IDN?\n")
        rawValue,numbytes = self.readRaw(1024)
        id = rawValue.decode('utf-8').strip()
        return id