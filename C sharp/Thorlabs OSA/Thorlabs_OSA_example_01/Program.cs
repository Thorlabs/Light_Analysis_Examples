/*
Thorlabs_OSA_example_01
Example last updated: 2026-11-03
Development environment: Visual Studio 2022
Target framework: .NET Framework 4.7.2, x64
Thorlabs SDK: ThorSpectra 3.40
Description: Read one spectrum from a Thorlabs Optical Spectrum Analyzer.
*/

using System;
using CSharpExamples.Common;

namespace Thorlabs_OSA_example_01
{
    internal static class Program
    {
        private static void Main()
        {
            Console.WriteLine("Example 1 - Read one spectrum from a Thorlabs OSA");

            try
            {
                using (OsaConnection connection = OsaConnection.OpenFirst())
                using (AcquisitionResult acquisition = SingleAcquisition.Acquire(connection.Device))
                {
                    SpectrumHelpers.PrintValues(acquisition.Spectrum);
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
