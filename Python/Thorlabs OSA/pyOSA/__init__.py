from pyOSA.constants import constants
from pyOSA.units import units
from pyOSA.FTSLib import FTSLib
from pyOSA.core import core, VirtualOSAException
from pyOSA.instrument import Instrument, InstrumentSeriesException, AcquisitionException
from pyOSA.analysis import analysis
from pyOSA.spectrum_t import spectrum_t
initialize = core.initialize
create_virtual_OSA20X = core.create_virtual_OSA20X
create_virtual_Redstone = core.create_virtual_Redstone