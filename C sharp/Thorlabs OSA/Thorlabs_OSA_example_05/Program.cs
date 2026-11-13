/*
Thorlabs_OSA_example_05
Example last updated: 2026-11-03
Development environment: Visual Studio 2022
Target framework: .NET Framework 4.7.2, x64
Thorlabs SDK: ThorSpectra 3.40
Description: Continuously track and print the strongest peak position.
*/

using System;
using System.Linq;
using CSharpExamples.Common;
using ThorlabsOSAWrapper;

namespace Thorlabs_OSA_example_05
{
    internal static class Program
    {
        private static void Main()
        {
            Console.WriteLine("Example 5 - Track the strongest peak over time");

            try
            {
                using (OsaConnection connection = OsaConnection.OpenFirst())
                using (var acquisition = new ContinuousAcquisition(connection.Device))
                {
                    var analysis = new LibraryAnalysis();
                    bool isRedstone =
                        connection.Device.GetInstrumentSeries() == InstrumentSeries.RedstoneSeries;
                    ushort stitchedSpectrumChannel =
                        connection.Device.GetStitchedSpectrumChannelIndex();

                    acquisition.SpectrumReceived += spectrum =>
                    {
                        if (isRedstone && spectrum.channelIndex != stitchedSpectrumChannel)
                        {
                            return;
                        }

                        XUnit spectrumXUnit = (XUnit)spectrum.XAxisUnit;
                        PeakTrackAnalysisResult result =
                            analysis.PeakTrack(spectrum, 0.01, 3.0, 0, (int)spectrum.Length, 20);
                        if (result.Failure)
                        {
                            Console.WriteLine(
                                "{0:HH:mm:ss.fff}\tPeak track analysis failed: {1}",
                                spectrum.TimeStamp,
                                AnalysisResultMessage.DescribeFailure(result));
                        }
                        else if (result.Number == 0)
                        {
                            Console.WriteLine(
                                "{0:HH:mm:ss.fff}\tPeak track found no peaks above the configured threshold.",
                                spectrum.TimeStamp);
                        }
                        else
                        {
                            PeakAnalysisResult peak =
                                result.data.OrderByDescending(candidate => candidate.peakLevel).First();
                            Console.WriteLine(
                                "{0:HH:mm:ss.fff}\t{1:F4} {2}",
                                spectrum.TimeStamp,
                                peak.centroidPosition,
                                SpectrumHelpers.GetXUnitLabel(spectrumXUnit));
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
