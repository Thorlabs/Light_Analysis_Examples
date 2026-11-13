# Thorlabs OSA C++ examples

## Included example

This folder contains C++ sample code showing how to control and acquire spectra
from Thorlabs optical spectrum analyzers (OSAs). The example supports the OSA20x
and OSA30x (Redstone) series.

- [AcquireDataFromOSA](AcquireDataFromOSA/README.md): acquire 100 spectra using
  an asynchronous callback, with a virtual Redstone fallback when no physical
  instrument is detected.

## Requirements

- Visual Studio 2022 with the **Desktop development with C++** workload and
  MSVC v143 toolset.
- [ThorSpectra](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=osa),
  including the native C/C++ SDK headers and libraries.
- Windows, x64.

The projects expect ThorSpectra at
`C:\Program Files\Thorlabs\ThorSpectra`. The ThorSpectra DLL directory must be
on `PATH`, which the installer normally configures.

Open `AcquireDataFromOSA.sln` to get started. See the
[example README](AcquireDataFromOSA/README.md) for build and run instructions,
custom installation paths, and troubleshooting.

## More information

Refer to the native SDK documentation included with your ThorSpectra
installation for API details and error codes.
