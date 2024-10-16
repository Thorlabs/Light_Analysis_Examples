//Example Date of Creation(YYYY - MM - DD) 2024 - 07 - 26
//Example Date of Last Modification on Github 2024 - 07 - 26
//Version of C++ used for Testing and IDE: C++ 14, Visual Studio 2022
//Version of the Thorlabs SDK used : ThorSpectra version 3.25
//Example Description: This example shows how to search the available CCS spectrometers, 
//connect the spectrometer, set the integration time and save the spectrum to the file. 

#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "fstream"
#include "Windows.h"
#include "TLCCS.h" 
#include "visa.h"  

//==============================================================================
// Constants
//===========================================================================   

#define MY_INTEGRATION_TIME   0.1            // unit: s
#define MY_SAMPLE_FILE        "sample.txt"   // the file to store the values to
#define MY_SCAN_COUNT         3              // the scan count

//===========================================================================
// Globals
//===========================================================================   

std::ofstream outfile(MY_SAMPLE_FILE);       // file handling
ViSession   instr = VI_NULL;                 // instrument handle  

//===========================================================================
// Prototypes
//===========================================================================   

void error_exit(ViStatus err);
void waitKeypress(void);

//==============================================================================
// Main
//==============================================================================
int main()
{
    ViStatus    err = VI_SUCCESS;           // error variable
    ViSession   resMgr = VI_NULL;              // resource manager
    ViUInt32    cnt = 0;                    // counts found devices
    ViInt32     status = 0;                    // status variable
    ViReal64    data[TLCCS_NUM_PIXELS];          // scan data array
    ViReal64    wavelength[TLCCS_NUM_PIXELS];   // wavelength array
    ViChar      rscStr[VI_FIND_BUFLEN];          // resource string

    printf("Thorlabs CCS instrument driver sample application\n");

    // Find resources
    printf("Scanning for CCS instruments ...\n");
    if ((err = viOpenDefaultRM(&resMgr))) error_exit(err);
    if ((err = viFindRsrc(resMgr, TLCCS_FIND_PATTERN, VI_NULL, &cnt, rscStr))) error_exit(err);
    printf("Found %u instrument%s ...\n\n", cnt, (cnt > 1) ? "s" : "");
    viClose(resMgr);
    
    // try to open CCS
    printf("Opening session to '%s' ...\n\n", rscStr);
    err = tlccs_init(rscStr, VI_OFF, VI_OFF, &instr);
    // error handling
    if (err)  error_exit(err);

    // try to open file
    if (!outfile)
    {
        printf("Fail to open the TXT file.\n");
        // close CCS
        tlccs_close(instr);
        waitKeypress();
        return 0;
    }

    // set integration time
    err = tlccs_setIntegrationTime(instr, MY_INTEGRATION_TIME);
    // error handling
    if (err)  error_exit(err);

    //Use factory adjustment data to generate the wavelength data array
    err = tlccs_getWavelengthData(instr, TLCCS_CAL_DATA_SET_FACTORY, wavelength, VI_NULL, VI_NULL);
    // error handling
    if (err)  error_exit(err);

    // initial scan
    err = tlccs_startScan(instr);
    // error handling
    if (err)  error_exit(err);

    int i = 0;
    while (i < MY_SCAN_COUNT)
    {
        // request device status
        err = tlccs_getDeviceStatus(instr, &status);
        // error handling
        if (err)  error_exit(err);

        // camera is idle -> we can trigger a scan
        if (status & TLCCS_STATUS_SCAN_IDLE)
        {
            // trigger scan
            err = tlccs_startScan(instr);
            // error handling
            if (err)  error_exit(err);
        }

        // camera has data available for transfer
        if (status & TLCCS_STATUS_SCAN_TRANSFER)
        {
            printf("Starting scan %d of %d ...\n\n", i + 1, MY_SCAN_COUNT);
            
            // trigger scan
            err = tlccs_getScanData(instr, data);
            // error handling
            if (err)  error_exit(err);

            // add seperator
            outfile << "----------------- Scan No. " << i + 1 << "-----------------\n";

            // get time stamp
            time_t now = time(0);

            // store time stamp to file
            char dt[66];
            ctime_s(dt, sizeof dt, &now);
            outfile << dt;

            // store data to file
            for (int j = 0; j < TLCCS_NUM_PIXELS; j++)
            {
                outfile << "Pixel:" << j + 1 << "; Wavelength: " << wavelength[j] << "; Value: " << data[j] << "\n";
            }
         // one scan is done
         ++i;

        }
    }
    // close CCS
    tlccs_close(instr);
    // close output file
    outfile.close();

    waitKeypress();

    // leave main
    return err;
}


/*---------------------------------------------------------------------------
  Error exit
---------------------------------------------------------------------------*/
void error_exit(ViStatus err)
{
    ViChar ebuf[TLCCS_ERR_DESCR_BUFFER_SIZE];

    // Print error
    tlccs_error_message(instr, err, ebuf);
    fprintf(stderr, "ERROR: %s\n", ebuf);

    // Close instrument handle if open
    if (instr != VI_NULL) tlccs_close(instr);

    // Close file stream if open
    if (outfile)  outfile.close();

    // Exit program
    waitKeypress();

    exit(err);
}


/*---------------------------------------------------------------------------
  Print keypress message and wait
---------------------------------------------------------------------------*/
void waitKeypress(void)
{
    printf("Press <ENTER> to exit\n");
    while (getchar() == EOF);
}
