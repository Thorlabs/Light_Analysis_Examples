//Example Date of Creation(YYYY - MM - DD) 2023 - 02 - 15
//Example Date of Last Modification on Github 2023 - 03 - 15
//Version of .NET Framework used for Testing: 4.7.2
//Version of the Thorlabs Dll: 2.0.0.0
//Example Description: This example includes the initialization of the spectrometer.
//The calculation of absorption spectrum and optical density spectrum, the display of the spectrums and data storage.

using System;
using System.Drawing;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using System.Threading;
using System.IO;
using Thorlabs.ccs.interop64;

namespace CCS___Absorption_Measurement
{
    public class Program
    {
        static void Main(string[] args)
        {
            //For the initialization, the resource name needs to be changed to the name of the connected device
            //The resource name has this format: USB0::0x1313::<product ID>::<serial number>::RAW"

            // Product IDs are:
            // 0x8081: CCS100
            // 0x8083: CCS125
            // 0x8085: CCS150
            // 0x8087: CCS175
            // 0x8089: CCS200
            string ProductID = "0x8089";

            //The serial number is printed on the CCS spectrometer, please insert the SN number starts with "M"
            string SerialNumber = "M00488869";

            //Set the integration time, the unit is microsecond
            //The value should be within the range from 0.01 ms to 60000 ms
            double IntegrationTime = 500;

            //Set the location to save the spectrum data
            string FileLocation = "C:\\Users\\zizhang\\Downloads";


            //Initialization
            TLCCS ccsSeries;
            try
            {
                //Create the resource name
                string ResourceName = "USB0::0x1313::" + ProductID + "::" + SerialNumber + "::RAW";
                ccsSeries = new TLCCS(ResourceName, false, false);
                Console.WriteLine("{0} is initialized!", SerialNumber);
            }
            catch
            {
                Console.WriteLine("Initialization failed. Please inspect:\n 1. If the READY LED is green. \n 2. If the serial number and the item number is correct.");
                Console.WriteLine("Press any key to exit");
                Console.ReadKey();
                return;
            }

            //Evaluate if the integration time is within the range.
            //The unit is microsecond (ms).
            if (IntegrationTime < 0.01)
            {
                Console.WriteLine("Integration time {0} ms is too small. Integration time will be set to 0.01 ms.", IntegrationTime);
                IntegrationTime = 0.01;
            }
            else if (IntegrationTime > 60000)
            {
                Console.WriteLine("Integration time {0} ms is too large. Integration time will be set to 60000 ms.", IntegrationTime);
                IntegrationTime = 60000;
            }
            else Console.WriteLine("Integration time is set to {0} ms. ", IntegrationTime);

            //Set the integration time to CCS. The unit used in CCS is second.
            ccsSeries.setIntegrationTime(IntegrationTime*0.001);

            //Get the wavelength data
            double[] DataWavelength = new double[3648];
            short DataSet = 0;
            double MinWavelength = 0;
            double MaxWavelength = 0;
            ccsSeries.getWavelengthData(DataSet, DataWavelength, out MinWavelength, out MaxWavelength);

            //Measure the reference spectrum
            Console.WriteLine("Press <ENTER> to start measurement of reference spectrum.");
            double[] RefIntensity = new double[3648];
            if (Console.ReadKey().Key == ConsoleKey.Enter)
            {
                try
                {
                    Console.WriteLine("Scan started.");
                    ccsSeries.startScan();

                    //Wait for the scan to finish.
                    int status;
                    ccsSeries.getDeviceStatus(out status);
                    while (status != 17)
                    {
                        ccsSeries.getDeviceStatus(out status);
                        Thread.Sleep(100);
                    }
                    //The scan finished. Get the reference spectrum data.
                    ccsSeries.getScanData(RefIntensity);
                    Console.WriteLine("Scan finished.");
                }
                catch
                {
                    Console.WriteLine("Scan failed.");
                    Console.WriteLine("Press any key to exit");
                    Console.ReadKey();
                    ccsSeries.Dispose();
                    return;
                }
            }

            //Measurement with sample
            Console.WriteLine("Press <ENTER> to start measurement of sample spectrum.");
            double[] SampleIntensity = new double[3648];
            if (Console.ReadKey().Key == ConsoleKey.Enter)
            {
                try
                {
                    Console.WriteLine("Scan started.");
                    ccsSeries.startScan();

                    //Wait for the scan to finish.
                    int status;
                    ccsSeries.getDeviceStatus(out status);
                    while (status != 17)
                    {
                        ccsSeries.getDeviceStatus(out status);
                        Thread.Sleep(100);
                    }
                    //The scan finished. Get the sample spectrum data.
                    ccsSeries.getScanData(SampleIntensity);
                    Console.WriteLine("Scan finished.");
                }
                catch
                {
                    Console.WriteLine("Scan failed.");
                    Console.WriteLine("Press ANY KEY to exit");
                    Console.ReadKey();
                    ccsSeries.Dispose();
                    return;
                }
            }

            //Calculate the absorption and optical density of the sample.
            //Formulas:
            //Absorption[%] = ((Reference Spectrum - Sample Spectrum) / Reference Spectrum) * 100
            //Optical density = - log_10 (Transmission) =~ - log_10 (1- Absorption)
            //Conditional Staments are necessary to prevent errors due to impossible mathematical operations.
            double[] Absorption = new double[3648];
            double[] OD = new double[3648];
            for (int i = 0; i<3647;i++)
            {
                Absorption[i] = (RefIntensity[i] - SampleIntensity[i]) / RefIntensity[i] * 100;
                if (double.IsNaN(Absorption[i]) || double.IsInfinity(Absorption[i]))
                    Absorption[i] = 0;
                
                OD[i] = -Math.Log10(1 - (Absorption[i] / 100));
                if (double.IsNaN(OD[i]) || double.IsInfinity(OD[i]))
                    OD[i] = 0;
            }
            //Plot the spectrum
            Program program = new Program();
            program.ShowAbsorptionChart(Absorption, DataWavelength);
            program.ShowODChart(OD, DataWavelength);

            //Dispose the device
            ccsSeries.Dispose();

            //Save the spectrums
            Console.WriteLine("Enter <Y> to save the current Absorption and OD spectrums to {0}. Enter ANY OTHER KEY to exit.",FileLocation);
            if (Console.ReadLine().Equals("Y"))
            {
                program.SaveSpectrum(FileLocation,Absorption,OD,DataWavelength);
                Console.WriteLine("Press ANY KEY to exit.");
                Console.ReadKey();
            }
            else return;
            
        }


