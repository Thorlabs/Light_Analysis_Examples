#Tested with Python 3.10, 64 bit

#Import the PyVISA and time library to Python.
import pyvisa
import time

#Opens a resource manager
rm = pyvisa.ResourceManager()

#Opens the connection to the device. The variable instr is the handle for the device.
# !!! In the USB number the serial number (M00...) needs to be changed to the one of the connected device.
instr = rm.open_resource('USB0::0x1313::0x80C8::M00460202::INSTR')

#The command instr.query can be used when you want to get data from the device.
# *IDN? returns the identification of the device.
print("Used device:", instr.query("*IDN?"))


#The command instr.write can be used to write data to the device when you do not expect a response from the device.
#Set the DC2200 to constant current mode, set the current, switch the LED on.
instr.write("SOURCE1:MODE CC")
instr.write("SOURCE1:CCURENT:CURRENT 0.01")
instr.write("OUTPUT1:STATE ON")
print("Switch LED on.")

time.sleep(1)

#Query the current applied to the LED and switch the LED off.
print("Applied LED current [A]:", instr.query("SENSE3:CURRENT:DATA?"))

instr.write("OUTPUT1:STATE OFF")

time.sleep(1)

#Set the DC2200 to PWM mode, set the current, frequency, duty cycle and number of pulses.
instr.write("SOURCE1:MODE PWM")
instr.write("SOURCE1:PWM:CURRENT 0.01")
instr.write("SOURCE1:PWM:FREQUENCY 5")
instr.write("SOURCE1:PWM:DCYCLE 50")
instr.write("SOURCE1:PWM:COUNT 20")

#Start the PWM mode for the set number of pulses.
instr.write("OUTPUT1:STATE ON")
print("Start 20 pulses.")

#Close the handle to the device and the resource manager.
instr.close()
rm.close()
