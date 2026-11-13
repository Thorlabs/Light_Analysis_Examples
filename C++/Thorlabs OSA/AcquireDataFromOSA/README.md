# AcquireDataFromOSA

`AcquireDataFromOSA` is a Windows x64 console example that uses the native
ThorSpectra SDK (`FTSLib`) to acquire spectra from a Thorlabs optical spectrum
analyzer.

## Requirements

- Visual Studio 2022 with the **Desktop development with C++** workload and
  MSVC v143 toolset.
- Thorlabs ThorSpectra installed, including the SDK headers and libraries.
- An OSA20x or Redstone instrument, or the virtual Redstone used automatically
  when no physical instrument is detected.

The project expects ThorSpectra at:

```text
C:\Program Files\Thorlabs\ThorSpectra
```

It reads headers from `include` and links `FTSLib.lib` from `lib` under that
directory. The ThorSpectra DLL directory must be on `PATH`; the ThorSpectra
installer normally configures this.

## Build and run

1. Install ThorSpectra before opening Visual Studio so the updated `PATH` is
   available. Restart Visual Studio if it was already open.
2. Open `AcquireDataFromOSA.sln` in the parent directory.
3. Select **Debug** or **Release**, with platform **x64**.
4. Build the solution, then run with **Ctrl+F5**.

For a non-default ThorSpectra installation, set the `ThorSpectraDir` MSBuild
property. For example, from a Visual Studio Developer PowerShell in the
parent directory:

```powershell
msbuild .\AcquireDataFromOSA.sln /p:Configuration=Release /p:Platform=x64 /p:ThorSpectraDir="D:\Thorlabs\ThorSpectra"
```

To use the custom path in Visual Studio, set the `ThorSpectraDir` environment
variable before starting Visual Studio. The project uses it unless the MSBuild
property is explicitly overridden.

## What the example does

1. Discovers physical instruments and opens instrument index `0`. If none are
   found, it creates a virtual Redstone OSA305 with a simulated LLD1530 source.
2. Sets low resolution and low sensitivity using the settings for the detected
   OSA20x or Redstone series.
3. Starts continuous acquisition and reads spectrum arrays in an asynchronous
   callback.
4. Counts spectra from connected instrument and prints acquisition progress.
5. Stops after 100 spectra, a five-minute timeout, an acquisition error, or a
   user stop, then clears callbacks and closes the instrument.

Press **Q** or **Esc** during acquisition to stop early.

The example reads spectrum data into memory but does not save files or plot
the data. To process or export the values, extend `ReadOutSpectrum()` in
`AcquireDataFromOSA.cpp`.

## Troubleshooting

- **Headers or `FTSLib.lib` not found:** check the ThorSpectra installation path
  and the `ThorSpectraDir` property.
- **DLL not found at startup:** check that the ThorSpectra DLL directory is on
  `PATH` and restart Visual Studio after changing it.
- **A virtual instrument is used unexpectedly:** no physical instrument was
  detected. Check the instrument connection and that ThorSpectra can detect it.
- **An SDK operation fails:** the console prints the operation and its numeric
  error code. Refer to the installed SDK documentation for the code's meaning.
