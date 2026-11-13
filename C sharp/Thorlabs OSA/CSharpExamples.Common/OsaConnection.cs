using System;
using ThorlabsOSAWrapper;

namespace CSharpExamples.Common
{
    public sealed class OsaConnection : IDisposable
    {
        private bool _disposed;

        private OsaConnection(DeviceLocator locator, LibDeviceInterface device)
        {
            Locator = locator;
            Device = device;
        }

        public DeviceLocator Locator { get; }

        public LibDeviceInterface Device { get; }

        public static OsaConnection OpenFirst()
        {
            Console.WriteLine("Searching for OSAs...");
            var locator = new DeviceLocator();
            int count = locator.InitializeSpectrometers();
            if (count <= 0)
            {
                locator.StopAllRetrievalsOnGUIClose();
                throw new InvalidOperationException("No Thorlabs OSA was found.");
            }

            var device = new LibDeviceInterface(0U);
            Console.WriteLine(
                "Connected to {0}, serial {1}.",
                device.GetInstrumentModel(),
                device.InstrumentDescription.GetSerial());

            return new OsaConnection(locator, device);
        }

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            _disposed = true;
            Device.ClearCallbacks();
            Device.CloseSpectrometer();
            Device.Dispose();
            Locator.StopAllRetrievalsOnGUIClose();
        }
    }
}
