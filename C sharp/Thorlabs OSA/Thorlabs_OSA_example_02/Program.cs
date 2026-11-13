/*
Thorlabs_OSA_example_02
Example last updated: 2026-11-03
Development environment: Visual Studio 2022
Target framework: .NET Framework 4.7.2, x64
Thorlabs SDK: ThorSpectra 3.40
Description: Measure all supported resolution and sensitivity combinations and save SPF2 files.
*/

using System;
using System.IO;
using CSharpExamples.Common;
using ThorlabsOSAWrapper;

namespace Thorlabs_OSA_example_02
{
    internal static class Program
    {
        private static void Main(string[] args)
        {
            Console.WriteLine("Example 2 - Acquire all resolution/sensitivity combinations");
            string outputDirectory = args.Length > 0 ? args[0] : Path.Combine(Path.GetTempPath(), "ThorlabsOSA");
            Directory.CreateDirectory(outputDirectory);
            Console.WriteLine("Press Q or Ctrl+C to stop after the current device operation.");

            try
            {
                using (var cancellation = new ConsoleCancellation())
                using (OsaConnection connection = OsaConnection.OpenFirst())
                {
                    foreach (IChannelInterface channel in connection.Device.ChannelInterfaces)
                    {
                        channel.AcquisitionSettings.AutomaticGain = true;
                        channel.AcquisitionSettings.AverageSpecNum = 5;
                    }

                    var fileIO = new FileIOInterface();
                    string model = connection.Device.GetInstrumentModel().ToString();

                    foreach (ModeOption resolution in ModeCatalog.GetResolutions(connection.Device))
                    {
                        if (cancellation.Poll())
                        {
                            break;
                        }

                        OperationResult resolutionResult = connection.Device.SetResolutionMode(resolution.Value);
                        if (resolutionResult.Failure)
                        {
                            Console.WriteLine("Skipping resolution {0}: {1}", resolution.Name, resolutionResult.ErrorMessage);
                            continue;
                        }

                        foreach (ModeOption sensitivity in ModeCatalog.GetSensitivities(connection.Device))
                        {
                            if (cancellation.Poll())
                            {
                                break;
                            }

                            OperationResult sensitivityResult = connection.Device.SetSensitivityMode(sensitivity.Value);
                            if (sensitivityResult.Failure)
                            {
                                Console.WriteLine(
                                    "Skipping {0}/{1}: {2}",
                                    resolution.Name,
                                    sensitivity.Name,
                                    sensitivityResult.ErrorMessage);
                                continue;
                            }

                            Console.WriteLine(
                                "Measuring {0}, {1}...",
                                resolution.Name,
                                sensitivity.Name);

                            using (AcquisitionResult acquisition = SingleAcquisition.Acquire(
                                connection.Device,
                                cancellationRequested: cancellation.Poll))
                            {
                                SpectrumHelpers.ConvertToNanometersVacuumAndNormalizedDbm(acquisition.Spectrum);
                                string fileName = string.Format(
                                    "spectrum_{0}_{1}_{2}.spf2",
                                    SpectrumHelpers.SafeFileName(model),
                                    SpectrumHelpers.SafeFileName(resolution.Name),
                                    SpectrumHelpers.SafeFileName(sensitivity.Name));
                                string path = Path.Combine(outputDirectory, fileName);

                                OperationGuard.ThrowIfFailed(
                                    fileIO.WriteSpectrum(
                                        acquisition.Spectrum,
                                        path,
                                        (int)FTSSpectrumFileFormat.SPF2File),
                                    "write " + path);
                                Console.WriteLine("Saved {0}", path);
                            }
                        }
                    }
                }
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Acquisition stopped by the user.");
            }
            catch (Exception exception)
            {
                Console.Error.WriteLine(exception.Message);
                Environment.ExitCode = 1;
            }
        }
    }
}
