using System;
using System.Threading;
using System.Threading.Tasks;
using System.Drawing;
using System.Windows.Forms;
using System.Collections;
using Thorlabs.ccs.interop64;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;
//using System.Runtime.InteropServices;

namespace CCS_Continuous_Scan
{
    public partial class Form1 : Form
    {

        private TLCCS ccsSeries;

        public Form1()
        {
            InitializeComponent();
                        
            //insert the default serial number here
            textBox_SerialNumber.Text = "00488869";

            //select the default item number index here
            //0 -> CCS100
            //1 -> CCS125
            //2 -> CCS150
            //3 -> CCS175
            //4 -> CCS200
            ComboBox_ItemNumber.SelectedIndex = 4;

        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            // release the device
            if (ccsSeries != null)
                ccsSeries.Dispose();
        }


        private void button_Initialize_Click(object sender, EventArgs e)
        {

            // set the busy cursor
            this.Cursor = Cursors.WaitCursor;

            // initialize device with the resource name
            string ItemNumber_internal = "";
            switch (ComboBox_ItemNumber.SelectedIndex)
            {
                case 0: //CCS100
                    ItemNumber_internal = "0x8081";
                    break;
                case 1: //CCS125
                    ItemNumber_internal = "0x8083";
                    break;
                case 2: //CCS150
                    ItemNumber_internal = "0x8085";
                    break;
                case 3: //CCS175
                    ItemNumber_internal = "0x8087";
                    break;
                case 4: //CCS200
                    ItemNumber_internal = "0x8089";
                    break;
            }

            string resourceName = "USB0::0x1313::" + ItemNumber_internal + "::M" + textBox_SerialNumber.Text.ToString() + "::RAW";

            try
            {
                ccsSeries = new TLCCS(resourceName, true, true);
                button_Initialize.Text = "Initialization Succeed!";

                //disable the initialize button and enable the scanning button
                button_Initialize.BackColor = Color.PaleGreen;
                button_Initialize.Enabled = false;
                button_StartScanCont.Enabled = true;

                //set the cursor to default
                this.Cursor = Cursors.Arrow;
            }
            catch
            {
                MessageBox.Show("Initialization failed. Please inspect:\n 1. If the READY LED is green. \n 2. If the serial number and the item number is correct.");
                //set the cursor to default
                this.Cursor = Cursors.Arrow;
            }
        }

        //if the scan button is clicked, set the "StartScan" value to true
        //if the stop scan button is clicked, set the "StartScan" value to false
        public bool StartScan;

        private void button_StartScanCont_Click(object sender, EventArgs e)
        {
            StartScan = true;

            //set integration time, convert the unit from "ms" to "s"
            double integration_time = (double)numericUpDown_IntegrationTime.Value/1000; 
            ccsSeries.setIntegrationTime(integration_time);

            //disable the scan button, disable the modification of integration time, and enable the stop button
            button_StartScanCont.Enabled = false;
            numericUpDown_IntegrationTime.Enabled = false;
            button_StopScan.Enabled = true;

            //create a task and start continuous scan
            Task ScanContTask = new Task(() => ScanCont());
            ScanContTask.Start();
        }

        private void ScanCont()
        {
            //get the wavelength data
            double[] Data_Lambda = new double[3648];
            short Data_Set = 0;
            double Minimum_Wavelength = 0;
            double Maximum_Wavelength = 0;
            ccsSeries.getWavelengthData(Data_Set, Data_Lambda, out Minimum_Wavelength, out Maximum_Wavelength);

            while (StartScan == true)
            {
                double[] Data_Intensity = new double[3648];
                ccsSeries.startScan();

                //scaning is started. Read the device status and wait one scanning finishes.
                Task GetDeviceStatusTask = Task.Run(() => GetDeviceStatus());
                GetDeviceStatusTask.Wait();
                GetDeviceStatusTask.Dispose();
                                
                if (StartScan == false)
                    break;
                                
                try
                {
                    //get the real integeration time
                    //this value is calculated from timer counter so may slightly differ from the set value.
                    double Get_Time = 0;
                    ccsSeries.getIntegrationTime(out Get_Time);

                    //convert from "s" to "ms"
                    Get_Time *= 1000; 
                    Thread.Sleep(100);

                    //draw the spectrum, record the integration time and device status
                    ccsSeries.getScanData(Data_Intensity);
                    this.Invoke(new Action(() => {
                        chart1.Series[0].Points.DataBindXY(Data_Lambda, Data_Intensity);
                        Show_Integration_Time.Text = Convert.ToString(Get_Time);
                        DeviceStatus.Text = "Finished";
                    }));
                }
                catch
                {
                    MessageBox.Show("Scanning failed");

                    //finish the scanning and modify the button status
                    this.Invoke(new Action(() =>{
                       button_StartScanCont.Enabled = true;
                       numericUpDown_IntegrationTime.Enabled = true;
                       button_StopScan.Enabled = false;
                     }));
                    
                    break;
                }
            }
        }

        private void GetDeviceStatus()
        {
            int status=0;
            int res;
            if (StartScan == true)
                res = ccsSeries.getDeviceStatus(out status);
            Thread.Sleep(100);

            //status = 17 means the scanning completes
            while (status != 17 && StartScan == true)
            {
                res = ccsSeries.getDeviceStatus(out status);

                this.Invoke(new Action(() =>
                {
                     DeviceStatus.Text = "Acquiring...";
                }));
                Thread.Sleep(100);
            }

        }
        
        private void button_StopScan_Click(object sender, EventArgs e)
        {
            StartScan = false;

            // set the busy cursor
            this.Cursor = Cursors.WaitCursor;
            
            //wait for the task to complete and then reset the CCS spectrometer
            Task.WaitAll();
            Thread.Sleep(500);
            ccsSeries.reset();

            //modify the button status
            button_StartScanCont.Enabled = true;
            numericUpDown_IntegrationTime.Enabled = true;
            button_StopScan.Enabled = false;
            DeviceStatus.Text = "stopped";
            Show_Integration_Time.Text = "";

            //ser the cursor to default
            this.Cursor = Cursors.Arrow;

        }


        private void Form1_Load(object sender, EventArgs e)
        {

        }


    }

}
