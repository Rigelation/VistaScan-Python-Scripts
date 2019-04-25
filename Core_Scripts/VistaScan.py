import os;
import ctypes;
from ctypes import *;

MAX_PATH = 255;

dllVSScripting = cdll.LoadLibrary(os.environ["ProgramFiles"] + '\Molecular Vista\VistaScan\scripting.11\VistaScanScripting.dll');

SCRIPTING_SUCCESS = 1;

SCRIPTING_ERROR_GENERIC                      = 0;
SCRIPTING_ERROR_ALREADYCONNECTED             = -1;
SCRIPTING_ERROR_COMMANDNOTFOUND              = -2;
SCRIPTING_ERROR_TIMEOUT                      = -3;
SCRIPTING_ERROR_NOTCONNECTED                 = -4;
SCRIPTING_ERROR_OUTOFRESOURCES               = -5;
SCRIPTING_ERROR_INVALIDPARAMETER             = -6;
SCRIPTING_ERROR_INVALIDRESPONSE              = -7;   #probably a program/DLL version mismatch
SCRIPTING_ERROR_FAILED                       = -8;
SCRIPTING_ERROR_NOTIMPLEMENTED               = -9;
SCRIPTING_ERROR_NOTALLOWEDNOW                = -10;  #not allowed at this time
SCRIPTING_ERROR_DATASIZEMISMATCH             = -11;  #not enough data was sent
SCRIPTING_ERROR_NOTENOUGHSPACE               = -12;  #provided buffer was not large enough
SCRIPTING_ERROR_INCOMPATIBLE                 = -13;

SCRIPTING_VALUE_QUERY = 1;              #query the current value
SCRIPTING_VALUE_SET = 2;                #set the value
SCRIPTING_VALUE_QUERYANDSET = 3;        #set the value and return the previous value
SCRIPTING_VALUE_SETANDQUERY = 4;        #set the value and return the current value


FEEDBACKMODE_OFF = -1;
FEEDBACKMODE_CONTACT = 0;
FEEDBACKMODE_FORCEMODULATION = 1;
FEEDBACKMODE_TAPPING = 2;
FEEDBACKMODE_NONCONTACT = 3;
FEEDBACKMODE_RESONANCE_OPTICALFORCE = 4;
FEEDBACKMODE_BIMODAL = 5;
FEEDBACKMODE_KELVINPROBE = 6;
FEEDBACKMODE_TUNINGFORK = 7;
FEEDBACKMODE_TUNINGFORK_BIMODAL = 8;
FEEDBACKMODE_STM = 9;

SCRIPTING_LINESCANDIRECTION_FORWARD = 1;
SCRIPTING_LINESCANDIRECTION_BACKWARD = 2;
SCRIPTING_LINESCANDIRECTION_FLY = 4;

APPROACH_SLOW = 1;
APPROACH_FAST = 2;

LIA0 = 0;
LIA1 = 1;
LIA2 = 2;
LIA3 = 3;

LOCKININPUT_A = 0;
LOCKININPUT_B = 1;

CAMERA_TOP = 0;
CAMERA_BOTTOM = 1;


#events
#struct SCRIPTING_Event
class SCRIPTING_Event(Structure):
    _fields_ = [
        ("pName", c_char_p),        #null terminated
        ("countBytes", c_int),
        ("pData", POINTER(c_byte))  #what is pointed to depends on the event name (pName).
                                    #see event names and EventData_* structures
        ];


#event 'RowCompleted'
NAME_EVENT_SCAN_ROWCOMPLETE = 'RowCompleted';
class EventData_Scan_RowComplete(Structure):
    _fields_ = [
        ("indexRow", c_int)
        ];

#event 'StartScanPixel'
NAME_EVENT_SCAN_STARTPIXEL = 'StartScanPixel';
class EventData_Scan_StartPixel(Structure):
    _fields_ = [
        ("indexRow", c_int),
        ("indexCol", c_int),
        ("direction", c_int)
        ];

class c_pixelSpectrum(Structure):
    _fields_ = [
        ("wavelength", c_double),
        ("intensity", c_double),
        ];

TIMEOUT_INFINITE = 0xffffffff;


#return type is 'int' (ctypes default)
cdll.VistaScanScripting.Connect.argtypes = [];
cdll.VistaScanScripting.Disconnect.argtypes = [];

#UserMessage
#  message
#  button captions separated by ';'
#  caption of default button
cdll.VistaScanScripting.UserMessage.argtypes = [c_char_p, c_char_p, c_char_p];

cdll.VistaScanScripting.ImageData_SaveCurrentData.argtypes = [];
cdll.VistaScanScripting.ImageData_SavePath.argtypes = [POINTER(c_char), POINTER(c_uint), c_uint];
cdll.VistaScanScripting.ImageData_Filename.argtypes = [POINTER(c_char), POINTER(c_uint), c_uint];

cdll.VistaScanScripting.Scanner_IsScanning.argtypes = [POINTER(c_bool), c_uint];
cdll.VistaScanScripting.Scanner_Position.argtypes = [POINTER(c_double), POINTER(c_double), c_uint];
cdll.VistaScanScripting.Scanner_StartScan.argtypes = [];
cdll.VistaScanScripting.Scanner_ContinueScan.argtypes = [];
cdll.VistaScanScripting.Scanner_StopScan.argtypes = [];
cdll.VistaScanScripting.Scanner_StartInteractiveScan.argtypes = [];
cdll.VistaScanScripting.Scanner_InteractiveScan_DoneRecordingPixel.argtypes = [];

cdll.VistaScanScripting.ScanParameter_LineScanDirections.argtypes = [POINTER(c_uint), c_uint];
cdll.VistaScanScripting.ScanParameter_LinesPerSecond.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.ScanParameter_Area.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_uint];
cdll.VistaScanScripting.ScanParameter_Angle.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.ScanParameter_Resolution.argtypes = [POINTER(c_uint), c_uint];
cdll.VistaScanScripting.ScanParameter_LoopMode.argtypes = [POINTER(c_uint), c_uint];

