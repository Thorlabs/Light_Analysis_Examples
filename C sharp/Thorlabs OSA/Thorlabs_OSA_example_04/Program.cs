/*
Thorlabs_OSA_example_04
Example last updated: 2026-11-03
Development environment: Visual Studio 2022
Target framework: .NET Framework 4.7.2, x64
Thorlabs SDK: ThorSpectra 3.40
Description: Continuously acquire spectra and interferograms and run peak track and wavemeter analysis.
*/

using System;
using System.Linq;
using CSharpExamples.Common;
using ThorlabsOSAWrapper;

namespace Thorlabs_OSA_example_04
{
    internal static class Program
    {
        private static void Main()
        {
            Console.WriteLine("Example 4 - Continuous wavemeter and peak track analysis");

            try
            {
                using (OsaConnection connection = OsaConnection.OpenFirst())
                using (var acquisition = new ContinuousAcquisition(connection.Device))
                {
                    var analysis = new LibraryAnalysis();
                    var conversions = new UnitConversions();
                    var unitLock = new object();
                    XUnit outputXUnit = XUnit.wavenumbers;
                    bool isRedstone =
                        connection.Device.GetInstrumentSeries() == InstrumentSeries.RedstoneSeries;
                    ushort wavemeterChannel = isRedstone
                        ? connection.Device.GetDUTChannelIndices().First()
                        : (ushort)0;
                    ushort stitchedSpectrumChannel =
                        connection.Device.GetStitchedSpectrumChannelIndex();

                    acquisition.InterferogramReceived += interferogram =>
                    {
                        if (isRedstone && interferogram.channelIndex != wavemeterChannel)
                        {
                            return;
                        }

                        WavelengthMeterAnalysisResult result =
                            analysis.WavelengthMeter(interferogram, 0U, interferogram.Length);
                        if (result.Success)
                        {
                            XUnit wavemeterUnit;
                            lock (unitLock)
                            {
                                wavemeterUnit = outputXUnit;
                            }

                            if (!SpectrumHelpers.CanConvertWavenumberTo(wavemeterUnit))
                            {
                                wavemeterUnit = XUnit.wavenumbers;
                            }

                            double wavemeterValue = SpectrumHelpers.ConvertWavenumber(
                                result.wavenumber,
                                wavemeterUnit,
                                conversions);
                            double wavemeterError = SpectrumHelpers.ConvertWavenumberUncertainty(
                                result.wavenumber,
                                result.waveNumberError,
                                wavemeterUnit,
                                conversions);
                            Console.WriteLine(
                                "{0:HH:mm:ss} wavemeter: {1:F6} +/- {2:F8} {3}",
                                interferogram.TimeStamp,
                                wavemeterValue,
                                wavemeterError,
                                SpectrumHelpers.GetXUnitLabel(wavemeterUnit));
                        }
                        else
                        {
                            Console.WriteLine(
                                "Wavemeter analysis failed: " +
                                AnalysisResultMessage.DescribeFailure(result));
                        }
                    };

                    acquisition.SpectrumReceived += spectrum =>
                    {
                        if (isRedstone && spectrum.channelIndex != stitchedSpectrumChannel)
                        {
                            return;
                        }

                        XUnit spectrumXUnit = (XUnit)spectrum.XAxisUnit;
                        YUnit spectrumYUnit = (YUnit)spectrum.YAxisUnit;
                        lock (unitLock)
                        {
                            outputXUnit = spectrumXUnit;
                        }

                        PeakTrackAnalysisResult result =
                            analysis.PeakTrack(spectrum, 0.01, 3.0, 0, (int)spectrum.Length, 20);
                        if (result.Failure)
                        {
                            Console.WriteLine(
                                "Peak track analysis failed: " +
                                AnalysisResultMessage.DescribeFailure(result));
                        }
                        else if (result.Number == 0)
                        {
                            Console.WriteLine(
                                "{0:HH:mm:ss} Peak track found no peaks above the configured threshold.",
                                spectrum.TimeStamp);
                        }
                        else
                        {
                            PeakAnalysisResult peak =
                                result.data.OrderByDescending(candidate => candidate.peakLevel).First();
                            Console.WriteLine(
                                "{0:HH:mm:ss} highest peak: {1:F6} {2}, level {3:F3} {4}",
                                spectrum.TimeStamp,
                                peak.centroidPosition,
                                SpectrumHelpers.GetXUnitLabel(spectrumXUnit),
                                peak.peakLevel,
                                SpectrumHelpers.GetYUnitLabel(spectrumYUnit));
                        }
                    };

                    acquisition.AcquisitionError += message => Console.Error.WriteLine("OSA: " + message);
                    acquisition.Start();
                    ConsoleStop.WaitForQuit();
                }
            }
            catch (Exception exception)
            {
                Console.Error.WriteLine(exception.Message);
                Environment.ExitCode = 1;
            }
        }
    }
}
