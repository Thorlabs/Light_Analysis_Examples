# JSON Parameter Export and Import Example
This command line sample demonstrates how to export and import the Power Meter runtime parameters
in [JSON]() format. 

# Details 

The parameter export and import functionality allows to save and restore a set of paramters for example for a certain expermiment.

## Limitations
Please do not use this to modify the parameters. Moving parameter sets between differente Power Meters is not supported but you 
can use this feature to clone a device configuration within one Meter family. You can also only import parameters within 
one sensor family. So for example from one photodiode to another photodiode but not from photodiode to pyroelectric sensor.


# Example Output

```
Found devices
[AnyVisa Device(USB0::0x1313::0x80B4::Jonny1::INSTR)]

Thorlabs,PM62,M00000002,1.0.0.3
Export JSON out of meter
{"pm":{"name":"PM62","ser":"M00000002","calD":"05-Feb-2024","adap":1},"sens":[{"name":"S130C","ser": "11071126","calD":"4-AUG-2011","ch": 0,"type":1,"aRan":false,"gIdx":8,"wavel":400.00,"resp":5.314501e-03,"atten":0.000000e+00,"bArea":0.708822,"wUnit":0,"wMin":"-inf","wMax":"inf", "mode": 2, "bandw":0, "pFilt":1, "pThre":10}]}
0,"No error"

Import JSON into meter again
SYST:PARA:IMPO:JSON 1,'{"pm":{"name":"PM62","ser":"Jonny1","calD":"05-Feb-2024","adap":1},"sens":[{"name":"S130C","ser": "1'
SYST:PARA:IMPO:JSON 1,'1071126","calD":"4-AUG-2011","ch": 0,"type":1,"aRan":false,"gIdx":8,"wavel":400.00,"resp":5.314501e-'
SYST:PARA:IMPO:JSON 1,'03,"atten":0.000000e+00,"bArea":0.708822,"wUnit":0,"wMin":"-inf","wMax":"inf", "mode": 2, "bandw":0,'
SYST:PARA:IMPO:JSON 1,' "pFilt":1, "pThre":10}]}'
0,"No error"
```

## anyvisa python Library
You can download anyvisa library wheel in this Github repository. Please refer to this [README](../Readme.md) how to install it. 

## Supported Meters
- PM103
- PM103E
- PM5020
- PM6x
