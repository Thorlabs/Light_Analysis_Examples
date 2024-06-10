import os
import ctypes as c
import logging
r'''
This module facilitates the loading of the FTSLib.dll for ThorSpectra.

### Initializing FTSLib.dll ###

To initialize FTSLib.dll, use the `load_dll` function.
If the default ThorSpectra folder is not accessible, provide a custom path:
```python
load_dll(r'C:\tmp\special\folder')  # Loads FTSLib.dll from the specified folder
```

Note: The provided path should lead to the directory containing FTSLib.dll or directly to the FTSLib.dll file.
Ensure the path is adjusted according to your ThorSpectra installation.

# Example usage:
# load_dll()  # FTSLib.dll is located using the system path
# load_dll(r'C:\Program Files\Thorlabs\ThorSpectra')  # Manually specify the ThorSpectra folder
'''

logger = logging.getLogger("pyOSA")

def guess_dll_path():
    """Try locating FTSLib.dll from the system path
    """
    system_path = os.getenv("PATH").split(";")
    pathlist = [path for path in system_path if path.endswith("\\ThorSpectra")]
    if len(pathlist) > 0:
        dll_path = str(pathlist[0])
        dll_full_path = os.path.join(dll_path, "FTSLib.dll")
    else:
        raise Exception("ThorSpectra not found in path, please add to path "
                        "or edit FTSLib.py to point to FTSLib.dll")
    return dll_full_path

def check_version(dll):
    """
    Check if the correct version of ThorSpectra is used
    """
    try:
        dll.FTS_GetNearestHigherAllowedFFTLength
    except AttributeError:
        raise Exception("pyOSA requires ThorSpectra 3.31 or higher")

def load_dll(dll_path: str=None):
    """load FTSLib.dll from dll_path, if no path is specified
    then try to find ThorSpectra and load it from there.
    """
    if dll_path is not None:
        # Make sure the path includes the filename of the dll file
        if not dll_path.lower().endswith(".dll"):
            dll_path = os.path.join(dll_path, "FTSLib.dll")
    else:
        dll_path = guess_dll_path()

    if not os.path.exists(dll_path):
        raise Exception(f"DLL {dll_path} not found")
    logger.info(f"Loading DLL: {dll_path}")
    cdll = c.CDLL(dll_path) # Load the dll
    check_version(cdll)
    return cdll



FTSLib = load_dll()
