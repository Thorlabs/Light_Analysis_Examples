//Example Date of Creation(YYYY - MM - DD) 2024 - 06 - 11
//Example Date of Last Modification on Github 2024 - 06 - 11
//Version of C++ used for Testing and IDE: C++ 14, Visual Studio 2022
//Version of the Thorlabs SDK used : Wavefront Sensor Software version 6.1

#include <stdlib.h>
#include <stdio.h>
#include "wfs.h" // Wavefront Sensor driver's header file

using namespace std;

void handle_errors(int);
int select_instrument(ViChar resourceName[], ViChar serialNum[]);
int select_mla(ViInt32 mlaSelected);
int run_auto_exposure();
int set_pupil_to_the_measured_beam();
ViSession instr = VI_NULL;

int main(void)
{
	/*================Set WFS parameters================*/
	//the blacklevel corresponds to the [black level] in the Camera Settings tab
	ViInt32 blackLevel = 0;

	//the noisefloor corresponds to the [noise cut level] in the Camera Settings tab
	ViInt32 noiseFloor = 0;

	//the dynamicNoiseCut corresponds to the [Auto] button besides the noise cut level in the Camera Settings tab
	//Valid values: 0 = inactivate, 1 = activate
	ViInt32 dynamicNoiseCut = 0;

	//the cancelWavefrontTilt corresponds to [Cancel Average Wavefront Tilt] in the MLA/Wavefront tab
	//Valid values: 0 = calculate deviations normal, 1 = subtract mean deviation in pupil from all spot deviations
	ViInt32 cancelWavefrontTilt = 0; 

	//the limitToPupil corresponds to the [Limit Wavefront Calculation and Display to Pupil Interior] in the Pupil Definition tab
	//Valid values: 0 = calculate the wavefront for full spots, 1= calculate the wavefront inside the pupil
	ViInt32 limitToPupil = 1;
	
	
	int err;
	ViChar resourceName[64];
	ViChar serialNum[64];

	// Show all and select one WFS instrument
	if (!select_instrument(resourceName,serialNum))
	{
		printf("\nNo available instrument selected. \n");
		return 0; // program ends here if no instrument selected
	}

	// Open the Wavefront Sensor instrument
	if (err = WFS_init(resourceName, VI_FALSE, VI_FALSE, &instr))
		handle_errors(err);

	// print out the resource name
	printf("Serial Number of the Connected WFS: %s\n", serialNum);

	ViInt32 mlaSelected=0;
	if (!select_mla(mlaSelected))
	{
		printf("No available instrument selected. \n");
		return 0; // program ends here if no instrument selected
	}

	WFS_SelectMla(instr, mlaSelected - 1);

	//configure camera resolution and pixel format. 
	//pixel format: Thorlabs WFS instruments currently support only 8 bit format.
	//camera resolution: full list of available resolutions can be found in C:\Program Files (x86)\IVI Foundation\VISA\WinNT\WFS\Manual\WFS_files\FunctWFS_ConfigureCam.html
	ViInt32 numSpotsX, numSpotsY;
	if (err = WFS_ConfigureCam(instr, PIXEL_FORMAT_MONO8, CAM_RES_768, &numSpotsX, &numSpotsY))
		handle_errors(err);

	//set WFS reference plane to internal reference plane
	//other user-defined reference planes can be configured in the WFS software.These are saved to a.ref file and are accessed by passing a 1 instead of 0
	if (err = WFS_SetReferencePlane(instr, 0))
		handle_errors(err);

	//set black level
	if (err = WFS_SetBlackLevelOffset(instr, blackLevel))
		handle_errors(err);

	//auto tune the exposure time
	printf("\nAuto tunning the exposure time, please wait...");
	if (run_auto_exposure())
		printf("auto exposure setting succeeds.\n");
	else
	{
		printf("Fail to set suitable exposure time and master gain. Program finishes.\n");
		WFS_close(instr);
		return 0;
	}

	//set pupil. the diameter and the center of the pupil equals to the diameter of the center of the current beam
	if (set_pupil_to_the_measured_beam() == 0)
	{
		printf("Fail to detect the beam. Program finishes.\n");
		WFS_close(instr);
		return 0;
	}
	
	//take a spot field image
	ViReal64 exposureTimeAct, masterGainAct;
	if (err = WFS_TakeSpotfieldImageAutoExpos(instr, &exposureTimeAct, &masterGainAct))
		handle_errors(err);

	//auto set the noise floor. the range is from 0 to limit
	if (err = WFS_CutImageNoiseFloor(instr, noiseFloor))
		handle_errors(err);
	
	//Display Current WFS Settings
	ViInt32 blackLevelOffsetAct;
	ViReal64 pupilCenterX, pupilCenterY, pupilDiaX, pupilDiaY;
	WFS_GetBlackLevelOffset(instr, &blackLevelOffsetAct);
	WFS_GetPupil(instr, &pupilCenterX, &pupilCenterY, &pupilDiaX, &pupilDiaY);
	printf("\n\nWFS Settings:\n");
	printf("Black Level Offset: %d\n", blackLevelOffsetAct);
	printf("Noise Cut Floor: %d. ", noiseFloor);
	printf("Dynamic Noise Cut: ");
	if (dynamicNoiseCut) printf("Yes\n");
	else printf("No\n");
	printf("Exposure Time: %.3f\n", exposureTimeAct);
	printf("Master Gain: %.3f\n", masterGainAct);
	printf("Pupil Position: x= %.3f, y= %.3f. Pupil Diameter: Phi_x= %.3f, Phi_y= %.3f\n", pupilCenterX, pupilCenterY, pupilDiaX, pupilDiaY);
	printf("Limit the Wavefront Calculation to Pupil: ");
	if (limitToPupil) printf("Yes\n\n");
	else printf("No\n\n");
	printf("Cancel Tilt: ");
	if (cancelWavefrontTilt) printf("Yes\n");
	else printf("No\n");
	
	
	//calculate Beam Centroid and print values
	ViReal64 beamCentroidX, beamCentroidY, beamDiameterX, beamDiameterY;
	if (err = WFS_CalcBeamCentroidDia(instr, &beamCentroidX, &beamCentroidY, &beamDiameterX, &beamDiameterY))
		handle_errors(err);
	printf("Beam Centroid X: %.3f mm\n", beamCentroidX);
	printf("Beam Centroid Y: %.3f mm\n", beamCentroidY);
	printf("Beam Diameter X: %.3f mm\n", beamDiameterX);
	printf("Beam Diameter Y: %.3f mm\n", beamDiameterY);

	// calculate all spot centroid positions using dynamic noise cut option
	if (err = WFS_CalcSpotsCentrDiaIntens(instr, dynamicNoiseCut, 1))
		handle_errors(err);

	// calculate spot deviations to internal reference
	if (err = WFS_CalcSpotToReferenceDeviations(instr, cancelWavefrontTilt))
		handle_errors(err);

	//calculate wavefront array
	//wavefront type valid settings:
	//0 = Measured Wavefront
	//1 = Reconstructed Wavefront based on Zernike coefficients
	//2 = Difference between measured and reconstructed Wavefront
	//structure of the wavefrontArray: First array index is the spot number in Y, second index the spot number in X direction. 
	//unit of the wavefrontArray elements: um
	float wavefrontArray[80][80];
	if (err = WFS_CalcWavefront(instr, 0, limitToPupil, *wavefrontArray))
		handle_errors(err);


	//calculate the wavefront values
	//WFS_CalcWavefront is required before calling WFS_CalcWavefrontStatistics
	ViReal64 wavefrontMin, wavefrontMax, wavefrontPV, wavefrontMean, wavefrontRMS, wavefrontWeightedRMS;
	if (err = WFS_CalcWavefrontStatistics(instr,&wavefrontMin,&wavefrontMax,&wavefrontPV,&wavefrontMean,&wavefrontRMS,&wavefrontWeightedRMS))
		handle_errors(err);
	printf("RMS wavefront: %.3f um\n", wavefrontRMS);
	printf("PV wavefront: %.3f um\n\n", wavefrontPV);
	
	//close the device
	WFS_close(instr);
	return 0;
}



