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
from matplotlib.widgets import Button
import VistaScan
import time

#Parameters***************************************************************
TakeNewData = True #If True, take image series with VistaScan.
Cutoff = 0.99 #Fraction of values not to use when calculating center
Resolution = 32 #Must set to match resolution of image
NumSlices = 15
ScanSpeed = 10
HalfZRange = 8.3
HalfXRange = 8.3
HalfYRange = 8.3
XSliderRange = 8.3
YSliderRange = 8.3
DataDirectory = "C:/Users/Supervisor/Desktop/Scripts/PMAlignData/AlignPM03/"
PiFMScale = 8/2650000 #Convert amplitude to mV
PhaseScale = 4/39853 #Convert phase to deg

FileName = "AlignPMTest_"
#*************************************************************************

#Functions****************************************************************

#Opens a .int image as a numpy array
def OpenImg( ChannelName, ImgNumber, ImgDirectory, ImgName, Res=Resolution ):
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

        self.im = ax.imshow(self.X[:, :, self.ind], cmap = Color)
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

#Buttons
#Based on example from https://matplotlib.org/gallery/widgets/buttons.html
class ControlButtons():
    ind = 0
#    SaveDir = VistaScan.GetSaveDirectory()

    def Get_Immediate_Subdirectories(a_dir):
        return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

    def GetDir(self, event):
        self.ind += 1
        print("Get Directory button pressed")
        print(VistaScan.GetSaveDirectory())

    def MakeDir(self, event):
        print("Make Directory button pressed")
        NewDir = "D:\\AFM Data\\Customers\\IBM\\Martha Sanchez\\OG322 Photoresist Scum"
        os.mkdir(NewDir)
        
    def ChangeDir(self, event):
        print("Change Directory button pressed")
        NewDir = "D:\\AFM Data\\Customers\\IBM\\Martha Sanchez\\OG322 Photoresist Scum"
        NewFileName = "AlignPMTest_"
        VistaScan.SetSaveDirectoryAndFilename(NewDir, NewFileName)
        
    def ListDirs(self, event):
        print("ListDirs button pressed")
        NewDir = "D:\\AFM Data\\Customers\\IBM\\Martha Sanchez\\OG322 Photoresist Scum"
        print([x[0] for x in os.walk("D:\\AFM Data\\Customers\\IBM\\Martha Sanchez\\OG322 Photoresist Scum")])
        x = [name for name in os.listdir(NewDir) if os.path.isdir(os.path.join(NewDir, name))]
        print(type(x))
        print(len(x))
        print(x[0])
        CurrDir = VistaScan.GetSaveDirectory()
        print(CurrDir)
        CurrDir = os.path.normpath(CurrDir)
        print(CurrDir)
        
        for i in range(len(x)):
            print(x[i])
        

#************************************************************************


#Script******************************************************************


###Initialize the arrays that will store data###
PiFMImgStack = np.zeros((Resolution, Resolution, NumSlices), dtype = float)
PhaseImgStack = np.zeros((Resolution, Resolution, NumSlices), dtype = float)
SpotAmplitudes = np.arange(NumSlices, dtype = float)
PhaseAmplitudes = np.arange(NumSlices, dtype = float)

ZStep = HalfZRange * 2 / (NumSlices - 1) #Size of steps in Z

###Set up VistaScan###
result = VistaScan.Connect()
print('Connect to VistaScan result = ', result)
if TakeNewData == True:
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
    Image = OpenImg("PiFMFwd", step + 1, NewDir, NewFileName) #Open the image
    for y in range(Resolution): #Write to PiFMImgStack
        for x in range (Resolution):
            PiFMImgStack[y, x, step] = Image[y, x] * float(PiFMScale)
    #Get the average intensity of the hotspot
    HighPoints = np.where(Image > Cutoff * np.amax(Image))
    SpotAmplitudes[step] = float(AvgPoints(HighPoints, Image)) * float(PiFMScale)
    #Get the Phase Data
    Image = OpenImg("PhaseFwd", step + 1, NewDir, NewFileName) #Open the image
    for y in range(Resolution): #Write to PhaseImgStack
        for x in range (Resolution):
            PhaseImgStack[y, x, step] = float(Image[y, x]) * float(PhaseScale)
#            print("Image[y, x] is ", float(Image[y, x]))
    HighPoints = np.where(Image > Cutoff * np.amax(Image))
    PhaseAmplitudes[step] = float(AvgPoints(HighPoints, Image)) * float(PhaseScale)
    if step == 27:
        print('Avg value at step 27 is ', AvgPoints(HighPoints, Image))
        print('Multiplied by PhaseScale: ', float(AvgPoints(HighPoints, Image)) * float(PhaseScale))
        print('PhaseAmplitudes[27] is ', PhaseAmplitudes[27])
        print('PhaseImgStack[y, x, step] is ', PhaseImgStack[17, 17, step])


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

plt.subplots_adjust(bottom=0.2)
callback = ControlButtons()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
axnewdir = plt.axes([0.59, 0.05, 0.1, 0.075])
axlistdirs = plt.axes([0.48, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Get Dir')
bnext.on_clicked(callback.GetDir)
bprev = Button(axprev, 'Make Dir')
bprev.on_clicked(callback.MakeDir)
bnewdir = Button(axnewdir, 'Change Dir')
bnewdir.on_clicked(callback.ChangeDir)
blistdirs = Button(axlistdirs, 'List')
blistdirs.on_clicked(callback.ListDirs)

plt.show()

if TakeNewData == True:
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
    Image = OpenImg("PiFMFwd", HighestValImgLoc, NewDir, NewFileName)
    HighPoints = np.where(Image > Cutoff * np.amax(Image))
    Center = FindCenter(HighPoints)
    print('XY Center is ', Center)
    print('Center[0] returns', Center[0])
    #Extra math because scan is currently at 270 deg
    XCenter = (-Center[0] / Resolution) * HalfXRange * 2 + HalfXRange
    YCenter = (-Center[1] / Resolution) * HalfYRange * 2 + HalfYRange
    
    #Move XY to upper left corner
    VistaScan.SetSlipstickX(HalfXRange)            
    time.sleep(0.5) #Just in case
    VistaScan.SetSlipstickY(HalfYRange)
    time.sleep(0.5) #Just in case
    
    #Move Y
    VistaScan.SetSlipstickY(YCenter)
    time.sleep(0.5) #Just in case
    
    #Move X   
    VistaScan.SetSlipstickX(XCenter)

VistaScan.SetSaveDirectoryAndFilename(CurrentDir, CurrentFileName)


#result = VistaScan.Disconnect()
#print('VistaScan disconnect result = ', result)

#***********************************************************************