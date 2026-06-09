"""
EPG1_pyserial
Example Date of Creation: 2026-06-09
Example Date of Last Modification on Github: 2026-06-09
Version of Python: 3.13
Version of the Thorlabs SDK used: -
==================
Example Description: The example shows how to use SCPI commands in Python with pyserial. It shows how to connect to the EPG1 controller, query some information, set some parameters and close the connection. 
"""

import serial
import time

def main():
    #Make the COM port settings 
    baud_rate = 9600
    data_bits = 8
    stop_bits = 1
    Parity = serial.PARITY_NONE
    time_out=1
    #Change this to the COM port of the EPG1 controller.
    #The COM port number can e.g. be seen in the device manager.
    COM_port = "COM10"
    ser = serial.Serial(port = COM_port, baudrate = baud_rate, bytesize=data_bits, parity=Parity, stopbits=stop_bits,timeout=time_out)
    time.sleep(2) #Wait for the connection to be established.

    print(query_command(ser,'SYStem:PRODUCT?')  ) 

    print("Serial number: ", query_command(ser,'SYStem:SERial?')   )
    
    status=query_command(ser,'SYStem:STATus?')
    print("System status code: ", status)   
    if status == '0':
        print("System status: Not ready, unit booting")
    elif status == '1':
        print("System status: Ready to accept commands")
    elif status == '2':
        print("System status: Instrument busy, cannot accept commands")
    
    write_command(ser, 'TRIGGER: 0')#Trigger set to internal.

    write_command(ser,'REPRATE: 2')#Set the repetition rate to 0.2 Hz.
    
    response=query_command(ser,'REPRATE?')#Query the repetition rate to confirm it is set correctly.
    repetition_rate = int(response) * 0.1 #Convert the response to Hz.
    print("Repetition rate set to: ", repetition_rate, "Hz")
   
    write_command(ser,'PULSE1:WIDth: 0.001')#Set the pulse width to 1 ms.
    print("Pulse width set to: ", query_command(ser,'PULSE1:WIDth?'))#Query the pulse width to confirm it is set correctly.

    write_command(ser,'PULSE1:ENable: 1')#Enable the pulse output.
   
    ser.close()
    print("Serial connection closed.")
    del ser

def write_command(ser, command):
    ser.write(command.encode('utf-8') + b'\n')
    response= (ser.readline()).decode('utf-8').strip()
    if response!='1':
        print("writing command failed: ", command, " response: ", response)

def query_command(ser, command):
    ser.write(command.encode('utf-8') + b'\n')
    response= (ser.readline()).decode('utf-8').strip()
    return response

if __name__ == "__main__":
    main()