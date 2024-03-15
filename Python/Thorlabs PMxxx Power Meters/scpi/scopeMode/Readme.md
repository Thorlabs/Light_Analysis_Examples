# Scope Examples
The Thorlabs Power Meters supports Scope Mode to measure and store a software or hardware triggered
measurement sequence within the device memory. All python examples in this folder use direclty 
text based SCPI commands with the Thorlabs anyVisa python library for device communication. 

The examples prepare the device for software or hardware triggered Scope Mode measurement, configure the
Scope Measurement itself and fetch and plot the the results are finaly. For plotting the matplotlib 
library is used. 

For more technical background information about scope mode refer to e.g. [SCPI command description](commandDocu/pm5020) html file.

The folder contains 3 examples
## Single Channel Scope - singleChanScope.py
Supported Meters
- PM6x

## PM103 Scope Example - pm103Scope.py
Supported Meters
- PM103
- PM103E

## Dual Channel Scope Example - dualChanScope.py
- PM5020

## matplotlib python library
You can download and install matplotlib library using pip. 

```
python -m pip install matplotlib
```
### anyvisa python Library
You can download anyvisa library wheel in this Github repository. Please refer to this [README](anyvisa) how to install it. 
