using System;

namespace PM5020
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label2 = new System.Windows.Forms.Label();
            this.buttonConnect = new System.Windows.Forms.Button();
            this.buttonMeasCancel = new System.Windows.Forms.Button();
            this.textBoxStatus = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.buttonStartMeas = new System.Windows.Forms.Button();
            this.textBoxValue1 = new System.Windows.Forms.TextBox();
            this.textBoxWavelength1 = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.groupBoxChannel1 = new System.Windows.Forms.GroupBox();
            this.buttonZero1 = new System.Windows.Forms.Button();
            this.checkBoxAutoRange1 = new System.Windows.Forms.CheckBox();
            this.textBoxAveraging1 = new System.Windows.Forms.TextBox();
            this.label17 = new System.Windows.Forms.Label();
            this.comboBoxPowerRange1 = new System.Windows.Forms.ComboBox();
            this.label15 = new System.Windows.Forms.Label();
            this.textBoxBaseline1 = new System.Windows.Forms.TextBox();
            this.comboBoxEnergyRange1 = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.groupBoxChannel2 = new System.Windows.Forms.GroupBox();
            this.textBoxBaseline2 = new System.Windows.Forms.TextBox();
            this.buttonZero2 = new System.Windows.Forms.Button();
            this.label8 = new System.Windows.Forms.Label();
            this.checkBoxAutoRange2 = new System.Windows.Forms.CheckBox();
            this.label6 = new System.Windows.Forms.Label();
            this.textBoxAveraging2 = new System.Windows.Forms.TextBox();
            this.label9 = new System.Windows.Forms.Label();
            this.comboBoxPowerRange2 = new System.Windows.Forms.ComboBox();
            this.label10 = new System.Windows.Forms.Label();
            this.comboBoxEnergyRange2 = new System.Windows.Forms.ComboBox();
            this.label11 = new System.Windows.Forms.Label();
            this.textBoxWavelength2 = new System.Windows.Forms.TextBox();
            this.label12 = new System.Windows.Forms.Label();
            this.label13 = new System.Windows.Forms.Label();
            this.label14 = new System.Windows.Forms.Label();
            this.textBoxValue2 = new System.Windows.Forms.TextBox();
            this.checkBoxNorm1 = new System.Windows.Forms.CheckBox();
            this.checkBoxNorm2 = new System.Windows.Forms.CheckBox();
            this.checkBoxSum = new System.Windows.Forms.CheckBox();
            this.checkBoxSubstrate = new System.Windows.Forms.CheckBox();
            this.label16 = new System.Windows.Forms.Label();
            this.textBoxCalcResult = new System.Windows.Forms.TextBox();
            this.groupBoxDataProcessing = new System.Windows.Forms.GroupBox();
            this.label18 = new System.Windows.Forms.Label();
            this.label19 = new System.Windows.Forms.Label();
            this.label22 = new System.Windows.Forms.Label();
            this.label24 = new System.Windows.Forms.Label();
            this.label25 = new System.Windows.Forms.Label();
            this.label26 = new System.Windows.Forms.Label();
            this.groupBoxChannel1.SuspendLayout();
            this.groupBoxChannel2.SuspendLayout();
            this.groupBoxDataProcessing.SuspendLayout();
            this.SuspendLayout();
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.label2.Location = new System.Drawing.Point(394, 19);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(181, 25);
            this.label2.TabIndex = 1;
            this.label2.Text = "PM5020 Example";
            // 
            // buttonConnect
            // 
            this.buttonConnect.Location = new System.Drawing.Point(34, 50);
            this.buttonConnect.Name = "buttonConnect";
            this.buttonConnect.Size = new System.Drawing.Size(97, 52);
            this.buttonConnect.TabIndex = 2;
            this.buttonConnect.Text = "Connect";
            this.buttonConnect.UseVisualStyleBackColor = true;
            this.buttonConnect.Click += new System.EventHandler(this.buttonConnect_Click);
            // 
            // buttonMeasCancel
            // 
            this.buttonMeasCancel.Enabled = false;
            this.buttonMeasCancel.Location = new System.Drawing.Point(619, 128);
            this.buttonMeasCancel.Name = "buttonMeasCancel";
            this.buttonMeasCancel.Size = new System.Drawing.Size(129, 69);
            this.buttonMeasCancel.TabIndex = 3;
            this.buttonMeasCancel.Text = "Cancel Measurement";
            this.buttonMeasCancel.UseVisualStyleBackColor = true;
            this.buttonMeasCancel.Click += new System.EventHandler(this.buttonMeasCancel_Click);
            // 
            // textBoxStatus
            // 
            this.textBoxStatus.Location = new System.Drawing.Point(221, 63);
            this.textBoxStatus.Name = "textBoxStatus";
            this.textBoxStatus.ReadOnly = true;
            this.textBoxStatus.Size = new System.Drawing.Size(548, 26);
            this.textBoxStatus.TabIndex = 4;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(159, 64);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(56, 20);
            this.label3.TabIndex = 5;
            this.label3.Text = "Status";
            // 
            // buttonStartMeas
            // 
            this.buttonStartMeas.Enabled = false;
            this.buttonStartMeas.Location = new System.Drawing.Point(481, 128);
            this.buttonStartMeas.Name = "buttonStartMeas";
            this.buttonStartMeas.Size = new System.Drawing.Size(125, 69);
            this.buttonStartMeas.TabIndex = 6;
            this.buttonStartMeas.Text = "Start Measurement";
            this.buttonStartMeas.UseVisualStyleBackColor = true;
            this.buttonStartMeas.Click += new System.EventHandler(this.buttonStartMeas_Click);
            // 
            // textBoxValue1
            // 
            this.textBoxValue1.Location = new System.Drawing.Point(605, 221);
            this.textBoxValue1.Name = "textBoxValue1";
            this.textBoxValue1.ReadOnly = true;
            this.textBoxValue1.Size = new System.Drawing.Size(143, 26);
            this.textBoxValue1.TabIndex = 7;
            // 
            // textBoxWavelength1
            // 
            this.textBoxWavelength1.Location = new System.Drawing.Point(26, 66);
            this.textBoxWavelength1.Name = "textBoxWavelength1";
            this.textBoxWavelength1.Size = new System.Drawing.Size(100, 26);
            this.textBoxWavelength1.TabIndex = 8;
            this.textBoxWavelength1.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.textBoxWavelenght1_KeyPressed);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(22, 43);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(129, 20);
            this.label1.TabIndex = 9;
            this.label1.Text = "Wavelength (nm)";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(22, 179);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(105, 20);
            this.label5.TabIndex = 11;
            this.label5.Text = "Power Range";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(22, 367);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(80, 20);
            this.label7.TabIndex = 13;
            this.label7.Text = "Averaging";
            // 
            // groupBoxChannel1
            // 
            this.groupBoxChannel1.Controls.Add(this.buttonZero1);
            this.groupBoxChannel1.Controls.Add(this.checkBoxAutoRange1);
            this.groupBoxChannel1.Controls.Add(this.textBoxAveraging1);
            this.groupBoxChannel1.Controls.Add(this.label7);
            this.groupBoxChannel1.Controls.Add(this.label17);
            this.groupBoxChannel1.Controls.Add(this.comboBoxPowerRange1);
            this.groupBoxChannel1.Controls.Add(this.label1);
            this.groupBoxChannel1.Controls.Add(this.label15);
            this.groupBoxChannel1.Controls.Add(this.textBoxBaseline1);
            this.groupBoxChannel1.Controls.Add(this.comboBoxEnergyRange1);
            this.groupBoxChannel1.Controls.Add(this.label4);
            this.groupBoxChannel1.Controls.Add(this.textBoxWavelength1);
            this.groupBoxChannel1.Controls.Add(this.label5);
            this.groupBoxChannel1.Location = new System.Drawing.Point(25, 119);
            this.groupBoxChannel1.Name = "groupBoxChannel1";
            this.groupBoxChannel1.Size = new System.Drawing.Size(207, 428);
            this.groupBoxChannel1.TabIndex = 15;
            this.groupBoxChannel1.TabStop = false;
            this.groupBoxChannel1.Text = "Channel1";
            // 
            // buttonZero1
            // 
            this.buttonZero1.Location = new System.Drawing.Point(26, 261);
            this.buttonZero1.Name = "buttonZero1";
            this.buttonZero1.Size = new System.Drawing.Size(80, 30);
            this.buttonZero1.TabIndex = 18;
            this.buttonZero1.Tag = "0";
            this.buttonZero1.Text = "Zeroing";
            this.buttonZero1.UseVisualStyleBackColor = true;
            this.buttonZero1.Click += new System.EventHandler(this.buttonZero1_Click);
            // 
            // checkBoxAutoRange1
            // 
            this.checkBoxAutoRange1.AutoSize = true;
            this.checkBoxAutoRange1.Location = new System.Drawing.Point(26, 234);
            this.checkBoxAutoRange1.Name = "checkBoxAutoRange1";
            this.checkBoxAutoRange1.Size = new System.Drawing.Size(121, 24);
            this.checkBoxAutoRange1.TabIndex = 17;
            this.checkBoxAutoRange1.Text = "Auto Range";
            this.checkBoxAutoRange1.UseVisualStyleBackColor = true;
            this.checkBoxAutoRange1.CheckedChanged += new System.EventHandler(this.checkBoxAutoRange1_Changed);
            // 
            // textBoxAveraging1
            // 
            this.textBoxAveraging1.Location = new System.Drawing.Point(26, 391);
            this.textBoxAveraging1.Name = "textBoxAveraging1";
            this.textBoxAveraging1.Size = new System.Drawing.Size(100, 26);
            this.textBoxAveraging1.TabIndex = 16;
            this.textBoxAveraging1.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.textBoxAveraging1_KeyPressed);
            // 
            // label17
            // 
            this.label17.AutoSize = true;
            this.label17.Location = new System.Drawing.Point(132, 333);
            this.label17.Name = "label17";
            this.label17.Size = new System.Drawing.Size(23, 20);
            this.label17.TabIndex = 29;
            this.label17.Text = "%";
            // 
            // comboBoxPowerRange1
            // 
            this.comboBoxPowerRange1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxPowerRange1.FormattingEnabled = true;
            this.comboBoxPowerRange1.ImeMode = System.Windows.Forms.ImeMode.NoControl;
            this.comboBoxPowerRange1.Location = new System.Drawing.Point(26, 202);
            this.comboBoxPowerRange1.Name = "comboBoxPowerRange1";
            this.comboBoxPowerRange1.Size = new System.Drawing.Size(121, 28);
            this.comboBoxPowerRange1.TabIndex = 15;
            this.comboBoxPowerRange1.SelectedIndexChanged += new System.EventHandler(this.comboBoxPowerRange1_Changed);
            // 
            // label15
            // 
            this.label15.AutoSize = true;
            this.label15.Location = new System.Drawing.Point(22, 304);
            this.label15.Name = "label15";
            this.label15.Size = new System.Drawing.Size(70, 20);
            this.label15.TabIndex = 23;
            this.label15.Text = "Baseline";
            // 
            // textBoxBaseline1
            // 
            this.textBoxBaseline1.Location = new System.Drawing.Point(26, 330);
            this.textBoxBaseline1.Name = "textBoxBaseline1";
            this.textBoxBaseline1.Size = new System.Drawing.Size(100, 26);
            this.textBoxBaseline1.TabIndex = 24;
            this.textBoxBaseline1.Tag = "0";
            this.textBoxBaseline1.Text = "0";
            this.textBoxBaseline1.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.textBoxBaseline1_KeyPressed);
            // 
            // comboBoxEnergyRange1
            // 
            this.comboBoxEnergyRange1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxEnergyRange1.FormattingEnabled = true;
            this.comboBoxEnergyRange1.Location = new System.Drawing.Point(26, 131);
            this.comboBoxEnergyRange1.Name = "comboBoxEnergyRange1";
            this.comboBoxEnergyRange1.Size = new System.Drawing.Size(121, 28);
            this.comboBoxEnergyRange1.TabIndex = 14;
            this.comboBoxEnergyRange1.SelectedIndexChanged += new System.EventHandler(this.comboBoxEnergyRange1_Changed);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(22, 108);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(111, 20);
            this.label4.TabIndex = 10;
            this.label4.Text = "Energy Range";
            // 
            // groupBoxChannel2
            // 
            this.groupBoxChannel2.Controls.Add(this.textBoxBaseline2);
            this.groupBoxChannel2.Controls.Add(this.buttonZero2);
            this.groupBoxChannel2.Controls.Add(this.label8);
            this.groupBoxChannel2.Controls.Add(this.checkBoxAutoRange2);
            this.groupBoxChannel2.Controls.Add(this.label6);
            this.groupBoxChannel2.Controls.Add(this.textBoxAveraging2);
            this.groupBoxChannel2.Controls.Add(this.label9);
            this.groupBoxChannel2.Controls.Add(this.comboBoxPowerRange2);
            this.groupBoxChannel2.Controls.Add(this.label10);
            this.groupBoxChannel2.Controls.Add(this.comboBoxEnergyRange2);
            this.groupBoxChannel2.Controls.Add(this.label11);
            this.groupBoxChannel2.Controls.Add(this.textBoxWavelength2);
            this.groupBoxChannel2.Controls.Add(this.label12);
            this.groupBoxChannel2.Location = new System.Drawing.Point(238, 119);
            this.groupBoxChannel2.Name = "groupBoxChannel2";
            this.groupBoxChannel2.Size = new System.Drawing.Size(208, 428);
            this.groupBoxChannel2.TabIndex = 17;
            this.groupBoxChannel2.TabStop = false;
            this.groupBoxChannel2.Text = "Channel2";
            // 
            // textBoxBaseline2
            // 
            this.textBoxBaseline2.Location = new System.Drawing.Point(26, 331);
            this.textBoxBaseline2.Name = "textBoxBaseline2";
            this.textBoxBaseline2.Size = new System.Drawing.Size(100, 26);
            this.textBoxBaseline2.TabIndex = 32;
            this.textBoxBaseline2.Tag = "0";
            this.textBoxBaseline2.Text = "0";
            this.textBoxBaseline2.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.textBoxBaseline2_KeyPressed);
            // 
            // buttonZero2
            // 
            this.buttonZero2.Location = new System.Drawing.Point(25, 261);
            this.buttonZero2.Name = "buttonZero2";
            this.buttonZero2.Size = new System.Drawing.Size(77, 30);
            this.buttonZero2.TabIndex = 19;
            this.buttonZero2.Tag = "0";
            this.buttonZero2.Text = "Zeroing";
            this.buttonZero2.UseVisualStyleBackColor = true;
            this.buttonZero2.Click += new System.EventHandler(this.buttonZero2_Click);
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(132, 334);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(23, 20);
            this.label8.TabIndex = 31;
            this.label8.Text = "%";
            // 
            // checkBoxAutoRange2
            // 
            this.checkBoxAutoRange2.AutoSize = true;
            this.checkBoxAutoRange2.Location = new System.Drawing.Point(26, 234);
            this.checkBoxAutoRange2.Name = "checkBoxAutoRange2";
            this.checkBoxAutoRange2.Size = new System.Drawing.Size(121, 24);
            this.checkBoxAutoRange2.TabIndex = 18;
            this.checkBoxAutoRange2.Text = "Auto Range";
            this.checkBoxAutoRange2.UseVisualStyleBackColor = true;
            this.checkBoxAutoRange2.CheckedChanged += new System.EventHandler(this.checkBoxAutoRange2_Changed);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(22, 304);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(70, 20);
            this.label6.TabIndex = 30;
            this.label6.Text = "Baseline";
            // 
            // textBoxAveraging2
            // 
            this.textBoxAveraging2.Location = new System.Drawing.Point(25, 393);
            this.textBoxAveraging2.Name = "textBoxAveraging2";
            this.textBoxAveraging2.Size = new System.Drawing.Size(100, 26);
            this.textBoxAveraging2.TabIndex = 16;
            this.textBoxAveraging2.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.textBoxAveraging2_KeyPressed);
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(22, 367);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(80, 20);
            this.label9.TabIndex = 13;
            this.label9.Text = "Averaging";
            // 
            // comboBoxPowerRange2
            // 
            this.comboBoxPowerRange2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxPowerRange2.FormattingEnabled = true;
            this.comboBoxPowerRange2.Location = new System.Drawing.Point(26, 202);
            this.comboBoxPowerRange2.Name = "comboBoxPowerRange2";
            this.comboBoxPowerRange2.Size = new System.Drawing.Size(121, 28);
            this.comboBoxPowerRange2.TabIndex = 15;
            this.comboBoxPowerRange2.SelectedIndexChanged += new System.EventHandler(this.comboBoxPowerRange2_Changed);
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(22, 43);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(129, 20);
            this.label10.TabIndex = 9;
            this.label10.Text = "Wavelength (nm)";
            // 
            // comboBoxEnergyRange2
            // 
            this.comboBoxEnergyRange2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxEnergyRange2.FormattingEnabled = true;
            this.comboBoxEnergyRange2.Location = new System.Drawing.Point(26, 131);
            this.comboBoxEnergyRange2.Name = "comboBoxEnergyRange2";
            this.comboBoxEnergyRange2.Size = new System.Drawing.Size(121, 28);
            this.comboBoxEnergyRange2.TabIndex = 14;
            this.comboBoxEnergyRange2.SelectedIndexChanged += new System.EventHandler(this.comboBoxEnergyRange2_Changed);
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(22, 108);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(111, 20);
            this.label11.TabIndex = 10;
            this.label11.Text = "Energy Range";
            // 
            // textBoxWavelength2
            // 
            this.textBoxWavelength2.Location = new System.Drawing.Point(26, 66);
            this.textBoxWavelength2.Name = "textBoxWavelength2";
            this.textBoxWavelength2.Size = new System.Drawing.Size(100, 26);
            this.textBoxWavelength2.TabIndex = 8;
            this.textBoxWavelength2.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.textBoxWavelenght2_KeyPressed);
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Location = new System.Drawing.Point(22, 179);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(105, 20);
            this.label12.TabIndex = 11;
            this.label12.Text = "Power Range";
            // 
            // label13
            // 
            this.label13.AutoSize = true;
            this.label13.Location = new System.Drawing.Point(477, 227);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(122, 20);
            this.label13.TabIndex = 18;
            this.label13.Text = "Channel1 Value";
            // 
            // label14
            // 
            this.label14.AutoSize = true;
            this.label14.Location = new System.Drawing.Point(477, 264);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(122, 20);
            this.label14.TabIndex = 19;
            this.label14.Text = "Channel2 Value";
            // 
            // textBoxValue2
            // 
            this.textBoxValue2.Location = new System.Drawing.Point(605, 261);
            this.textBoxValue2.Name = "textBoxValue2";
            this.textBoxValue2.ReadOnly = true;
            this.textBoxValue2.Size = new System.Drawing.Size(143, 26);
            this.textBoxValue2.TabIndex = 20;
            // 
            // checkBoxNorm1
            // 
            this.checkBoxNorm1.AutoSize = true;
            this.checkBoxNorm1.Location = new System.Drawing.Point(8, 37);
            this.checkBoxNorm1.Name = "checkBoxNorm1";
            this.checkBoxNorm1.Size = new System.Drawing.Size(177, 24);
            this.checkBoxNorm1.TabIndex = 21;
            this.checkBoxNorm1.Text = "Normalize Channel1";
            this.checkBoxNorm1.UseVisualStyleBackColor = true;
            this.checkBoxNorm1.MouseUp += new System.Windows.Forms.MouseEventHandler(this.checkBoxDataProcess_MouseUp);
            // 
            // checkBoxNorm2
            // 
            this.checkBoxNorm2.AutoSize = true;
            this.checkBoxNorm2.Location = new System.Drawing.Point(8, 75);
            this.checkBoxNorm2.Name = "checkBoxNorm2";
            this.checkBoxNorm2.Size = new System.Drawing.Size(177, 24);
            this.checkBoxNorm2.TabIndex = 22;
            this.checkBoxNorm2.Text = "Normalize Channel2";
            this.checkBoxNorm2.UseVisualStyleBackColor = true;
            this.checkBoxNorm2.MouseUp += new System.Windows.Forms.MouseEventHandler(this.checkBoxDataProcess_MouseUp);
            // 
            // checkBoxSum
            // 
            this.checkBoxSum.AutoSize = true;
            this.checkBoxSum.Location = new System.Drawing.Point(8, 153);
            this.checkBoxSum.Name = "checkBoxSum";
            this.checkBoxSum.Size = new System.Drawing.Size(206, 24);
            this.checkBoxSum.TabIndex = 25;
            this.checkBoxSum.Text = "Sum of Power or Energy";
            this.checkBoxSum.UseVisualStyleBackColor = true;
            this.checkBoxSum.MouseUp += new System.Windows.Forms.MouseEventHandler(this.checkBoxDataProcess_MouseUp);
            // 
            // checkBoxSubstrate
            // 
            this.checkBoxSubstrate.AutoSize = true;
            this.checkBoxSubstrate.Location = new System.Drawing.Point(8, 114);
            this.checkBoxSubstrate.Name = "checkBoxSubstrate";
            this.checkBoxSubstrate.Size = new System.Drawing.Size(263, 24);
            this.checkBoxSubstrate.TabIndex = 26;
            this.checkBoxSubstrate.Text = "Substraction of Power or Energy";
            this.checkBoxSubstrate.UseVisualStyleBackColor = true;
            this.checkBoxSubstrate.MouseUp += new System.Windows.Forms.MouseEventHandler(this.checkBoxDataProcess_MouseUp);
            // 
            // label16
            // 
            this.label16.AutoSize = true;
            this.label16.Location = new System.Drawing.Point(477, 302);
            this.label16.Name = "label16";
            this.label16.Size = new System.Drawing.Size(90, 20);
            this.label16.TabIndex = 27;
            this.label16.Text = "Calc Result";
            // 
            // textBoxCalcResult
            // 
            this.textBoxCalcResult.Enabled = false;
            this.textBoxCalcResult.Location = new System.Drawing.Point(605, 302);
            this.textBoxCalcResult.Name = "textBoxCalcResult";
            this.textBoxCalcResult.ReadOnly = true;
            this.textBoxCalcResult.Size = new System.Drawing.Size(143, 26);
            this.textBoxCalcResult.TabIndex = 28;
            // 
            // groupBoxDataProcessing
            // 
            this.groupBoxDataProcessing.Controls.Add(this.checkBoxNorm1);
            this.groupBoxDataProcessing.Controls.Add(this.checkBoxNorm2);
            this.groupBoxDataProcessing.Controls.Add(this.checkBoxSubstrate);
            this.groupBoxDataProcessing.Controls.Add(this.checkBoxSum);
            this.groupBoxDataProcessing.Enabled = false;
            this.groupBoxDataProcessing.Location = new System.Drawing.Point(474, 352);
            this.groupBoxDataProcessing.Name = "groupBoxDataProcessing";
            this.groupBoxDataProcessing.Size = new System.Drawing.Size(274, 195);
            this.groupBoxDataProcessing.TabIndex = 30;
            this.groupBoxDataProcessing.TabStop = false;
            this.groupBoxDataProcessing.Text = "Data Processing";
            // 
            // label18
            // 
            this.label18.AutoSize = true;
            this.label18.Location = new System.Drawing.Point(769, 135);
            this.label18.Name = "label18";
            this.label18.Size = new System.Drawing.Size(175, 20);
            this.label18.TabIndex = 31;
            this.label18.Text = "Explanation about GUI:";
            // 
            // label19
            // 
            this.label19.Location = new System.Drawing.Point(769, 164);
            this.label19.Name = "label19";
            this.label19.Size = new System.Drawing.Size(307, 109);
            this.label19.TabIndex = 32;
            this.label19.Text = "1. \"Channel1/2\" Group Box contains the settings for the sensor in Channel 1/2. Wh" +
    "en the parameters are modified successfully, the \"Status\" textbox will prompt yo" +
    "u. ";
            // 
            // label22
            // 
            this.label22.Location = new System.Drawing.Point(769, 277);
            this.label22.Name = "label22";
            this.label22.Size = new System.Drawing.Size(291, 51);
            this.label22.TabIndex = 35;
            this.label22.Text = "2. \"Channel1/2 Value\" shows the power or energy value for Channel 1/2.";
            // 
            // label24
            // 
            this.label24.Location = new System.Drawing.Point(769, 320);
            this.label24.Name = "label24";
            this.label24.Size = new System.Drawing.Size(291, 85);
            this.label24.TabIndex = 37;
            this.label24.Text = "\"Calc Result\" shows the data procesing results. It\'s available only when two powe" +
    "r sensors or two energy sensors are connected.";
            // 
            // label25
            // 
            this.label25.Location = new System.Drawing.Point(769, 413);
            this.label25.Name = "label25";
            this.label25.Size = new System.Drawing.Size(291, 63);
            this.label25.TabIndex = 38;
            this.label25.Text = "3. \"Normalize Channel1\" calculates the ratio of channel2\'s value to channel1\'s va" +
    "lue.";
            // 
            // label26
            // 
            this.label26.Location = new System.Drawing.Point(769, 476);
            this.label26.Name = "label26";
            this.label26.Size = new System.Drawing.Size(291, 67);
            this.label26.TabIndex = 39;
            this.label26.Text = "\"Normalize Channel2\" calculates the ratio of channel1\'s value to channel2\'s value" +
    ".";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1074, 559);
            this.Controls.Add(this.label26);
            this.Controls.Add(this.label25);
            this.Controls.Add(this.label24);
            this.Controls.Add(this.label22);
            this.Controls.Add(this.label19);
            this.Controls.Add(this.label18);
            this.Controls.Add(this.groupBoxDataProcessing);
            this.Controls.Add(this.textBoxCalcResult);
            this.Controls.Add(this.label16);
            this.Controls.Add(this.textBoxValue2);
            this.Controls.Add(this.label14);
            this.Controls.Add(this.label13);
            this.Controls.Add(this.groupBoxChannel2);
            this.Controls.Add(this.groupBoxChannel1);
            this.Controls.Add(this.textBoxValue1);
            this.Controls.Add(this.buttonStartMeas);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.textBoxStatus);
            this.Controls.Add(this.buttonMeasCancel);
            this.Controls.Add(this.buttonConnect);
            this.Controls.Add(this.label2);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.groupBoxChannel1.ResumeLayout(false);
            this.groupBoxChannel1.PerformLayout();
            this.groupBoxChannel2.ResumeLayout(false);
            this.groupBoxChannel2.PerformLayout();
            this.groupBoxDataProcessing.ResumeLayout(false);
            this.groupBoxDataProcessing.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button buttonConnect;
        private System.Windows.Forms.Button buttonMeasCancel;
        private System.Windows.Forms.TextBox textBoxStatus;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button buttonStartMeas;
        private System.Windows.Forms.TextBox textBoxValue1;
        private System.Windows.Forms.TextBox textBoxWavelength1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.GroupBox groupBoxChannel1;
        private System.Windows.Forms.TextBox textBoxAveraging1;
        private System.Windows.Forms.GroupBox groupBoxChannel2;
        private System.Windows.Forms.TextBox textBoxAveraging2;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.ComboBox comboBoxPowerRange2;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.ComboBox comboBoxEnergyRange2;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.TextBox textBoxWavelength2;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.TextBox textBoxValue2;
        private System.Windows.Forms.CheckBox checkBoxNorm1;
        private System.Windows.Forms.CheckBox checkBoxNorm2;
        private System.Windows.Forms.Label label15;
        private System.Windows.Forms.TextBox textBoxBaseline1;
        private System.Windows.Forms.CheckBox checkBoxSum;
        private System.Windows.Forms.CheckBox checkBoxSubstrate;
        private System.Windows.Forms.Label label16;
        private System.Windows.Forms.TextBox textBoxCalcResult;
        private System.Windows.Forms.Label label17;
        private System.Windows.Forms.GroupBox groupBoxDataProcessing;
        private System.Windows.Forms.CheckBox checkBoxAutoRange1;
        private System.Windows.Forms.CheckBox checkBoxAutoRange2;
        private System.Windows.Forms.ComboBox comboBoxEnergyRange1;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.ComboBox comboBoxPowerRange1;
        private System.Windows.Forms.Button buttonZero1;
        private System.Windows.Forms.Button buttonZero2;
        private System.Windows.Forms.TextBox textBoxBaseline2;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label18;
        private System.Windows.Forms.Label label19;
        private System.Windows.Forms.Label label22;
        private System.Windows.Forms.Label label24;
        private System.Windows.Forms.Label label25;
        private System.Windows.Forms.Label label26;
    }
}