/*===============================================================================================================================
  Handle Errors
  This function retrieves the appropriate text to the given error number and closes the connection in case of an error
===============================================================================================================================*/
void handle_errors(int err)
{
	char buf[512];

	if (!err) return;

	// Get error string
	WFS_error_message(instr, err, buf);

	if (err < 0) // errors
	{
		printf("\nWavefront Sensor Error: %s\n", buf);

		// close instrument after an error has occured
		printf("\nSample program will be closed because of the occured error. ");
		WFS_close(instr); // required to release allocated driver data
		exit(1);
	}
}

/*===============================================================================================================================
  Select Instrument
===============================================================================================================================*/
int select_instrument(ViChar resourceName[], ViChar serialNum[])
{
	ViInt32 err, instrCount, instrSelected;
	ViInt32 deviceID;
	ViInt32 inUse;
	ViChar instrName[256];

	// Find available instruments
	if (err = WFS_GetInstrumentListLen(VI_NULL, &instrCount))
		handle_errors(err);

	// List available instruments
	printf("Available Wavefront Sensor instruments:\n");

	for (int i = 0; i < instrCount; i++)
	{
		if (err = WFS_GetInstrumentListInfo(VI_NULL, i, &deviceID, &inUse, instrName, serialNum, VI_NULL))
			handle_errors(err);

		printf("%4d   %s    %s    %s\n", deviceID, instrName, serialNum, (!inUse) ? "" : "(inUse)");
	}

	serialNum = 0;

	// Select instrument
	printf("Select a Wavefront Sensor instrument: ");
	scanf_s("%d", &instrSelected);
	if (instrSelected > instrCount || instrSelected <= 0)
	{
		printf("invalid input! ");
		return 0;
	}

	if (err = WFS_GetInstrumentListInfo(VI_NULL, instrSelected - 1, VI_NULL, VI_NULL, VI_NULL, serialNum, resourceName))
		handle_errors(err);

	return 1;
}


