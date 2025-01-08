//Example Date of Creation(YYYY - MM - DD) 2024 - 04 - 24
//Example Date of Last Modification on Github 2024 - 04 - 24
//Version of C++ used for Testing and IDE: C++ 14, Visual Studio 2022
//Version of the Thorlabs SDK used : Beam version 9.1.5787.560
//Example Description: The sample code shows how to control a BP209 beam profiler in C++. 
//In the example the available beam profilers are found, a connection is established, several parameters are set, 
//several output values are displayed and a 2D image is shown.

#include "string"
#include "stdio.h"
#include "stdlib.h"
#include "TLBP2.h"
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

// forward declaration
void print_error_msg(ViStatus err);
void Beam_Profile_Reconstruction();
ViSession m_instrumentHandle;

//set the measured laser wavelengh unit: nm
double wavelength = 633; 
//Set the user power factor:
//1. measure the power of your light source with an external power meter
//2. set the user power factor to 1.0 and get the Total Power from the slit measurement.
//3. Calculate the power factor.User power factor = external measured power / slit measured power.
double powerCorrectionFactor = 1;

int main(int argc, char* argv)
{
	ViStatus res;
	m_instrumentHandle = 0;

	// get the number of connected devices
	ViUInt32 deviceCount = 0;
	TLBP2_get_connected_devices(VI_NULL, VI_NULL, &deviceCount);

	if (deviceCount == 0)
	{
		printf("No device connected\n");
		return 0;
	}

	// initialize the buffer for the resource strings
	BP2_DEVICE* resStr = new BP2_DEVICE[deviceCount];

	// get the reource strings of the connected devices
	res = TLBP2_get_connected_devices(VI_NULL, resStr, &deviceCount);
	if (res != VI_SUCCESS)
	{
		print_error_msg(res);
		delete[] resStr;
		return 0;
	}

	// connect with the first device
	res = TLBP2_init(resStr[0].resourceString, VI_TRUE, VI_TRUE, &m_instrumentHandle);
	if ((res & _VI_ERROR) > 0)
	{
		print_error_msg(res);
		return 0;
	}
	char serialNo[128];
	res = TLBP2_get_serial_number(m_instrumentHandle, serialNo);
	printf("%s is connected. \n", serialNo);

	// release the buffer for the resource strings
	delete[] resStr;
	
	//set auto gain
	res = TLBP2_set_auto_gain(m_instrumentHandle, VI_TRUE);
	if ((res & _VI_ERROR) > 0)
	{
		print_error_msg(res);
		return 0;
	}

	//set bandwidth
	ViReal64 bw_buffer[4] = { 125,125,125,125 };
	res = TLBP2_set_bandwidths(m_instrumentHandle, bw_buffer);
	if ((res & _VI_ERROR) > 0)
	{
		print_error_msg(res);
		return 0;
	}
	
	//set wavelength
	res = TLBP2_set_wavelength(m_instrumentHandle, wavelength);
	if ((res & _VI_ERROR) > 0)
	{
		print_error_msg(res);
		return 0;
	}

	//set power factor
	res = TLBP2_set_user_power_factor(m_instrumentHandle, powerCorrectionFactor);
	if ((res & _VI_ERROR) > 0)
	{
		print_error_msg(res);
		return 0;
	}

	//set scanning method
	int scanningMethod = -1;
	printf("Select the scanning method: \n");
	printf("  0. slit scanning mode(for beam diameter > 20um); \n  1. knife edge mode(for beam diameter <= 20um) ");
	scanf_s("%d", &scanningMethod);
	if (scanningMethod == 0 || scanningMethod == 1)
	{
		res = TLBP2_set_scanning_method(m_instrumentHandle, 0, scanningMethod);
		res = TLBP2_set_scanning_method(m_instrumentHandle, 1, scanningMethod);
		res = TLBP2_set_scanning_method(m_instrumentHandle, 2, scanningMethod);
		res = TLBP2_set_scanning_method(m_instrumentHandle, 3, scanningMethod);
		if ((res & _VI_ERROR) > 0)
		{
			print_error_msg(res);
			return 0;
		}
	}
	else
	{
		printf("Invalid Input! The scanning method is set to slit scanning mode.\n");
		res = TLBP2_set_scanning_method(m_instrumentHandle, 0, 0);
		res = TLBP2_set_scanning_method(m_instrumentHandle, 1, 0);
		res = TLBP2_set_scanning_method(m_instrumentHandle, 2, 0);
		res = TLBP2_set_scanning_method(m_instrumentHandle, 3, 0);
		if ((res & _VI_ERROR) > 0)
		{
			print_error_msg(res);
			return 0;
		}
	}

	//set drum speed
	ViUInt16 sampleCount;
	ViReal64 resolution;
	if(scanningMethod == 0) //slit scanning mode
		res = TLBP2_set_drum_speed_ex(m_instrumentHandle, 10, &sampleCount, &resolution);
	else //knife edge mode
		res = TLBP2_set_drum_speed_ex(m_instrumentHandle, 2, &sampleCount, &resolution);
	if ((res & _VI_ERROR) > 0)
	{
		print_error_msg(res);
		return 0;
	}

	//set position correction
	res = TLBP2_set_position_correction(m_instrumentHandle, VI_TRUE);
	if ((res & _VI_ERROR) > 0)
	{
		print_error_msg(res);
		return 0;
	}

	//set speed correction
	res = TLBP2_set_speed_correction(m_instrumentHandle, VI_TRUE);
	if ((res & _VI_ERROR) > 0)
	{
		print_error_msg(res);
		return 0;
	}
	
	// Waiting the device to be ready for a new measurement
	ViUInt16 device_status = 0;
	while (res == VI_SUCCESS && (device_status & BP2_STATUS_SCAN_AVAILABLE) == 0)
	{
		res = TLBP2_get_device_status(m_instrumentHandle, &device_status);
	}

	static BP2_SLIT_DATA slit_data[4], slit_data_kinfe[4]; /// BP2_MAX_SLIT_COUNT = 4
	static BP2_CALCULATIONS calculation_result[4], calculation_result_knife[4];
	static ViReal64 power_intensities[7500];
	static ViBoolean slit_indices[4] = { VI_TRUE, VI_TRUE, VI_TRUE, VI_TRUE};
	ViReal64 power;
	ViReal32 powerSaturation;
	ViUInt8 gain[4];
	ViUInt8 gainPower;

	//Adjusting the gain. 
	//When the auto gain is set to TRUE, the gain will be corrected with every measurement and take effect in the next measurement.
	printf("Adjusting Gain...\n");
	for (int i = 0; i < 10; i++)
	{
		res = TLBP2_get_slit_scan_data(m_instrumentHandle, slit_data, calculation_result, &power, &powerSaturation, power_intensities);
		res = TLBP2_get_gains(m_instrumentHandle, gain, &gainPower);
		printf("Gain:\n");
		printf("  25um slit x: %d, 25um slit y: %d\n", gain[0],gain[1]);
		printf("  5um slit x: %d, 5um slit y: %d\n", gain[2], gain[3]);
		printf("Power Saturation: %.2f%%\n\n", powerSaturation*100);
	}

	//Start a measurement
	if (scanningMethod == 0)//slit scanning mode
	{
		//Get the slit scan data
		res = TLBP2_get_slit_scan_data(m_instrumentHandle, slit_data, calculation_result, &power, &powerSaturation, power_intensities);
		if (res == VI_SUCCESS)
		{
			printf("Corrected Power value: %.2f mW\n", power);
			printf("5um Slit X Centroid Position: %.2f\n", calculation_result[2].centroidPosition);
			printf("5um Slit Y Centroid Position: %.2f\n", calculation_result[3].centroidPosition);
			printf("5um Slit X Gaussian Fit Diameter: %.2f\n", calculation_result[2].gaussianFitDiameter);
			printf("5um Slit Y Gaussian Fit Diameter: %.2f\n", calculation_result[3].gaussianFitDiameter);
			Beam_Profile_Reconstruction();
		}
	}
	else//knife edge mode
	{
		//Calculate the knife edge data from the slit data.
		res = TLBP2_get_slit_scan_data(m_instrumentHandle, slit_data, calculation_result, &power, &powerSaturation, power_intensities);
		res = TLBP2_get_knife_edge_reconstruction(m_instrumentHandle, slit_data, calculation_result, slit_indices, slit_data_kinfe, calculation_result_knife);
		if (res == VI_SUCCESS)
		{
			printf("Corrected Power value: %.2f mW\n", power);
			printf("25um Slit X Centroid Position: %.2f\n", calculation_result_knife[0].centroidPosition);
			printf("25um Slit Y Centroid Position: %.2f\n", calculation_result_knife[1].centroidPosition);
			printf("25um Slit X Gaussian Fit Diameter: %f\n", calculation_result_knife[0].gaussianFitDiameter);
			printf("25um Slit Y Gaussian Fit Diameter: %f\n", calculation_result_knife[1].gaussianFitDiameter);
		}
		else
			printf("Fail to reconstruct the knife edge data\n");
	}

	// release the device
	TLBP2_close(m_instrumentHandle);

	return 0;
}

