# Scope Examples
The Thorlabs Power Meters supports Scope Mode to measure and store a software or hardware triggered
measurement sequence within the device memory. All python examples in this folder use direclty 
text based SCPI commands with the Thorlabs anyVisa python library for device communication. 

The examples prepare the device for software or hardware triggered Scope Mode measurement, configure the
Scope Measurement itself and fetch and plot the the results are finaly. For plotting the matplotlib 
library is used. 

For more technical background information about scope mode refer to SCPI command description. You can find a description for every Meter in the  [commandDocu](../commandDocu) folder. For example the PM103 [SCPI command description](https://htmlpreview.github.io/?https://github.com/Selanarixx/Light_Analysis_Examples/blob/develop/Python/Thorlabs%20PMxxx%20Power%20Meters/scpi/commandDocu/pm103.html) html file.

The folder contains 3 examples
## Single Channel Scope - singleChanScope.py
Supported Meters
- PM6x

## PM103 Scope Example - pm103Scope.py
Supported Meters
- PM103
- PM103E

## Dual Channel Scope Example - dualChanScope.py
Supported Meters
- PM5020

## matplotlib python library
You can download and install matplotlib library using pip. 

```
python -m pip install matplotlib
```
### anyvisa python Library
You can download anyvisa library wheel in this Github repository. Please refer to this [README](anyvisa) how to install it. 
