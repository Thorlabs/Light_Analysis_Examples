# Ethernet Raw Socket Communication 
This python command line sample demonstrates how to communicate with a Thorlabs Ethernet capable power meter using
raw python socket communication without any additional library like anyvisa.

# Details 
The powermeter uses a binary protocol to frame large request/response messages to multiple TCP packets. The given codes
uses synchronous IO to implement this binary protocol for data exchange. The example does not contain any network device
discovery. You need to know the IP and port number of the power meter to connect. Once the connection is established you
can use the methods to send and receive text and binary request and response data. The implementation is totally platform
independent. 

For more technical background information about fast mode refer to SCPI command description. You can find a description for 
every Meter in the  [commandDocu](../commandDocu) folder. For example the PM103E [SCPI command description](https://htmlpreview.github.io/?https://github.com/Selanarixx/Light_Analysis_Examples/blob/develop/Python/Thorlabs%20PMxxx%20Power%20Meters/scpi/commandDocu/pm103E.html) html file.

## Limitations
Please be aware the power meter will close the connection automatically if no communication is ongoing for 30 seconds.
If you send an ernous (e.g. an unkown SCPI command) request, the receive function will issue a timeout error as the
device does not send any response data. 

## Supported Meters
- PM103E
- PM5020
