# Thorlabs PMxxx Power Meters — Rust Example (Linux, USBTMC/SCPI)

Rust port of the C++ SCPI example (`C++/Thorlabs PMxxx Power Meters/scpi/PMXXX_SCPI.cpp`).
The C++ version talks to the meter through NI-VISA on Windows; this one talks to the
**Linux kernel USBTMC driver** (`/dev/usbtmc*`) directly, so it needs:

- no NI-VISA / Thorlabs TLPMX driver,
- only one small third-party crate (`nix`, used solely for the USBTMC ioctls) —
  everything else is the Rust standard library,
- any Linux host where the `usbtmc` kernel driver is enabled (virtually all distros).

Works with the USBTMC-based Thorlabs power meters (PM100D/PM100D2, PM101/102/103/104,
PM5020, ...) on e.g. x86_64 or ARM64 boards.

SCPI command documentation for these instruments can be found in
[`Python/Thorlabs PMxxx Power Meters/SCPI/commandDocu/`](../../../Python/Thorlabs%20PMxxx%20Power%20Meters/SCPI/commandDocu/).

## What the example does

1. Enumerates `/dev/usbtmc*` nodes belonging to Thorlabs instruments (USB vendor id `0x1313`).
2. Opens the meter, asserts USB488 Remote Enable and reads `*IDN?`.
3. Sets the sensor correction wavelength (`SENSE:CORRECTION:WAVELENGTH`) and verifies it.
4. Sets the averaging rate (`SENSE:AVERAGE`) and verifies it.
5. Blocking mode: `MEASURE:POWER?` + `SENS1:TEMP:DATA?` readings in a loop.
6. Continuous mode (manual §"Continuous Measurements"): `ABOR` → `CONF:POW` →
   `INIT:CONT`, then poll `FETC:STAT?`, fetch binary results with
   `FETC:BINA? 0,1000,0`, and read the temperature non-invasively with
   `SENS1:TEMP:DATA?` — power and temperature are acquired together without
   interrupting the measurement (roughly 5× faster per sample than `MEAS?`).

## Build and run

```bash
cargo run --release                # defaults: 800 nm, averaging 1000, 10 samples
cargo run -- --wavelength 1550 -n 5 -i 100
cargo run -- --skip-config         # leave the meter configured, just read
cargo run -- --device /dev/usbtmc0
```

Example output (PM100D2):

```
/dev/usbtmc0 connected.
Remote enable (REN) asserted.
IDN: Thorlabs,PM100D2,P00XXXXXX,1.5.0
The wavelength is set to 800 nm
The average rate is set to 1000
--- [1/2] Blocking one-shot acquisition (MEASure?) ---
Reading 10 power samples...
Sample [1756741600123]  0:  2.998700e-5 W temp:24.85
Sample [1756741601201]  1:  3.001100e-5 W temp:24.85
...
[MEAS?  ] Mean power: 3.000200e-5 W (min 2.998700e-5, max 3.001900e-5, n=10)

--- [2/2] Continuous non-blocking acquisition (INIT:CONT + FETC:BINA?) ---
Reading 10 power samples in continuous mode...
Sample [1756741605321]  0: 2.998700E-5 W temp: 24.85
Sample [1756741606455]  1: 3.001100E-5 W temp: 24.85
...
[INIT:CONT] Mean power: 3.000200e-5 W (min 2.998700e-5, max 3.001900e-5, n=10)
Program finishes.
```

## Permissions (one-time setup)

`/dev/usbtmc*` nodes are owned by `root` by default. To allow a normal user to
access Thorlabs instruments, install the udev rule from this folder:

```bash
sudo cp 99-thorlabs-usbtmc.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger           # or unplug/replug the power meter
```

The rule grants the `plugdev` group read/write access to every `usbtmc` device with
Thorlabs' USB vendor id:

```
# 99-thorlabs-usbtmc.rules
KERNEL=="usbtmc*", ATTRS{idVendor}=="1313", MODE="0660", GROUP="plugdev"
```

Without the rule you can still run the example with `sudo`.

## Notes

