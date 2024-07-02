"""
Example Thorlabs Power Meter JSON parameter export and import
Example Date of Creation                            2024-04-08
Example Date of Last Modification on Github         2024-04-08
Version of Python                                   3.11.2
Version of the Thorlabs SDK used                    anyvisa0.3.0
==================
This examples shows how to export all runtime parameters of the Thorlabs Power Meter in JSON
format. After export the parameter set can be imported to the meter at any time again. 
Do not use this to modify the parameters. It is a export/import functionality.
"""
from anyvisa import AnyVisa
import sys

def main():
    devices = []
    devices = AnyVisa.FindResources("USB0:?*:INSTR")

    print("Found devices")
    print(devices)
    print()

    #test if we found at least one meter
    if not devices:
        print("Require at least one powermeter for this demo")
        sys.exit(-1)

    #Use with pattern to ensure all resources are released finally
    with devices[0] as d:
        print(d.query("*IDN?").strip())
                
        print("Export JSON out of meter")
        exp = d.query('SYST:PARA:EXPO:JSON?').strip()
        print(exp)
        print(d.query("SYST:ERR?").strip())
        print()
        
        print ("Import JSON into meter again")
        #To import parameters we need to split the JSON into multiple command calls.
        for idx in range(0,len(exp), 100):
            chunk = exp[idx:idx+100]            
            print("SYST:PARA:IMPO:JSON 1,'"+chunk+"'")
            d.write("SYST:PARA:IMPO:JSON 1,'"+chunk+"'")

        print(d.query("SYST:ERR?").strip())

if __name__ == '__main__':
    main()