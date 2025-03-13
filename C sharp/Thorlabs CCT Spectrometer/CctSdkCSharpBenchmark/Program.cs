//Example Date of Creation(YYYY - MM - DD) 2025 - 03 - 13
//Example Date of Last Modification on Github 2025 - 03 - 13
//Version of .NET Framework used for Testing: 4.8
//Version of the ThorSpectra installation: 3.35
//Example Description: Benchmark Application Example is a Console Application, which connects to first available Spectrometer and performs the following workflow:
//-Sets acquisition parameters: Exposure and amount of frames for Hardware Averaging.
//- Acquire series of Spectra.
//- Evaluate effective frame rate within the series.
//- Save Benchmark results along with stamps of each acquired spectrum frame into a file.
//After the workflow is finished, the Application disposes all SDK objects and exits.


using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace CctSdkCSharpBenchmark;

/// <summary>
/// Example Console Application to run Benchmark of SDK for Thorlabs Compact Spectrometer:<br/>
/// 0) Initialize workflow;<br/>
/// 1) Detect hardware connected via USB or Ethernet;<br/>
/// 2) Connect to up and running Spectrometer;<br/>
/// 3) Set (3.a) Sensor Exposure and (3.b) Hardware Averaging;<br/>
/// 4) Prepare Data containers for reporting;<br/>
/// 5) Acquire series of Spectra;<br/>
/// 6) Print and save results;<br/>
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
        
        logger.LogInformation("Started .NET CSharp Benchmark of Thorlabs Compact Spectrometer SDK.");

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

            #endregion

            #region 3.a) Set Sensor Exposure

            // Specify Sensor Exposure (Integration Time) in ms
            float targetExposure = 0.01f;
            
            // set to target
            bool exposureResult = await spectrometer.SetManualExposureAsync(exposure: targetExposure, cancellationToken);
            
            // get for control check
            var currentExposure = spectrometer.ManualExposure;

            if (Math.Abs(currentExposure - targetExposure) > 0.001f 
                || !exposureResult)
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
            int targetAve = 1;
            
            // set to target
            bool resultAve = await spectrometer.SetHwAverageAsync(ave: targetAve, cancellationToken);
            
            // get for control check
            var currentAve = spectrometer.HwAverage;

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
            
            #region 4) Prepare data containers
            
            DateTime started = DateTime.Now;

            ulong amount = 1000;

            var ticks = new ulong[amount];

            StringBuilder PrepareReport(ulong first, ulong last)
            {
                DateTime finished = DateTime.Now;

                Thorlabs.ManagedDevice.CompactSpectrographDriver.Dataset.ISpectrumXY calibration = spectrometer.GetActiveDispersionAndAmplitudeCorrection();

                ulong average = (last - first) / (amount - 1);

                var output = new StringBuilder();

                output.AppendLine($"Device ID:\t{deviceId}");
                output.AppendLine();
                output.AppendLine($"Handshaking Timestamp:\t{calibration.Acquired:O}");
                output.AppendLine($"Handshaking Ticks:\t{calibration.Tick} microseconds");
                output.AppendLine();
                output.AppendLine($"Benchmark started:\t{started:O}");
                output.AppendLine($"Benchmark finished:\t{finished:O}");
                output.AppendLine();
                output.AppendLine($"Amount of acquisitions:\t{amount} Spectra");
                output.AppendLine($"Single Exposure Time:\t{targetExposure} ms");
                output.AppendLine($"Hardware Averaging:\t{targetAve} Frames");
                output.AppendLine();
                output.AppendLine($"Ticks of First:\t{first} microseconds");
                output.AppendLine($"Ticks of Last:\t{last} microseconds");
                output.AppendLine();
                output.AppendLine($"Average period between Spectra:\t{((double)average / 1000d):F2} ms");
                output.AppendLine($"Frame Rate:\t{(1000000d / (double)average):F1} Hz");
                output.AppendLine();

                return output;
            }

            #endregion

            #region 5) Acquire series of Spectra

            logger.LogInformation($"Acquisitions started with overall integration time of {targetExposure * targetAve} milliseconds each in amount of {amount}.");

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

            #endregion

            #region 6) Print Results and save into File

            StringBuilder result = PrepareReport(ticks.FirstOrDefault(), ticks.LastOrDefault());

            Console.WriteLine();
            Console.WriteLine(result);
            Console.WriteLine();

            result.AppendLine($"Ticks of each Spectrum");
            result.AppendLine(string.Join("\n", ticks));

            string rootFolder = Environment.ExpandEnvironmentVariables(
                Environment.GetEnvironmentVariable(
                    System.Runtime.InteropServices.RuntimeInformation.IsOSPlatform(
                        System.Runtime.InteropServices.OSPlatform.Windows)
                        ? "LocalAppData"
                        : "HOME")
                ?? string.Empty);
            
            string folder = Path.Combine(rootFolder, ".Thorlabs", "CompactSpectrometer", deviceId);
            
            string filename = $"Benchmark_{started:yyyy-MM-dd_HH-mm-ss-fff}{Thorlabs.SpectraData.ToolValidation.ConfigExtension}";

            if (!string.IsNullOrEmpty(folder) &&
                Thorlabs.SpectraData.ToolValidation.CheckInvalidCharsInStringForPath(folder) &&
                Thorlabs.SpectraData.ToolValidation.CheckInvalidCharsInStringForFilename(filename))
            {
                Directory.CreateDirectory(folder);

                if (Directory.Exists(folder))
                {
                    string outputUri = Path.Combine(folder, filename);

                    File.WriteAllText(outputUri, result.ToString());

                    logger.LogInformation($"Benchmark results are saved into path: '{outputUri}'");
                }
                else
                {
                    logger.LogInformation($"Cannot create destination path '{folder}' - Benchmark dara acquired at '{started}' will be lost and application stopped.");
                }
            }
            else
            {
                logger.LogInformation($"Cannot define output path after successful Benchmark at '{started}' - application will be stopped.");
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
        
            logger.LogInformation("Finished .NET CSharp Benchmark of Thorlabs Compact Spectrometer SDK.");

            #endregion
        }
    }
}