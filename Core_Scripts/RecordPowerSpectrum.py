#WARNING: THIS SCRIPT WILL BE OVERWRITTEN BY THE INSTALLER!
#IF YOU MUST MODIFY IT, MAKE A COPY OF THIS FILE
#  AND EDIT RecordPowerSpectrum.bat TO CALL YOUR COPY INSTEAD OF THIS FILE

import sys;
import time;
import ctypes;
import struct;


#This code requires Python 3.6 or newer.
import os;
import importlib.util;
spec = importlib.util.spec_from_file_location('VistaScan', 
		os.environ["ProgramFiles"] + '\\Molecular Vista\\VistaScan\\scripting.11\\VistaScan.py');
VistaScan = importlib.util.module_from_spec(spec);
spec.loader.exec_module(VistaScan);



DISTANCE_LIFT = 300;        #microns
CHANNELID_PIFM = 17;
SIGNAL_REQUIRED = 1.2;        #volts

SPECTRUM_SECONDS = 30;
SPECTRUM_REPEATCOUNT = 6;

VistaScan.Connect();


print('Recording power profile to ' + sys.argv[1] + '...');

#ask the user whether they want to lift X hundred microns
resultQuery = VistaScan.UserMessage(
          'This procedure will:\n'
        + ' - Lift the tip ' + str(DISTANCE_LIFT) + ' microns\n'
        + ' - Record the laser power\n'
        + '\nProceed?',
        ['Proceed', 'Cancel'],
        'Proceed'
        );
print("User selected '" + resultQuery + "'");
if (resultQuery == 'Proceed'):
    #  lift head X hundred microns
    print("Retract tip");
    VistaScan.RetractTip();
    print("Lift head");
    positionHead = VistaScan.GetHeadPosition();
    VistaScan.MoveHeadToPosition(positionHead + DISTANCE_LIFT);

    #query mode1 frequency
    print("Auto sweep");
    VistaScan.AutoSetDriveFrequency();
    frequencyMode1 = VistaScan.GetTipFrequency1();
    print("Mode 1 frequency = " + str(frequencyMode1));

    # re-center on the 1st mode
    print("Set frequency = mode1");
    VistaScan.SetTipParameter_DriveFrequency1(frequencyMode1);
    # set the modulation frequency to direct drive
    VistaScan.SetLaserController1_Frequency(frequencyMode1);
       
    # set the pulse duration to close to the highest allowable at that frequency
#!    must add, or make this automatic for the laser

    # check the signal strength at the weakest power wavenumber
    print("Check signal strength");
    signalHave = VistaScan.ReadChannel(CHANNELID_PIFM);
    print("Have " + str(signalHave) + " V, looking for " + str(SIGNAL_REQUIRED) + " V");

    # If the signal is below a certain threshold
    bContinue = True;
    if (signalHave < SIGNAL_REQUIRED):
        # ask the user whether they would like to proceed, or check the alignment.
        resultQuery = VistaScan.UserMessage(
                'The signal is very low, proceed anyway?',
                ['Proceed', 'Cancel'],
                'Cancel'
                );
        if (resultQuery != 'Proceed'):
            bContinue = False;
    
    if (bContinue):
        # The spectrum itself is taken by averaging several spectra.
        # I've been using 6x 30s a lot, so you could start with that,
        # but I may ask for a different combination after testing more.
        VistaScan.SetSpectrumTime(SPECTRUM_SECONDS);
        VistaScan.SetSpectrumRepeat(True);
        VistaScan.SetSpectrumRepeatCount(SPECTRUM_REPEATCOUNT);

        print("Recording spectrum, Please wait...");
        VistaScan.StartLaserSweep();
        while (VistaScan.IsLaserSweeping()):
            time.sleep(0.1);
        spectrum = VistaScan.GetLaserSpectrum();

        #Write spectrum to file specified on command line (sys.argv[1])
        fileOut = open(sys.argv[1], 'wt');
        fileOut.write('#Wavenumber (cm^-1)\tIntensity\n');
        for indexItem in range(0, len(spectrum)):
            fileOut.write(str(spectrum[indexItem]['wavelength']) + '\t' + str(spectrum[indexItem]['intensity']) + '\n');
        fileOut.close();

#Restore any desired previous state

result = VistaScan.Disconnect();
