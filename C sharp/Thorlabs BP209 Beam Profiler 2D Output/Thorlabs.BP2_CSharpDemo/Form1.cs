// Title: BP209 2D Reconstruction C Sharp Example. 
// Created Date: 2024 - 10 - 12
// Last modified date: 2024 - 10 - 12
// .NET version: 4.8
// Thorlabs SDK Version: Beam version 9.1.5787.560
// Notes: This example is based on the C sharp example which is installed to
// C:\Program Files (x86)\IVI Foundation\VISA\WinNT\TLBP2\Examples during software installation. 
// This example has added the 2D reconstruction algorithm and the reconstructed beam image is displayed. 

namespace Thorlabs.BP2_CSharpDemo
{
   using System;
    using System.Text;
    using System.Windows.Forms;
    using System.Drawing;
    using Thorlabs.TLBP2.Interop;
    using System.Runtime.InteropServices;

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
      /// array of data structures for each slit.
      /// </summary>
      private bp2_slit_data[] bp2SlitData = new bp2_slit_data[4];

      /// <summary>
      /// array of calculation structures for each slit.
      /// </summary>
      private bp2_calculations[] bp2Calculations = new bp2_calculations[4];

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

         // alternative implementation
         ////this.connectToTheFirstDeviceByRM();  

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
            this.status = this.bp2Device.set_drum_speed(10.0);
            this.status = this.bp2Device.set_drum_speed_ex(10.0, out sampleCount, out sampleResolution);

            // activate the position correction to have the same calculation results as the Thorlabs Beam Application
            this.status = this.bp2Device.set_position_correction(true);

            // activate the automatic gain calcuation
            this.status = this.bp2Device.set_auto_gain(true);

            // activate the drum speed correction
            this.status = this.bp2Device.set_speed_correction(true);

            // use the offset for 10Hz to be compatible with the release version 5.0
            this.status = this.bp2Device.set_reference_position(0, 4, 100.0);
            this.status = this.bp2Device.set_reference_position(1, 4, -100.0);
            this.status = this.bp2Device.set_reference_position(2, 4, 100.0);
            this.status = this.bp2Device.set_reference_position(3, 4, -100.0);

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
      /// search for connected devices and connect to the first one.
      /// Use the VISA resource manager and simple data types.
      /// </summary>
      private void ConnectToTheFirstDeviceByRM()
      {
         // get the resource string of the first device
         string[] bp2Resources = BP2_ResourceManager.FindRscBP2();

         if (bp2Resources.Length > 0)
         {
            // connect to the first device
            this.bp2Device = new TLBP2(bp2Resources[0], false, false);
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
            if (0 == this.bp2Device.get_drum_speed(out drumSpeed))
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

         // the gain and drum speed will be corrected during the measurement
         double power;
         float powerWindowSaturation;
         if ((deviceStatus & 1) == 1 &&
             0 == this.bp2Device.get_slit_scan_data(this.bp2SlitData, this.bp2Calculations, out power, out powerWindowSaturation, null))
         {
            this.textBox_peakPositionSlit1.Text      = this.bp2Calculations[0].PeakPosition.ToString("f2");
            this.textBox_peakIntensitySlit1.Text = (this.bp2Calculations[0].PeakIntensity * 100.0f / ((float)0x7AFF - this.bp2SlitData[0].SlitDarkLevel)).ToString("f2");
            this.textBox_centroidPositionSlit1.Text  = this.bp2Calculations[0].CentroidPos.ToString("f2");

            this.textBox_peakPositionSlit2.Text = this.bp2Calculations[1].PeakPosition.ToString("f2");
            this.textBox_peakIntensitySlit2.Text = (this.bp2Calculations[1].PeakIntensity * 100.0f / ((float)0x7AFF - this.bp2SlitData[1].SlitDarkLevel)).ToString("f2");
            this.textBox_centroidPositionSlit2.Text = this.bp2Calculations[1].CentroidPos.ToString("f2");

            this.textBox_powerSaturation.Text   = (powerWindowSaturation*100.0).ToString("f2");

            this.chart25um.Series[0].Points.DataBindXY(bp2SlitData[0].SlitSamplesPositions, bp2SlitData[0].SlitSamplesIntensities);
            this.chart25um.Series[1].Points.DataBindXY(bp2SlitData[1].SlitSamplesPositions, bp2SlitData[1].SlitSamplesIntensities);
            this.chart5um.Series[0].Points.DataBindXY(bp2SlitData[2].SlitSamplesPositions, bp2SlitData[2].SlitSamplesIntensities);
            this.chart5um.Series[1].Points.DataBindXY(bp2SlitData[3].SlitSamplesPositions, bp2SlitData[3].SlitSamplesIntensities);

            //Calculate and display the 2D reconstruction image
            Get2DReconstruction();
         }
      }

        /// <summary>
        /// Calculate the 2D reconstructed beam intensity distribution and display the image on the WinForm
        /// </summary>
        private void Get2DReconstruction()
      {
            double[] sampleIntensitiesX = new double[7500];
            double[] sampleIntensitiesY = new double[7500];
            double[] samplePositionX = new double[7500];
            double[] samplePositionY = new double[7500];
            double[] gaussianFitIntensitiesX = new double[7500];
            double[] gaussianFitIntensitiesY = new double[7500];
            double power;
            float powerSaturation;
            float temp;

            //Request the scan data
            this.bp2Device.request_scan_data(out power,out powerSaturation,null);
            //Get the intensities from the 25um X slit and the 25um Y slit
            this.bp2Device.get_sample_intensities(0, sampleIntensitiesX, samplePositionX);
            this.bp2Device.get_sample_intensities(1, sampleIntensitiesY, samplePositionY);

            //Get the gaussian fit intensites from the 25um X slit and the 25um Y slit
            this.bp2Device.get_slit_gaussian_fit(0, out temp,out temp,out temp,gaussianFitIntensitiesX);
            this.bp2Device.get_slit_gaussian_fit(1, out temp, out temp, out temp, gaussianFitIntensitiesY);

            //2D reconstruction 
            double[,] imageData = new double[750, 750];
            double imageDataMax = 0;
            int ixz, iyz;
            for (int ix = 0; ix < 750; ix++)
            {
                for (int iy = 0; iy < 750; iy++)
                {
                    //2D reconstruction algorithm
                    ixz = (750 - ix - 1) * 10;
                    iyz = (750 - iy - 1) * 10;
                    imageData[ix, iy] = sampleIntensitiesX[ixz] * gaussianFitIntensitiesX[ixz] * sampleIntensitiesY[iyz] * gaussianFitIntensitiesY[iyz];

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
            int imageGrayValue;
            Bitmap bitmap = new Bitmap(750, 750);
            for (int x = 0; x < 750; x++)
            {
                for (int y = 0; y < 750; y++)
                {
                    imageGrayValue = (int)(imageData[x, y] * 255 / imageDataMax);
                    Color color = Color.FromArgb(imageGrayValue, imageGrayValue, imageGrayValue);
                    bitmap.SetPixel(x, y, color);
                }
            }

            // set the bitmap to the Image property
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