//Reconstruct the x-axis intensity distrubution and the 2D intensity distribution
void Beam_Profile_Reconstruction()
{
	ViStatus res;
	static ViReal64 sampleIntensitiesX[7500];
	static ViReal64 sampleIntensitiesY[7500];
	static ViReal64 samplePositionsX[7500];
	static ViReal64 samplePositionsY[7500];
	static ViReal64 gaussianFitIntensitiesX[7500];
	static ViReal64 gaussianFitIntensitiesY[7500];
	ViReal32 gaussianFitPercentageX, gaussianFitPercentageY;

	//Request the scan data
	TLBP2_request_scan_data(m_instrumentHandle, VI_NULL, VI_NULL, VI_NULL);
	//Get the intensities from the 5um X slit and the 5um Y slit 
	res = TLBP2_get_sample_intensities(m_instrumentHandle, 2, sampleIntensitiesX, samplePositionsX);
	res = TLBP2_get_sample_intensities(m_instrumentHandle, 3, sampleIntensitiesY, samplePositionsY);
	//Get the Gausian fit intensities from the 5um X slit and the 5um Y slit 
	res = TLBP2_get_slit_gaussian_fit(m_instrumentHandle, 2, VI_NULL, VI_NULL, &gaussianFitPercentageX, gaussianFitIntensitiesX);
	res = TLBP2_get_slit_gaussian_fit(m_instrumentHandle, 3, VI_NULL, VI_NULL, &gaussianFitPercentageY, gaussianFitIntensitiesY);

	//Matrices to store image data for every pixel
	Mat IntensityXImage(500, 500, CV_8UC1, Scalar(255));
	Mat GaussianXImage(500, 500, CV_8UC1, Scalar(255));

	//Matrices to store position, intensities, and gauiisan fit inensities
	Mat positionX(7500, 1, CV_64F, samplePositionsX);
	Mat intensitiesX(7500, 1, CV_64F, sampleIntensitiesX);
	Mat intensitiesGaussianX(7500, 1, CV_64F,gaussianFitIntensitiesX);

	//Normalize the intensities and position values to the size of the image
	normalize(intensitiesX, intensitiesX, 0, 250, NORM_MINMAX, -1, Mat());
	normalize(intensitiesGaussianX, intensitiesGaussianX, 0, 250 * gaussianFitPercentageX, NORM_MINMAX, -1, Mat());
	normalize(positionX, positionX, 0, 500, NORM_MINMAX, -1, Mat());

	//Draw intensities curve and gaussian fit curve on respective images
	vector<Point> curvePoints;
	vector<Point> curvePointsGaussian;
	for (int i = 0; i < 7500; ++i)
	{
		Point pt(positionX.at<double>(i, 0), 250 - intensitiesX.at<double>(i, 0));
		curvePoints.push_back(pt);
		Point ptGaussian(positionX.at<double>(i, 0), 250 - intensitiesGaussianX.at<double>(i, 0));
		curvePointsGaussian.push_back(ptGaussian);
	}
	polylines(IntensityXImage, curvePoints, false, Scalar(0), 1);
	polylines(GaussianXImage, curvePointsGaussian, false, Scalar(0), 1);

	//Draw x and y coordinate axes
	line(IntensityXImage, Point(0, 250), Point(500 - 1, 250), Scalar(0), 1);
	line(GaussianXImage, Point(0, 250), Point(500 - 1, 250), Scalar(0), 1);
	line(IntensityXImage, Point(250, 500 - 1), Point(250, 0), Scalar(0), 1);
	line(GaussianXImage, Point(250, 500 - 1), Point(250, 0), Scalar(0), 1);

	//Variables for intensity calculation in 2D reconstrution
	int ixz, iyz;
	static float intensityTemp[750][750];
	float intensityMax = 0;
	//Matrix to store the 2D intensity distribution
	Mat reconstructionImage(750, 750, CV_8UC1,Scalar(0));

	//Calculate intensity distribution for 2D reconstruction
	for (int row = 0; row < 750; row++)
	{
		for (int col = 0; col < 750; col++)
		{
			ixz = (750 - row - 1) * 10;
			iyz = (750 - col - 1) * 10;

			intensityTemp[row][col] = sampleIntensitiesX[ixz] * gaussianFitIntensitiesX[ixz] * sampleIntensitiesY[iyz] * gaussianFitIntensitiesY[iyz];
			if (intensityTemp[row][col] > intensityMax)
			{
				intensityMax = intensityTemp[row][col];
			}
		}
	}

	//Normalize intensity values for 2D reconstruction
	for (int row = 0; row < 750; row++)
	{
		for (int col = 0; col < 750; col++)
		{
			reconstructionImage.at<uchar>(col, row) = (uchar)(255 * intensityTemp[row][col] / intensityMax);
		}
	}
	imshow("X Intensity", IntensityXImage);
	imshow("X Gaussian Fit Intensity", GaussianXImage);
	imshow("2D Reconstruction", reconstructionImage);
	waitKey(0);
}

// prints the error message from an error code
void print_error_msg(ViStatus errorCode)
{
	char messageBuffer[256];

	// Get error string
	TLBP2_error_message(m_instrumentHandle, errorCode, messageBuffer);

	if ((errorCode & _VI_ERROR) == 0) // just a scan warning, no error
		printf("Beam Profiler Warning: %s\n", messageBuffer);
	else // errors
	{
		printf("Beam Profiler Error: %s\n", messageBuffer);

		// close instrument after an error has occured
		if (m_instrumentHandle > 0)
			TLBP2_close(m_instrumentHandle);
	}
}