/*===============================================================================================================================
  Select MLA
===============================================================================================================================*/
int select_mla(ViInt32 mlaSelected)
{
	int err;
	ViInt32 mlaCount;
	ViChar mlaName[20];
	ViReal64 camPitch, lensletPitch;

	// Read out number of available Microlens Arrays 
	if (err = WFS_GetMlaCount(instr, &mlaCount))
		handle_errors(err);

	// List available Microlens Arrays
	printf("\nAvailable Microlens Arrays:\n");
	for (int i = 0; i < mlaCount; i++)
	{
		if (WFS_GetMlaData(instr, i, mlaName, &camPitch, &lensletPitch, VI_NULL, VI_NULL, VI_NULL, VI_NULL, VI_NULL))
			handle_errors(err);

		printf("%2d  %s   CamPitch=%6.3f LensletPitch=%6.3f\n", i+1, mlaName, camPitch, camPitch);
	}

	// Select MLA
	printf("Select a Microlens Array: ");
	scanf_s("%d", &mlaSelected);
	if (mlaSelected > mlaCount || mlaSelected <= 0)
	{
		printf("invalid input! ");
		return 0;
	}

	return 1;
}

/*===============================================================================================================================
  Set the exposure time automatically
===============================================================================================================================*/
int run_auto_exposure()
{
	int err;
	ViReal64 exposureTimeAct,masterGainAct;
	ViInt32 status;
	// run the function 20 times to auto adjust the exposure time and gain
	for (int i = 0; i < 20; i++)
	{
		if (err = WFS_TakeSpotfieldImageAutoExpos(instr, &exposureTimeAct, &masterGainAct))
			handle_errors(err);
	}

	if (err = WFS_GetStatus(instr, &status))
		handle_errors(err);

	if (status & 0x00000002)
	{
		printf("Power too high\n");
		return 0;
	}
	else if (status & 0x00000004)
	{
		printf("Power too low\n");
		return 0;
	}
	else if (status & 0x00000008)
	{
		printf("High ambient light\n");
		return 0;
	}
	else if (status & 0x00000010)
	{
		printf("Spot Contrast too low\n");
		return 0;
	}
	else
	{
		//the captured image can be used.
		return 1;
	}
}

/*===============================================================================================================================
  Set the pupil to the measured beam. 
  Only the spots that are located within the pupil are used for fitting the measured wavefront distortions to Zernike functions. 
===============================================================================================================================*/
int set_pupil_to_the_measured_beam()
{
	int err;
	ViReal64 beamCentroidX, beamCentroidY, beamDiameterX, beamDiameterY;

	//calculate the beam diameter and beam centroid position
	if (err = WFS_CalcBeamCentroidDia(instr, &beamCentroidX, &beamCentroidY, &beamDiameterX, &beamDiameterY))
		handle_errors(err);

	if (beamDiameterX == 0 || beamDiameterY == 0)
	{	
		//if the x-axis or y-axis beam diameter is 0, means the sensor fails to detect a beam.
	 	return 0;
	}
	else
	{
		//set the pupil to the calculated beam diameter and beam centroid position
		if (err = WFS_SetPupil(instr, beamCentroidX, beamCentroidY, beamDiameterX, beamDiameterY))
			handle_errors(err);
		return 1;
	}

}

