/*
Thorlabs_OSA_example_03
Example last updated: 2026-11-03
Development environment: Visual Studio 2022
Target framework: .NET Framework 4.7.2, x64
Thorlabs SDK: ThorSpectra 3.40
Description: Load an SPF2 measurement and run peak-track or wavemeter analysis.
*/

using System;
using System.IO;
using System.Windows.Forms;
using CSharpExamples.Common;
using ThorlabsOSAWrapper;

namespace Thorlabs_OSA_example_03
{
    internal static class Program
    {
        [STAThread]
        private static void Main(string[] args)
        {
            Console.WriteLine("Example 3 - Load and analyze an SPF2 measurement");
            string fileName = SelectFile(args);
            if (fileName == null)
            {
                Console.WriteLine("No file selected.");
                return;
            }

            var fileIO = new FileIOInterface();
            try
            {
                int count = fileIO.CountSpectraInFile(fileName);
                if (count <= 0)
                {
                    throw new FileLoadException("The selected file contains no readable measurements.", fileName);
                }

                LibraryTrace.Clear(0);
                TraceSpectrumStruct measurement = LibraryTrace.GetTrace(0);
                OperationGuard.ThrowIfFailed(
                    fileIO.ReadSpectrum(measurement, fileName, 0U),
                    "read the first measurement");

                Console.WriteLine(
                    "{0}, serial {1}, resolution mode {2}, sensitivity mode {3}",
                    measurement.InstrumentModel,
                    measurement.interferometerSerial,
                    ModeCatalog.GetResolutionName(
                        measurement.instrument_series,
                        measurement.resolutionMode),
                    ModeCatalog.GetSensitivityName(
                        measurement.instrument_series,
                        measurement.sensitivityMode));

                var analysis = new LibraryAnalysis();
                if (measurement.IsInterferogram())
                {
                    Console.WriteLine("Interferogram found in file!");
                    WavelengthMeterAnalysisResult wavemeter =
                        analysis.WavelengthMeter(measurement, 0U, measurement.Length);
                    OperationGuard.ThrowIfFailed(wavemeter, "run wavemeter analysis");
                    Console.WriteLine(
                        "Wavemeter: {0:F4} +/- {1:F8} cm^-1",
                        wavemeter.wavenumber,
                        wavemeter.waveNumberError);
                }
                else if (measurement.IsSpectrum())
                {
                    Console.WriteLine("Spectrum found in file!");
                    SpectrumHelpers.ConvertToNanometersVacuumAndNormalizedDbm(measurement);
                    XUnit xUnit = (XUnit)measurement.XAxisUnit;
                    YUnit yUnit = (YUnit)measurement.YAxisUnit;
                    string xUnitLabel = SpectrumHelpers.GetXUnitLabel(xUnit);
                    string yUnitLabel = SpectrumHelpers.GetYUnitLabel(yUnit);
                    double threshold = measurement.y_min +
                                       (measurement.y_max - measurement.y_min) * 0.5;
                    PeakTrackAnalysisResult peaks = analysis.PeakTrack(
                        measurement,
                        threshold,
                        3.0,
                        0,
                        (int)measurement.Length,
                        10);
                    OperationGuard.ThrowIfFailed(peaks, "run peak-track analysis");

                    Console.WriteLine("Found {0} peak(s).", peaks.Number);
                    for (int index = 0; index < peaks.Number; index++)
                    {
                        PeakAnalysisResult peak = peaks.data[index];
                        Console.WriteLine(
                            "Peak {0}: centroid={1:F4} {2}, level={3:F3} {4}, FWHM={5:F6} {2}",
                            index,
                            peak.centroidPosition,
                            xUnitLabel,
                            peak.peakLevel,
                            yUnitLabel,
                            peak.FWHM);
                    }
                }
                else
                {
                    Console.WriteLine("Neither a spectrum nor an interferogram found in file!");
                }
            }
            catch (Exception exception)
            {
                Console.Error.WriteLine(exception.Message);
                Environment.ExitCode = 1;
            }
            finally
            {
                LibraryTrace.Clear(0);
            }
        }

        private static string SelectFile(string[] args)
        {
            if (args.Length > 0)
            {
                if (!File.Exists(args[0]))
                {
                    Console.Error.WriteLine("File not found: " + args[0]);
                    Environment.ExitCode = 2;
                    return null;
                }

                return Path.GetFullPath(args[0]);
            }

            using (var dialog = new OpenFileDialog())
            {
                dialog.Title = "Select an OSA measurement";
                dialog.Filter = "SPF2 files (*.spf2)|*.spf2|All files (*.*)|*.*";
                dialog.CheckFileExists = true;
                dialog.Multiselect = false;
                return dialog.ShowDialog() == DialogResult.OK ? dialog.FileName : null;
            }
        }
    }
}
