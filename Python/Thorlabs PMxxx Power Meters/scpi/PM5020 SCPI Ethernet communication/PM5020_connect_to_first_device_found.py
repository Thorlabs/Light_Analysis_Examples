# Start a device search and open first device found
from anyvisa import AnyVisa
devices = []
devices = AnyVisa.FindResources("?*")
if devices:
    with devices[0] as d:
        print(d)
        print(d.lib())
        print(d.auto_query("*IDN?"))


