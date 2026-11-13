#include "stdafx.h"

#include <conio.h>

#include <atomic>
#include <chrono>
#include <cstdio>
#include <thread>
#include <vector>

#include <FTSData.h>
#include <FTSpectrometer.h>
#include <FTSVirtualSpectrometer.h>

namespace
{
constexpr SpectrometerIndex Spectrometer = 0U;
constexpr unsigned int SpectraToAcquire = 100U;
constexpr auto AcquisitionTimeout = std::chrono::minutes(5);

std::atomic<unsigned int> acquiredSpectra{ 0U };
std::atomic<int> acquisitionError{ FTS_SUCCESS };
std::atomic<ChannelIndex> outputChannel{ 0U };

bool CheckStatus(const char* operation, int status)
{
    if (status == FTS_SUCCESS)
    {
        std::printf("%s succeeded.\n", operation);
        return true;
    }

    std::printf("%s failed with error %d.\n", operation, status);
    return false;
}

template <typename Operation>
bool RunOperation(const char* description, Operation operation)
{
    std::printf("%s...\n", description);
    return CheckStatus(description, operation());
}

bool ConfigureSpectrometer(OSA_SERIES series)
{
    unsigned short resolutionMode = RESOLUTION_UNKNOWN;
    unsigned short sensitivityMode = SENSITIVITY_UNKNOWN;
    const char* seriesName = nullptr;
    const char* resolutionName = nullptr;
    const char* sensitivityName = nullptr;

    switch (series)
    {
    case REDSTONE_SERIES:
        seriesName = "Redstone";
        resolutionMode = REDSTONE_RESOLUTION_LOW;
        sensitivityMode = REDSTONE_SENSITIVITY_LOW;
        resolutionName = "Low";
        sensitivityName = "Low";
        break;

    case OSA200_SERIES:
        seriesName = "OSA20x";
        resolutionMode = OSA200_RESOLUTION_LOW;
        sensitivityMode = OSA200_SENSITIVITY_LOW;
        resolutionName = "Low";
        sensitivityName = "Low";
        break;

    default:
        std::printf("Unsupported spectrometer series %u.\n", static_cast<unsigned int>(series));
        return false;
    }

    std::printf("Configuring %s acquisition settings.\n", seriesName);
    std::printf(
        "Setting resolution to %s (SDK value %u)...\n",
        resolutionName,
        static_cast<unsigned int>(resolutionMode));
    const bool resolutionSet = CheckStatus(
        "Setting resolution",
        FTS_SetResolutionMode(Spectrometer, resolutionMode));
    if (!resolutionSet)
    {
        return false;
    }

    std::printf(
        "Setting sensitivity to %s (SDK value %u)...\n",
        sensitivityName,
        static_cast<unsigned int>(sensitivityMode));
    return CheckStatus(
        "Setting sensitivity",
        FTS_SetSensitivityMode(Spectrometer, sensitivityMode));
}

bool AbortRequested()
{
    while (_kbhit())
    {
        const int key = _getch();
        if (key == 27 || key == 'q' || key == 'Q')
        {
            return true;
        }
    }

    return false;
}

bool ReadOutSpectrum(SpectrometerIndex spectrometerIndex, ChannelIndex channelIndex)
{
    unsigned int length = 0U;
    int xValueFormat = X_VAL_MINMAX;

    int status = FTS_GetLastSpectrumArrays_ext(
        spectrometerIndex,
        channelIndex,
        nullptr,
        nullptr,
        nullptr,
        &xValueFormat,
        &length);
    if (status != FTS_SUCCESS)
    {
        std::printf(
            "Could not determine spectrum size for channel %u: %d.\n",
            static_cast<unsigned int>(channelIndex),
            status);
        return false;
    }

    if (length == 0U || (xValueFormat != X_VAL_ARRAY && xValueFormat != X_VAL_MINMAX))
    {
        std::printf(
            "Spectrum metadata for channel %u is invalid.\n",
            static_cast<unsigned int>(channelIndex));
        return false;
    }

    std::vector<float> spectrum(length);
    std::vector<float> xAxis(xValueFormat == X_VAL_ARRAY ? length : 2U);

    status = FTS_GetLastSpectrumArrays_ext(
        spectrometerIndex,
        channelIndex,
        spectrum.data(),
        xAxis.data(),
        nullptr,
        &xValueFormat,
        &length);
    if (status != FTS_SUCCESS)
    {
        std::printf(
            "Could not read spectrum for channel %u: %d.\n",
            static_cast<unsigned int>(channelIndex),
            status);
        return false;
    }

    return true;
}

void AcquisitionCallback(
    SpectrometerIndex spectrometerIndex,
    ChannelIndex channelIndex,
    unsigned int updateFlag,
    unsigned int status,
    unsigned short /*typeOfStatus*/)
{
    if (status != FTS_SUCCESS && status != FTS_FINISHED)
    {
        acquisitionError.store(static_cast<int>(status));
        return;
    }

    constexpr unsigned int SpectrumUpdated = 2U;
    if (updateFlag != SpectrumUpdated)
    {
        return;
    }

    if (!ReadOutSpectrum(spectrometerIndex, channelIndex))
    {
        acquisitionError.store(FTS_FAIL);
        return;
    }

    if (channelIndex == outputChannel.load())
    {
        const unsigned int count = acquiredSpectra.fetch_add(1U) + 1U;
        std::printf(
            "Read spectrum %u of %u from channel %u.\n",
            count,
            SpectraToAcquire,
            static_cast<unsigned int>(channelIndex));
    }
}

bool CreateVirtualOSA()
{
    if (!RunOperation(
            "Creating virtual Redstone OSA",
            []()
            {
                return FTS_CreateVirtualSpectrometer(Spectrometer, INSTRUMENT_VIRTUAL_REDSTONE305);
            }))
    {
        return false;
    }

    return RunOperation(
        "Configuring virtual Redstone source",
        []()
        {
            return FTS_SetupVirtualRedstoneSource(Spectrometer, VIRTUAL_REDSTONE_SOURCE_LLD1530);
        });
}
}