cdll.VistaScanScripting.FeedbackParameter_FeedbackMode.argtypes = [POINTER(c_int), c_uint];

cdll.VistaScanScripting.FeedbackParameter_Setpoint.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.FeedbackParameter_Ki.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.FeedbackParameter_Kp.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.FeedbackParameter_Bias.argtypes = [POINTER(c_double), c_uint];

cdll.VistaScanScripting.FeedbackParameter_AmplitudeSetpoint.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.FeedbackParameter_AmplitudeKi.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.FeedbackParameter_AmplitudeKp.argtypes = [POINTER(c_double), c_uint];

cdll.VistaScanScripting.FeedbackParameter_FrequencySetpoint.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.FeedbackParameter_FrequencyKp.argtypes = [POINTER(c_double), c_uint];

cdll.VistaScanScripting.Head_Position.argtypes = [POINTER(c_double), c_uint];

cdll.VistaScanScripting.Laser_StartSweep.argtypes = [];
cdll.VistaScanScripting.Laser_CurrentSpectrum.argtypes = [POINTER(c_pixelSpectrum), POINTER(c_uint), c_uint];
cdll.VistaScanScripting.Laser_IsSweeping.argtypes = [POINTER(c_bool), c_uint];

cdll.VistaScanScripting.Camera_Resolution.argtypes = [c_uint, POINTER(c_uint), POINTER(c_uint), c_uint];
cdll.VistaScanScripting.Camera_ImageFormat.argtypes = [c_uint, POINTER(c_uint), POINTER(c_uint), c_uint];
cdll.VistaScanScripting.Camera_CurrentImageData.argtypes = [c_uint, POINTER(c_double), POINTER(c_uint), c_uint];

cdll.VistaScanScripting.LaserController1_Frequency.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.LaserController1_ZeroPhase.argtypes = [];
cdll.VistaScanScripting.LaserController2_Frequency.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.LaserController2_ZeroPhase.argtypes = [];

cdll.VistaScanScripting.Lockin_Input.argtypes = [c_int, POINTER(c_int), c_uint];

cdll.VistaScanScripting.PiFMTuner_SweepCenter.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.PiFMTuner_SweepWidth.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.PiFMTuner_StartSweep.argtypes = [];
cdll.VistaScanScripting.PiFMTuner_IsSweeping.argtypes = [POINTER(c_bool), c_uint];
cdll.VistaScanScripting.PiFMTuner_CurrentSpectrum.argtypes = [POINTER(c_pixelSpectrum), POINTER(c_uint), c_uint];

cdll.VistaScanScripting.Polarizer_Position.argtypes = [POINTER(c_double), c_uint];

cdll.VistaScanScripting.TipParameter_DriveFrequency1.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.TipParameter_DriveAmplitude1.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.TipParameter_Frequency2.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.TipParameter_DriveAmplitude2.argtypes = [POINTER(c_double), c_uint];

cdll.VistaScanScripting.Tip_SweepFrequencies.argtypes = [];
cdll.VistaScanScripting.Tip_AutoSetDriveFrequency.argtypes = [];
cdll.VistaScanScripting.Tip_ModeFrequency1.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.Tip_ModeFrequency2.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.Tip_Retract.argtypes = [];
cdll.VistaScanScripting.Tip_Release.argtypes = [];
cdll.VistaScanScripting.Tip_Approach.argtypes = [c_uint];

cdll.VistaScanScripting.TipTiltX.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.TipTiltY.argtypes = [POINTER(c_double), c_uint];

cdll.VistaScanScripting.Channel_Value.argtypes = [c_int, POINTER(c_double), c_uint];
cdll.VistaScanScripting.Channel_ImageData.argtypes = [c_int, c_uint, c_uint, POINTER(c_double), POINTER(c_uint), c_uint];

cdll.VistaScanScripting.Slipstick_Voltage.argtypes = [c_uint, POINTER(c_double), c_uint];

cdll.VistaScanScripting.Spectrometer_ExposureTime.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.Spectrometer_CurrentImageData.argtypes = [POINTER(c_pixelSpectrum), POINTER(c_uint), c_uint];

cdll.VistaScanScripting.SpectrumParameter_Time.argtypes = [POINTER(c_double), c_uint];
cdll.VistaScanScripting.SpectrumParameter_Repeat.argtypes = [POINTER(c_bool), c_uint];
cdll.VistaScanScripting.SpectrumParameter_RepeatCount.argtypes = [POINTER(c_uint), c_uint];

cdll.VistaScanScripting.Test_Run.argtypes = [c_char_p, c_char_p];

cdll.VistaScanScripting.TunableLaser_PowerState.argtypes = [c_uint, POINTER(c_uint), c_uint];
cdll.VistaScanScripting.TunableLaser_Wavenumber.argtypes = [c_uint, POINTER(c_double), c_uint];
cdll.VistaScanScripting.TunableLaser_Wavelength.argtypes = [c_uint, POINTER(c_double), c_uint];

cdll.VistaScanScripting.RegisterForEvent.argtypes = [c_char_p];
cdll.VistaScanScripting.UnregisterForEvent.argtypes = [c_char_p];
cdll.VistaScanScripting.WaitForNextEvent.argtypes = [c_uint, POINTER(POINTER(SCRIPTING_Event))];

