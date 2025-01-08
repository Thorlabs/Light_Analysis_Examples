//Example Date of Creation(YYYY - MM - DD) 2023 - 05 - 24
//Example Date of Last Modification on Github 2023 - 05 - 24
//Version of .NET Framework used for Testing: 4.7.2
//Version of the Thorlabs Dll: 5.6.4927.658
//Example Description: This example has a GUI interface, including the initialization, parameter reading, parameter setting and value display. 
//If two power sensors or two energy sensors are connected to the PM5020 simultaneously, data processing like normalization, 
//sum and difference functions are also available. This example is also compatible with single-channel meters like PM10X series.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using Thorlabs.TLPMX_64.Interop;

namespace PM5020
{
    internal static class Program
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
