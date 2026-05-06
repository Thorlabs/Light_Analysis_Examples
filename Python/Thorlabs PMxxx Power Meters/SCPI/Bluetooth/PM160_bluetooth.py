"""
PM160_bluetooth.py
Example Date of Creation: 2026-05-06
Example Date of Last Modification on Github: 2026-05-06
Version of Python: 3.13
Version of the Thorlabs SDK used: -
==================
Example Description: The example shows how to connect a PM160 powermeter with Bluetooth and acquire a measurement. 
tested with PM160T
"""
import serial
import time

def open_bt_port():
    for attempt in range(3):
        try:
            print(f"Opening COM4 (try {attempt+1})...")
            ser = serial.Serial(
                port="COM4",#check device manager for correct COM port number
                baudrate=9600,
                timeout=1,
                write_timeout=1
            )
            return ser
        except serial.SerialException as e:
            print("Open failed:", e)
            time.sleep(2)
    raise RuntimeError("Bluetooth COM port not available")

def main():
    ser = open_bt_port()

    time.sleep(2.0)
    ser.reset_input_buffer()

    ser.write(b"*IDN?\n")
    time.sleep(0.3)
    print(ser.readline().decode(errors="ignore"))

    ser.write(b"MEAS?\n")
    time.sleep(0.3)
    print("Measurement value:", ser.readline().decode(errors="ignore"))

    ser.close()

if __name__ == "__main__":
    main()
