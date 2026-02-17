// Title: BP209 2D Reconstruction C Sharp Example. 
// Created Date: 2024 - 10 - 12
// Last modified date: 2026 - 01 - 29
// .NET version: 4.8
// Thorlabs SDK Version: Beam version 9.3
// Notes: This example is based on the C sharp example which is installed to
// C:\Program Files (x86)\IVI Foundation\VISA\WinNT\TLBP2\Examples during software installation. 
// This example has added the 2D reconstruction algorithm and the reconstructed beam image is displayed. 

namespace Thorlabs.BP2_CSharpDemo
{
    using System;
    using System.Data;
    using System.Drawing;
    using System.Drawing.Imaging;
    using System.Runtime.InteropServices;
    using System.Text;
    using System.Windows.Forms;
    using Thorlabs.TLBP2.Interop;

    /// <summary>
    /// Initializes the form
    /// </summary>
   public partial class Form1 : Form
   {
      /// <summary>
      /// Class to access a <c>Thorlabs BP2</c> instrument.
      /// </summary>
      private TLBP2 bp2Device = null;

      /// <summary>
      /// catches the returned status by a driver function.
      /// </summary>
      private int status;

      /// <summary>
      /// poll for a valid scan
      /// </summary>
      private Timer scanTimer = null;

      /// <summary>
      /// Initializes a new instance of the <see cref="Form1"/> class.
      /// </summary>
      public Form1()
      {
         this.InitializeComponent();

         this.chart25um.Titles.Add("Slits 25µm");
         this.chart5um.Titles.Add("Slits 5µm");
 
         // implementation with driver functions
         this.ConnectToTheFirstDevice();

         if (this.bp2Device != null)
         {
            // get the instrument information
            StringBuilder instrText = new StringBuilder(256);
            if (0 == this.bp2Device.get_instrument_name(instrText))
            {
               this.textBox_instrumentName.Text = instrText.ToString();
            }

            if (0 == this.bp2Device.get_serial_number(instrText))
            {
               this.textBox_serialNumber.Text = instrText.ToString();
            }

            StringBuilder instrRev = new StringBuilder(256);
            if (0 == this.bp2Device.revision_query(instrText, instrRev))
            {
               this.textBox_driverVersion.Text = instrText.ToString();
            }

            // clear the status bar
            this.toolStripStatusLabel1.Text = string.Empty;

            // increase the drum speed
            ushort sampleCount;
            double sampleResolution;
            this.status = this.bp2Device.clear_drum_speed_offset();
            this.status = this.bp2Device.set_drum_speed_ex(10.0, out sampleCount, out sampleResolution);

            // activate the position correction to have the same calculation results as the Thorlabs Beam Application
            this.status = this.bp2Device.set_position_correction(true);

            // activate the automatic gain calcuation
            this.status = this.bp2Device.set_auto_gain(true);

            // activate the drum speed correction
            this.status = this.bp2Device.set_speed_correction(true);

            // return all position coordinates from -4500 µm to 4500 µm and flip the x scans
            this.status = this.bp2Device.setThorlabsBeamCompatibleCoordinateSystem(true);
            
            // set the calculation area to auto rectangle, and set the clip level to 1%
            // which is the same as the software default settings
            this.status = this.bp2Device.set_calculation_area(0,true,0.01f,0,0);
            this.status = this.bp2Device.set_calculation_area(1,true,0.01f,0,0);
            this.status = this.bp2Device.set_calculation_area(2,true,0.01f,0,0);
            this.status = this.bp2Device.set_calculation_area(3,true,0.01f,0,0);

            // poll for a valid scan
            this.scanTimer = new Timer();
            this.scanTimer.Interval = 50;
            this.scanTimer.Tick += this.ScanTimer_Tick;
            this.scanTimer.Start();
         }
      }

      /// <summary>
      /// search for connected devices and connect to the first one.
      /// Use only driver functions and structures.
      /// </summary>
      private void ConnectToTheFirstDevice()
      {
         // intialize the driver class to call the pseudo static function "get_connected_devices"
         this.bp2Device = new TLBP2(new IntPtr());
         if (this.bp2Device != null)
         {
            uint deviceCount;
            this.status = this.bp2Device.get_connected_devices(null, out deviceCount);

            if (this.status == 0 && deviceCount > 0)
            {
               bp2_device[] deviceList = new bp2_device[deviceCount];
               this.status = this.bp2Device.get_connected_devices(deviceList, out deviceCount);

               if (this.status == 0)
               {
                  // connect to the first device
                  this.bp2Device = new TLBP2(deviceList[0].ResourceString, false, false);
               }
               else
               {
                  this.bp2Device.Dispose();
                  this.bp2Device = null;
               }
            }
            else
            {
               this.bp2Device.Dispose();
               this.bp2Device = null;
            }
         }
      }