        /// <summary>
        /// plot the absorption spectrum
        /// </summary>
        private void ShowAbsorptionChart(double[] DataIntensity, double[] DataWavelength)
        {
            var form1 = new Form();
            
            Chart chart1 = new Chart();
            Label label1 = new Label();
            ChartArea chartArea1 = new ChartArea();
            Series series1 = new Series();
            Title title1 = new Title();

            
            form1.Controls.Add(chart1);
            form1.Text = "Absorption";
            form1.Size = new Size(830, 430);

            chart1.Series.Add(series1);
            chart1.ChartAreas.Add(chartArea1);
            chart1.Titles.Add(title1);
            chart1.Size = new Size(800, 400);
            chart1.Series[0].Points.DataBindXY(DataWavelength, DataIntensity);

            series1.ChartType = SeriesChartType.Line;
            series1.XValueType = ChartValueType.Int32;
            
            chartArea1.Axes[0].Title = "Wavelength[nm]";
            chartArea1.Axes[1].Title = "Absorption[%]";
            chartArea1.Axes[1].Maximum = 110;
            chartArea1.Axes[1].Minimum = -10;

            title1.Text = "Absorption Spectrum";

            Application.Run(form1);
        }

        /// <summary>
        /// plot the optical density spectrum
        /// </summary>
        private void ShowODChart(double[] DataIntensity, double[] DataWavelength)
        {
            var form1 = new Form();

            Chart chart1 = new Chart();
            Label label1 = new Label();
            ChartArea chartArea1 = new ChartArea();
            Series series1 = new Series();
            Title title1 = new Title();

            form1.Controls.Add(chart1);
            form1.Text = "Optical Density";
            form1.Size = new Size(830,430);
            
            chart1.Series.Add(series1);
            chart1.ChartAreas.Add(chartArea1);
            chart1.Titles.Add(title1);
            chart1.Size = new Size(800, 400);
            chart1.Series[0].Points.DataBindXY(DataWavelength, DataIntensity);

            series1.ChartType = SeriesChartType.Line;
            series1.XValueType = ChartValueType.Int32;
            
            chartArea1.Axes[0].Title = "Wavelength[nm]";
            chartArea1.Axes[1].Title = "Optical Density";

            title1.Text = "Otical Density";

            Application.Run(form1);
        }

        /// <summary>
        ///Creating a new .TXT format file, and save the absorption, optical density and wavelength data to the file.
        ///If the file already exists, it will be overwritten.
        /// </summary>
        private void SaveSpectrum(string FileLocation,double[] DataAbsorption, double[] DataOD,double[] DataWavelength)
        {
            string savedata = "Absrption(%)  OD  Wavelength(nm)\n";
            
            for (int i = 0; i < 3647; i++)
            {
                savedata += Convert.ToString(DataAbsorption[i]) + "  ";
                savedata += Convert.ToString(DataOD[i]) + "  ";
                savedata += Convert.ToString(DataWavelength[i]) + "\n";
            }
                        
            FileStream fs = new FileStream(FileLocation + "\\CCS Spectrum " + DateTime.Now.ToString("yyyyMMdd HHmmssfff")+".txt",FileMode.Create);
            StreamWriter sw= new StreamWriter(fs);
            sw.Write(savedata);
            sw.Close();
            fs.Close();
            Console.WriteLine("Absorption and OD are saved to " + FileLocation + " successfully!");

        }
    }
  
}
