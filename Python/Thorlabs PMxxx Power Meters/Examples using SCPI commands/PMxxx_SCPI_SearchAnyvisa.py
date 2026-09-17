# Start a device search and open first device found
from anyvisa import AnyVisa
devices = []
#run device search with wildcard
devices = AnyVisa.FindResources("?*")

#Found at least one device?
if devices:
    #Use with pattern to ensure all resources are released finally
    with devices[0] as d:
        #print device resource string and used library (pyvisa or tlvisa)
        print(d, d.lib())
        #print device identification
        print(d.auto_query("*IDN?"))


