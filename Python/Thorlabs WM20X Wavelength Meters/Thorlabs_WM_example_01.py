"""
Thorlabs_VM_example_01
Example Date of Creation: 2025-08-22
Example Date of Last Modification on Github: 2025-08-22
Version of Python: 3.12.4
==================
Example Description: Read the wavelength from Thorlabs Wavelength Meter WM20X using TCP
"""
import time
import socket
import struct

# Set the address to the IP number of your wavelength meter
wavemeteradress = "192.168.55.6"

def build_request_frame(cmd):
    # This creates the TCP frames that are sent to the wavelength meter.
    # The basic example only supports single frame requests
    # Full example of the TCP frames can be found with the PM5020 examples
    payload = cmd.encode()
    FRAME_START = 0xCA
    return struct.pack('<BBH', FRAME_START, 0, len(payload)) + payload

def recv_response(sock):
    # Recieves and parses a TCP packet from the wavelength meter.
    data = b''
    seq = 0
    HEADER_SIZE = 4
    while True:
        # Loop because response might be multi frame
        hdr = sock.recv(HEADER_SIZE)
        if len(hdr) < HEADER_SIZE:
            break
        start, cnt, plen = struct.unpack('<BBH', hdr)
        if cnt != seq:
            break
        part = sock.recv(plen)
        data += part
        if start != 0xCB:
            break  # no more frames
        seq += 1
    return data.decode(errors='ignore')

def send_cmd(sock, cmd):
    # Build and send a SCPI command to the wavelength meter
    sock.sendall(build_request_frame(cmd))

def request_response(sock, cmd):
    # Send a SCPI command to the wavelength meter and 
    # read the answer from it
    send_cmd(sock, cmd)
    return recv_response(sock)

with socket.create_connection((wavemeteradress, 2000), timeout=5) as s:
    while True:
        try:
            response = request_response(s, "MEAS:WAV?\n")
            wavelength = float(response.strip())
            print(f"{wavelength} nm(vac)")
        except Exception as e:
            print(e)
            time.sleep(1)