# CCT SDK .NET Examples

## Required NuGet Packages

- Thorlabs.ManagedDevice
- Thorlabs.ManagedDevice.SerialPortDriver
- Thorlabs.ManagedDevice.EthernetPortDriver
- Thorlabs.ManagedDevice.JetiBoardDriver
- Thorlabs.ManagedDevice.CompactSpectrographDriver
- Thorlabs.SpectraData
- Thorlabs.SharedUtils

Distributed in folder `NuGet`, which is referenced by its relative path in *NuGet.Config* file.


## Source Code explanation of the .NET Example

### Structure of the .NET Example

.NET Example is a Console Application, which connects to first available Spectrometer and performs the following workflow:
- Sets acquisition parameters: Exposure and amount of frames for Hardware Averaging.
- Capture Dark Spectrum with closed Shutter for this purpose.
- Acquire Spectrum.
- Save acquired Spectrum data into a file.

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
       * Example code of using the Compact Spectrometer SDK
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


### Connection to a Spectrometer

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


#### Devices Discovery parameters

When Virtual device is needed to be initialized as well, enable this via flag WithVirtual as listed below.
Then after further initialization the Virtual Device will be available with Device ID: "CCT10-VIRTUAL".

```csharp
startupHelper.WithVirtual = true;
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


#### Auto Discovery and Retrieve of the Spectrometer object

The device discovery routine returns a list of string identifiers of all available Spectrometers.
A handle to particular Spectrometer can be retrieved then from Method `GetCompactSpectrographById``.
The Example Application takes just a first one from the list:
```csharp
string? deviceId = discoveredDevices.FirstOrDefault();

Thorlabs.ManagedDevice.CompactSpectrographDriver.ICompactSpectrographDriver? spectrometer = 
    startupHelper.GetCompactSpectrographById(deviceId);
```


#### Manual disconnect and reconnect

When needed for long running services, the Spectrometer can be temporary disconnected in order to release the Hardware resource for other clients, 
e.g. for using in the ThorSpectra Software. The disconnection operation runs immediately:
```csharp
bool disconnected = await startupHelper.SetSpectrometerDisconnectedByIdAsync(deviceId);
```
Later, if it is needed to reconnect to the Spectrometer after other client closed its interaction with the Hardware, the Spectrometer can be connected back.
However, the connection routine will be only scheduled for the next run of the device discovery routine. Full listing for this operation is below:
```csharp
bool reconnect = await startupHelper.SetSpectrometerDisconnectedByIdAsync(deviceId, connectBack: true);
_ = await startupHelper.GetKnownDevicesAsync(cancellationToken);
```


### Set Acquisition Parameters

#### Exposure

Sensor Exposure for single spectrum frame is handled in milliseconds via a value of type `float`:
```csharp
bool resultExposure = await spectrometer
	.SetManualExposureAsync(
		exposure: targetExposure, cancellationToken);

// getter of current setting
float currentExposure = spectrometer.ManualExposure;
```

#### Hardware Averaging

Averaging of multiple spectrum frames on the Spectrometer Hardware before sending data to the Client Software is counted via a value of type `int`:
```csharp
bool resultAve = await spectrometer
	.SetHwAverageAsync(
		ave: targetAve, cancellationToken);

// getter of current setting
int currentAve = spectrometer.HwAverage;
```


#### Input Hardware Trigger

