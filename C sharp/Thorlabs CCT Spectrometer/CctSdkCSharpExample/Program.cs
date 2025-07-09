//Example Date of Creation(YYYY - MM - DD) 2025 - 03 - 13
//Example Date of Last Modification on Github 2025 - 03 - 13
//Version of .NET Framework used for Testing: 4.8
//Version of the ThorSpectra installation: 3.35
//Example Description: Benchmark Application Example is a Console Application, which connects to first available spectrometer and performs the following workflow:
//-Sets acquisition parameters: Exposure and amount of frames for Hardware Averaging.
//-Acquire single spectrum
//-Saves spectrum into a file
//After the workflow is finished, the application disposes all SDK objects and exits.

using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace CctSdkCSharpExample;

/// <summary>
/// Example Console Application to run Thorlabs Compact Spectrometer:<br/>
/// 0) Initialize workflow;<br/>
/// 1) Detect hardware connected via USB or Ethernet;<br/>
/// 2) Connect to up and running Spectrometer;<br/>
/// 3) Set (3.a) Sensor Exposure and (3.b) Hardware Averaging;<br/>
/// 4) Update Dark Spectrum;<br/>
/// 5) Acquire single Spectrum;<br/>
/// 6) Save spectrum into file;<br/>
/// 7) Dispose objects and closes Operating System handles for the hardware resources.<br/>
/// </summary>
internal static class Program
{
    private static async Task Main(string[] args)
    {
        #region 0) Initialize workflow

        // Use Console Logger instead of Console.WriteLine(string), because it can be shared with SDK of the Compact Spectrometers 
        var logVerbosity = LogLevel.Information;
        using ILoggerFactory factory = LoggerFactory.Create(builder => builder.SetMinimumLevel(logVerbosity).AddConsole());
        ILogger logger = factory.CreateLogger(nameof(Program));

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

            #region Demonstration of Hardware disconnect and reconnect

            /* 
             * Demonstration of API for temporary disconnect of the Spectrometer with later reconnect 
             *

            // Disconnect after a pause
            int pause_sec = 3;
            Thread.Sleep(pause_sec * 1000);
            bool disconnected = await startupHelper.SetSpectrometerDisconnectedByIdAsync(deviceId);
            if (disconnected)
            {
                logger.LogInformation($"Spectrometer is temporary disconnected for {pause_sec} seconds");
            }
            else
            {
                logger.LogInformation($"Cannot temporary disconnect Spectrometer '{deviceId}' - application will be stopped.");
                return;
            }

            // Reconnect after a pause
            Thread.Sleep(pause_sec * 1000);
            bool reconnect = await startupHelper.SetSpectrometerDisconnectedByIdAsync(deviceId, connectBack: true);
            if (reconnect)
            {
                logger.LogInformation($"Spectrometer is scheduled to be reconnected, acquisition starts in {pause_sec} seconds");
            }
            else
            {
                logger.LogInformation($"Cannot schedule reconnection of the Spectrometer '{deviceId}' - application will be stopped.");
                return;
            }
            _ = await startupHelper.GetKnownDevicesAsync(cancellationToken);
            Thread.Sleep(pause_sec * 1000);

            */

            #endregion

            #region Demonstration of enabling the Trigger Mode

            /* 
             * Demonstration of usage of the Input Hardware Trigger Mode
             *

            bool resultTrig = await spectrometer.SetInputHwTriggerAsync(enabled: true, aveNoWait: false, slopeFallingEdge: false, cancellationToken);

            if (resultTrig)
            {
                logger.LogInformation($"Input Hardware Trigger Mode is switched: {(spectrometer.HwTriggerIn ? "ON" : "OFF")}");
            }
            else
            {
                logger.LogInformation($"Cannot set input Hardware Trigger Mode - application will be stopped.");
                return;
            }

            */

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
}