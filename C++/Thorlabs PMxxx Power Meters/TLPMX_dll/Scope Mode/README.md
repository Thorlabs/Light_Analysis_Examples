# C++ Scope Mode Example
This C++ sample code demonstrates how to use Thorlabs Power Meter Scope Mode. In Scope mode the 
device behaves like an oszillocope. The Meters support Software or Hardware triggers to fill the
internal scope buffer.

# Details 

The scope mode stores all fast measurement results within a fixed size internal buffer. Once the 
buffer is full the scope is disarmed and results can be read out of buffer at any speed. 
Every measurement result will be a tuple (single channel) or tripplet (dual channel). In hardware
triggered scope measurement you can also see samples before the trigger condition. The meter might 
support internal and external hardware trigger signals. 

For more technical background information about Scope Mode refer to SCPI command description. You can find a description for every Meter in the  [commandDocu](../../../../Python/Thorlabs%20PMxxx%20Power%20Meters/scpi/commandDocu) folder. For example the PM103 [SCPI command description](https://htmlpreview.github.io/?https://github.com/Selanarixx/Light_Analysis_Examples/blob/develop/Python/Thorlabs%20PMxxx%20Power%20Meters/scpi/commandDocu/pm103.html) html file.

## Limitations
Please be aware the scope mode is only available in CW measurement mode. Peak measurement mode 
is not supported. 

## Supported Meters
- PM103
- PM103E
- PM5020
- PM6x
