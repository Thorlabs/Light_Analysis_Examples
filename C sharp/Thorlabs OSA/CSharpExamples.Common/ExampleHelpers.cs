using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using ThorlabsOSAWrapper;

namespace CSharpExamples.Common
{
    public static class OperationGuard
    {
        public static void ThrowIfFailed(OperationResult result, string operation)
        {
            if (result == null)
            {
                throw new InvalidOperationException("Could not " + operation + ": no result was returned.");
            }

            if (result.Failure)
            {
                throw new InvalidOperationException(
                    "Could not " + operation + ": " + result.ErrorMessage);
            }
        }
    }

    public static class AnalysisResultMessage
    {
        public static string DescribeFailure(OperationResult result)
        {
            string codeName = Enum.IsDefined(typeof(FTSFlag), result.ReturnCode)
                ? ((FTSFlag)result.ReturnCode).ToString()
                : "UnknownError";
            string description = result.ReturnCode == (int)FTSFlag.WavelengthMeterErrorOutOfRange
                ? "The measured wavelength is outside the wavelength-meter analysis range."
                : null;
            string nativeMessage = IsUsableNativeMessage(result.ErrorMessage)
                ? result.ErrorMessage.Trim()
                : null;

            return string.Format(
                "return code {0} ({1}){2}{3}",
                result.ReturnCode,
                codeName,
                description == null ? string.Empty : ": " + description,
                nativeMessage == null ? string.Empty : " Native message: " + nativeMessage);
        }

        private static bool IsUsableNativeMessage(string message)
        {
            if (string.IsNullOrWhiteSpace(message) || message.Length > 512)
            {
                return false;
            }

            return message.All(character =>
                !char.IsControl(character) ||
                character == '\r' ||
                character == '\n' ||
                character == '\t');
        }
    }

    public sealed class ModeOption
    {
        public ModeOption(ushort value, string name)
        {
            Value = value;
            Name = name;
        }

        public ushort Value { get; }

        public string Name { get; }
    }

    public static class ModeCatalog
    {
        public static string GetResolutionName(ushort instrumentSeries, uint value)
        {
            switch ((InstrumentSeries)instrumentSeries)
            {
                case InstrumentSeries.RedstoneSeries:
                    return new RedstoneResolutionMode((int)value).ToShortString();
                case InstrumentSeries.OSA200Series:
                    return new OSAResolutionMode((int)value).ToString();
                default:
                    return "Unknown (" + value + ")";
            }
        }

        public static string GetSensitivityName(ushort instrumentSeries, uint value)
        {
            switch ((InstrumentSeries)instrumentSeries)
            {
                case InstrumentSeries.RedstoneSeries:
                    return new RedstoneSensitivityMode((int)value).ToShortString();
                case InstrumentSeries.OSA200Series:
                    return new OSASensitivityMode((int)value).ToString();
                default:
                    return "Unknown (" + value + ")";
            }
        }

        public static IReadOnlyList<ModeOption> GetResolutions(LibDeviceInterface device)
        {
            if (device.GetInstrumentSeries() == InstrumentSeries.RedstoneSeries)
            {
                return RedstoneResolutionMode.ListAll()
                    .Select(mode => new ModeOption((ushort)(int)mode, mode.ToShortString()))
                    .ToArray();
            }

            return OSAResolutionMode.ListAll()
                .Select(mode => new ModeOption((ushort)(int)mode, mode.ToString()))
                .ToArray();
        }

        public static IReadOnlyList<ModeOption> GetSensitivities(LibDeviceInterface device)
        {
            if (device.GetInstrumentSeries() == InstrumentSeries.RedstoneSeries)
            {
                bool highResolution =
                    device.GetCurrentResolutionMode() ==
                    RedstoneResolutionMode.REDSTONE_RESOLUTION_HIGH;

                return RedstoneSensitivityMode.ListAll()
                    .Where(mode =>
                        (int)mode != (highResolution
                            ? RedstoneSensitivityMode.REDSTONE_SENSITIVITY_HIGH
                            : RedstoneSensitivityMode.REDSTONE_SENSITIVITY_HIGH_SPECIAL))
                    .Select(mode => new ModeOption((ushort)(int)mode, mode.ToShortString()))
                    .ToArray();
            }

            return OSASensitivityMode.ListAll()
                .Select(mode => new ModeOption((ushort)(int)mode, mode.ToString()))
                .ToArray();
        }
    }

    public static class SpectrumHelpers
    {
        public static string GetXUnitLabel(XUnit unit)
        {
            switch (unit)
            {
                case XUnit.wavenumbers:
                    return "cm^-1";
                case XUnit.THz:
                    return "THz";
                case XUnit.nmVac:
                    return "nm (vac)";
                case XUnit.nmAir:
                    return "nm (air)";
                case XUnit.electronVolts:
                    return "eV";
                case XUnit.ramanShifts:
                    return "cm^-1 Raman shift";
                default:
                    return unit.ToString();
            }
        }

