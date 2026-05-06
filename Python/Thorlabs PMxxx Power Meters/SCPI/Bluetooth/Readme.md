## Bluetooth examples with SCPI commands

After turning on the bluetooth powermeter, bluetooth has to be activated in the Windows settings.
The PM160* are classical bluetooth devices. They will appear with an incoming and a outgoing COM port in the Windows Device Manager.
The outgoing COM port number has to be used in the Python example to open a serial connection.

The PM100D3 and PM61* are bluetooth low energy (BLE) devices. They will not appear in the Windows Device Manager as a COM port. The anyvisa library is used in the example.
