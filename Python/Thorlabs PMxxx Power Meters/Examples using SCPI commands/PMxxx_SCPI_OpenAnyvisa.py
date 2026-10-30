# Open a known device by resource string
from anyvisa import AnyVisa

#USB example:      "TCPIP0::10.10.4.77::PM5020_07::INSTR"
#Serial example    "TCPIP0::10.10.4.77::PM5020_07::INSTR"
#Ethernet example  "TCPIP0::10.10.4.77::PM5020_07::INSTR"
#BLE example       "TCPIP0::10.10.4.77::PM5020_07::INSTR"

#Use with pattern to ensure all resources are released finally
with AnyVisa.TL_Open("TCPIP0::10.10.4.77::PM5020_07::INSTR") as d:
    #print device resource string and used library (pyvisa or tlvisa)
    print(d,d.lib())
    #print device identification
    print(d.auto_query("*IDN?"))