> **Disclaimer:** the remarks in this section (including the PM100D2/PM100D3 notes
> below) come mostly from hands-on testing against a single PM100D2 (fw 1.0.7).
> Statements about other models or firmware versions, and details taken from the
> SCPI manual without local reproduction, have **not been further verified** —
> they are provided for reference only.

- Each `write()` to `/dev/usbtmcN` is sent as one complete USBTMC message, so one
  `write` per SCPI command is the correct pattern (no stream buffering).
- `MEASURE:POWER?` answers in watts. Use `SENSE:POW:UNIT DBM` first if you prefer dBm
  (not further verified).
- The averaging rate trades measurement speed for noise: with 1000 the meter averages
  1000 ADC readings internally, so each query takes correspondingly longer
  (per the manual; not further verified).
- For Windows (NI-VISA) or the Thorlabs TLPMX driver, see the C++ and Python folders.

### PM100D2/PM100D3 specific: Remote Enable (REN) is mandatory

Handheld battery-powered meters (PM100D2, fw 1.0.7) stay in **local mode after every
cold boot and ignore all SCPI traffic** until the host asserts the USB488 **Remote
Enable** control request (`USBTMC488_REQUEST_REN_CONTROL`, wValue=1). NI-VISA does
this automatically when a session is opened on Windows, which is why those meters
"only work on Windows". The stock Linux `usbtmc` driver never asserts REN by itself.

This example mirrors the full NI-VISA session ritual, observed in a USB capture of
a Windows host:

1. on open: assert REN (`enable_remote_mode()`, an `ioctl(USBTMC488_IOCTL_REN_CONTROL)`
   via the `nix` crate) and wait 600 ms — the firmware needs that settle time
   before it processes commands;
2. on close (via `impl Drop`): `GOTO_LOCAL` then REN(0), releasing the meter the
   same way NI-VISA does. Skipping this closing ritual and repeatedly starting
   sessions with a bare REN(1) can wedge the firmware state machine after a few
   runs; if that happens, either recover from the front panel (*Connectivity* →
   *GO local*) or use the `USBTMC_IOCTL_CLEAR_IN_HALT` + `USBTMC_IOCTL_CLEAR`
   ioctls on `/dev/usbtmcN` (recovery recipe not further verified).

Other quirks of these meters (same caveat: partly from the manual or
single-device observations, not further verified — for reference only):

- **A query that gets no response wedges the whole remote interface** (the screen USB
  icon turns red while blocked). If that happens, the meter can be released from its
  front panel: in the *Connectivity* menu, select *GO local*. Verified offenders on
  PM100D2 fw 1.0.7: any undefined
  header such as `FETCH:TEMP?`, `SENSe3:TEMPerature:DATA?` (channel only exists on the
  PM100D3), and — surprisingly — the **long-form/no-suffix spelling**
  `SENSe:TEMPerature:DATA?`. The firmware command parser only handles the
  **short form with an explicit suffix: `SENS1:TEMP:DATA?`**, which works fine,
  is non-blocking and returns the last temperature (~1–2 Hz refresh). Always
  use that spelling; `MEASure:TEMPerature?` also works but is a full
  ABOR;CONF;INIT;FETC sequence (~400 ms) that aborts a running continuous measurement.
- `MEAS?`/`FETC?` may block the interface for up to 10 s — the kernel driver's
  default read timeout is only 5 s, so this example raises it to 15 s
  (`USBTMC_IOCTL_SET_TIMEOUT` in `ScpiInstrument::open`).
- Before fetching from a continuous run, always `CONF:POW` once — `FETC?` returns
  whatever unit was configured last (e.g. temperature after a `MEAS:TEMP?`).
- Per the official SCPI manual: when a `MEAS?`/`READ?`/`FETC?` query times out
  (e.g. no light pulses with a photodiode in peak mode), **do not send any further
  command (including `ABOR`) for at least 10 seconds**, otherwise "communication will
  crash totally" and only a full power cycle recovers it.
- A negative power reading of tens of µW with the sensor dark is normal zero-offset
  noise; run `SENSe:CORRection:COLLect:ZERO` (with the sensor covered) to zero it
  (from the manual; not further verified).
