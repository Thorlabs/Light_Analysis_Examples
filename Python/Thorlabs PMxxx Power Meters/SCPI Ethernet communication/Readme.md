# PM5020 Ethernet Communication

Pyvisa does not work to communicate with PM5020, PM103E and PM60 via Ethernet with SCPI commands.
We provide the Anyvisa library here.
Installation with the command:
```
python -m pip install anyvisa-0.3.0-py3-none-any.whl
```

## Included Examples
The examples also works with PM103E and PM60.

### PM5020 connect to first device found
The sample code shows how to connect to the first device found. 

### PM5020 connect to known device
The sample code shows how to connect to a device where serial number and IP address are known. 
