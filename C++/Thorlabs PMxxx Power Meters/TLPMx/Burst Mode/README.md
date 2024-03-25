# C++ Burst Mode Example
This C++ sample code demonstrates how to use Thorlabs Power Meter Burst Mode. In Burst mode the 
device stores a sequence of measurements for every hardware trigger condition in an internal memory. 

# Details 

The burst mode stores a one or multiple measurements for every hardware trigger condition. You can also
force a trigger condition by software. Once you finished the measurement you can query the measurement results at any speed. Every measurement result will be a tuple (single channel) or tripplet (dual channel). 

## Limitations
Please be aware the burst mode is only available in CW measurement mode. Peak measurement mode 
is not supported. For closer details refer to the Burst Mode description in the [SCPI command](scpiTODO)
description. 

## Supported Meters
- PM103
- PM103E
- PM5020
- PM62
- PM63
