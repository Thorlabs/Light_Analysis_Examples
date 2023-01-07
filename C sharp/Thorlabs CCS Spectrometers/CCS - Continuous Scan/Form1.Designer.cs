namespace CCS_Continuous_Scan
{
    partial class Form1
    {
        /// <summary>
        /// Erforderliche Designervariable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Verwendete Ressourcen bereinigen.
        /// </summary>
        /// <param name="disposing">True, wenn verwaltete Ressourcen gelöscht werden sollen; andernfalls False.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Vom Windows Form-Designer generierter Code

        /// <summary>
        /// Erforderliche Methode für die Designerunterstützung.
        /// Der Inhalt der Methode darf nicht mit dem Code-Editor geändert werden.
        /// </summary>
        private void InitializeComponent()
        {
            System.Windows.Forms.DataVisualization.Charting.ChartArea chartArea1 = new System.Windows.Forms.DataVisualization.Charting.ChartArea();
            System.Windows.Forms.DataVisualization.Charting.Series series1 = new System.Windows.Forms.DataVisualization.Charting.Series();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.textBox_SerialNumber = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.ComboBox_ItemNumber = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.button_Initialize = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.numericUpDown_IntegrationTime = new System.Windows.Forms.NumericUpDown();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.button_StopScan = new System.Windows.Forms.Button();
            this.button_StartScanCont = new System.Windows.Forms.Button();
            this.chart1 = new System.Windows.Forms.DataVisualization.Charting.Chart();
            this.Show_Integration_Time = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.DeviceStatus = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_IntegrationTime)).BeginInit();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.chart1)).BeginInit();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.textBox_SerialNumber);
            this.groupBox1.Controls.Add(this.label3);
            this.groupBox1.Controls.Add(this.label1);
            this.groupBox1.Controls.Add(this.ComboBox_ItemNumber);
            this.groupBox1.Controls.Add(this.label4);
            this.groupBox1.Controls.Add(this.button_Initialize);
            this.groupBox1.Location = new System.Drawing.Point(18, 18);
            this.groupBox1.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Padding = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.groupBox1.Size = new System.Drawing.Size(419, 171);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Instrument Informations";
            // 
            // textBox_SerialNumber
            // 
            this.textBox_SerialNumber.Location = new System.Drawing.Point(31, 63);
            this.textBox_SerialNumber.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.textBox_SerialNumber.Name = "textBox_SerialNumber";
            this.textBox_SerialNumber.Size = new System.Drawing.Size(148, 26);
            this.textBox_SerialNumber.TabIndex = 1;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(8, 36);
            this.label3.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(397, 20);
            this.label3.TabIndex = 4;
            this.label3.Text = "Insert the 8 numerics serial number (with leading zeros)";
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(9, 63);
            this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(30, 35);
            this.label1.TabIndex = 5;
            this.label1.Text = "M";
            // 
            // ComboBox_ItemNumber
            // 
            this.ComboBox_ItemNumber.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.ComboBox_ItemNumber.Items.AddRange(new object[] {
            "CCS100",
            "CCS125",
            "CCS150",
            "CCS175",
            "CCS200"});
            this.ComboBox_ItemNumber.Location = new System.Drawing.Point(13, 126);
            this.ComboBox_ItemNumber.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.ComboBox_ItemNumber.Name = "ComboBox_ItemNumber";
            this.ComboBox_ItemNumber.Size = new System.Drawing.Size(148, 28);
            this.ComboBox_ItemNumber.TabIndex = 5;
            // 
            // label4
            // 
            this.label4.Location = new System.Drawing.Point(8, 98);
            this.label4.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(208, 35);
            this.label4.TabIndex = 6;
            this.label4.Text = "Select the Item Number";
            // 
            // button_Initialize
            // 
            this.button_Initialize.Location = new System.Drawing.Point(293, 82);
            this.button_Initialize.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.button_Initialize.Name = "button_Initialize";
            this.button_Initialize.Size = new System.Drawing.Size(112, 79);
            this.button_Initialize.TabIndex = 7;
            this.button_Initialize.Text = "Initialize!";
            this.button_Initialize.UseVisualStyleBackColor = true;
            this.button_Initialize.Click += new System.EventHandler(this.button_Initialize_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(9, 37);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(273, 20);
            this.label2.TabIndex = 2;
            this.label2.Text = "Integration Time:                               ms";
            // 
            // numericUpDown_IntegrationTime
            // 
            this.numericUpDown_IntegrationTime.DecimalPlaces = 2;
            this.numericUpDown_IntegrationTime.Location = new System.Drawing.Point(142, 34);
            this.numericUpDown_IntegrationTime.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.numericUpDown_IntegrationTime.Maximum = new decimal(new int[] {
            60000,
            0,
            0,
            0});
            this.numericUpDown_IntegrationTime.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            131072});
            this.numericUpDown_IntegrationTime.Name = "numericUpDown_IntegrationTime";
            this.numericUpDown_IntegrationTime.Size = new System.Drawing.Size(110, 26);
            this.numericUpDown_IntegrationTime.TabIndex = 3;
            this.numericUpDown_IntegrationTime.Value = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.numericUpDown_IntegrationTime);
            this.groupBox2.Controls.Add(this.button_StopScan);
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Controls.Add(this.button_StartScanCont);
            this.groupBox2.Location = new System.Drawing.Point(451, 18);
            this.groupBox2.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Padding = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.groupBox2.Size = new System.Drawing.Size(297, 171);
            this.groupBox2.TabIndex = 4;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Instrumenmt Settings";
            // 
            // button_StopScan
            // 
            this.button_StopScan.Enabled = false;
            this.button_StopScan.Location = new System.Drawing.Point(14, 126);
            this.button_StopScan.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.button_StopScan.Name = "button_StopScan";
            this.button_StopScan.Size = new System.Drawing.Size(238, 35);
            this.button_StopScan.TabIndex = 5;
            this.button_StopScan.Text = "Stop Scan";
            this.button_StopScan.UseVisualStyleBackColor = true;
            this.button_StopScan.Click += new System.EventHandler(this.button_StopScan_Click);
            // 
            // button_StartScanCont
            // 
            this.button_StartScanCont.Enabled = false;
            this.button_StartScanCont.Location = new System.Drawing.Point(14, 82);
            this.button_StartScanCont.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.button_StartScanCont.Name = "button_StartScanCont";
            this.button_StartScanCont.Size = new System.Drawing.Size(238, 35);
            this.button_StartScanCont.TabIndex = 7;
            this.button_StartScanCont.Text = "Start Continuous Scan";
            this.button_StartScanCont.UseVisualStyleBackColor = true;
            this.button_StartScanCont.Click += new System.EventHandler(this.button_StartScanCont_Click);
            // 
            // chart1
            // 
            chartArea1.AxisX.Interval = 200D;
            chartArea1.AxisX.IntervalAutoMode = System.Windows.Forms.DataVisualization.Charting.IntervalAutoMode.VariableCount;
            chartArea1.AxisX.IntervalOffsetType = System.Windows.Forms.DataVisualization.Charting.DateTimeIntervalType.Number;
            chartArea1.Name = "ChartArea1";
            this.chart1.ChartAreas.Add(chartArea1);
            this.chart1.Location = new System.Drawing.Point(13, 235);
            this.chart1.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.chart1.Name = "chart1";
            series1.ChartArea = "ChartArea1";
            series1.ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            series1.Name = "Series1";
            series1.XValueMember = "6";
            series1.XValueType = System.Windows.Forms.DataVisualization.Charting.ChartValueType.Int32;
            this.chart1.Series.Add(series1);
            this.chart1.Size = new System.Drawing.Size(735, 385);
            this.chart1.TabIndex = 6;
            this.chart1.Text = "chart1";
            // 
            // Show_Integration_Time
            // 
            this.Show_Integration_Time.Enabled = false;
            this.Show_Integration_Time.Location = new System.Drawing.Point(216, 199);
            this.Show_Integration_Time.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.Show_Integration_Time.Name = "Show_Integration_Time";
            this.Show_Integration_Time.ReadOnly = true;
            this.Show_Integration_Time.Size = new System.Drawing.Size(124, 26);
            this.Show_Integration_Time.TabIndex = 8;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(18, 202);
            this.label5.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(353, 20);
            this.label5.TabIndex = 8;
            this.label5.Text = "Current Integration Time is                                  ms";
            // 
            // DeviceStatus
            // 
            this.DeviceStatus.Enabled = false;
            this.DeviceStatus.Location = new System.Drawing.Point(598, 199);
            this.DeviceStatus.Name = "DeviceStatus";
            this.DeviceStatus.ReadOnly = true;
            this.DeviceStatus.Size = new System.Drawing.Size(128, 26);
            this.DeviceStatus.TabIndex = 9;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(460, 202);
            this.label6.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(131, 20);
            this.label6.TabIndex = 8;
            this.label6.Text = "Scanning Status:";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(781, 634);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.DeviceStatus);
            this.Controls.Add(this.Show_Integration_Time);
            this.Controls.Add(this.chart1);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.label5);
            this.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.Name = "Form1";
            this.Text = "CSS Continuous Scan Demo ";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            this.Load += new System.EventHandler(this.Form1_Load);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_IntegrationTime)).EndInit();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.chart1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.TextBox textBox_SerialNumber;
        private System.Windows.Forms.ComboBox ComboBox_ItemNumber;
        private System.Windows.Forms.NumericUpDown numericUpDown_IntegrationTime;
        private System.Windows.Forms.Button button_Initialize;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Button button_StopScan;
        private System.Windows.Forms.Button button_StartScanCont;
        private System.Windows.Forms.DataVisualization.Charting.Chart chart1;
        private System.Windows.Forms.TextBox Show_Integration_Time;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox DeviceStatus;
        private System.Windows.Forms.Label label6;
    }
}

