using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Threading;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using CSharpExamples.Common;
using ThorlabsOSAWrapper;

namespace Thorlabs_OSA_GUI
{
    public sealed class MainForm : Form
    {
        private const int MaximumPlotPoints = 4000;

        private readonly Button _connectButton;
        private readonly Button _acquireButton;
        private readonly Label _statusLabel;
        private readonly Chart _spectrumChart;
        private readonly Chart _interferogramChart;
        private readonly System.Windows.Forms.Timer _renderTimer;
        private readonly LibraryAnalysis _analysis = new LibraryAnalysis();

        private OsaConnection _connection;
        private ContinuousAcquisition _acquisition;
        private bool _isRedstone;
        private ushort _wavemeterChannel;
        private ushort _stitchedSpectrumChannel;
        private PlotFrame _latestSpectrumFrame;
        private PlotFrame _latestInterferogramFrame;
        private string _latestAcquisitionError;

        public MainForm()
        {
            Text = "Thorlabs OSA C# live view";
            Width = 1100;
            Height = 750;
            StartPosition = FormStartPosition.CenterScreen;

            var toolbar = new FlowLayoutPanel
            {
                Dock = DockStyle.Top,
                AutoSize = true,
                Padding = new Padding(8)
            };

            _connectButton = new Button
            {
                AutoSize = true,
                Text = "Find and connect"
            };
            _connectButton.Click += Connect;

            _acquireButton = new Button
            {
                AutoSize = true,
                Enabled = false,
                Text = "Start continuous acquisition"
            };
            _acquireButton.Click += ToggleAcquisition;

            _statusLabel = new Label
            {
                AutoSize = true,
                Padding = new Padding(12, 7, 0, 0),
                Text = "Not connected"
            };

            toolbar.Controls.Add(_connectButton);
            toolbar.Controls.Add(_acquireButton);
            toolbar.Controls.Add(_statusLabel);

            var plots = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 2
            };
            plots.RowStyles.Add(new RowStyle(SizeType.Percent, 50));
            plots.RowStyles.Add(new RowStyle(SizeType.Percent, 50));

            _spectrumChart = CreateChart("Spectrum");
            _interferogramChart = CreateChart("Interferogram");
            plots.Controls.Add(_spectrumChart, 0, 0);
            plots.Controls.Add(_interferogramChart, 0, 1);

            Controls.Add(plots);
            Controls.Add(toolbar);

            _renderTimer = new System.Windows.Forms.Timer { Interval = 250 };
            _renderTimer.Tick += RenderLatestFrames;
            _renderTimer.Start();

            FormClosing += OnFormClosing;
        }

        private static Chart CreateChart(string title)
        {
            var chart = new Chart { Dock = DockStyle.Fill };
            var area = new ChartArea("PlotArea");
            area.AxisX.Title = "X";
            area.AxisY.Title = "Signal";
            area.AxisX.LabelStyle.Format = "G6";
            area.AxisY.LabelStyle.Format = "G6";
            chart.ChartAreas.Add(area);
            chart.Titles.Add(title);
            chart.Series.Add(new Series("Data")
            {
                ChartArea = area.Name,
                ChartType = SeriesChartType.FastLine,
                BorderWidth = 2,
                XValueType = ChartValueType.Double,
                YValueType = ChartValueType.Double
            });
            return chart;
        }