        public static string GetYUnitLabel(YUnit unit)
        {
            switch (unit)
            {
                case YUnit.dBm:
                    return "dBm";
                case YUnit.dBmNormalized:
                    return "dBm (normalized)";
                case YUnit.milliWatts:
                    return "mW";
                case YUnit.milliWattsNormalized:
                    return "mW (normalized)";
                case YUnit.counts:
                    return "counts";
                case YUnit.AU:
                    return "a.u.";
                default:
                    return unit.ToString();
            }
        }

        public static bool CanConvertWavenumberTo(XUnit unit)
        {
            return unit == XUnit.wavenumbers ||
                   unit == XUnit.THz ||
                   unit == XUnit.nmVac ||
                   unit == XUnit.nmAir ||
                   unit == XUnit.electronVolts;
        }

        public static double ConvertWavenumber(
            double wavenumber,
            XUnit targetUnit,
            UnitConversions conversions)
        {
            switch (targetUnit)
            {
                case XUnit.wavenumbers:
                    return wavenumber;
                case XUnit.THz:
                    return conversions.ConvertWaveNumberToTeraHertz(wavenumber);
                case XUnit.nmVac:
                    return conversions.ConvertWaveNumberToNanometerVac(wavenumber);
                case XUnit.nmAir:
                    return conversions.ConvertWaveNumberToNanometerAirPeckAndReeder(wavenumber);
                case XUnit.electronVolts:
                    return conversions.ConvertWaveNumberToElectronVolt(wavenumber);
                default:
                    throw new NotSupportedException(
                        "Cannot convert a wavemeter result to " + targetUnit + ".");
            }
        }

        public static double ConvertWavenumberUncertainty(
            double wavenumber,
            double uncertainty,
            XUnit targetUnit,
            UnitConversions conversions)
        {
            double low = ConvertWavenumber(wavenumber - uncertainty, targetUnit, conversions);
            double high = ConvertWavenumber(wavenumber + uncertainty, targetUnit, conversions);
            return Math.Abs(high - low) * 0.5;
        }

        public static void ConvertToNanometersVacuumAndNormalizedDbm(SpectrumStruct spectrum)
        {
            var conversions = new UnitConversions();
            var yUnit = (YUnit)spectrum.YAxisUnit;

            if (yUnit == YUnit.dBm)
            {
                OperationGuard.ThrowIfFailed(
                    conversions.ConvertSpectrumToPowerDensity(spectrum),
                    "convert absolute dBm to power density");
            }
            else if (yUnit == YUnit.milliWatts ||
                     yUnit == YUnit.milliWattsNormalized)
            {
                OperationGuard.ThrowIfFailed(
                    conversions.ConvertSpectrumTodBm(spectrum, true),
                    "convert the y-axis to normalized dBm");
            }
            else if (yUnit != YUnit.dBmNormalized)
            {
                throw new NotSupportedException(
                    "Cannot convert the spectrum from y-axis unit " + yUnit +
                    " to normalized dBm.");
            }

            if ((XUnit)spectrum.XAxisUnit != XUnit.nmVac)
            {
                OperationGuard.ThrowIfFailed(
                    conversions.ConvertSpectrumToNanometerVac(spectrum, true),
                    "convert the x-axis to vacuum nanometers");
            }
        }

        public static void PrintValues(SpectrumStruct spectrum)
        {
            Console.WriteLine(
                "Length: {0}, X unit: {1}, Y unit: {2}",
                spectrum.Length,
                spectrum.XAxisUnit,
                spectrum.YAxisUnit);

            for (int index = 0; index < spectrum.Length; index++)
            {
                Console.WriteLine(
                    "{0:R}\t{1:R}",
                    spectrum.GetXAtIndex(index),
                    spectrum.Value[index]);
            }
        }

        public static string SafeFileName(string value)
        {
            var invalidCharacters = Path.GetInvalidFileNameChars();
            return new string(value.Where(character => !invalidCharacters.Contains(character) &&
                                                       !char.IsWhiteSpace(character)).ToArray());
        }
    }

    public static class ConsoleStop
    {
        public static void WaitForQuit()
        {
            bool stopRequested = false;
            Console.CancelKeyPress += (sender, args) =>
            {
                args.Cancel = true;
                stopRequested = true;
            };

            Console.WriteLine("Press Q or Ctrl+C to stop.");
            while (!stopRequested)
            {
                if (Console.KeyAvailable && Console.ReadKey(true).Key == ConsoleKey.Q)
                {
                    stopRequested = true;
                }
                else
                {
                    System.Threading.Thread.Sleep(50);
                }
            }
        }
    }

    public sealed class ConsoleCancellation : IDisposable
    {
        private readonly ConsoleCancelEventHandler _cancelHandler;
        private volatile bool _cancellationRequested;

        public ConsoleCancellation()
        {
            _cancelHandler = (sender, args) =>
            {
                args.Cancel = true;
                _cancellationRequested = true;
            };
            Console.CancelKeyPress += _cancelHandler;
        }

        public bool Poll()
        {
            if (_cancellationRequested)
            {
                return true;
            }

            if (!Console.IsInputRedirected &&
                Console.KeyAvailable &&
                Console.ReadKey(true).Key == ConsoleKey.Q)
            {
                _cancellationRequested = true;
            }

            return _cancellationRequested;
        }

        public void Dispose()
        {
            Console.CancelKeyPress -= _cancelHandler;
        }
    }
}
