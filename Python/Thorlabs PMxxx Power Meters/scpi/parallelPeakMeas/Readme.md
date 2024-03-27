# Parallel Peak Measurement Example

This python sample demonstrates how to use multiple Thorlabs Power Meters within one experiment 
to measure peak energy in Joule simultaniously. The example is based on SCPI commands and uses 
the anyvisa Thorlabs library. 

## Details

The code establishes a connection to all Power Meters and configures all of them with the 
same parameters. Once initialiiation is complete the program waits for any of the device 
to detect a peak. Once at least on meter measured a peak, the program tries to fetch a 
measurement from every other PM of the experiment. In case one of the meters did not detect 
a peak in time the file will contain any placeholder. The measurement results or place 
holders are finally stored in .csv file.

To terminate the program use `CTRL + C`. 

## anyvisa python Library
You can download anyvisa library wheel in this Github repository. Please refer to this [README](TODO) how to install it. 

## Supported Meters
- PM103
- PM103E
- PM5020