      /// <summary>
      /// poll for a new measurement and fill the structures with the calculation results.
      /// </summary>
      private void GetMeasurement()
      {
         // get the drum speed
         double drumSpeed;
         try
         {
            if (0 == this.bp2Device.get_averaged_drum_speed(out drumSpeed))
            {
               this.textBox_drumSpeed.Text = drumSpeed.ToString("f2");
            }
         }
         catch (System.Runtime.InteropServices.ExternalException ex)
         {
            // if the speed could not be measured -> this should cause no exception
            if (ex.ErrorCode != -1074001659)
               throw ex;
         }

         // get the drum status
         ushort deviceStatus = 0;
         if (0 == this.bp2Device.get_device_status(out deviceStatus))
         {
            if ((deviceStatus & 4) == 4)
            {
               this.toolStripStatusLabel1.Text = "Drum speed not stabilized.";
            }
            else if ((deviceStatus & 2) == 2)
               this.toolStripStatusLabel1.Text = "Instrument is ready";
         }
         
         double power;
         float powerSaturation;
         ushort peakIndex1, peakIndex2,sampleCount1,sampleCount2,centroidIndexSlit1, centroidIndexSlit2;
         float peakPositionSlit1, peakPositionSlit2, centroidPositionSlit1, centroidPositionSlit2, peakIntensitySlit1, peakIntensitySlit2;
         float darkLevelSlit1, darkLevelSlit2;

         if ((deviceStatus & 1) == 1 && 0 == this.bp2Device.request_scan_data(out power, out powerSaturation, null))
         {
            // get the peak position and centriod position
            this.bp2Device.get_slit_peak(0, out peakIndex1, out peakPositionSlit1, out peakIntensitySlit1);
            this.bp2Device.get_slit_peak(1, out peakIndex2, out peakPositionSlit2, out peakIntensitySlit2);
            this.bp2Device.get_scan_data_information(0, out sampleCount1, out darkLevelSlit1);
            this.bp2Device.get_scan_data_information(1, out sampleCount2, out darkLevelSlit2);
            this.bp2Device.get_slit_centroid(0, out centroidIndexSlit1,out centroidPositionSlit1);
            this.bp2Device.get_slit_centroid(1, out centroidIndexSlit2, out centroidPositionSlit2);

            this.textBox_peakPositionSlit1.Text = peakPositionSlit1.ToString("f2");
            this.textBox_peakIntensitySlit1.Text = (peakIntensitySlit1 * 100.0f / ((float)0x7AFF - darkLevelSlit1)).ToString("f2");
            this.textBox_centroidPositionSlit1.Text  = centroidPositionSlit1.ToString("f2");

            this.textBox_peakPositionSlit2.Text = peakPositionSlit2.ToString("f2");
            this.textBox_peakIntensitySlit2.Text = (peakIntensitySlit2 * 100.0f / ((float)0x7AFF - darkLevelSlit2)).ToString("f2");
            this.textBox_centroidPositionSlit2.Text = centroidPositionSlit2.ToString("f2");

            this.textBox_powerSaturation.Text   = (powerSaturation*100.0).ToString("f2");

            GetChartAnd2DReconstruction();

         }
      }

