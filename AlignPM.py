# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 12:35:35 2019

@author: Will Morrison
"""
from __future__ import print_function
import os.path
import numpy as np
import matplotlib.pyplot as plt
import VistaScan
import time

#Parameters***************************************************************
TakeNewData = True #If True, take image series with VistaScan.
Cutoff = 0.99 #Fraction of values not to use when calculating center
Resolution = 32 #Must set to match resolution of image
ScanSpeed = 0.78
HalfZRange = 8.3
HalfXRange = 8.3
HalfYRange = 8.3
XSliderRange = 8.3
YSliderRange = 8.3
DataDirectory = "C:/Users/Supervisor/Desktop/Scripts/AlignPM_Data/Test32/"
AmpScale = 8/2650000 #Convert amplitude to mV
PhaseScale = 1 #Convert phase to deg

FileName = "AlignPMTest_"
#*************************************************************************

#Functions****************************************************************

#Opens a .int image as a numpy array
def OpenImg( ChannelName, ImgNumber, Res=Resolution ):
    ImgFilePath = GetImgFilePath(ChannelName, ImgNumber)
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
def GetImgFilePath(ChannelName, ImgNumber, Directory = DataDirectory, Name = FileName): #ImgNumber starts at 1
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
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.X[:, :, self.ind])
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()

#************************************************************************


#Script******************************************************************

###Initialize the arrays that will store data###
PiFMImgStack = np.zeros((Resolution, Resolution, Resolution))
PhaseImgStack = np.zeros((Resolution, Resolution, Resolution))
SpotAmplitudes = np.arange(Resolution)

ZStep = HalfZRange * 2 / (Resolution - 1) #Size of steps in Z

###Set up VistaScan###
result = VistaScan.Connect()
print('Connect to VistaScan result = ', result)
if TakeNewData == True:
    VistaScan.SetScanParameter_Speed(ScanSpeed) #Set scan speed
    print('Scan speed set to: ', VistaScan.GetScanParameter_Speed())
    #Set resolution
    #Set laser pulse duration
    #Record current laser frequency
    #Change laser frequency to first mode

###Get the Data###
for step in range(Resolution):
    NewZPos = -HalfZRange + step * ZStep
    if TakeNewData == True: #Check whether to take an image with VistaScan
        VistaScan.SetSlipstickZ(NewZPos)
        VistaScan.StartScan()
        while VistaScan.IsScannerScanning() == True: #loop to check whether the scan has finished
            time.sleep(0.3) #wait                                    
    print('Finished scan at z = ', NewZPos)
    #Get the image's filepath
    Image = OpenImg("PiFMFwd", step + 1) #Open the image
    for y in range(Resolution): #Write to PiFMImgStack
        for x in range (Resolution):
            PiFMImgStack[y, x, step] = Image[y, x]   
    #Get the average intensity of the hotspot
    HighPoints = np.where(Image > Cutoff * np.amax(Image))
    SpotAmplitudes[step] = AvgPoints(HighPoints, Image)

###Generate the plots###
#Amplitudes Plot
plt.figure(47)
XAxis = np.arange(Resolution)
plt.plot(XAxis, SpotAmplitudes)

#PiFM Images scroll-able plot
PiFMScrollPlot, ax = plt.subplots(1, 1)
tracker = IndexTracker(ax, PiFMImgStack)
PiFMScrollPlot.canvas.mpl_connect('scroll_event', tracker.onscroll)

#Phase Images scroll-able plot
#AmpScrollPlot, ax = plt.subplots(1, 1)
#tracker = IndexTracker(ax, PiFMImgStack)
#AmpScrollPlot.canvas.mpl_connect('scroll_event', tracker.onscroll)

plt.show()

#Move parabolic mirror to location of max signal
HighestValImgLoc = np.argmax(SpotAmplitudes)
print('Highest value image is at ', HighestValImgLoc)
ZCenter = (HighestValImgLoc / Resolution) * HalfZRange * 2 - HalfZRange
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
Image = OpenImg("PiFMFwd", HighestValImgLoc)
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


result = VistaScan.Disconnect()
print('VistaScan disconnect result = ', result)

#***********************************************************************