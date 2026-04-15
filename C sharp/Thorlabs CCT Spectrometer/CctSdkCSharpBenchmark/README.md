# CCT SDK .NET Benchmark Application

## Required NuGet Packages

- Thorlabs.ManagedDevice
- Thorlabs.ManagedDevice.SerialPortDriver
- Thorlabs.ManagedDevice.EthernetPortDriver
- Thorlabs.ManagedDevice.JetiBoardDriver
- Thorlabs.ManagedDevice.CompactSpectrographDriver
- Thorlabs.SpectraData
- Thorlabs.SharedUtils

Distributed in folder `NuGet`, which is referenced by its relative path in *NuGet.Config* file.


## Structure of the Benchmark Application Example

Benchmark Application Example is a Console Application, which connects to first available Spectrometer and performs the following workflow:
- Sets acquisition parameters: Exposure and amount of frames for Hardware Averaging.
- Acquire series of Spectra.
- Evaluate effective frame rate within the series.
- Save Benchmark results along with stamps of each acquired spectrum frame into a file.
After workflow is finished, the Application disposes all SDK objects and exits.

Base structure of this Application is represented on code snippet below:

```csharp
internal static class Program
{
  private static async Task Main(string[] args)
  {
    /*
     * Initialialization section with basic connection to the SDK
     */

    try
    {
      /*
       * Application code of using the Compact Spectrometer SDK
       */
    }
    catch (Exception e)
    {
      /*
       * Report on any uhandled Exceptions into Console
       */
    }
    finally
    {
      /*
       * Dispose of objects.
       */
    }
  }
}

```

For interraction with Operator Console output is added from each execution step. 
Instead of using method `Console.WriteLine(string)` example implementation of the `Microsoft.Extensions.Logging.ILogger` interface is used from the driver library, 
it also includes tracing into a file in folder "%TEMP%\Thorlabs\CCT_SDK".
The CCD Software Driver supports any logger implementing the `Microsoft.Extensions.Logging.ILogger` interface.
For example, in an Application with use of Dependency Injection, into constructor (as shown below) can be passed loggers created by `LoggerFactory` Factory of the .NET.


## Connection to a Spectrometer

An object, which runs automatic discovery of Compact Spectrometers connected via USB and Ethernet 
and makes sure that they are in up and running state, 
can be initialized via Constructor without parameters below:

```csharp
var startupHelper = 
	new Thorlabs
		.ManagedDevice
		.CompactSpectrographDriver
		.Workflow
		.StartupHelperCompactSpectrometer(logger);
```

Running of the device discovery and establishing connections can be made awaited using an asynchronous routine listed below. 
Same Method can be used for syncing states of the Spectrometers when hardware connections have changed.

```csharp
IEnumerable<string> discoveredDevices = await startupHelper
	.GetKnownDevicesAsync(cancellationToken);
```

When IP-Address of Ethernet connected Spectrometer is not discoverable via UDP Broadcasting,
its IP Address can be provided for direct accessing into an IP Address registration Method:
```csharp
startupHelper.RegisterEthernetIpAddress("192.168.0.160");
```

The device discovery routine returns a list of string identifiers of all available Spectrometers.
A handle to particular Spectrometer can be retrieved then from Method `GetCompactSpectrographById``.
The Example Application takes just a first one from the list:
```csharp
string? deviceId = discoveredDevices.FirstOrDefault();

Thorlabs.ManagedDevice.CompactSpectrographDriver.ICompactSpectrographDriver? spectrometer = 
    startupHelper.GetCompactSpectrographById(deviceId);
```


## Set Acquisition Parameters

Sensor Exposure for single spectrum frame is handled in milliseconds via a value of type `float`.
For benchmarking purposes it is set to minimum possible value of 0.01 ms:
```csharp
bool resultExposure = await spectrometer
	.SetManualExposureAsync(
		exposure: 0.01f, cancellationToken);

// getter of current setting
float currentExposure = spectrometer.ManualExposure;
```

Averaging of multiple spectrum frames on the Spectrometer Hardware before sending data to the Client Software is counted via a value of type `int`.
For benchmarking purposes it is set to minimum possible value of single frame acquisition:
```csharp
bool resultAve = await spectrometer
	.SetHwAverageAsync(
		ave: 1, cancellationToken);

// getter of current setting
int currentAve = spectrometer.HwAverage;
```


## Acquire of series of Spectra

The Spectrum acquisition method runs measurement at current settings for certain large number times:
```csharp
for (ulong i = 0; i < amount; i++)
{
	Thorlabs.ManagedDevice.CompactSpectrographDriver.Dataset.ISpectrumXY? spectrumOutput =
		await spectrometer.AcquireSingleSpectrumAsync(cancellationToken);

	if (spectrumOutput == null)
	{
		logger.LogInformation($"Cannot acquire Spectrum - application will be stopped.");
		return;
	}
	else
	{
		ticks[i] = spectrumOutput.Tick;
	}
}
```

Along with Spectrum data each returned dataset contains the following related information:

- Dispersion Correction: Property `Wavelength`, an array of `double` values;
- Timestamp of the measurement: Property `Acquired` of type `DateTime`. Additionally, a Stamp of Microseconds ticks from the Spectrometer CPU is stored in Property `Tick` of type `ulong`;
- Sensor Exposure in milliseconds: Property `SensorExposureMs` of type `float`;
- Amount of Frames averaged on the Spectrometer Hardware: Property `HardwareAverage` of type `int`;
- Whether the Spectrum Acquisition of this frame was triggered by Input Trigger Event: Property `InputHardwareTrigger` of type `bool`;
- Whether Amplitude Correction was applied to measured Spectrum intensity: Property `AmplitudeCorrected` of type `bool`.

For frames distinguishing and time counting purposes, value of Property `Tick` is bufferred.
	
The Spectrum intensity values itself are stored in Property `Intensity` of the returned dataset, which is an array of `double` values. 


## Results representaion

Example output from the Benchmark Application run:

- CCT10 Spectrometer with 2048 pixels

```
Handshaking Timestamp:	2024-12-05T09:47:00.8887756Z
Handshaking Ticks:	340731592 microseconds

Benchmark started:	2024-12-05T10:47:01.2587665+01:00
Benchmark finished:	2024-12-05T10:47:31.8712984+01:00

Amount of acquisitions:	10000 Spectra
Single Exposure Time:	0,01 ms
Hardware Averaging:	1 Frames

Ticks of First:	341108474 microseconds
Ticks of Last:	371708209 microseconds

Average period between Spectra:	3,06 ms
Frame Rate:	326,8 Hz
```

- CCT12 Spectrometer with 4096 pixels

```
Handshaking Timestamp:	2024-12-05T11:00:59.7685820Z
Handshaking Ticks:	15535471 microseconds

Benchmark started:	2024-12-05T12:01:00.2085536+01:00
Benchmark finished:	2024-12-05T12:01:57.4210563+01:00

Amount of acquisitions:	10000 Spectra
Single Exposure Time:	0,01 ms
Hardware Averaging:	1 Frames

Ticks of First:	15987619 microseconds
Ticks of Last:	73177983 microseconds

Average period between Spectra:	5,72 ms
Frame Rate:	174,9 Hz
```