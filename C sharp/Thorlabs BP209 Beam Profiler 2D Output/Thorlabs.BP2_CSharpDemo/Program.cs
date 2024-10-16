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
   using System.Windows.Forms;

   /// <summary>
   /// Entry point of the application
   /// </summary>
   public static class Program
   {
      /// <summary>
      /// The main entry point for the application.
      /// </summary>
      [STAThread]
      public static void Main()
      {
         Application.EnableVisualStyles();
         Application.SetCompatibleTextRenderingDefault(false);
         Application.Run(new Form1());
      }
   }
}
