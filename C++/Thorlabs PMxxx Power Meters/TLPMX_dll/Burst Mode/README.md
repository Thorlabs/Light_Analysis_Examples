# C++ Burst Mode Example
This C++ sample code demonstrates how to use Thorlabs Power Meter Burst Mode. In Burst mode the 
device stores a sequence of measurements for every hardware trigger condition in an internal memory. 

# Details 

The burst mode stores a one or multiple measurements for every hardware trigger condition. You can also
force a trigger condition by software. Once you finished the measurement you can query the measurement results at any speed. Every measurement result will be a tuple (single channel) or tripplet (dual channel). 

For more technical background information about Burst Mode refer to SCPI command description. You can find a description for every Meter in the  [commandDocu](../../../../Python/Thorlabs%20PMxxx%20Power%20Meters/scpi/commandDocu) folder. For example the PM103 [SCPI command description](https://htmlpreview.github.io/?https://github.com/Selanarixx/Light_Analysis_Examples/blob/develop/Python/Thorlabs%20PMxxx%20Power%20Meters/scpi/commandDocu/pm103.html) html file.

## Limitations
Please be aware the burst mode is only available in CW measurement mode. Peak measurement mode 
is not supported.

## Supported Meters
- PM103
- PM103E
- PM5020
- PM62
- PM63