        private void Connect(object sender, EventArgs eventArgs)
        {
            StopAcquisition();
            _connection?.Dispose();
            _connection = null;

            _connectButton.Enabled = false;
            _acquireButton.Enabled = false;
            _statusLabel.Text = "Searching for and initializing Thorlabs OSAs...";
            UseWaitCursor = true;
            _statusLabel.Refresh();
            _connectButton.Refresh();

            try
            {
                _connection = OsaConnection.OpenFirst();
                _isRedstone =
                    _connection.Device.GetInstrumentSeries() == InstrumentSeries.RedstoneSeries;
                _wavemeterChannel = _isRedstone
                    ? _connection.Device.GetDUTChannelIndices().First()
                    : (ushort)0;
                _stitchedSpectrumChannel =
                    _connection.Device.GetStitchedSpectrumChannelIndex();
                _acquireButton.Enabled = true;
                _statusLabel.Text = string.Format(
                    "Connected: {0}, serial {1}",
                    _connection.Device.GetInstrumentModel(),
                    _connection.Device.InstrumentDescription.GetSerial());
            }
            catch (Exception exception)
            {
                _connectButton.Enabled = true;
                _statusLabel.Text = exception.Message;
                MessageBox.Show(this, exception.Message, "Connection failed", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
                UseWaitCursor = false;
            }
        }

        private void ToggleAcquisition(object sender, EventArgs eventArgs)
        {
            if (_acquisition == null)
            {
                StartAcquisition();
            }
            else
            {
                _acquireButton.Enabled = false;
                _statusLabel.Text = "Stopping acquisition...";
                _statusLabel.Refresh();
                StopAcquisition();
            }
        }

        private void StartAcquisition()
        {
            try
            {
                _acquisition = new ContinuousAcquisition(_connection.Device);
                _acquisition.SpectrumReceived += OnSpectrum;
                _acquisition.InterferogramReceived += OnInterferogram;
                _acquisition.AcquisitionError += OnAcquisitionError;
                _acquisition.Start();

                _connectButton.Enabled = false;
                _acquireButton.Text = "Stop acquisition";
                _statusLabel.Text = "Acquiring...";
            }
            catch (Exception exception)
            {
                StopAcquisition();
                MessageBox.Show(this, exception.Message, "Acquisition failed", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void StopAcquisition()
        {
            if (_acquisition != null)
            {
                _acquisition.SpectrumReceived -= OnSpectrum;
                _acquisition.InterferogramReceived -= OnInterferogram;
                _acquisition.AcquisitionError -= OnAcquisitionError;
                _acquisition.Dispose();
                _acquisition = null;
            }

            _connectButton.Enabled = _connection == null;
            _acquireButton.Enabled = _connection != null;
            _acquireButton.Text = "Start continuous acquisition";
            _statusLabel.Text = _connection == null ? "Not connected" : "Connected; acquisition stopped";
            Interlocked.Exchange(ref _latestSpectrumFrame, null);
            Interlocked.Exchange(ref _latestInterferogramFrame, null);
            Interlocked.Exchange(ref _latestAcquisitionError, null);
        }

        private void OnSpectrum(SpectrumStruct spectrum)
        {
            if (_isRedstone && spectrum.channelIndex != _stitchedSpectrumChannel)
            {
                return;
            }

            string title = string.Format(
                "Spectrum - {0:HH:mm:ss}",
                spectrum.TimeStamp);
            PeakTrackAnalysisResult peaks =
                _analysis.PeakTrack(spectrum, 0.01, 3.0, 0, (int)spectrum.Length, 1);
            if (peaks.Success && peaks.Number > 0)
            {
                title += string.Format(" - highest peak {0:G8} cm^-1", peaks.data[0].centroidPosition);
            }

            Interlocked.Exchange(
                ref _latestSpectrumFrame,
                CreatePlotFrame(spectrum, title));
        }

        private void OnInterferogram(SpectrumStruct interferogram)
        {
            if (_isRedstone && interferogram.channelIndex != _wavemeterChannel)
            {
                return;
            }

            string title = string.Format(
                "Interferogram - {0:HH:mm:ss}",
                interferogram.TimeStamp);
            WavelengthMeterAnalysisResult wavemeter =
                _analysis.WavelengthMeter(interferogram, 0U, interferogram.Length);
            if (wavemeter.Success)
            {
                title += string.Format(" - {0:G9} +/- {1:G4} cm^-1", wavemeter.wavenumber, wavemeter.waveNumberError);
            }

            Interlocked.Exchange(
                ref _latestInterferogramFrame,
                CreatePlotFrame(interferogram, title));
        }

        private static PlotFrame CreatePlotFrame(SpectrumStruct data, string title)
        {
            int length = Math.Min((int)data.Length, data.Value.Count);
            if (length == 0)
            {
                return null;
            }

            int step = Math.Max(1, (length + MaximumPlotPoints - 1) / MaximumPlotPoints);
            var x = new List<double>(Math.Min(length, MaximumPlotPoints + 1));
            var y = new List<double>(Math.Min(length, MaximumPlotPoints + 1));

            for (int index = 0; index < length; index += step)
            {
                AddFinitePoint(data, index, x, y);
            }

            if ((length - 1) % step != 0)
            {
                AddFinitePoint(data, length - 1, x, y);
            }

            if (x.Count == 0)
            {
                return null;
            }

            if (x[0] > x[x.Count - 1])
            {
                x.Reverse();
                y.Reverse();
            }

            return new PlotFrame(x.ToArray(), y.ToArray(), title);
        }

        private static void AddFinitePoint(
            SpectrumStruct data,
            int index,
            ICollection<double> x,
            ICollection<double> y)
        {
            double xValue = data.GetXAtIndex(index);
            double yValue = data.Value[index];
            if (!double.IsNaN(xValue) &&
                !double.IsInfinity(xValue) &&
                !double.IsNaN(yValue) &&
                !double.IsInfinity(yValue))
            {
                x.Add(xValue);
                y.Add(yValue);
            }
        }

        private void RenderLatestFrames(object sender, EventArgs eventArgs)
        {
            RenderFrame(
                _spectrumChart,
                Interlocked.Exchange(ref _latestSpectrumFrame, null));
            RenderFrame(
                _interferogramChart,
                Interlocked.Exchange(ref _latestInterferogramFrame, null));

            string error = Interlocked.Exchange(ref _latestAcquisitionError, null);
            if (error != null)
            {
                _statusLabel.Text = "OSA: " + error;
            }
        }

        private static void RenderFrame(Chart chart, PlotFrame frame)
        {
            if (frame == null)
            {
                return;
            }

            Series series = chart.Series["Data"];
            series.Points.Clear();
            series.Points.DataBindXY(frame.X, frame.Y);
            chart.Titles[0].Text = frame.Title;
            chart.ResetAutoValues();
            chart.ChartAreas["PlotArea"].RecalculateAxesScale();
            chart.Invalidate();
        }

        private void OnAcquisitionError(string message)
        {
            Interlocked.Exchange(ref _latestAcquisitionError, message);
        }

        private void OnFormClosing(object sender, FormClosingEventArgs eventArgs)
        {
            _renderTimer.Stop();
            StopAcquisition();
            _connection?.Dispose();
            _connection = null;
            _renderTimer.Dispose();
        }

        private sealed class PlotFrame
        {
            public PlotFrame(double[] x, double[] y, string title)
            {
                X = x;
                Y = y;
                Title = title;
            }

            public double[] X { get; }

            public double[] Y { get; }

            public string Title { get; }
        }
    }
}
