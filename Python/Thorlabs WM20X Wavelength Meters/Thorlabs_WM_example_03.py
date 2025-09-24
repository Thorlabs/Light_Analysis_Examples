"""
Thorlabs_VM_example_03
Example Date of Creation: 2025-08-22
Example Date of Last Modification on Github: 2025-08-22
Version of Python: 3.12.4
Version of Platform Firmware: 0.9.12
Version of Interferometer Firmware: 0.58
==================
Example Description: Read the wavelength from Thorlabs WM20X Wavelength Meter using RS232
"""
import time
import serial

ser = serial.Serial("COM7", 115200, timeout=2) # Modify COM7 to your serial port

def request_response(cmd):
    # This writes a command to the serial port,
    # and then waits for the answer and returns it.
    ser.write(cmd.encode())
    response = ser.readline().decode('utf-8')
    return f"{response}"

while True:
    try:
        response = request_response("MEAS:WAV?\n")
        wavelength = float(response.strip())
        print(f"{wavelength} nm(vac)")
    except Exception as e:
        print(e)
        time.sleep(1)