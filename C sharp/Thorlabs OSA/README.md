# Thorlabs OSA C# examples

These examples are C# counterparts to the five Python examples at [GitHub](
https://github.com/Thorlabs/Light_Analysis_Examples/tree/main/Python/Thorlabs%20OSA).
They use `ThorlabsOSAWrapper.dll` directly and target .NET Framework 4.7.2, x64.

## Compatibility

- Example last updated: 2026-11-03
- Development environment: Visual Studio 2022
- Target framework: .NET Framework 4.7.2
- Platform: x64
- Thorlabs SDK: ThorSpectra 3.40

Projects:

- `Thorlabs_OSA_example_01`: acquire and print one spectrum.
- `Thorlabs_OSA_example_02`: acquire every supported resolution/sensitivity combination and save SPF2 files.
- `Thorlabs_OSA_example_03`: select or pass an SPF2 measurement and run peak-track or wavemeter analysis.
- `Thorlabs_OSA_example_04`: continuous spectrum/interferogram acquisition with peak-track and wavemeter analysis.
- `Thorlabs_OSA_example_05`: continuously print the strongest peak position over time.
- `Thorlabs_OSA_GUI`: simple WinForms live spectrum/interferogram viewer.

The projects expect ThorSpectra at:

`C:\Program Files\Thorlabs\ThorSpectra`

If it is installed elsewhere, set the `ThorSpectraPath` MSBuild property. For
example:

```powershell
msbuild CSharpExamples.sln /p:Configuration=Release /p:Platform=x64 /p:ThorSpectraPath="D:\Thorlabs\ThorSpectra"
```

The examples connect to instrument index 0. Press `Q` or `Ctrl+C` to stop the
continuous console examples cleanly.