def MessageFromError(error):
    lookupErrors = {
        SCRIPTING_ERROR_GENERIC                      : 'Generic error',
        SCRIPTING_ERROR_ALREADYCONNECTED             : 'Already connected',
        SCRIPTING_ERROR_COMMANDNOTFOUND              : 'Command not found',
        SCRIPTING_ERROR_TIMEOUT                      : 'Timeout',
        SCRIPTING_ERROR_NOTCONNECTED                 : 'Not connected',
        SCRIPTING_ERROR_OUTOFRESOURCES               : 'Out of resources',
        SCRIPTING_ERROR_INVALIDPARAMETER             : 'Invalid parameter',
        SCRIPTING_ERROR_INVALIDRESPONSE              : 'Invalid response',
        SCRIPTING_ERROR_FAILED                       : 'Failed',
        SCRIPTING_ERROR_NOTIMPLEMENTED               : 'Not implemented',
        SCRIPTING_ERROR_NOTALLOWEDNOW                : 'Not allowed now',
        SCRIPTING_ERROR_DATASIZEMISMATCH             : 'Data size mismatch',
        SCRIPTING_ERROR_NOTENOUGHSPACE               : 'Buffer is not big enough',
        SCRIPTING_ERROR_INCOMPATIBLE                 : 'DLL version is incompatible with current Vistascan'
    }
    return lookupErrors.get(error, str(error));
    
def Connect():
    result = dllVSScripting.Connect();
    if (result <= 0):
        raise Exception('failed to connect: ' + MessageFromError(result));

def Disconnect():
    return dllVSScripting.Disconnect();


def UserMessage(message, listButtons, buttonDefault):
    messageC = message.encode('utf-8');
    strButtons = ';'.join(listButtons);
    strButtonsC = strButtons.encode('utf-8');

    indexDefault = -1;
    for indexTest in range(0, len(listButtons)):
        if (buttonDefault == listButtons[indexTest]):
            indexDefault = indexTest;
            break;
    indexC = c_uint(indexDefault);

    result = dllVSScripting.UserMessage(messageC, strButtonsC, byref(indexC));
    if (result <= 0):
        raise Exception('UserMessage() failed: ' + MessageFromError(result));

    if ((indexC.value < 0) or (indexC.value >= len(listButtons))):
        buttonSelected = '';
    else:
        buttonSelected = listButtons[indexC.value];
    return buttonSelected;


def SaveCurrentScanData():
    result = dllVSScripting.ImageData_SaveCurrentData();
    if (result <= 0):
        raise Exception('SaveCurrentScanData() failed: ' + str(result));

