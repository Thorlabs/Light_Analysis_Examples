using System;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using ThorlabsOSAWrapper;

namespace CSharpExamples.Common
{
    public sealed class AcquisitionResult : IDisposable
    {
        public SpectrumStruct Spectrum { get; set; }

        public SpectrumStruct Interferogram { get; set; }

        public void Dispose()
        {
            Spectrum?.Dispose();
            Interferogram?.Dispose();
        }
    }

    public static class SingleAcquisition
    {
        public static AcquisitionResult Acquire(
            LibDeviceInterface device,
            bool includeInterferogram = false,
            int timeoutMilliseconds = 120000,
            Func<bool> cancellationRequested = null)
        {
            var completed = new ManualResetEventSlim(false);
            var result = new AcquisitionResult();
            string acquisitionError = null;
            bool isRedstone =
                device.GetInstrumentSeries() == InstrumentSeries.RedstoneSeries;
            ushort stitchedSpectrumChannel = device.GetStitchedSpectrumChannelIndex();
            ushort interferogramChannel = isRedstone
                ? device.GetDUTChannelIndices().First()
                : (ushort)0;

            EventHandler<ContinuousProcessingCallbackEventArgs> callback = (sender, args) =>
            {
                OSACallbackMessage message = args.CallbackMessage;
                if (message.LastErrorFlag != FTSFlag.SUCCESS &&
                    message.LastErrorFlag != FTSFlag.FINISHED)
                {
                    acquisitionError = message.LastErrorFlag.ToString();
                    completed.Set();
                    return;
                }

                if (includeInterferogram &&
                    result.Interferogram == null &&
                    message.LastDataTypeUpdateFlag == AcquisitionUpdateFlag.Interferogram &&
                    (!isRedstone || message.ChannelIndex == interferogramChannel))
                {
                    result.Interferogram = SpectrumReader.ReadInterferogram(device, message.ChannelIndex);
                }
                else if (result.Spectrum == null &&
                         message.LastDataTypeUpdateFlag == AcquisitionUpdateFlag.Spectrum &&
                         (!isRedstone || message.ChannelIndex == stitchedSpectrumChannel))
                {
                    result.Spectrum = SpectrumReader.ReadSpectrum(device, message.ChannelIndex);
                }

                if (result.Spectrum != null &&
                    (!includeInterferogram || result.Interferogram != null))
                {
                    completed.Set();
                }
            };

            device.OnSingleAcquisition += callback;
            try
            {
                OperationResult startResult = device.AcquireSingleSpectrum();
                OperationGuard.ThrowIfFailed(startResult, "start a single acquisition");

                var stopwatch = Stopwatch.StartNew();
                while (!completed.Wait(50))
                {
                    if (cancellationRequested != null && cancellationRequested())
                    {
                        device.StopContinuousAcquisition();
                        throw new OperationCanceledException("The acquisition was cancelled.");
                    }

                    if (stopwatch.ElapsedMilliseconds >= timeoutMilliseconds)
                    {
                        throw new TimeoutException("Timed out waiting for the OSA acquisition.");
                    }
                }

                if (cancellationRequested != null && cancellationRequested())
                {
                    device.StopContinuousAcquisition();
                    throw new OperationCanceledException("The acquisition was cancelled.");
                }

                if (acquisitionError != null)
                {
                    throw new InvalidOperationException("OSA acquisition failed: " + acquisitionError);
                }

                if (result.Spectrum == null)
                {
                    throw new InvalidOperationException("The acquisition finished without returning a spectrum.");
                }

                return result;
            }
            catch
            {
                result.Dispose();
                throw;
            }
            finally
            {
                device.OnSingleAcquisition -= callback;
                completed.Dispose();
            }
        }
    }

    public sealed class ContinuousAcquisition : IDisposable
    {
        private readonly LibDeviceInterface _device;
        private bool _started;

        public ContinuousAcquisition(LibDeviceInterface device)
        {
            _device = device ?? throw new ArgumentNullException(nameof(device));
        }

        public event Action<SpectrumStruct> SpectrumReceived = delegate { };

