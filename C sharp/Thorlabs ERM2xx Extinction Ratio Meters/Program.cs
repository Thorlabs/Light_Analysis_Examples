// Title: ERM200 in C#. 
// Created Date: 2024 - 05 - 28
// Last modified date: 2024 - 05 - 28
// .NET version: 4.8.2
// Thorlabs DLL version: 1.1
// Notes:The example connects to a Thorlabs ERM200 and measures the
// extinction ratio and power going through a PM fiber. 


using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using Thorlabs.ERM200_64.Interop;

namespace ERM200
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Create instance of ERM200. 
            TLERM200 tlerm200 = new TLERM200(new IntPtr());

            // Declare variables and string string containers 
            uint resCnt = 0;
            bool deviceAvailable;
            ushort minWavelength;
            ushort maxWavelength;
            double ER;
            double phi;
            double power;
            StringBuilder modelName = new StringBuilder(256);
            StringBuilder serialNumber = new StringBuilder(256);
            StringBuilder manufacturer = new StringBuilder(256);
            StringBuilder resourceString = new StringBuilder(256);
            
            // Get device info and resource name. 
            int err = tlerm200.findRsrc(out resCnt);
            if (0 != err)
                return;

            if (resCnt == 0)
                return;

            
            err = tlerm200.getRsrcInfo(0, modelName, serialNumber, manufacturer, out deviceAvailable);
            if (0 != err)
                return;

            
            err = tlerm200.getRsrcName(0, resourceString);
            if (0 != err)
                return;

            // Connect to device using resource name.
            tlerm200 = new TLERM200(resourceString.ToString(), true, true);

            // Get wavelength range.
            err = tlerm200.getWavelengthRange(out minWavelength, out maxWavelength);
            if (0 != err)
                return;
            Thread.Sleep(5);
            
            // Get ER measurement.
            err = tlerm200.getMeasurement(out ER, out phi);
            if (0 != err)
                return;
            Console.WriteLine("Extinction Ratio = " + ER + "\nPolarization Angle = " + phi);
            Thread.Sleep(5);

            // Get power measuerment. 
            err = tlerm200.getPower(out power);
            if (0 != err)
                return;
            Console.WriteLine("Power going through the fiber = " + power);
            Thread.Sleep(5);

            // Close the device and release all ressources.
            tlerm200.Dispose();
        }
    }
}
