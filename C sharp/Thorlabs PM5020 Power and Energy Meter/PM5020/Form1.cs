using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Runtime.InteropServices;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using Thorlabs.TLPMX_64.Interop;


namespace PM5020
{
    public partial class Form1 : Form
    {
        private TLPMX tlpmx;
        BackgroundWorker backgroundWorker1 = new BackgroundWorker();
        BackgroundWorker backgroundWorker2 = new BackgroundWorker();
        ManualResetEvent manualReset = new ManualResetEvent(true);

        //save the Power or energy range values
        double[] powerRangelistDouble = new double[9];
        double[] energyRangelistDouble = new double[6];

        public Form1()
        {
            InitializeComponent();
            //The background worker to display the realtime energy or power for both channels.
            backgroundWorker1.DoWork += backgroundWorker1_Dowork_ValuesRefresh;
            backgroundWorker1.ProgressChanged += BackgroundWorker1_ProgressChanged;
            backgroundWorker1.WorkerReportsProgress = true;
            backgroundWorker1.WorkerSupportsCancellation = true;
            //The background worker to show the calculation result from the data processing functions.
            backgroundWorker2.DoWork += backgroundWorker2_DoWork_CalcResultRefresh;
            backgroundWorker2.ProgressChanged += BackgroundWorker2_ProgressChanged;
            backgroundWorker2.WorkerReportsProgress = true;
            backgroundWorker2.WorkerSupportsCancellation = true;

        }

