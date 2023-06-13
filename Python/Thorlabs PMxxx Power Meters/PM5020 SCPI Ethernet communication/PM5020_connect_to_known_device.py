# Open a known device by resource string
from anyvisa import AnyVisa
with AnyVisa.TL_Open("TCPIP0::10.10.4.77::PM5020_07::INSTR") as d:
    print(d)
    print(d.lib())
    print(d.auto_query("*IDN?"))




