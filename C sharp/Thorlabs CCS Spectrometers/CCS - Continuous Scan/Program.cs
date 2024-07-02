//Example Date of Creation(YYYY - MM - DD) 2023 - 02 - 15
//Example Date of Last Modification on Github 2023 - 03 - 15
//Version of .NET Framework used for Testing: 4.7.2
//Version of the Thorlabs Dll: 2.0.0.0
//Example Description: This example has a GUI interface, includes the initialization of the spectrometer 
//and real-time spectrum display with a set integration time.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace CCS_Continuous_Scan
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }
}