By default Spectrometer is acquiring in Free Running Mode. Events from Input Hardwware Trigger can be used for starting acquisition after switching the Mode using method listed below.
When Input Hardware Trigger is used, two methods of collecting spectra data for hardware averaging are available. 
By default, each spectrum frame requires own Trigger Event and output spectrum is sent by Spectrometer to client Software only after all necessary frames are collected and averaged. 
Otherwise acquisition of all necessary spectrum frames for hardware averaging is started immediately on a single Trigger Event.
Also, default slope of the TTL signal, which is taken as Trigger Event is Rising Edge; related argument can be passed to use Falling Edge instead.
Selection of all these parameters is defined in the same method, which controls state of the Input Hardware Trigger, for example:
```csharp
// switch listening from input hardware trigger and define default 
// hardware averaging collection method and TTL Slope for the Trigger Event
bool resultTrig = await spectrometer
	.SetInputHwTriggerAsync(
		enabled: true, aveNoWait: false, slopeFallingEdge: false, cancellationToken);

// getters of current Input Hardware trigger Settings:
bool currentHwAve = spectrometer.HwTriggerIn;
bool currentTriggeredAveragingMode = spectrometer.HwTriggerInAveNoWait;
bool currentInputTriggerSlope = spectrometer.HwTriggerInSlope;
```


#### Output Hardware Trigger

The output Hardware trigger is always issued on the acquisition start, except when its delay exceeds the acquisition time. The delay setting is handled in milliseconds via a value of type `float`.
In order to schedule acquisition start after issuing of the Output Hardware Trigger, this setting should be set to negative value.
```
bool resultDelay = await spectrometer
	.SetOutputHwTriggerDelayAsync(
		delay: targetDelay, cancellationToken);


// getter of current Setting of Delay for Output trigger signal on acquisition start:
float currentOutputTriggerDelay = spectrometer.HwTriggerOutDelayMs;
```


#### Amplitude Correction

When need to use Amplitude Correction for the acquired Spectrum, set related flag as listed below:
```csharp
spectrometer.UseAmplitudeCorrection = true;
```