        private void BackgroundWorker1_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            throw new NotImplementedException();
        }
        private void BackgroundWorker2_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            throw new NotImplementedException();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            // release the device
            if (tlpmx != null)
                tlpmx.Dispose();
        }

        /// <summary>
        /// Find all the available deivces, then connect and initialize the first device. 
        /// If the device is initialized successfully, the sensor type for both channels will be recognized and the settings will be displayed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void buttonConnect_Click(object sender, EventArgs e)
        {
            try
            {
                //set the cursor to busy when connecting and initializing the device
                this.Cursor = Cursors.WaitCursor;
                
                //find availiable devices
                HandleRef Instrument_Handle = new HandleRef();
                TLPMX searchDevice = new TLPMX(Instrument_Handle.Handle);
                int err = searchDevice.findRsrc(out uint resourceCount);

                if (resourceCount >= 1)
                {
                    StringBuilder descr = new StringBuilder(1024);
                    StringBuilder consoleName= new StringBuilder(1024);
                    StringBuilder consoleSerialNumber = new StringBuilder(1024);

                    //Connect the first power meter and get the device information
                    err = searchDevice.getRsrcInfo(0, consoleName, consoleSerialNumber, null, out bool deviceAvailable);
                    err = searchDevice.getRsrcName(0, descr);
                    string firstPowermeterFound = descr.ToString();
                    tlpmx = new TLPMX(firstPowermeterFound, true, false);
                    textBoxStatus.Text = consoleSerialNumber.ToString() + " is connected.";
                    
                    //Get the info about the connected sensors and the parameters
                    SensorChannelScan(Convert.ToString(consoleName));
                    GetCurrentParameters();
                    
                    //change the color of the Connect button and enable Measurement buttons
                    buttonConnect.Enabled = false;
                    buttonConnect.BackColor = Color.PaleGreen;
                    buttonStartMeas.Enabled = true;
                    buttonMeasCancel.Enabled = true;

                }
                else if (resourceCount == 0)
                {
                    searchDevice.Dispose();
                    textBoxStatus.Text = "No power meter could be found.";
                    this.Cursor = Cursors.Arrow;
                    return;
                }
                
                this.Cursor = Cursors.Arrow;
            }
            catch (Exception ex)
            {
                textBoxStatus.Text = ex.Message;
                this.Cursor = Cursors.Arrow;
            }

        }

        /// <summary>
        /// Recognize the sensor types of both channels. Besides PM5020, other single channel consoles are also compatible.
        /// </summary>
        /// <param name="consoleName"></param> 
        private void SensorChannelScan(string consoleName)
        {
            StringBuilder sensorData1 = new StringBuilder(1024);
            StringBuilder sensorData2 = new StringBuilder(1024);
            short sensorType1, sensorType2, sensorSubType1, sensorSubType2;

            //detect if the sensors are connected and get the sensor types
            try
            {
                int err = tlpmx.getSensorInfo(sensorData1, sensorData1, sensorData1, out sensorType1, out sensorSubType1, out short flag1, 1);
                err = tlpmx.getSensorInfo(sensorData2, sensorData2, sensorData2, out sensorType2, out sensorSubType2, out short flag2, 2);
            }
            catch(Exception ex)
            {
                textBoxStatus.Text = ex.Message;
                return;
            }

            //sensorType = 0x00: no sensor
            //sensorType = 0x01: photodiode power sensor
            //sensorType = 0x02: thermal power sensor
            //sensorType = 0x03: pyroelectric energy sensor
            //no sensor is available
            if (sensorType1 == 0x00 && sensorType2 == 0x00)
            {
                textBoxStatus.Text += " There is no sensor!";
                groupBoxChannel1.Enabled = false;
                groupBoxChannel1.BackColor = Color.LightGray;
                groupBoxChannel2.Enabled = false;
                groupBoxChannel2.BackColor = Color.LightGray;
            }
            //two sensors are connected
            else if (consoleName == "PM5020" && sensorType1 != 0x00 && sensorType2 != 0x00)
            {
                //identify whether the sensor is a power sensor or an energy sensor
                if (sensorType1 == 0x03)
                {
                    comboBoxPowerRange1.Enabled = false;
                    checkBoxAutoRange1.Enabled = false;
                    buttonZero1.Enabled = false;
                }
                else comboBoxEnergyRange1.Enabled = false;

                if (sensorType2 == 0x03)
                {
                    comboBoxPowerRange2.Enabled = false;
                    checkBoxAutoRange2.Enabled = false;
                    buttonZero2.Enabled = false;
                }
                else comboBoxEnergyRange2.Enabled = false;
                
                //if the senors in two channels are both power sensors or energy sensors, enable data processing
                if ((sensorType1 == 0x03 && sensorType2 == 0x03) || (sensorType1 != 0x03 && sensorType2 != 0x03))
                {
                    groupBoxDataProcessing.Enabled = true;
                    textBoxCalcResult.Enabled = true;
                }
            }
            //one sensor is connected
            else if (sensorType1 != 0x00)
            {
                textBoxStatus.Text += " Channel 1 is available";
                groupBoxChannel2.Enabled = false;
                groupBoxChannel2.BackColor = Color.LightGray;

                if (sensorType1 == 0x03)
                {
                    comboBoxPowerRange1.Enabled = false;
                    checkBoxAutoRange1.Enabled = false;
                    buttonZero1.Enabled = false;
                }
                else comboBoxEnergyRange1.Enabled = false;
            }
            else if (sensorType1 == 0x00 && sensorType2 != 0x00)
            {
                textBoxStatus.Text += " Channel 2 is available";
                groupBoxChannel1.Enabled = false;
                groupBoxChannel1.BackColor = Color.LightGray;

                if (sensorType2 == 0x03)
                {
                    comboBoxPowerRange2.Enabled = false;
                    checkBoxAutoRange2.Enabled = false;
                    buttonZero2.Enabled = false;
                }
                else comboBoxEnergyRange2.Enabled = false;
            }
            
        }

        /// <summary>
        /// Get the current parameters, including wavelength, power range, energy range, auto range, and averaging.
        /// </summary>
        private void GetCurrentParameters()
        {
            try
            {
                //get the parameters of Channel 1
                if (groupBoxChannel1.Enabled == true)
                {
                    int err = tlpmx.getWavelength(0, out double wavelength1, 1);
                    textBoxWavelength1.Text = wavelength1.ToString();
                    
                    err = tlpmx.getAvgCnt(out short averageCount1, 1);
                    textBoxAveraging1.Text = averageCount1.ToString();

                    if (comboBoxPowerRange1.Enabled == true)
                    {
                        err = tlpmx.getPowerAutorange(out bool powerAuto, 1);
                        checkBoxAutoRange1.Checked = powerAuto;
                        if (powerAuto == true) 
                            comboBoxPowerRange1.Enabled = false;

                        PowerRangeListCreate(comboBoxPowerRange1, 1);
                    }

                    if (comboBoxEnergyRange1.Enabled == true)
                    {
                        EnergyRangeListCreate(comboBoxEnergyRange1, 1);
                    }   
                }
                //get the settings of Channel 2
                if (groupBoxChannel2.Enabled == true) 
                {
                    int err = tlpmx.getWavelength(0, out double wavelength2, 2);
                    textBoxWavelength2.Text = wavelength2.ToString();

                    err = tlpmx.getAvgCnt(out short averageCount2, 2);
                    textBoxAveraging2.Text = averageCount2.ToString();

                    if (comboBoxPowerRange2.Enabled == true)
                    {
                        err = tlpmx.getPowerAutorange(out bool powerAuto, 2);
                        checkBoxAutoRange2.Checked = powerAuto;
                        if (powerAuto == true) 
                            comboBoxPowerRange2.Enabled = false;

                        PowerRangeListCreate(comboBoxPowerRange2, 2);
                    }

                    if (comboBoxEnergyRange2.Enabled == true)
                    {
                        EnergyRangeListCreate(comboBoxEnergyRange2, 2);
                    }
                }
            }
            catch (Exception ex)
            {
                textBoxStatus.Text = ex.Message;
            }
        }

        private void buttonStartMeas_Click(object sender, EventArgs e)
        {
            if (backgroundWorker1.IsBusy != true)
            {
                // run the "backgroundWorker1_Dowork_ValuesRefresh" method
                backgroundWorker1.RunWorkerAsync();

                // run the "backgroundWorker2_DoWork_CalcResultRefresh" method
                backgroundWorker2.RunWorkerAsync();

                buttonStartMeas.Enabled = false;
                buttonStartMeas.BackColor = Color.PaleGreen;
            }

        }

        /// <summary>
        /// The background worker to show the realtime energy or power for both channels.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void backgroundWorker1_Dowork_ValuesRefresh(object sender, DoWorkEventArgs e)
        {
            double powerValue1, powerValue2, energyValue1, energyValue2;
            //the background worker will be paused if the device is visited from other events
            manualReset.WaitOne();

            try
            {
                while (backgroundWorker1.CancellationPending == false)
                {
                    if (groupBoxChannel1.Enabled == true)
                    {
                        // the power value for Channel1 will be gotten if Channel1 is available and the sensor is a power sensor
                        if (checkBoxAutoRange1.Enabled == true)
                        {
                            tlpmx.measPower(out powerValue1, 1);
                            //Only if the measured power is larger than baseline, it will be displayed.
                            tlpmx.getPowerRange(0,out double powerRangeCurr1, 1);
                            if (powerValue1 > powerRangeCurr1*Convert.ToDouble(textBoxBaseline1.Tag))
                            {
                                if (textBoxValue1.InvokeRequired)
                                {
                                    Action<double> actionDelegate = (x) => { textBoxValue1.Text = x.ToString() + " W"; };
                                    //The "Zeroing" button in the GUI enables substrating the background power. 
                                    //The background power is saved to the tag object after clicking the "Zeroing" button.
                                    textBoxValue1.Invoke(actionDelegate, powerValue1 - Convert.ToDouble(buttonZero1.Tag));
                                }
                                else textBoxValue1.Text = powerValue1.ToString() + " W";
                            }  
                        }
                        // the energy value for Channel1 will be gotten if Channel1 is available and the sensor is an energy sensor
                        else if (comboBoxEnergyRange1.Enabled == true)
                        {
                            tlpmx.measEnergy(out energyValue1, 1);
                            //Only if the measured energy is larger than baseline, it will be displayed.
                            tlpmx.getEnergyRange(0, out double energyRangeCurr1, 1);
                            if (energyValue1 > energyRangeCurr1* Convert.ToDouble(textBoxBaseline1.Tag))
                            {
                                if (textBoxValue1.InvokeRequired)
                                {
                                    Action<double> actionDelegate = (x) => { textBoxValue1.Text = x.ToString() + " J"; };
                                    textBoxValue1.Invoke(actionDelegate, energyValue1);
                                }
                                else textBoxValue1.Text = energyValue1.ToString() + " J";
                            }
                        }

                    }

                    if (groupBoxChannel2.Enabled == true)
                    {
                        // the power value for Channel2 will be gotten if Channel2 is available and the sensor is a power sensor
                        if (checkBoxAutoRange2.Enabled == true)
                        {
                            tlpmx.measPower(out powerValue2, 2);
                            //Only if the measured power is larger than baseline, it will be displayed.
                            tlpmx.getPowerRange(0, out double powerRangeCurr2, 2);
                            if (powerValue2 > powerRangeCurr2 * Convert.ToDouble(textBoxBaseline2.Tag))
                            {
                                if (textBoxValue2.InvokeRequired)
                                {
                                    Action<double> actionDelegate = (x) => { textBoxValue2.Text = x.ToString() + " W"; };
                                    //The "Zeroing" button in the GUI enables substrating the background power. 
                                    //The background power is saved to the tag object after clicking the "Zeroing" button.
                                    textBoxValue2.Invoke(actionDelegate, powerValue2 - Convert.ToDouble(buttonZero2.Tag));
                                }
                                else textBoxValue2.Text = powerValue2.ToString() + " W";
                            }
                        }
                        // the energy value for Channel2 will be gotten if Channel2 is available and the sensor is an energy sensor
                        else if (comboBoxEnergyRange2.Enabled == true)
                        {                          
                            int err = tlpmx.measEnergy(out energyValue2, 2);
                            //Only if the measured energy is larger than baseline, it will be displayed.
                            tlpmx.getEnergyRange(0, out double energyRangeCurr2, 2);
                            if (energyValue2 > energyRangeCurr2 * Convert.ToDouble(textBoxBaseline2.Tag))
                            {
                                if (textBoxValue2.InvokeRequired)
                                {
                                    Action<double> actionDelegate = (x) => { textBoxValue2.Text = x.ToString() + " J"; };
                                    textBoxValue2.Invoke(actionDelegate, energyValue2);
                                }
                                else textBoxValue2.Text = energyValue2.ToString() + " J";
                            }
                        }
                   }

                
                }
            }
            catch (Exception ex)
            {
                if (textBoxStatus.InvokeRequired)
                {
                    Action<Exception> actionDelegate = (x) => { textBoxStatus.Text = x.Message; };
                    textBoxStatus.Invoke(actionDelegate, ex);
                }
                else textBoxStatus.Text = ex.Message;
            }
        }

        /// <summary>
        /// The background worker to show the calculation result from the data processing functions.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void backgroundWorker2_DoWork_CalcResultRefresh(object sender, DoWorkEventArgs e)
        {
            while (backgroundWorker1.CancellationPending == false)
            {
                if (checkBoxNorm1.Checked || checkBoxNorm2.Checked || checkBoxSum.Checked || checkBoxSubstrate.Checked)
                {
                    double doubleValue1,doubleValue2;
                    string stringValue1 = "", stringValue2 = "";
                    char valueUnit;

                    //read the current displayed power or energy values from two channels' textboxes
                    if (textBoxValue1.InvokeRequired)
                    {
                        Func<string> funcDelegate = () => { return textBoxValue1.Text; };
                        stringValue1 = (string)textBoxValue1.Invoke(funcDelegate);
                    }
                    else stringValue1 = textBoxValue1.Text;
                    if (textBoxValue2.InvokeRequired)
                    {
                        Func<string> funcDelegate = () => { return textBoxValue2.Text; };
                        stringValue2 = (string)textBoxValue2.Invoke(funcDelegate);
                    }
                    else stringValue2 = textBoxValue2.Text;

                    //remove the unit, and convert the values from String to Double
                    try
                    {
                        doubleValue1 = Convert.ToDouble(stringValue1.Substring(0, stringValue1.Length - 1));
                        doubleValue2 = Convert.ToDouble(stringValue2.Substring(0, stringValue2.Length - 1));
                        valueUnit = stringValue1.Last();
                    }
                    catch (Exception ex)
                    {
                        if (textBoxStatus.InvokeRequired)
                        {
                            Action<Exception> actionDelegate = (x) => { textBoxStatus.Text = x.Message; };
                            textBoxStatus.Invoke(actionDelegate, ex);
                        }
                        else textBoxStatus.Text = ex.Message;
                        continue;
                    }

                    //data processing for four different functions
                    //normalize channel 1, and the ratio of channel2 value to channel1 value is calculated
                    if (checkBoxNorm1.Checked == true)
                    {
                        if (textBoxCalcResult.InvokeRequired)
                        {
                            Action<double> actionDelegate = (x) => { textBoxCalcResult.Text = x.ToString(); };
                            textBoxCalcResult.Invoke(actionDelegate, doubleValue2 / doubleValue1);
                        }
                        else textBoxCalcResult.Text = (doubleValue2 / doubleValue1).ToString() + " a.u.";
                    }
                    //normalize channel 2, and the ratio of channel1 value to channel2 value is calculated
                    else if (checkBoxNorm2.Checked == true)
                    {
                        if (textBoxCalcResult.InvokeRequired)
                        {
                            Action<double> actionDelegate = (x) => { textBoxCalcResult.Text = x.ToString(); };
                            textBoxCalcResult.Invoke(actionDelegate, doubleValue1 / doubleValue2);
                        }
                        else textBoxCalcResult.Text = (doubleValue1 / doubleValue2).ToString() + " a.u.";
                    }
                    //the sum of the values from two channels is calculated.
                    else if (checkBoxSum.Checked == true)
                    {
                        if (textBoxCalcResult.InvokeRequired)
                        {
                            Action<double,double,char> actionDelegate = (x,y,z) => { textBoxCalcResult.Text = (x + y).ToString() + z; };
                            textBoxCalcResult.Invoke(actionDelegate, doubleValue1, doubleValue2, valueUnit);
                        }
                        else textBoxCalcResult.Text = (doubleValue1 + doubleValue2).ToString() + valueUnit;
                    }
                    //the difference of the values from two channels is calculated.
                    else if (checkBoxSubstrate.Checked == true)
                    {
                        if (textBoxCalcResult.InvokeRequired)
                        {
                            Action<double, double, char> actionDelegate = (x, y, z) => { textBoxCalcResult.Text = (x - y).ToString() + z; };
                            textBoxCalcResult.Invoke(actionDelegate, doubleValue1, doubleValue2, valueUnit);
                        }
                        else textBoxCalcResult.Text = (doubleValue1 - doubleValue2).ToString() + valueUnit;
                    }
                }                
            }
        }

        private void buttonMeasCancel_Click(object sender, EventArgs e)
        {
            backgroundWorker1.CancelAsync();
            backgroundWorker2.CancelAsync();

            //release the "Start Measurement" button
            buttonStartMeas.Enabled = true;
            buttonStartMeas.BackColor = SystemColors.Control;
        }

        private void textBoxWavelenght1_KeyPressed(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar =='\r')
            {
                //pause the backgroundworker
                manualReset.Reset();

                if (!double.TryParse(textBoxWavelength1.Text, out double result) && textBoxWavelength1.Text != "")
                {
                    MessageBox.Show("Please input a valid number!");
                    textBoxWavelength1.Text = "";
                }
                else if (textBoxWavelength1.Text != "")
                {
                    tlpmx.setWavelength(Convert.ToDouble(textBoxWavelength1.Text), 1);
                    tlpmx.getWavelength(0, out double wavelength1, 1);
                    if (wavelength1 == Convert.ToDouble(textBoxWavelength1.Text))
                    {
                        //wavelength influences the available power range. So the power range combo box need to be refreshed.
                        if (checkBoxAutoRange1.Enabled == true)
                        {
                            PowerRangeListCreate(comboBoxPowerRange1, 1);
                        }
                        else if (comboBoxEnergyRange1.Enabled == true)
                        {
                            EnergyRangeListCreate(comboBoxEnergyRange1, 1);
                        }

                        textBoxStatus.Text = "Wavelength of Channel1 is set to " + textBoxWavelength1.Text + " nm";
                    }

                }

                //continue the backgroundworker
                manualReset.Set();

            }           
        }

        private void comboBoxPowerRange1_Changed(object sender, EventArgs e)
        {
            //if the "Connect" button's color is the "Control" System Color
            //this means that the combobox index changing is caused by GetCurrentParameters() method
            //so this method will be skiped
            if (buttonConnect.BackColor == SystemColors.Control)
                return;

            //pause the backgroundworker
            manualReset.Reset();

            int comboBoxIndex = comboBoxPowerRange1.SelectedIndex;
            //the setting of the power range follows the round up principle
            //multiply the power range by a factor can avoid the calculation error of double type variables
            tlpmx.setPowerRange(powerRangelistDouble[comboBoxIndex] * 0.95, 1);
            Thread.Sleep(100);
            tlpmx.getPowerRange(0, out double powerRangeCurr, 1);
            textBoxStatus.Text = "Power range of Channel1 is set to " + powerRangeCurr + " W";

            //continue the backgroundworker
            manualReset.Set();

        }

        private void comboBoxEnergyRange1_Changed(object sender, EventArgs e)
        {
            //if the "Connect" button's color is the "Control" System Color
            //this means that the combobox index changing is caused by GetCurrentParameters() method
            //so this method will be skiped
            if (buttonConnect.BackColor == SystemColors.Control)
                return;

            //pause the backgroundworker
            manualReset.Reset();

            int comboBoxIndex = comboBoxEnergyRange1.SelectedIndex;
            //the setting of the energy range follows the round up principle
            //multiply the energy range by a factor can avoid the calculation error of double type variables
            tlpmx.setEnergyRange(energyRangelistDouble[comboBoxIndex] * 0.95, 1);
            Thread.Sleep(100);
            tlpmx.getEnergyRange(0, out double energyRangeCurr, 1);
            textBoxStatus.Text = "Energy range of Channel1 is set to " + energyRangeCurr + " J";

            //continue the backgroundworker
            manualReset.Set();
        }

        private void checkBoxAutoRange1_Changed(object sender, EventArgs e)
        {
            //if the connect button's color is "Control" system color
            //this means that the check box status change is caused by form initialization
            //so the function will be skiped
            if (buttonConnect.BackColor == SystemColors.Control)
                return;

            //pause the backgroundworker
            manualReset.Reset();

            tlpmx.setPowerAutoRange(checkBoxAutoRange1.Checked, 1);
            tlpmx.getPowerAutorange(out bool powerAuto, 1);

            if (powerAuto == true)
            {
                textBoxStatus.Text = "Auto power range is activated for Channel1.";
                comboBoxPowerRange1.Enabled = false;
            }
            else if (powerAuto == false)
            {
                textBoxStatus.Text = "Auto power range is cancelled for Channel1.";
                comboBoxPowerRange1.Enabled = true;

                //refresh the power range combobox
                PowerRangeListCreate(comboBoxPowerRange1,1);
            }
            //continue the backgroundworker
            manualReset.Set();

        }

        private void textBoxAveraging1_KeyPressed(object sender, KeyPressEventArgs e)
        {
            //pause the backgroundworker
            manualReset.Reset();

            if (e.KeyChar == '\r')
            {
                if (!uint.TryParse(textBoxAveraging1.Text, out uint result) && textBoxAveraging1.Text != "")
                {
                    MessageBox.Show("Please input a valid number!");
                    textBoxAveraging1.Text = "";
                }
                else
                {
                    tlpmx.setAvgCnt(Convert.ToInt16(textBoxAveraging1.Text), 1);
                    tlpmx.getAvgCnt(out Int16 AverageCount, 1);
                    if (AverageCount == Convert.ToInt16(textBoxAveraging1.Text))
                        textBoxStatus.Text = "Average Count of Channel 1 is set to" + AverageCount;
                }
            }
            //continue the backgroundworker
            manualReset.Set();
        }

        private void buttonZero1_Click(object sender, EventArgs e)
        {
            //pause the backgroundworker
            manualReset.Reset();

            tlpmx.measPower(out double power,1);
            buttonZero1.Tag = power;
            textBoxStatus.Text = "Zeroing Channel1 succeeds.";
            //continue the backgroundworker
            manualReset.Set();
        }

        private void textBoxBaseline1_KeyPressed(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == '\r')
            {
                //pause the backgroundworker
                manualReset.Reset();

                if (!double.TryParse(textBoxBaseline1.Text, out double result) && textBoxBaseline1.Text != "")
                {
                    MessageBox.Show("Please input a valid number!");
                    textBoxBaseline1.Text = "";
                    return;
                }

                double baseline1 = Convert.ToDouble(textBoxBaseline1.Text);

                if (baseline1 < 100 && baseline1 >= 0)
                {
                    textBoxBaseline1.Tag = baseline1 / 100;
                    textBoxStatus.Text = "Baseline of Channel1 is set to " + textBoxBaseline1.Text + " % of current power/energy range.";
                }
                manualReset.Set();
            }  
        }

        private void textBoxWavelenght2_KeyPressed(object sender, KeyPressEventArgs e)
        {

            if (e.KeyChar == '\r')
            {
                manualReset.Reset();

                if (!double.TryParse(textBoxWavelength2.Text, out double result) && textBoxWavelength2.Text != "")
                {
                    MessageBox.Show("Please input a valid number!");
                    textBoxWavelength2.Text = "";
                }
                else if (textBoxWavelength2.Text != "")
                {
                    tlpmx.setWavelength(Convert.ToDouble(textBoxWavelength2.Text), 2);
                    tlpmx.getWavelength(0, out double wavelength2, 2);
                    if (wavelength2 == Convert.ToDouble(textBoxWavelength2.Text))
                    {

                        //wavelength influences the power range. So the power range combo box need to be refreshed.
                        if (checkBoxAutoRange2.Enabled == true)
                        {
                            PowerRangeListCreate(comboBoxPowerRange2, 2);
                        }
                        else if (comboBoxEnergyRange2.Enabled == true)
                        {
                            EnergyRangeListCreate(comboBoxEnergyRange2, 2);
                        }
                        textBoxStatus.Text = "Wavelength of Channel2 is set to " + textBoxWavelength2.Text + " nm";
                    }

                }
                manualReset.Set();
            }
        }

        private void comboBoxPowerRange2_Changed(object sender, EventArgs e)
        {
            //if the "Connect" button's color is the "Control" System Color
            //this means that the combobox index changing is caused by GetCurrentParameters() method
            //so this method will be skiped
            if (buttonConnect.BackColor == SystemColors.Control)
                return;

            //pause the backgroundworker
            manualReset.Reset();

            int comboBoxIndex = comboBoxPowerRange2.SelectedIndex;
            //the setting of the power range follows the round up principle
            //multiply the power range by a factor can avoid the calculation error of double type variables
            tlpmx.setPowerRange(powerRangelistDouble[comboBoxIndex] * 0.95, 2);
            Thread.Sleep(100);
            tlpmx.getPowerRange(0, out double powerRangeCurr, 2);
            textBoxStatus.Text = "Power range of Channel2 is set to " + powerRangeCurr + " W";

            //continue the backgroundworker
            manualReset.Set();

        }

        private void comboBoxEnergyRange2_Changed(object sender, EventArgs e)
        {
            //if the "Connect" button's color is the "Control" System Color
            //this means that the combobox index changing is caused by GetCurrentParameters() method
            //so this method will be skiped
            if (buttonConnect.BackColor == SystemColors.Control)
                return;

            //pause the backgroundworker
            manualReset.Reset();

            int comboBoxIndex = comboBoxEnergyRange2.SelectedIndex;
            //the setting of the energy range follows the round up principle
            //multiply the energy range by a factor can avoid the calculation error of double type variables
            tlpmx.setEnergyRange(energyRangelistDouble[comboBoxIndex] * 0.95, 2);
            Thread.Sleep(100);
            tlpmx.getEnergyRange(0, out double energyRangeCurr, 2);
            textBoxStatus.Text = "Energy range of Channel2 is set to " + energyRangeCurr + " J";

            //continue the backgroundworker
            manualReset.Set();
        }

        private void checkBoxAutoRange2_Changed(object sender, EventArgs e)
        {
            //if the connect button's color is "Control" system color
            //this means that the check box status change is caused by form initialization
            //so the function will be skiped
            if (buttonConnect.BackColor == SystemColors.Control)
                return;

            manualReset.Reset();

            tlpmx.setPowerAutoRange(checkBoxAutoRange2.Checked, 2);
            tlpmx.getPowerAutorange(out bool powerAuto, 2);

            if (powerAuto == checkBoxAutoRange2.Checked == true)
            {
                textBoxStatus.Text = "Auto power range is activated for Channel2.";
                comboBoxPowerRange2.Enabled = false;
            }
            else if (powerAuto == checkBoxAutoRange2.Checked == false)
            {
                textBoxStatus.Text = "Auto power range is cancelled for Channel2.";
                comboBoxPowerRange2.Enabled = true;

                PowerRangeListCreate(comboBoxPowerRange2, 2);
            }
            manualReset.Set();
        }

        private void textBoxAveraging2_KeyPressed(object sender, KeyPressEventArgs e)
        {

            manualReset.Reset();

            if (e.KeyChar == '\r')
            {
                if (!uint.TryParse(textBoxAveraging2.Text, out uint result) && textBoxAveraging2.Text != "")
                {
                    MessageBox.Show("Please input a valid number!");
                    textBoxAveraging2.Text = "";
                }
                else
                {
                    tlpmx.setAvgCnt(Convert.ToInt16(textBoxAveraging2.Text), 2);
                    tlpmx.getAvgCnt(out Int16 AverageCount, 2);
                    if (AverageCount == Convert.ToInt16(textBoxAveraging2.Text))
                        textBoxStatus.Text = "Average Count of Channel 2 is set to" + AverageCount;
                }
            }

            manualReset.Set();
        }

        private void buttonZero2_Click(object sender, EventArgs e)
        {
            manualReset.Reset();

            tlpmx.measPower(out double power, 2);
            buttonZero2.Tag = power;
            textBoxStatus.Text = "Zeroing Channel2 succeeds.";
            manualReset.Set();
        }

        private void textBoxBaseline2_KeyPressed(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == '\r')
            {
                manualReset.Reset();

                if (!double.TryParse(textBoxBaseline2.Text, out double result) && textBoxBaseline2.Text != "")
                {
                    MessageBox.Show("Please input a valid number!");
                    textBoxBaseline2.Text = "";
                    return;
                }

                double baseline2 = Convert.ToDouble(textBoxBaseline2.Text);

                if (baseline2 < 100 && baseline2 > 0)
                {
                    textBoxBaseline2.Tag = baseline2 / 100;
                    textBoxStatus.Text = "Baseline of Channel2 is set to " + textBoxBaseline2.Text + " % of current power/energy range.";
                }
                manualReset.Set();
            }
        }

        private void checkBoxDataProcess_MouseUp(object sender, EventArgs e) 
        {
            CheckBox thisCheckBox = sender as CheckBox;

            //only one data processing function can be activated.
            if (thisCheckBox.Checked == true)
            {
                checkBoxNorm1.Checked = false;
                checkBoxNorm2.Checked = false;
                checkBoxSubstrate.Checked = false;
                checkBoxSum.Checked = false;

                thisCheckBox.Checked = true;
            }
        }

        /// <summary>
        /// Create the power range list. 
        /// </summary>
        /// <param name="comboBox">the combo box that the list should write to.</param>
        /// <param name="channel">the channel number.The value should be 1 or 2.</param>
        /// <returns></returns>
        private void PowerRangeListCreate(ComboBox comboBox, ushort channel)
        {
            //getPowerRange method acceptable values for "Attribute" input parameter
            //TLPM_ATTR_SET_VAL(0): Set value
            //TLPM_ATTR_MIN_VAL(1): Minimum value
            //TLPM_ATTR_MAX_VAL(2): Maximum value
            tlpmx.getPowerRange(0, out double powerRangeCurr, channel);
            tlpmx.getPowerRange(1, out double powerRangeMin, channel);
            tlpmx.getPowerRange(2, out double powerRangeMax, channel);

            //The min and max power range are added to the list. Then adjacent power ranges increase by a factor of 10.
            powerRangelistDouble[0] = powerRangeMin;
            double cache;
            int j = 1;
            for (int i = -6; i < 7 && j < 7 ; i++)
            {
                cache = powerRangeCurr * Math.Pow(10, i);
                if (Math.Round(cache / powerRangeMin, 1) > 1 && Math.Round(cache / powerRangeMax, 1) < 1)
                {
                    powerRangelistDouble[j] = cache;
                    j++;
                }
            }
            powerRangelistDouble[j] = powerRangeMax;


            //add the units for the power ranges
            string[] list = new string[j+1];
            for (int i = 0; i <= j; i++)
            {
                if (Math.Log10(powerRangelistDouble[i]) < -9)
                    list[i] = Math.Round((powerRangelistDouble[i] * 1E12), 2).ToString() + " pW";
                else if (Math.Log10(powerRangelistDouble[i]) >= -9 && Math.Log10(powerRangelistDouble[i]) < -6)
                    list[i] = Math.Round((powerRangelistDouble[i] * 1E9), 2).ToString() + " nW";
                else if (Math.Log10(powerRangelistDouble[i]) >= -6 && Math.Log10(powerRangelistDouble[i]) < -3)
                    list[i] = Math.Round((powerRangelistDouble[i] * 1E6), 2).ToString() + " uW";
                else if (Math.Log10(powerRangelistDouble[i]) >= -3 && Math.Log10(powerRangelistDouble[i]) < 0)
                    list[i] = Math.Round((powerRangelistDouble[i] * 1E3), 2).ToString() + " mW";
                else if (Math.Log10(powerRangelistDouble[i]) >= 0 && Math.Log10(powerRangelistDouble[i]) < 3)
                    list[i] = Math.Round((powerRangelistDouble[i] * 1E0), 2).ToString() + " W";
                else if (Math.Log10(powerRangelistDouble[i]) >= 3)
                    list[i] = Math.Round((powerRangelistDouble[i] * 1E3), 2).ToString() + " kW";
            }

            comboBox.Items.Clear();
            comboBox.Items.AddRange(list);

            int powerRangeCurrIndex = 0;

            //the current shown index of the combobox is the current selected power range
            for (int i = 0; i < 7; i++)
            {
                if (Math.Round(powerRangeCurr / powerRangelistDouble[i], 0) == 1)
                {
                    powerRangeCurrIndex = i;
                    break;
                }
            }
            comboBox.SelectedIndex = powerRangeCurrIndex;
        }

        /// <summary>
        /// Create the energy range list. 
        /// </summary>
        /// <param name="comboBox">the combo box that the list should write to.</param>
        /// <param name="channel">the channel number.The value should be 1 or 2.</param>
        /// <returns></returns>
        private void EnergyRangeListCreate(ComboBox comboBox, ushort channel)
        {
            //getEnergyRange method acceptable values for "Attribute" input parameter
            //TLPM_ATTR_SET_VAL(0): Set value
            //TLPM_ATTR_MIN_VAL(1): Minimum value
            //TLPM_ATTR_MAX_VAL(2): Maximum value
            tlpmx.getEnergyRange(0, out double energyRangeCurr, channel);
            tlpmx.getEnergyRange(1, out double energyRangeMin, channel);
            tlpmx.getEnergyRange(2, out double energyRangeMax, channel);

            //The min and max power range are added to the list. Then adjacent power ranges increase by a factor of 10.
            energyRangelistDouble[0] = energyRangeMin;
            double cache;
            int j = 1;
            for (int i = -6; i < 7 && j < 7; i++)
            {
                cache = energyRangeCurr * Math.Pow(10, i);
                if (Math.Round(cache / energyRangeMin, 1) > 1 && Math.Round(cache / energyRangeMax, 1) < 1)
                {
                    energyRangelistDouble[j] = cache;
                    j++;
                }
            }
            energyRangelistDouble[j] = energyRangeMax;


            //add the units for the energy ranges
            string[] list = new string[j + 1];
            for (int i = 0; i <= j; i++)
            {
                if (Math.Log10(energyRangelistDouble[i]) < -9)
                    list[i] = Math.Round((energyRangelistDouble[i] * 1E12), 2).ToString() + " pJ";
                else if (Math.Log10(energyRangelistDouble[i]) >= -9 && Math.Log10(energyRangelistDouble[i]) < -6)
                    list[i] = Math.Round((energyRangelistDouble[i] * 1E9), 2).ToString() + " nJ";
                else if (Math.Log10(energyRangelistDouble[i]) >= -6 && Math.Log10(energyRangelistDouble[i]) < -3)
                    list[i] = Math.Round((energyRangelistDouble[i] * 1E6), 2).ToString() + " uJ";
                else if (Math.Log10(energyRangelistDouble[i]) >= -3 && Math.Log10(energyRangelistDouble[i]) < 0)
                    list[i] = Math.Round((energyRangelistDouble[i] * 1E3), 2).ToString() + " mJ";
                else if (Math.Log10(energyRangelistDouble[i]) >= 0 && Math.Log10(energyRangelistDouble[i]) < 3)
                    list[i] = Math.Round((energyRangelistDouble[i] * 1E0), 2).ToString() + " J";
                else if (Math.Log10(energyRangelistDouble[i]) >= 3)
                    list[i] = Math.Round((energyRangelistDouble[i] * 1E3), 2).ToString() + " kJ";
            }

            comboBox.Items.Clear();
            comboBox.Items.AddRange(list);

            int energyRangeCurrIndex = 0;

            //the current shown index of the combobox is the current selected power range
            for (int i = 0; i < 7; i++)
            {
                if (Math.Round(energyRangeCurr / energyRangelistDouble[i], 0) == 1)
                {
                    energyRangeCurrIndex = i;
                    break;
                }
            }
            comboBox.SelectedIndex = energyRangeCurrIndex;

        }

    }
}
