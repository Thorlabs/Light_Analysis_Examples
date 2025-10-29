//Example Date of Creation(YYYY - MM - DD) 2025 - 10 - 07
//Example Date of Last Modification on Github 2025 - 10 - 07
//Version of C++ used for Testing and IDE: C++ 14, Visual Studio 2022
//Version of the Thorlabs SDK used : PAX1000 Software version 1.7
//Example Description: The sample code shows how to control a PAX1000 in C++. 
//In the example the available PAX1000 are found, a connection is established, 
//measurement mode and scan rate are set and scan data is read. Azimuth, ellipticity and DOP are printed to the console.
#include <stdio.h>
#include <string.h>
#include <visa.h>
#include "TLPAX.h"  
#include <windows.h> 

#define PI_VAL   (3.1415926535897932384626433832795f)  

ViStatus find_instrument(ViChar** resource);
void error_exit(ViSession instrHdl, ViStatus err);
void waitKeypress(void);
ViStatus get_device_id(ViSession ihdl);
ViStatus set_measurement_mode(ViSession ihdl);
ViStatus set_basic_scan_rate(ViSession ihdl);
ViStatus get_scan(ViSession ihdl);

int main()
{
    ViStatus    err;
    ViChar* rscPtr;
    ViSession   instrHdl = VI_NULL;
    int         c, done;

    printf("PAX1000 sample\n");

    // Find resources
    err = find_instrument(&rscPtr);
    if (err) error_exit(VI_NULL, err);
    if (rscPtr == NULL) exit(EXIT_SUCCESS); // No instrument found


    // Open session to PAX series instrumentset
    printf("Opening session to '%s' ...\n\n", rscPtr);
    err = TLPAX_init(rscPtr, VI_OFF, VI_ON, &instrHdl);
    if (err) error_exit(instrHdl, err);

    if ((err = get_device_id(instrHdl))) error_exit(instrHdl, err);
    if ((err = set_measurement_mode(instrHdl))) error_exit(instrHdl, err);
    if ((err = set_basic_scan_rate(instrHdl))) error_exit(instrHdl, err);

    Sleep(5000); // Wait 5 s until rotation stabilizes

    for (int i = 0; i < 5; i++)
    {
        if ((err = get_scan(instrHdl))) error_exit(instrHdl, err);
	}
    
    if (instrHdl != VI_NULL) TLPAX_close(instrHdl);
    return 0;
}

void clearInputBuffer()
{
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF);
}

void error_exit(ViSession instrHdl, ViStatus err)
{
    ViChar buf[TLPAX_ERR_DESCR_BUFFER_SIZE];

    // Print error
    TLPAX_errorMessage(instrHdl, err, buf);
    fprintf(stderr, "ERROR: %s\n", buf);

    // Close instrument handle if open
    if (instrHdl != VI_NULL) TLPAX_close(instrHdl);

    // Exit program
    waitKeypress();
    exit(EXIT_FAILURE);
}

void waitKeypress(void)
{
    printf("Press <ENTER> to exit\n");
    while (getchar() == EOF);
}

ViStatus find_instrument(ViChar** resource)
{
    ViStatus       err;
    static ViChar  rscBuf[TLPAX_BUFFER_SIZE];
    ViUInt32       findCnt;

    printf("Scanning for instruments ...\n");

    *resource = NULL;

    err = TLPAX_findRsrc(0, &findCnt);
    if (err) return err;

    if (findCnt < 1)
    {
        printf("No matching instruments found\n\n");
        return VI_ERROR_RSRC_NFOUND;
    }

    // connect to first device
    err = TLPAX_getRsrcName(0, 0, rscBuf);
    if (!err) *resource = rscBuf;
    return err;
}