        /// <summary>
        /// Calculate the 2D reconstructed beam intensity distribution and display the image on the WinForm
        /// </summary>
        private void GetChartAnd2DReconstruction()
      {
            double[] sampleIntensities25umX = new double[7500];
            double[] sampleIntensities25umY = new double[7500];
            double[] samplePosition25umX = new double[7500];
            double[] samplePosition25umY = new double[7500];
            double[] sampleIntensities5umX = new double[7500];
            double[] sampleIntensities5umY = new double[7500];
            double[] samplePosition5umX = new double[7500];
            double[] samplePosition5umY = new double[7500];
            double[] gaussianFitIntensities25umX = new double[7500];
            double[] gaussianFitIntensities25umY = new double[7500];
            float temp;
            
            //Get the intensities from the 25um X slit and the 25um Y slit
            this.bp2Device.get_sample_intensities(0, sampleIntensities25umX, samplePosition25umX);
            this.bp2Device.get_sample_intensities(1, sampleIntensities25umY, samplePosition25umY);

            //Get the intensities from the 5um X slit and the 5um Y slit
            this.bp2Device.get_sample_intensities(2, sampleIntensities5umX, samplePosition5umX);
            this.bp2Device.get_sample_intensities(3, sampleIntensities5umY, samplePosition5umY);

            //Chart display
            this.chart25um.Series[0].Points.DataBindXY(samplePosition25umX, sampleIntensities25umX);
            this.chart25um.Series[1].Points.DataBindXY(samplePosition25umY, sampleIntensities25umY);
            this.chart5um.Series[0].Points.DataBindXY(samplePosition5umX, sampleIntensities5umX);
            this.chart5um.Series[1].Points.DataBindXY(samplePosition5umY, sampleIntensities5umY);

            //Get the gaussian fit intensites from the 25um X slit and the 25um Y slit
            this.bp2Device.get_slit_gaussian_fit(0, out temp,out temp,out temp, gaussianFitIntensities25umX);
            this.bp2Device.get_slit_gaussian_fit(1, out temp, out temp, out temp, gaussianFitIntensities25umY);

            //2D reconstruction 
            int imageSize = 750;
            double[,] imageData = new double[imageSize, imageSize];
            double imageDataMax = 0;
            int ixz, iyz;
            for (int ix = 0; ix < imageSize; ix++)
            {
                for (int iy = 0; iy < imageSize; iy++)
                {
                    //2D reconstruction algorithm
                    ixz = (imageSize - ix - 1) * 7500 / imageSize;
                    iyz = (imageSize - iy - 1) * 7500 / imageSize;
                    imageData[ix, iy] = sampleIntensities25umX[ixz] * gaussianFitIntensities25umX[ixz] * sampleIntensities25umY[iyz] * gaussianFitIntensities25umY[iyz];

                    //set the negative values to zero
                    if (imageData[ix, iy] < 0)
                    {
                        imageData[ix, iy] = 0;
                    }
                    //find the maximum value
                    else if (imageData[ix, iy] > imageDataMax)
                    {
                        imageDataMax = imageData[ix, iy];
                    }
                }
            }

            //Normalize intensity values and generate the Bitmap image
            Bitmap bitmap = new Bitmap(imageSize, imageSize, PixelFormat.Format24bppRgb);
            BitmapData bmpData = bitmap.LockBits(
                new Rectangle(0, 0, imageSize, imageSize),ImageLockMode.WriteOnly,bitmap.PixelFormat);

            int stride = bmpData.Stride;
            byte[] pixelData = new byte[stride * imageSize];

            for (int y = 0; y < imageSize; y++)
            {
                for (int x = 0; x < imageSize; x++)
                {
                    int gray = (int)(imageData[x, y] * 255 / imageDataMax);
                    gray = Math.Min(255, Math.Max(0, gray));
                    int pixelIndex = y * stride + x * 3;
                    pixelData[pixelIndex + 0] = (byte)gray;
                    pixelData[pixelIndex + 1] = (byte)gray;
                    pixelData[pixelIndex + 2] = (byte)gray;
                }
            }

            Marshal.Copy(pixelData, 0, bmpData.Scan0, pixelData.Length);
            bitmap.UnlockBits(bmpData);
            this.reconstructionPicture.Image = bitmap;
        }
        /// <summary>
        /// If a new scan is available, get the data from the instrument and display the calculation results on the form.
        /// This function is called by the scan timer every <c>50ms</c>.
        /// </summary>
        /// <param name="sender">The timer object which has fired the event.</param>
        /// <param name="e">Parameters of the event.</param>
        private void ScanTimer_Tick(object sender, EventArgs e)
      {
         if (this.bp2Device != null)
         {
            this.GetMeasurement();
         }
      }

      /// <summary>
      /// This function is called before the main form will close.
      /// The connection to the instrument will be closed and all resources released.
      /// </summary>
      /// <param name="sender">Main form object.</param>
      /// <param name="e">Parameters for the close event.</param>
      private void Form1_FormClosing(object sender, FormClosingEventArgs e)
      {
         if (null != this.scanTimer)
         {
            this.scanTimer.Stop();
         }

         // close the device and release the resources
         if (this.bp2Device != null)
         {
            this.bp2Device.Dispose();
         }
      }
    }
}