def GetSaveDirectory():
    pathC = create_string_buffer(MAX_PATH + 1);
    countC = c_uint(len(pathC));
    result = dllVSScripting.ImageData_SavePath(pathC, byref(countC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetSaveDirectory() failed: ' + str(result));
    return pathC.value.decode('utf-8');

def GetMostRecentSaveFilename():
    nameFileC = create_string_buffer(MAX_PATH + 1);
    countC = c_uint(len(nameFileC));
    result = dllVSScripting.ImageData_Filename(nameFileC, byref(countC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetMostRecentSaveFilename() failed: ' + str(result));
    return nameFileC.value.decode('utf-8');

def SetSaveDirectoryAndFilename(path, filename):
    pathC = path.encode('utf-8');
    lenPathC = c_uint(len(pathC));
    filenameC = filename.encode('utf-8');
    lenFilenameC = c_uint(len(filenameC));
    result = dllVSScripting.ImageData_SavePath(pathC, byref(lenPathC), c_uint(SCRIPTING_VALUE_SET));
    if (result <= 0):
        raise Exception('SetSaveDirectoryAndFilename() failed: ' + str(result));
    else:
        result = dllVSScripting.ImageData_Filename(filenameC, byref(lenFilenameC), c_uint(SCRIPTING_VALUE_SET));
        if (result <= 0):
            raise Exception('SetSaveDirectoryAndFilename() failed: ' + str(result));
    return result;


def GetScanParameter_Speed():
    speedScanC = c_double();
    result = dllVSScripting.ScanParameter_LinesPerSecond(byref(speedScanC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetScanParameter_Speed() failed: ' + MessageFromError(result));
    return speedScanC.value;

def SetScanParameter_Speed(speedScan):
    speedScanC = c_double(speedScan);
    result = dllVSScripting.ScanParameter_LinesPerSecond(byref(speedScanC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetScanParameter_Speed() failed: ' + MessageFromError(result));
    return speedScanC.value;

def GetScanParameter_Area():
    xCenterC = c_double();
    yCenterC = c_double();
    widthC = c_double();
    result = dllVSScripting.ScanParameter_Area(byref(xCenterC), byref(yCenterC), byref(widthC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetScanParameter_Area() failed: ' + MessageFromError(result));
    return {'centerX': xCenterC.value, 'centerY': yCenterC.value, 'width': widthC.value};

def SetScanParameter_Area(areaScan):
    xCenterC = c_double(areaScan['centerX']);
    yCenterC = c_double(areaScan['centerY']);
    widthC = c_double(areaScan['width']);
    result = dllVSScripting.ScanParameter_Area(byref(xCenterC), byref(yCenterC), byref(widthC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetScanParameter_Area() failed: ' + MessageFromError(result));
    return {'centerX': xCenterC.value, 'centerY': yCenterC.value, 'width': widthC.value};

def GetTipParameter_DriveFrequency1():
    frequencyDriveC = c_double();
    result = dllVSScripting.TipParameter_DriveFrequency1(byref(frequencyDriveC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetTipParameter_DriveFrequency1() failed: ' + MessageFromError(result));
    return frequencyDriveC.value;

def SetTipParameter_DriveFrequency1(frequencyDrive):
    frequencyDriveC = c_double(frequencyDrive);
    result = dllVSScripting.TipParameter_DriveFrequency1(byref(frequencyDriveC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetTipParameter_DriveFrequency1() failed: ' + MessageFromError(result));
    return frequencyDriveC.value;

def GetTipParameter_Frequency2():
    frequencyC = c_double();
    result = dllVSScripting.TipParameter_Frequency2(byref(frequencyC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetTipParameter_Frequency2() failed: ' + MessageFromError(result));
    return frequencyC.value;

def SetTipParameter_Frequency2(frequency):
    frequencyC = c_double(frequency);
    result = dllVSScripting.TipParameter_Frequency2(byref(frequencyC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetTipParameter_Frequency2() failed: ' + MessageFromError(result));
    return frequencyC.value;

def GetTipParameter_DriveAmplitude1():
    amplitudeDriveC = c_double();
    result = dllVSScripting.TipParameter_DriveAmplitude1(byref(amplitudeDriveC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetTipParameter_DriveAmplitude1() failed: ' + MessageFromError(result));
    return amplitudeDriveC.value;

def SetTipParameter_DriveAmplitude1(amplitudeDrive):
    amplitudeDriveC = c_double(amplitudeDrive);
    result = dllVSScripting.TipParameter_DriveAmplitude1(byref(amplitudeDriveC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetTipParameter_DriveAmplitude1() failed: ' + MessageFromError(result));
    return amplitudeDriveC.value;

def GetTipParameter_DriveAmplitude2():
    amplitudeDriveC = c_double();
    result = dllVSScripting.TipParameter_DriveAmplitude2(byref(amplitudeDriveC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetTipParameter_DriveAmplitude2() failed: ' + MessageFromError(result));
    return amplitudeDriveC.value;

def SetTipParameter_DriveAmplitude2(amplitudeDrive):
    amplitudeDriveC = c_double(amplitudeDrive);
    result = dllVSScripting.TipParameter_DriveAmplitude2(byref(amplitudeDriveC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetTipParameter_DriveAmplitude2() failed: ' + MessageFromError(result));
    return amplitudeDriveC.value;


def GetHeadPosition():
    positionC = c_double()
    result = dllVSScripting.Head_Position(byref(positionC), c_int(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetHeadPosition() failed: ' + MessageFromError(result));
    return positionC.value;

def MoveHeadToPosition(position):
    positionC = c_double(position)
    result = dllVSScripting.Head_Position(byref(positionC), c_int(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('MoveHeadToPosition() failed: ' + MessageFromError(result));
    return positionC.value;

def RetractTip():
    result = dllVSScripting.Tip_Retract();
    if (result <= 0):
        raise Exception('RetractTip() failed: ' + MessageFromError(result));

def ReleaseTip():
    result = dllVSScripting.Tip_Release();
    if (result <= 0):
        raise Exception('ReleaseTip() failed: ' + MessageFromError(result));

def ApproachTipSlow():
    result = dllVSScripting.Tip_Approach(c_uint(APPROACH_SLOW));
    if (result <= 0):
        raise Exception('ApproachTipSlow() failed: ' + MessageFromError(result));

def ApproachTipFast():
    result = dllVSScripting.Tip_Approach(c_uint(APPROACH_FAST));
    if (result <= 0):
        raise Exception('ApproachTipFast() failed: ' + MessageFromError(result));

def GetTipFrequency1():
    frequencyC = c_double();
    result = dllVSScripting.Tip_ModeFrequency1(byref(frequencyC), c_int(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetTipFrequency1() failed: ' + MessageFromError(result));
    return frequencyC.value;

def GetTipFrequency2():
    frequencyC = c_double();
    result = dllVSScripting.Tip_ModeFrequency2(byref(frequencyC), c_int(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetTipFrequency2() failed: ' + MessageFromError(result));
    return frequencyC.value;

def SweepTipFrequencies():
    result = dllVSScripting.Tip_SweepFrequencies();
    if (result <= 0):
        raise Exception('SweepTipFrequencies() failed: ' + MessageFromError(result));

def AutoSetDriveFrequency():
    result = dllVSScripting.Tip_AutoSetDriveFrequency();
    if (result <= 0):
        raise Exception('AutoSetDriveFrequency() failed: ' + MessageFromError(result));

def IsScannerScanning():
    bIsScanning = c_bool();
    result = dllVSScripting.Scanner_IsScanning(byref(bIsScanning), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('IsScannerScanning() failed: ' + MessageFromError(result));
    return bIsScanning.value;

#Scanner coordinates match those used on the 'Approach/Scan' tab.
#The center of the scannable area is (0, 0).
def GetScannerPosition():
    xC = c_double();
    yC = c_double();
    result = dllVSScripting.Scanner_Position(byref(xC), byref(yC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetScannerPosition() failed: ' + MessageFromError(result));
    return {'x': xC.value, 'y': yC.value};

def SetScannerPosition(point):
    xC = c_double(point['x']);
    yC = c_double(point['y']);
    result = dllVSScripting.Scanner_Position(byref(xC), byref(yC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetScannerPosition() failed: ' + MessageFromError(result));
    return {'x': xC.value, 'y': yC.value};

def StartScan():
    result = dllVSScripting.Scanner_StartScan();
    if (result <= 0):
        raise Exception('StartScan() failed: ' + MessageFromError(result));

def StartInteractiveScan():
    result = dllVSScripting.Scanner_StartInteractiveScan();
    if (result <= 0):
        raise Exception('StartInteractiveScan() failed: ' + MessageFromError(result));

def InteractiveScan_NotifyDoneWithPixel():
    result = dllVSScripting.Scanner_InteractiveScan_DoneRecordingPixel();
    if (result <= 0):
        raise Exception('InteractiveScan_NotifyDoneWithPixel() failed: ' + MessageFromError(result));

def StopScan():
    result = dllVSScripting.Scanner_StopScan();
    if (result <= 0):
        raise Exception('StopScan() failed: ' + MessageFromError(result));

def GetScanParameter_LineScanDirections():
    directionsC = c_uint();
    result = dllVSScripting.ScanParameter_LineScanDirections(byref(directionsC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetScanParameter_LineScanDirections() failed: ' + MessageFromError(result));
    return directionsC.value; #TODO: Return a set?

def SetScanParameter_LineScanDirections(directions): #TODO: Receive a set?
    directionsC = c_uint(directions);
    result = dllVSScripting.ScanParameter_LineScanDirections(byref(directionsC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetScanParameter_LineScanDirections() failed: ' + MessageFromError(result));
    return directionsC.value; #TODO: Return a set?

def GetScanParameter_Angle():
    angleC = c_double();
    result = dllVSScripting.ScanParameter_Angle(byref(angleC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetScanParameter_Angle() failed: ' + MessageFromError(result));
    return angleC.value;

def SetScanParameter_Angle(angle):
    angleC = c_double(angle);
    result = dllVSScripting.ScanParameter_Angle(byref(angleC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetScanParameter_Angle() failed: ' + MessageFromError(result));
    return angleC.value;

def GetScanParameter_LoopMode():
    modeLoopC = c_uint();
    result = dllVSScripting.ScanParameter_LoopMode(byref(modeLoopC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetScanParameter_LoopMode() failed: ' + MessageFromError(result));
    return modeLoopC.value;

def SetScanParameter_LoopMode(modeLoop):
    modeLoopC = c_uint(modeLoop);
    result = dllVSScripting.ScanParameter_LoopMode(byref(modeLoopC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetScanParameter_LoopMode() failed: ' + MessageFromError(result));
    return modeLoopC.value;

def GetScanParameter_Resolution():
    resolutionC = c_uint();
    result = dllVSScripting.ScanParameter_Resolution(byref(resolutionC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetScanParameter_Resolution() failed: ' + MessageFromError(result));
    return resolutionC.value;

def SetScanParameter_Resolution(resolution):
    resolutionC = c_uint(resolution);
    result = dllVSScripting.ScanParameter_Resolution(byref(resolutionC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetScanParameter_Resolution() failed: ' + MessageFromError(result));
    return resolutionC.value;


def GetFeedbackMode():
    modeC = c_int();
    result = dllVSScripting.FeedbackParameter_FeedbackMode(byref(modeC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackMode() failed: ' + MessageFromError(result));
    return modeC.value;

def SetFeedbackMode(mode):
    modeC = c_int(mode);
    result = dllVSScripting.FeedbackParameter_FeedbackMode(byref(modeC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackMode() failed: ' + MessageFromError(result));
    return modeC.value;


def GetFeedbackParameter_SetPoint():
    setpointC = c_double();
    result = dllVSScripting.FeedbackParameter_Setpoint(byref(setpointC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackParameter_Setpoint() failed: ' + MessageFromError(result));
    return setpointC.value;

def SetFeedbackParameter_SetPoint(setpoint):
    setpointC = c_double(setpoint);
    result = dllVSScripting.FeedbackParameter_Setpoint(byref(setpointC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackParameter_Setpoint() failed: ' + MessageFromError(result));
    return setpointC.value;

def GetFeedbackParameter_Ki():
    kiC = c_double();
    result = dllVSScripting.FeedbackParameter_Ki(byref(kiC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackParameter_Ki() failed: ' + MessageFromError(result));
    return kiC.value;

def SetFeedbackParameter_Ki(ki):
    kiC = c_double(ki);1
    result = dllVSScripting.FeedbackParameter_Ki(byref(kiC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackParameter_Ki() failed: ' + MessageFromError(result));
    return kiC.value;

def GetFeedbackParameter_Kp():
    kpC = c_double();
    result = dllVSScripting.FeedbackParameter_Kp(byref(kpC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackParameter_Kp() failed: ' + MessageFromError(result));
    return kpC.value;

def SetFeedbackParameter_Kp(kp):
    kpC = c_double(kp);
    result = dllVSScripting.FeedbackParameter_Kp(byref(kpC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackParameter_Kp() failed: ' + MessageFromError(result));
    return kpC.value;

def GetFeedbackParameter_Bias():
    biasC = c_double();
    result = dllVSScripting.FeedbackParameter_Bias(byref(biasC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackParameter_Bias() failed: ' + MessageFromError(result));
    return biasC.value;

def SetFeedbackParameter_Bias(bias):
    biasC = c_double(bias);
    result = dllVSScripting.FeedbackParameter_Bias(byref(biasC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackParameter_Bias() failed: ' + MessageFromError(result));
    return biasC.value;

def GetFeedbackParameter_AmplitudeSetPoint():
    setpointC = c_double();
    result = dllVSScripting.FeedbackParameter_AmplitudeSetpoint(byref(setpointC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackParameter_AmplitudeSetpoint() failed: ' + MessageFromError(result));
    return setpointC.value;

def SetFeedbackParameter_AmplitudeSetPoint(setpoint):
    setpointC = c_double(setpoint);
    result = dllVSScripting.FeedbackParameter_AmplitudeSetpoint(byref(setpointC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackParameter_AmplitudeSetpoint() failed: ' + MessageFromError(result));
    return setpointC.value;

def GetFeedbackParameter_AmplitudeKi():
    kiC = c_double();
    result = dllVSScripting.FeedbackParameter_AmplitudeKi(byref(kiC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackParameter_AmplitudeKi() failed: ' + MessageFromError(result));
    return kiC.value;

def SetFeedbackParameter_AmplitudeKi(ki):
    kiC = c_double(ki);
    result = dllVSScripting.FeedbackParameter_AmplitudeKi(byref(kiC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackParameter_AmplitudeKi() failed: ' + MessageFromError(result));
    return kiC.value;

def GetFeedbackParameter_AmplitudeKp():
    kpC = c_double();
    result = dllVSScripting.FeedbackParameter_AmplitudeKp(byref(kpC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackParameter_AmplitudeKp() failed: ' + MessageFromError(result));
    return kpC.value;

def SetFeedbackParameter_AmplitudeKp(kp):
    kpC = c_double(kp);
    result = dllVSScripting.FeedbackParameter_AmplitudeKp(byref(kpC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackParameter_AmplitudeKp() failed: ' + MessageFromError(result));
    return kpC.value;

def GetFeedbackParameter_FrequencySetPoint():
    setpointC = c_double();
    result = dllVSScripting.FeedbackParameter_FrequencySetpoint(byref(setpointC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackParameter_FrequencySetpoint() failed: ' + MessageFromError(result));
    return setpointC.value;

def SetFeedbackParameter_FrequencySetPoint(setpoint):
    setpointC = c_double(setpoint);
    result = dllVSScripting.FeedbackParameter_FrequencySetpoint(byref(setpointC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackParameter_FrequencySetpoint() failed: ' + MessageFromError(result));
    return setpointC.value;

def GetFeedbackParameter_FrequencyKp():
    kpC = c_double();
    result = dllVSScripting.FeedbackParameter_FrequencyKp(byref(kpC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetFeedbackParameter_FrequencyKp() failed: ' + MessageFromError(result));
    return kpC.value;

def SetFeedbackParameter_FrequencyKp(kp):
    kpC = c_double(kp);
    result = dllVSScripting.FeedbackParameter_FrequencyKp(byref(kpC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetFeedbackParameter_FrequencyKp() failed: ' + MessageFromError(result));
    return kpC.value;

def LaserController1_ZeroPhase():
    result = dllVSScripting.LaserController1_ZeroPhase();
    if (result <= 0):
        raise Exception('LaserController1_ZeroPhase() failed: ' + MessageFromError(result));

def LaserController2_ZeroPhase():
    result = dllVSScripting.LaserController1_ZeroPhase();
    if (result <= 0):
        raise Exception('LaserController1_ZeroPhase() failed: ' + MessageFromError(result));

def GetLaserController1_Frequency():
    freqC = c_double();
    result = dllVSScripting.LaserController1_Frequency(byref(freqC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetLaserController1_Frequency() failed: ' + MessageFromError(result));
    return freqC.value;

def SetLaserController1_Frequency(freq):
    freqC = c_double(freq);
    result = dllVSScripting.LaserController1_Frequency(byref(freqC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetLaserController1_Frequency() failed: ' + MessageFromError(result));
    return freqC.value;

def GetLaserController2_Frequency():
    freqC = c_double();
    result = dllVSScripting.LaserController2_Frequency(byref(freqC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetLaserController2_Frequency() failed: ' + MessageFromError(result));
    return freqC.value;

def SetLaserController2_Frequency(freq):
    freqC = c_double(freq);
    result = dllVSScripting.LaserController2_Frequency(byref(freqC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetLaserController2_Frequency() failed: ' + MessageFromError(result));
    return freqC.value;

def GetPolarizerPosition():
    positionC = c_double();
    result = dllVSScripting.Polarizer_Position(byref(positionC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetPolarizerPosition() failed: ' + MessageFromError(result));
    return positionC.value;
   
def SetPolarizerPosition(position):
    positionC = c_double(position);
    result = dllVSScripting.Polarizer_Position(byref(positionC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetPolarizerPosition() failed: ' + MessageFromError(result));
    return positionC.value;

def GetLockin_Input(indexLockin):
    inputC = c_int();
    result = dllVSScripting.Lockin_Input(c_int(indexLockin), byref(inputC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetLockin_Input() failed: ' + MessageFromError(result));
    return inputC.value;

def SetLockin_Input(indexLockin, idInput):
    inputC = c_int(idInput);
    result = dllVSScripting.Lockin_Input(c_int(indexLockin), byref(inputC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetLockin_Input() failed: ' + MessageFromError(result));
    return inputC.value;

def SetSlipstickX(value):
    valueC = c_double(value);
    result = dllVSScripting.Slipstick_Voltage(c_uint(0), byref(valueC), c_uint(SCRIPTING_VALUE_SET));
    if (result <= 0):
        raise Exception('SetSlipstickX() failed: ' + MessageFromError(result));
    return valueC.value;

def SetSlipstickY(value):
    valueC = c_double(value);
    result = dllVSScripting.Slipstick_Voltage(c_uint(1), byref(valueC), c_uint(SCRIPTING_VALUE_SET));
    if (result <= 0):
        raise Exception('SetSlipstickY() failed: ' + MessageFromError(result));
    return valueC.value;

def SetSlipstickZ(value):
    valueC = c_double(value);
    result = dllVSScripting.Slipstick_Voltage(c_uint(2), byref(valueC), c_uint(SCRIPTING_VALUE_SET));
    if (result <= 0):
        raise Exception('SetSlipstickZ() failed: ' + MessageFromError(result));
    return valueC.value;

def SetTipTiltX(value):
    valueC = c_double(value);
    result = dllVSScripting.TipTiltX(byref(valueC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetTipTiltX() failed: ' + MessageFromError(result));
    return valueC.value;

def SetTipTiltY(value):
    valueC = c_double(value);
    result = dllVSScripting.TipTiltY(byref(valueC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetTipTiltY() failed: ' + MessageFromError(result));
    return valueC.value;

def GetTipTiltX():
    valueC = c_double();
    result = dllVSScripting.TipTiltX(byref(valueC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetTipTiltX() failed: ' + MessageFromError(result));
    return valueC.value;

def GetTipTiltY():
    valueC = c_double();
    result = dllVSScripting.TipTiltY(byref(valueC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetTipTiltY() failed: ' + MessageFromError(result));
    return valueC.value;

def WriteChannel(idChannel, value):
    valueC = c_double(value);
    result = dllVSScripting.Channel_Value(c_int(idChannel), byref(valueC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('WriteChannel() failed: ' + MessageFromError(result));
    return valueC.value;

def ReadChannel(idChannel):
    valueC = c_double();
    result = dllVSScripting.Channel_Value(c_int(idChannel), byref(valueC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetChannel() failed: ' + MessageFromError(result));
    return valueC.value;

def GetImageData(idChannel, indexRow, direction):
    countPixels = GetScanParameter_Resolution();
    valuesC = (c_double * countPixels)();
    valueCountC = c_uint32(countPixels);
    result = dllVSScripting.Channel_ImageData(c_int(idChannel), c_uint(indexRow), c_uint(direction), byref(valuesC), byref(valueCountC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetImageData() failed: ' + MessageFromError(result));
    listValues = [];
    for i in range(0, valueCountC.value):
        listValues.append(valuesC[i]);
    return listValues;


def IsLaserSweeping():
    bIsSweeping = c_bool();
    result = dllVSScripting.Laser_IsSweeping(byref(bIsSweeping), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('IsLaserSweeping() failed: ' + MessageFromError(result));
    return bIsSweeping.value;

def StartLaserSweep():
    return dllVSScripting.Laser_StartSweep();
    
def GetLaserSpectrum():
    countPixels = 2200;
    spectrumC = (c_pixelSpectrum * countPixels)();
    valueCountReadingsC = c_uint32(countPixels);
    result = dllVSScripting.Laser_CurrentSpectrum(byref(spectrumC), byref(valueCountReadingsC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetLaserSpectrum() failed: ' + MessageFromError(result));
    spectrum = [];
    for i in range(0, valueCountReadingsC.value):
        spectrum.append({'wavelength': spectrumC[i].wavelength, 'intensity': spectrumC[i].intensity});
    return spectrum;

def GetCameraImageData(idCamera):
    widthC = c_uint();
    heightC = c_uint();
    result = dllVSScripting.Camera_Resolution(c_uint(idCamera), byref(widthC), byref(heightC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetCameraImageData() failed: ' + MessageFromError(result));

    pixelsC = c_uint();
    bytesPerReadingC = c_uint();
    result = dllVSScripting.Camera_ImageFormat(c_uint(idCamera), byref(pixelsC), byref(bytesPerReadingC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetCameraImageData() failed: ' + MessageFromError(result));

    countReadings = widthC.value * heightC.value;
    dataC = (c_double * countReadings)();
    valueCountReadingsC = c_uint32(countReadings);
    result = dllVSScripting.Camera_CurrentImageData(c_uint(idCamera), byref(dataC), byref(valueCountReadingsC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetCameraImageData() failed: ' + MessageFromError(result));

    dataImage = {'width': widthC.value, 'height': heightC.value};
    dataImage['values'] = [];
    for i in range(0, valueCountReadingsC.value):
        dataImage['values'].append(dataC[i]);
    return dataImage;

def SetSpectrometerExposureTime(exposure):
    exposureC = c_double(exposure);
    result = dllVSScripting.Spectrometer_ExposureTime(byref(exposureC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetSpectrometerExposureTime() failed: ' + MessageFromError(result));
    return exposureC.value;

def GetSpectrometerExposureTime():
    exposureC = c_double();
    result = dllVSScripting.Spectrometer_ExposureTime(byref(exposureC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetSpectrometerExposureTime() failed: ' + MessageFromError(result));
    return exposureC.value;

def GetSpectrometerSpectrum():
    countPixels = 2048; #GetSpectrometerResolution();
    spectrumC = (c_pixelSpectrum * countPixels)();
    valueCountReadingsC = c_uint32(countPixels);
    result = dllVSScripting.Spectrometer_CurrentImageData(byref(spectrumC), byref(valueCountReadingsC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetSpectrometerSpectrum() failed: ' + MessageFromError(result));
    spectrum = [];
    for i in range(0, valueCountReadingsC.value):
        spectrum.append({'wavelength': spectrumC[i].wavelength, 'intensity': spectrumC[i].intensity});
    return spectrum;

def GetLaserPowerstate(indexController):
    powerC = c_uint();
    result = dllVSScripting.TunableLaser_PowerState(c_uint(indexController), byref(powerC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetLaserPowerstate() failed: ' + MessageFromError(result));
    return powerC.value;

def SetLaserPowerstate(indexController, powerstate):
    powerC = c_uint(powerstate);
    result = dllVSScripting.TunableLaser_PowerState(c_uint(indexController), byref(powerC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetLaserPowerstate() failed: ' + MessageFromError(result));
    return powerC.value;

def GetLaserWavenumber(indexController):
    wavenumberC = c_double();
    result = dllVSScripting.TunableLaser_Wavenumber(c_uint(indexController), byref(wavenumberC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetLaserWavenumber() failed: ' + MessageFromError(result));
    return wavenumberC.value;

def SetLaserWavenumber(indexController, wavenumber):
    wavenumberC = c_double(wavenumber);
    result = dllVSScripting.TunableLaser_Wavenumber(c_uint(indexController), byref(wavenumberC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetLaserWavenumber() failed: ' + MessageFromError(result));
    return wavenumberC.value;

def GetLaserWavelength(indexController):
    wavelengthC = c_double();
    result = dllVSScripting.TunableLaser_Wavelength(c_uint(indexController), byref(wavelengthC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetLaserWavelength() failed: ' + MessageFromError(result));
    return wavelengthC.value;

def SetLaserWavelength(indexController, wavelength):
    wavelengthC = c_double(wavelength);
    result = dllVSScripting.TunableLaser_Wavelength(c_uint(indexController), byref(wavelengthC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetLaserWavelength() failed: ' + MessageFromError(result));
    return wavelengthC.value;

def GetPiFMTunerSweepCenter():
    frequencyC = c_double();
    result = dllVSScripting.PiFMTuner_SweepCenter(byref(frequencyC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetPiFMTunerSweepCenter() failed: ' + MessageFromError(result));
    return frequencyC.value;

def SetPiFMTunerSweepCenter(frequencyCenter):
    frequencyC = c_double(frequencyCenter);
    result = dllVSScripting.PiFMTuner_SweepCenter(byref(frequencyC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetPiFMTunerSweepCenter() failed: ' + MessageFromError(result));
    return frequencyC.value;

def GetPiFMTunerSweepWidth():
    dFrequenciesC = c_double();
    result = dllVSScripting.PiFMTuner_SweepWidth(byref(dFrequenciesC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetPiFMTunerSweepWidth() failed: ' + MessageFromError(result));
    return dFrequenciesC.value;

def SetPiFMTunerSweepWidth(widthFrequencies):
    dFrequenciesC = c_double(widthFrequencies);
    result = dllVSScripting.PiFMTuner_SweepWidth(byref(dFrequenciesC), c_uint(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetPiFMTunerSweepWidth() failed: ' + MessageFromError(result));
    return dFrequenciesC.value;

def StartPiFMSweep():
    return dllVSScripting.PiFMTuner_StartSweep();

def IsPiFMSweeping():
    bIsSweeping = c_bool();
    result = dllVSScripting.PiFMTuner_IsSweeping(byref(bIsSweeping), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('IsPiFMSweeping() failed: ' + MessageFromError(result));
    return bIsSweeping.value;

def GetPiFMSpectrum():
    countPixels = 1024;
    spectrumC = (c_pixelSpectrum * countPixels)();
    valueCountReadingsC = c_uint32(countPixels);
    result = dllVSScripting.PiFMTuner_CurrentSpectrum(byref(spectrumC), byref(valueCountReadingsC), c_uint(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetPiFMSpectrum() failed: ' + MessageFromError(result));
    spectrum = [];
    for i in range(0, valueCountReadingsC.value):
        spectrum.append({'frequency': spectrumC[i].wavelength, 'intensity': spectrumC[i].intensity});
    return spectrum;


def GetSpectrumTime():
    timeC = c_double();
    result = dllVSScripting.SpectrumParameter_Time(byref(timeC), c_int(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetSpectrumTime() failed: ' + MessageFromError(result));
    return timeC.value;

def SetSpectrumTime(time):
    timeC = c_double(time);
    result = dllVSScripting.SpectrumParameter_Time(byref(timeC), c_int(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetSpectrumTime() failed: ' + MessageFromError(result));
    return timeC.value;

def GetSpectrumRepeat():
    bRepeatC = c_bool();
    result = dllVSScripting.SpectrumParameter_Repeat(byref(bRepeatC), c_int(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetSpectrumRepeat() failed: ' + MessageFromError(result));
    return bRepeatC.value;

def SetSpectrumRepeat(bRepeat):
    bRepeatC = c_bool(bRepeat);
    result = dllVSScripting.SpectrumParameter_Repeat(byref(bRepeatC), c_int(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetSpectrumRepeat() failed: ' + MessageFromError(result));
    return bRepeatC.value;

def GetSpectrumRepeatCount():
    countC = c_uint();
    result = dllVSScripting.SpectrumParameter_RepeatCount(byref(countC), c_int(SCRIPTING_VALUE_QUERY));
    if (result <= 0):
        raise Exception('GetSpectrumRepeatCount() failed: ' + MessageFromError(result));
    return countC.value;

def SetSpectrumRepeatCount(count):
    countC = c_uint(count);
    result = dllVSScripting.SpectrumParameter_RepeatCount(byref(countC), c_int(SCRIPTING_VALUE_SETANDQUERY));
    if (result <= 0):
        raise Exception('SetSpectrumRepeatCount() failed: ' + MessageFromError(result));
    return countC.value;


def RunTest(title, nameCategory):
    nameCategoryC = nameCategory.encode('utf-8');
    titleC = title.encode('utf-8');
    result = dllVSScripting.Test_Run(titleC, nameCategoryC);
#    if (result <= 0):
#        raise Exception('RunTest() failed: ' + MessageFromError(result));
    return result;

def RegisterForEvent(nameEvent):
    nameEventC = nameEvent.encode('utf-8');
    result = dllVSScripting.RegisterForEvent(nameEventC);
    if (result <= 0):
        raise Exception('RegisterForEvent() failed: ' + MessageFromError(result));
    return result;

def UnregisterForEvent(nameEvent):
    nameEventC = nameEvent.encode('utf-8');
    result = dllVSScripting.UnregisterForEvent(nameEventC);
    if (result <= 0):
        raise Exception('UnregisterForEvent() failed: ' + MessageFromError(result));

def WaitForNextEvent(timeout):
    pEventC = POINTER(SCRIPTING_Event)();
    result = dllVSScripting.WaitForNextEvent(c_uint(timeout), byref(pEventC));
    if (result <= 0):
        if (result == SCRIPTING_ERROR_TIMEOUT):
            return None;
        else:
            raise Exception('WaitForNextEvent() failed: ' + MessageFromError(result));
    eventReturn = {'name': pEventC.contents.pName.decode('utf-8')};
    countBytes = pEventC.contents.countBytes;
    if (eventReturn['name'] == NAME_EVENT_SCAN_ROWCOMPLETE):
        if (countBytes != 4):
            raise Exception('WaitForNextEvent() failed: Struct for '' + NAME_EVENT_SCAN_ROWCOMPLETE + '' is wrong size');
        pEvent = cast(pEventC.contents.pData, POINTER(EventData_Scan_RowComplete));
        eventReturn['row'] = cast(pEventC.contents.pData, POINTER(EventData_Scan_RowComplete)).contents.indexRow;
    elif (eventReturn['name'] == NAME_EVENT_SCAN_STARTPIXEL):
        if (countBytes != 12):
            raise Exception('WaitForNextEvent() failed: Struct for '' + NAME_EVENT_SCAN_STARTPIXEL + '' is wrong size');
        pEvent = cast(pEventC.contents.pData, POINTER(EventData_Scan_StartPixel));
        eventReturn['row'] = pEvent.contents.indexRow;
        eventReturn['col'] = pEvent.contents.indexCol;
        eventReturn['scandirection'] = pEvent.contents.direction;
    return eventReturn;