ViStatus get_device_id(ViSession ihdl)
{
    ViStatus err;
    ViChar   nameBuf[TLPAX_BUFFER_SIZE];
    ViChar   snBuf[TLPAX_BUFFER_SIZE];
    ViChar   revBuf[TLPAX_BUFFER_SIZE];

    err = TLPAX_identificationQuery(ihdl, VI_NULL, nameBuf, snBuf, revBuf);
    if (err) return err;
    printf("Instrument:    %s\n", nameBuf);
    printf("Serial number: %s\n", snBuf);
    printf("Firmware:      V%s\n", revBuf);
    if ((err = TLPAX_revisionQuery(ihdl, revBuf, VI_NULL))) return err;
    printf("Driver:        V%s\n", revBuf);

    return VI_SUCCESS;
}

char const* get_measurement_mode_label(ViUInt32 mode)
{
    char const* str;

    switch (mode)
    {
    case TLPAX_MEASMODE_IDLE:        str = "Idle, no measurements are taken";                          break;
    case TLPAX_MEASMODE_HALF_512:    str = "0.5 revolutions for one measurement, 512 points for FFT";  break;
    case TLPAX_MEASMODE_HALF_1024:   str = "0.5 revolutions for one measurement, 1024 points for FFT"; break;
    case TLPAX_MEASMODE_HALF_2048:   str = "0.5 revolutions for one measurement, 2048 points for FFT"; break;
    case TLPAX_MEASMODE_FULL_512:    str = "1 revolution for one measurement, 512 points for FFT";     break;
    case TLPAX_MEASMODE_FULL_1024:   str = "1 revolution for one measurement, 1024 points for FFT";    break;
    case TLPAX_MEASMODE_FULL_2048:   str = "1 revolution for one measurement, 2048 points for FFT";    break;
    case TLPAX_MEASMODE_DOUBLE_512:  str = "2 revolutions for one measurement, 512 points for FFT";    break;
    case TLPAX_MEASMODE_DOUBLE_1024: str = "2 revolutions for one measurement, 1024 points for FFT";   break;
    case TLPAX_MEASMODE_DOUBLE_2048: str = "2 revolutions for one measurement, 2048 points for FFT";   break;
    default:                         str = "unknown";                                                  break;
    }
    return str;
}


ViStatus set_measurement_mode(ViSession ihdl)
{
    ViUInt32 mode;

    printf("Set Measurement Mode...\n");
    for (mode = TLPAX_MEASMODE_IDLE; mode <= TLPAX_MEASMODE_DOUBLE_2048; mode++)
    {
        printf("(%d) %s\n", mode, get_measurement_mode_label(mode));
    }

    printf("\nPlease select: ");
    while ((mode = getchar()) == EOF);
    mode -= '0';
    clearInputBuffer();
    printf("\n");

    return TLPAX_setMeasurementMode(ihdl, mode);
}

ViStatus set_basic_scan_rate(ViSession ihdl)
{
    ViStatus err;
    ViReal64 bsr, min, max;
    char buf[1000];

    err = TLPAX_getBasicScanRateLimits(ihdl, &min, &max);
    if (err) return err;
    printf("Set Basic Sample Rate in 1/s...\n");
    printf("Enter new Basic Sample rate (%.1f ... %.1f 1/s): ", min, max);

    fgets(buf, sizeof(buf), stdin);
    sscanf_s(buf, "%lf", &bsr);
    err = TLPAX_setBasicScanRate(ihdl, bsr);
    printf("\n\n");
    return err;
}


ViStatus get_scan(ViSession ihdl)
{
    ViStatus err;
    ViSession scanId;
    ViReal64 azimuth;
    ViReal64 ellipticity;
    ViReal64 DOP = 0.0;

    err = TLPAX_getLatestScan(ihdl, &scanId);
    if (err) return err;
    printf("Scan Data:\n");
    err = TLPAX_getPolarization(VI_NULL, scanId, &azimuth, &ellipticity);
    if (!err) err = TLPAX_getDOP(VI_NULL, scanId, &DOP, NULL, NULL);
    TLPAX_releaseScan(VI_NULL, scanId);

    if (err) return err;
    printf("Azimuth:     %.1f degree\n", azimuth * 180.0 / PI_VAL);
    printf("Ellipticity: %.1f degree\n", ellipticity * 180.0 / PI_VAL);
    printf("DOP:         %.1f %%\n\n", DOP * 100.0);
    return VI_SUCCESS;
}

