int _tmain(int /*argc*/, _TCHAR* /*argv*/[])
{
    std::setvbuf(stdout, nullptr, _IONBF, 0);

    std::printf("Initializing spectrometers...\n");
    FTS_InitializeSpectrometers_ext(nullptr);
    unsigned int instrumentCount = FTS_GetInstrumentNum();
    std::printf("Found %u physical spectrometer(s).\n", instrumentCount);

    if (instrumentCount == 0U)
    {
        std::printf("No physical OSA found; using a virtual Redstone OSA.\n");
        if (!CreateVirtualOSA())
        {
            return 1;
        }
        instrumentCount = FTS_GetInstrumentNum();
    }

    if (instrumentCount == 0U)
    {
        std::printf("No spectrometer is available.\n");
        return 1;
    }

    if (!RunOperation(
            "Opening spectrometer",
            []()
            {
                return FTS_OpenSpectrometer(Spectrometer);
            }))
    {
        return 1;
    }

    char model[SPECTRUM_MODEL_STRLENGTH] = {};
    FTS_GetInstrumentProperty_ModelStr(Spectrometer, model);
    const OSA_SERIES series = FTS_GetInstrumentProperty_Series(Spectrometer);
    std::printf("Using %s.\n", model);

    int exitCode = 1;
    bool acquisitionStarted = false;

    if (!ConfigureSpectrometer(series))
    {
        RunOperation(
            "Closing spectrometer",
            []()
            {
                return FTS_CloseSpectrometer(Spectrometer);
            });
        return exitCode;
    }

    const unsigned int numberOfChannels = FTS_GetNumberOfChannels(Spectrometer);
    if (numberOfChannels == 0U)
    {
        std::printf("The spectrometer reported no acquisition channels.\n");
        RunOperation(
            "Closing spectrometer",
            []()
            {
                return FTS_CloseSpectrometer(Spectrometer);
            });
        return exitCode;
    }

    outputChannel.store(
        series == REDSTONE_SERIES
            ? static_cast<ChannelIndex>(FTS_GetStitchedChannelIndex())
            : 0U);
    std::printf(
        "Reading acquired spectra from channel %u.\n",
        static_cast<unsigned int>(outputChannel.load()));

    if (!RunOperation(
            "Starting continuous acquisition",
            []()
            {
                return FTS_StartContinuousAcquisition_ext(Spectrometer, &AcquisitionCallback);
            }))
    {
        RunOperation(
            "Closing spectrometer",
            []()
            {
                return FTS_CloseSpectrometer(Spectrometer);
            });
        return exitCode;
    }
    acquisitionStarted = true;

    std::printf("Press Q or Esc to stop acquisition.\n");
    const auto deadline = std::chrono::steady_clock::now() + AcquisitionTimeout;
    bool userAborted = false;
    while (acquiredSpectra.load() < SpectraToAcquire
        && acquisitionError.load() == FTS_SUCCESS
        && std::chrono::steady_clock::now() < deadline)
    {
        if (AbortRequested())
        {
            userAborted = true;
            break;
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    if (acquisitionStarted
        && !RunOperation(
            "Stopping continuous acquisition",
            []()
            {
                return FTS_StopContinuousAcquisition(Spectrometer);
            }))
    {
        acquisitionError.store(FTS_FAIL);
    }
    FTS_ClearCallbacks();

    if (acquisitionError.load() != FTS_SUCCESS)
    {
        std::printf("Acquisition stopped with error %d.\n", acquisitionError.load());
    }
    else if (userAborted)
    {
        std::printf("Acquisition stopped by user.\n");
        exitCode = 0;
    }
    else if (acquiredSpectra.load() < SpectraToAcquire)
    {
        std::printf("Acquisition timed out after five minutes.\n");
    }
    else
    {
        std::printf("Acquisition completed successfully.\n");
        exitCode = 0;
    }

    if (!RunOperation(
            "Closing spectrometer",
            []()
            {
                return FTS_CloseSpectrometer(Spectrometer);
            }))
    {
        exitCode = 1;
    }

    return exitCode;
}