Dataset containing the Amplitude correction itself along with the dispersion correction can be retrieved from method listed below.
The dataset format is the same as the Measurement Spectrum, explained in [spectrum dataset section](#spectrum-dataset).
```csharp
Thorlabs.ManagedDevice.CompactSpectrographDriver.Dataset.ISpectrumXY calibration = 
	spectrometer.GetActiveDispersionAndAmplitudeCorrection();
```


### Dark Spectrum and control of the Shutter position

When Dark Spectrum is acquired, it is subtracted by the Spectrometer Driver Library from each acquired Spectrum.
This operation is most valuable, when Dark Spectrum is acquired at the same acquisition parameters as target measurement.

The Spectrometer is equiped with a mechanical Shutter for enabling automation of the Dark Spectrum acquisition.
Because movement of the Shutter blade between open and closed positions requires some time, 
it is necessary to wait several tens of milliseconds before starting acquisition in next Shutter position every time the position was changed.

Overall algorithm for updating Dark Spectrum is to close the Shutter, run acquisition and open Shutter back for light measurement:
```csharp
// close the Shutter
bool shutter = await spectrometer.SetShutterAsync(open: false, cancellationToken);

// Mechanical Shutter requires some time to travel into changed position
await Task.Delay(TimeSpan.FromMilliseconds(40));

// acquire Dark Spectrum
bool resultDark = await spectrometer.UpdateDarkSpectrumAsync(drop: false, cancellationToken);

// open the Shutter again
shutter &= await spectrometer.SetShutterAsync(open: true, cancellationToken);

// Mechanical Shutter requires some time to travel into changed position
await Task.Delay(TimeSpan.FromMilliseconds(40));
```

Dropping of the Dark Spectrum:
```csharp
bool resultDarkDrop = await spectrometer
	.UpdateDarkSpectrumAsync(
		drop: true, cancellationToken);
```


### Acquire Spectrum

The Spectrum acquisition method runs measurement at current settings:
```csharp
Thorlabs.ManagedDevice.CompactSpectrographDriver.Dataset.ISpectrumXY? spectrumOutput = 
	await spectrometer.AcquireSingleSpectrumAsync(cancellationToken);
```

After Measurement is done, information on whether the latest spectrum received from the Spectrometer was saturated or not is available from property named `IsSaturated` of type `bool`.
The saturation is detected when at least one pixel has maximum value. 


#### Spectrum Dataset

Along with Spectrum data the returned dataset contains the following related information:

- Dispersion Correction: Property `Wavelength`, an array of `double` values;
- Timestamp of the measurement: Property `Acquired` of type `DateTime`. Additionally, a Stamp of Microseconds ticks from the Spectrometer CPU is stored in Property `Tick` of type `ulong`;
- Sensor Exposure in milliseconds: Property `SensorExposureMs` of type `float`;
- Amount of Frames averaged on the Spectrometer Hardware: Property `HardwareAverage` of type `int`;
- Whether the Spectrum Acquisition of this frame was triggered by Input Trigger Event: Property `InputHardwareTrigger` of type `bool`;
- Whether Amplitude Correction was applied to measured Spectrum intensity: Property `AmplitudeCorrected` of type `bool`.
	
The Spectrum intensity values itself are stored in Property `Intensity` of the returned dataset, which is an array of `double` values. 


### Spectrum Data Serialization

The Example .NET Application contains example how the returned Spectrum Dataset can be serialized into an XML file, 
where names of the XML elements are aligned with related Property names:
```csharp
var serializer = 
	new System.Xml.Serialization
		.XmlSerializer(
			typeof(Thorlabs.ManagedDevice.CompactSpectrographDriver.Dataset.SpectrumXY));

using Stream stream = new FileStream(outputUri, FileMode.Create, FileAccess.Write, FileShare.ReadWrite);

using TextWriter textWriter = new StreamWriter(stream);

serializer.Serialize(textWriter, spectrum);
```

Note, that because .NET XML Serializer requires concrete implementation of an interface for data serialization, 
related Class named `Dataset.SpectrumXY` is used from the Spectrometer Driver Library.


## .NET Example Benchmark Application

.NET Benchmark Application is a Console Application, which is a variation of the .NET Example
with the following difference in usage of the connected spectrometer:
- Sets acquisition parameters to minimum possible Exposure and disable Hardware Averaging.
- Acquire series of Spectra.
- Evaluate effective frame rate within the series.
- Save Benchmark results along with stamps of each acquired spectrum frame into a file.

Overall composition and used SDK methods are the same as in the .NET Example.


## How to Build the .NET Examples

The example Source code is distributed with a C# Project file of the SDK-Style.

The project is configured for multitarget build for .NET Framework 4.8 and .NET 8 on OS Windows and for .NET 8 on other Operating Systems.

Pre-build binaries are available in subfolder `bin`.


### Listing of complete Source code for the .NET Example

```csharp
internal static class Program
{
    private static async Task Main(string[] args)
    {
        #region 0) Initialize workflow

        var logVerbosity = Microsoft.Extensions.Logging.LogLevel.Information;
        Microsoft.Extensions.Logging.ILogger logger = CreateLogger(logVerbosity, withFileOutput: true);

        logger.LogInformation("Started .NET CSharp Example of Thorlabs Compact Spectrometer SDK.");

        using var cts = new CancellationTokenSource();
        var cancellationToken = cts.Token;

        Console.CancelKeyPress += (sender, e) =>
        {
            logger.LogInformation("Application was terminated.");
            cts.Cancel();
            e.Cancel = true;
        };

        var startupHelper = 
            new Thorlabs.ManagedDevice.CompactSpectrographDriver.Workflow
            .StartupHelperCompactSpectrometer(logger);

        /*
         * When Virtual device is needed, enable this via flag WithVirtual as listed below,
         * then after further initialization the Virtual Device will be available with Device ID: "CCT10-VIRTUAL"
         *
        startupHelper.WithVirtual = true;
         */
        
        #endregion

        try
        {
            #region 1) Detect hardware connected via USB or Ethernet

            /*
             * When IP-Address of Ethernet connected Spectrometer is not discoverable via UDP broadcast,
             * provide its IP Address directly
             * 
            startupHelper.RegisterEthernetIpAddress("192.168.0.160");
             */

            // Wait until complete workflow will be executed and get the list of discovered connected Spectrometers
            IEnumerable<string> discoveredDevices = await startupHelper.GetKnownDevicesAsync(cancellationToken);

            #endregion

            #region 2) Connect to up and running Spectrometer
        
            // Select the first available Spectrometer
            string? deviceId = discoveredDevices.FirstOrDefault();

            if (string.IsNullOrEmpty(deviceId))
            {
                logger.LogInformation($"No Compact Spectrometers detected, check USB or Ethernet connection.");
                return;
            }

            Thorlabs.ManagedDevice.CompactSpectrographDriver.ICompactSpectrographDriver? spectrometer = 
                startupHelper.GetCompactSpectrographById(deviceId);

            if (spectrometer == null)
            {
                logger.LogInformation($"Cannot connect to Compact Spectrometer '{deviceId}' - connection manager returned null reference.");
                return;
            }
            else
            {
                logger.LogInformation($"Successfully connected to Spectrometer '{deviceId}'");
            }

            /*
             * When need to use Amplitude Correction for the acquired Spectrum, set the flag as listed below
             * 
            spectrometer.UseAmplitudeCorrection = true;
             */

            #endregion

            #region 3.a) Set Sensor Exposure

            // Specify Sensor Exposure (Integration Time) in ms
            float targetExposure = 8.3f;
            
            // set to target
            bool resultExposure = await spectrometer.SetManualExposureAsync(exposure: targetExposure, cancellationToken);
            
            // get for control check
            float currentExposure = spectrometer.ManualExposure;

            if (Math.Abs(currentExposure - targetExposure) > 0.001f 
                || !resultExposure)
            {
                logger.LogInformation($"Cannot set Sensor Exposure to '{targetExposure}' ms - spectrometer state '{currentExposure}' ms; application will be stopped.");
                return;
            }
            else
            {
                logger.LogInformation($"Exposure set to {currentExposure} ms.");
            }

            #endregion
            
            #region 3.b) Set Hardware Averaging

            // Specify the number of frames for averaging on Spectrometer Hardware
            int targetAve = 5;
            
            // set to target
            bool resultAve = await spectrometer.SetHwAverageAsync(ave: targetAve, cancellationToken);
            
            // get for control check
            int currentAve = spectrometer.HwAverage;

            if (targetAve != currentAve
                || !resultAve)
            {
                logger.LogInformation($"Cannot set Hardware Averaging to '{targetAve}' frames - spectrometer state '{currentAve}' frames; application will be stopped.");
                return;
            }
            else
            {
                logger.LogInformation($"Averaging set to {currentAve} frames.");
            }

            #endregion

            #region 4) Update Dark Spectrum

            // close the Shutter
            bool shutter = await spectrometer.SetShutterAsync(open: false, cancellationToken);

            // Mechanical Shutter requires some time to travel into changed position
            await Task.Delay(TimeSpan.FromMilliseconds(40));

            // acquire Dark Spectrum
            bool resultDark = await spectrometer.UpdateDarkSpectrumAsync(drop: false, cancellationToken);

            if (!resultDark)
            {
                logger.LogInformation($"Cannot update Dark Spectrum - application will be stopped.");
                return;
            }
            else
            {
                logger.LogInformation($"Dark Spectrum updated.");
            }

            // open the Shutter again
            shutter &= await spectrometer.SetShutterAsync(open: true, cancellationToken);

            // Mechanical Shutter requires some time to travel into changed position
            await Task.Delay(TimeSpan.FromMilliseconds(40));

            if (!shutter)
            {
                logger.LogInformation($"Wrong operation of the shutter - application will be stopped.");
                return;
            }

            #endregion

            #region 5) Acquire single Spectrum

            logger.LogInformation($"Acquisition started with overall integration time of {targetExposure * targetAve} milliseconds.");
            
            Thorlabs.ManagedDevice.CompactSpectrographDriver.Dataset.ISpectrumXY? spectrumOutput = 
                await spectrometer.AcquireSingleSpectrumAsync(cancellationToken);
            // alternative source of the latest acquired spectrum is method spectrometer.GetLatestSpectrum() 

            if (spectrumOutput == null)
            {
                logger.LogInformation($"Cannot acquire Spectrum - application will be stopped.");
                return;
            }
            
            DateTime timestamp = spectrumOutput.Acquired;
            logger.LogInformation($"Successfully acquired Spectrum at '{timestamp}'");
            
            // Convert dataset to needed serializable format, e.g.
            var spectrum = spectrumOutput.Clone() as Thorlabs.ManagedDevice.CompactSpectrographDriver.Dataset.SpectrumXY;
            
            if (spectrum == null)
            {
                logger.LogInformation($"Cannot convert data from Spectrum acquired at '{timestamp}'");
                return;
            }

            #endregion

            #region 6) Save Spectrum into File

            string rootFolder = Environment.ExpandEnvironmentVariables(
                Environment.GetEnvironmentVariable(
                    System.Runtime.InteropServices.RuntimeInformation.IsOSPlatform(
                        System.Runtime.InteropServices.OSPlatform.Windows)
                        ? "LocalAppData"
                        : "HOME")
                ?? string.Empty);
            
            string folder = Path.Combine(rootFolder, ".Thorlabs", "CompactSpectrometer", deviceId);
            
            string filename = $"Snapshot_{spectrum.Acquired:yyyy-MM-dd_HH-mm-ss-fff}{Thorlabs.SpectraData.ToolValidation.WorkingExtension}";

            if (!string.IsNullOrEmpty(folder) &&
                Thorlabs.SpectraData.ToolValidation.CheckInvalidCharsInStringForPath(folder) &&
                Thorlabs.SpectraData.ToolValidation.CheckInvalidCharsInStringForFilename(filename))
            {
                Directory.CreateDirectory(folder);

                if (Directory.Exists(folder))
                {
                    string outputUri = Path.Combine(folder, filename);

                    var serializer = new System.Xml.Serialization.XmlSerializer(typeof(Thorlabs.ManagedDevice.CompactSpectrographDriver.Dataset.SpectrumXY));
                    using Stream stream = new FileStream(outputUri, FileMode.Create, FileAccess.Write, FileShare.ReadWrite);
                    using TextWriter textWriter = new StreamWriter(stream);
                    serializer.Serialize(textWriter, spectrum);
                    logger.LogInformation($"Spectrum acquired at '{timestamp}' saved into path: '{outputUri}'");
                }
                else
                {
                    logger.LogInformation($"Cannot create destination path '{folder}' - Spectrum dara acquired at '{timestamp}' will be lost and application stopped.");
                }
            }
            else
            {
                logger.LogInformation($"Cannot define output path after successful acquisition at '{timestamp}' - application will be stopped.");
            }

            #endregion
        }
        catch (Exception e)
        {
            logger.LogInformation($"Error occured: {e.Message}");
            throw;
        }
        finally
        {
            #region 7) Dispose objects and closes Operating System handles for the hardware resources

            // Startup Helper disposes registered connection managers automatically
            startupHelper.Dispose();

            logger.LogInformation("Finished .NET CSharp Example of Thorlabs Compact Spectrometer SDK.");

            #endregion
        }
    }

    /// <summary>
    /// Instantiate a Logger
    /// </summary>
    /// <param name="logVerbosity"></param>
    /// <returns></returns>
    private static Microsoft.Extensions.Logging.ILogger CreateLogger(LogLevel logVerbosity, bool withFileOutput)
    {
        /*
         * The CCT SDK accepts Loggers from .NET Microsoft.Extensions.Logging libraries.
         * E.g. when Microsoft.Extensions.Logging.Console NuGet package is referenced, a formatted Console Logger might be connected,
         * Example code:
         * 
        
        using ILoggerFactory factory = LoggerFactory.Create(builder => builder.SetMinimumLevel(logVerbosity).AddConsole());
        return factory.CreateLogger(nameof(Program));

        */

        // demo call of Console.WriteLine(string) wrapped into ILogger interface, with optional file trace
        return new Thorlabs.ManagedDevice.Trace.ExampleLogger(nameof(Program), logVerbosity, withFileOutput);
    }
}

```
