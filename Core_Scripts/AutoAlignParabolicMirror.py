#! C:\Users\Supervisor\Miniconda3\envs\py34_32\python.exe

# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 12:35:35 2019

@author: Will Morrison
"""
from __future__ import print_function
import os 
import os.path #Do I need this if I already have os?
import numpy as np
import matplotlib.pyplot as plt
import VistaScan
import time

#Parameters***************************************************************
TakeNewData = True #If True, take image series with VistaScan.
Cutoff = 0.99 #Fraction of values not to use when calculating center
NumSlices = 5
ScanSpeed = 10
HalfZRange = 8.3
HalfXRange = 7.527764705882328e-06
HalfYRange = 7.527764705882324e-06
XSliderRange = 8.3
YSliderRange = 8.3
PiFMScale = 8/2650000 #Convert amplitude to mV
PhaseScale = 4/39853 #Convert phase to deg

FileName = "AlignPMTest_"
#*************************************************************************

#Functions****************************************************************

#Get image resolution
def GetImgRes(FilePath): #Takes the path to a .txt image header file
    ImgHeader = open(FilePath, "rt")
    for line in ImgHeader:
        SplitLine = line.split(":")
        if "xPixel" in line:
            return(SplitLine[1])
            ImgHeader.close()
            break

#Opens a .int image as a numpy array
def OpenImg( ChannelName, ImgNumber, ImgDirectory, ImgName, Res):
    ImgFilePath = GetImgFilePath(ChannelName, ImgNumber, ImgDirectory, ImgName)
    print('ImgFilePath is ', ImgFilePath)
    ImgFile = open(ImgFilePath, "r")
    RawImgArray = np.fromfile(ImgFile, dtype=np.int32)
    ImgArray = np.reshape(RawImgArray, (Res, Res))
    ImgFile.close()
    return ImgArray

#Calculate the mean X and Y
def FindCenter( Points ):
    xPos = np.mean(Points[1])
    yPos = np.mean(Points[0])
    return [xPos, yPos]

#Get mean value of a set of points within an image
def AvgPoints( Points, Img ):
    NumPoints = np.size(Points[0])
    PointsVals = np.arange(NumPoints)
    for i in range(0, NumPoints):
        xPix = Points[1][i]
        yPix = Points[0][i]
        PointsVals[i] = Img[yPix, xPix]
        PointsAvg = np.mean(PointsVals)
    return PointsAvg

#Generate the filepath for a .int image
def GetImgFilePath(ChannelName, ImgNumber, Directory, Name): #ImgNumber starts at 1
    if ImgNumber < 10:
        ImgDir = os.path.normpath(Directory + Name + "000" + str(ImgNumber) + ChannelName + ".int")
    elif ImgNumber >= 10:
        ImgDir = os.path.normpath(Directory + Name + "00" + str(ImgNumber) + ChannelName + ".int")
    return ImgDir

#************************************************************************

#Classes*****************************************************************

#Mouse scroll-able plot of the image set
#From https://matplotlib.org/2.1.2/gallery/animation/image_slices_viewer.html
class IndexTracker(object):
    def __init__(self, ax, X, ChannelName, Color = 'viridis'):
        self.ax = ax
        ax.set_title(ChannelName)

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.X[:, :, self.ind], cmap = Color, vmin = np.amin(X), vmax = np.amax(X))
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step), "slice ", self.ind)
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        self.im.axes.figure.canvas.draw()      

#************************************************************************


#Script******************************************************************

###Set up VistaScan###
result = VistaScan.Connect()
print('Connect to VistaScan result = ', result)
Resolution = VistaScan.GetScanParameter_Resolution()
VistaScan.SetScanParameter_Speed(ScanSpeed) #Set scan speed
print('Scan speed set to: ', VistaScan.GetScanParameter_Speed())
CurrentDir = VistaScan.GetSaveDirectory() + "\\"
CurrentFileName = VistaScan.GetMostRecentSaveFilename()
print('Current directory is ', CurrentDir)
NumFolds = [name for name in os.listdir(CurrentDir) if os.path.isdir(os.path.join(CurrentDir, name))]
NewDir = CurrentDir + "PMAlign" + str(len(NumFolds))
os.mkdir(NewDir)
NewDir = NewDir + "\\"
NewFileName = "AlignPMTest_"
VistaScan.SetSaveDirectoryAndFilename(NewDir, NewFileName)
    #Set resolution
    #Set laser pulse duration
    #Record current laser frequency
    #Change laser frequency to first mode

###Initialize the arrays that will store data###
PiFMImgStack = np.zeros((Resolution, Resolution, NumSlices), dtype = float)
PhaseImgStack = np.zeros((Resolution, Resolution, NumSlices), dtype = float)
SpotAmplitudes = np.arange(NumSlices, dtype = float)
PhaseAmplitudes = np.arange(NumSlices, dtype = float)

ZStep = HalfZRange * 2 / (NumSlices - 1) #Size of steps in Z

###Get the Data###
for step in range(NumSlices):
    NewZPos = -HalfZRange + step * ZStep
    if TakeNewData == True: #Check whether to take an image with VistaScan
        VistaScan.SetSlipstickZ(NewZPos)
        time.sleep(0.5) #Wait for the slider to finish moving
        VistaScan.StartScan()
        while VistaScan.IsScannerScanning() == True: #loop to check whether the scan has finished
            time.sleep(0.3) #wait                                    
    print('Finished scan at z = ', NewZPos)
    #Get the PiFM Data
    Image = OpenImg("PiFMFwd", step + 1, NewDir, NewFileName, Resolution) #Open the image
    for y in range(Resolution): #Write to PiFMImgStack
        for x in range (Resolution):
            PiFMImgStack[y, x, step] = Image[y, x] * float(PiFMScale)
    #Get the average intensity of the hotspot
    HighPoints = np.where(Image > Cutoff * np.amax(Image))
    SpotAmplitudes[step] = float(AvgPoints(HighPoints, Image)) * float(PiFMScale)
    #Get the Phase Data
    Image = OpenImg("PhaseFwd", step + 1, NewDir, NewFileName, Resolution) #Open the image
    for y in range(Resolution): #Write to PhaseImgStack
        for x in range (Resolution):
            PhaseImgStack[y, x, step] = float(Image[y, x]) * float(PhaseScale)
    HighPoints = np.where(Image > Cutoff * np.amax(Image))
    PhaseAmplitudes[step] = float(AvgPoints(HighPoints, Image)) * float(PhaseScale)

#Move parabolic mirror to location of max signal
HighestValImgLoc = np.argmax(SpotAmplitudes)
print('Highest value image is at ', HighestValImgLoc)
ZCenter = (HighestValImgLoc / NumSlices) * HalfZRange * 2 - HalfZRange
print('ZCenter = ', ZCenter)
#Set Z position
VistaScan.SetSlipstickZ(-HalfZRange)
time.sleep(0.5)
VistaScan.SetSlipstickZ(ZCenter)
time.sleep(0.5)

#Take a scan at this position so that you can judge the subsequent XY placement
VistaScan.StartScan()
while VistaScan.IsScannerScanning() == True: #loop to check whether the scan has finished
    time.sleep(0.3) #wait    

#Set XY position
#Retrieve the image
Image = OpenImg("PiFMFwd", NumSlices + 1, NewDir, NewFileName, Resolution)
HighPoints = np.where(Image > Cutoff * np.amax(Image))
Center = FindCenter(HighPoints)
print('XY Center is ', Center)
print('Center[0] returns', Center[0])
#Extra math because scan is currently at 270 deg
YCenter = (-Center[0] / Resolution) * HalfXRange * 2 + HalfXRange
XCenter = (-Center[1] / Resolution) * HalfYRange * 2 + HalfYRange
print("XCenter: ", XCenter)
print("YCenter: ", YCenter)

VistaScan.SetScannerPosition({'x': HalfXRange, 'y': HalfYRange})
time.sleep(0.5)
VistaScan.SetScannerPosition({'x': XCenter, 'y': HalfYRange})
time.sleep(0.5)
VistaScan.SetScannerPosition({'x': XCenter, 'y': YCenter})

VistaScan.SetSaveDirectoryAndFilename(CurrentDir, CurrentFileName)

result = VistaScan.Disconnect()
print('VistaScan disconnect result = ', result)

###Generate the plots###

Plots, ax = plt.subplots(nrows=2, ncols=2)

#Phase Images scroll-able plot
Phase_Tracker = IndexTracker(ax[1,0], PhaseImgStack, 'Phase', 'viridis')
Plots.canvas.mpl_connect('scroll_event', Phase_Tracker.onscroll)

#PiFM Images scroll-able plot
PiFM_Tracker = IndexTracker(ax[0,0], PiFMImgStack, 'PiFM', 'nipy_spectral')
Plots.canvas.mpl_connect('scroll_event', PiFM_Tracker.onscroll)

#PiFM Amplitude plot
XAxis = np.arange(NumSlices)
ax[0,1].plot(XAxis, SpotAmplitudes)

#Phase Amplitude plot
ax[1,1].plot(XAxis, PhaseAmplitudes)

plt.show()

#***********************************************************************