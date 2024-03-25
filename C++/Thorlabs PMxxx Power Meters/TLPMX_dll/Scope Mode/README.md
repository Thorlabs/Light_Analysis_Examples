# C++ Scope Mode Example
This C++ sample code demonstrates how to use Thorlabs Power Meter Scope Mode. In Scope mode the 
device behaves like an oszillocope. The Meters support Software or Hardware triggers to fill the
internal scope buffer.

# Details 

The scope mode stores all fast measurement results within a fixed size internal buffer. Once the 
buffer is full the scope is disarmed and results can be read out of buffer at any speed. 
Every measurement result will be a tuple (single channel) or tripplet (dual channel). In hardware
triggered scope measurement you can also see samples before the trigger condition. The meter might 
support internal and external hardware trigger signals. For closer details refer to the Scope Mode description in the [SCPI command](scpiTODO)
description. 

## Limitations
Please be aware the scope mode is only available in CW measurement mode. Peak measurement mode 
is not supported. 

## Supported Meters
- PM103
- PM103E
- PM5020
- PM6x