        public event Action<SpectrumStruct> InterferogramReceived = delegate { };

        public event Action<string> AcquisitionError = delegate { };

        public void Start()
        {
            if (_started)
            {
                return;
            }

            _device.OnContinuousAcquisitionUpdate += OnAcquisitionUpdate;
            OperationResult result = _device.StartContinuousAcquisition();
            if (result.Failure)
            {
                _device.OnContinuousAcquisitionUpdate -= OnAcquisitionUpdate;
                OperationGuard.ThrowIfFailed(result, "start continuous acquisition");
            }

            _started = true;
        }

        public void Stop()
        {
            if (!_started)
            {
                return;
            }

            _device.StopContinuousAcquisition();
            _device.OnContinuousAcquisitionUpdate -= OnAcquisitionUpdate;
            _started = false;
        }

        public void Dispose()
        {
            Stop();
        }

        private void OnAcquisitionUpdate(object sender, ContinuousProcessingCallbackEventArgs args)
        {
            OSACallbackMessage message = args.CallbackMessage;
            if (message.LastErrorFlag != FTSFlag.SUCCESS &&
                message.LastErrorFlag != FTSFlag.FINISHED)
            {
                AcquisitionError(message.LastErrorFlag.ToString());
                return;
            }

            SpectrumStruct data = null;
            try
            {
                if (message.LastDataTypeUpdateFlag == AcquisitionUpdateFlag.Interferogram)
                {
                    data = SpectrumReader.ReadInterferogram(_device, message.ChannelIndex);
                    if (data != null)
                    {
                        InterferogramReceived(data);
                    }
                }
                else if (message.LastDataTypeUpdateFlag == AcquisitionUpdateFlag.Spectrum)
                {
                    data = SpectrumReader.ReadSpectrum(_device, message.ChannelIndex);
                    if (data != null)
                    {
                        SpectrumReceived(data);
                    }
                }
            }
            catch (Exception exception)
            {
                AcquisitionError(exception.Message);
            }
            finally
            {
                data?.Dispose();
            }
        }
    }

    public static class SpectrumReader
    {
        public static SpectrumStruct ReadSpectrum(LibDeviceInterface device, ushort channelIndex)
        {
            if (channelIndex == device.GetStitchedSpectrumChannelIndex())
            {
                uint length = device.GetLastStitchedSpectrumLength();
                if (length == 0)
                {
                    return null;
                }

                var spectrum = new SpectrumStruct(length, true);
                OperationResult result = device.GetLastStitchedSpectrum(spectrum);
                if (result.Failure)
                {
                    spectrum.Dispose();
                    OperationGuard.ThrowIfFailed(result, "read the stitched spectrum");
                }

                return spectrum;
            }

            if (!device.GetDUTChannelIndices().Contains(channelIndex))
            {
                return null;
            }

            IChannelInterface channel = device.ChannelInterfaces[channelIndex];
            uint channelLength = channel.GetLastSpectrumLength();
            if (channelLength == 0)
            {
                return null;
            }

            var channelSpectrum = new SpectrumStruct(channelLength, true);
            OperationResult channelResult = channel.GetLastSpectrum(channelSpectrum);
            if (channelResult.Failure)
            {
                channelSpectrum.Dispose();
                OperationGuard.ThrowIfFailed(channelResult, "read the channel spectrum");
            }

            return channelSpectrum;
        }

        public static SpectrumStruct ReadInterferogram(
            LibDeviceInterface device,
            ushort channelIndex)
        {
            if (channelIndex >= device.ChannelInterfaces.Length)
            {
                return null;
            }

            IChannelInterface channel = device.ChannelInterfaces[channelIndex];
            uint length = channel.GetLastInterferogramLength();
            if (length == 0)
            {
                return null;
            }

            var interferogram = new SpectrumStruct(length, true);
            OperationResult result = channel.GetLastInterferogram(interferogram);
            if (result.Failure)
            {
                interferogram.Dispose();
                OperationGuard.ThrowIfFailed(result, "read the interferogram");
            }

            return interferogram;
        }
    }
}
