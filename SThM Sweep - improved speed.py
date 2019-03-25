#! C:\Users\Supervisor\Miniconda3\envs\py34_32\python.exe


# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:58:44 2019

@author: Will Morrison
"""

import VistaScan
import time
import numpy as np
import matplotlib.pyplot as plt


EndTemp = 450
StepSize = 30 #mV
NumPoints = 250 #Total number of points to sweep
Resistor = 1000 #Ohms
WaitTime = 0.05 #Time between measurements in seconds
TBLimit = 10 #Amount of T-B change at which to stop the sweep (mV)
ZLimit = 5 #nm Amount that HeadZ is allowed to drop into the sample before we stop the loop.
BiasLimit = 5000

Temp = 29 #Need to initialize for loop
Counter = 0

VistaScan.Connect()
VistaScan.SetFeedbackParameter_Bias(0)
TB = VistaScan.ReadChannel(9)
MinTB = TB - TBLimit

#Initialize the data array
SweepDataArr = np.zeros((NumPoints, 8), dtype = float)

StartTime = time.time()
Z = VistaScan.ReadChannel(-2)
MinZ = Z - ZLimit
#Sweep the temperature and record the data
while Counter < NumPoints and Z > MinZ:
    if (Counter * StepSize) > BiasLimit: #Bias limit
        break
    Bias = Counter * StepSize / 1000 + 0.1
    VistaScan.WriteChannel(65, Bias) #Set the voltage
    ###Calculate the temp etc.###
    VOne = VistaScan.ReadChannel(131) #Aux2
    VTwo = VistaScan.ReadChannel(140) #Aux3
    VResistor = VOne - VTwo
    CurrentTip = VResistor / Resistor * 1000 #in mA
    PowerTip = VTwo * CurrentTip #in mW
    ResistanceTip = VTwo / (CurrentTip / 1000) #in Ohms
    Temp = 1.0612 * PowerTip**6 - 15.533 * PowerTip**5 + 81.12 * PowerTip**4 - 181.66 * PowerTip**3 + 188.11 * PowerTip**2 + 18.443 * PowerTip + 302.59
    Temp = Temp - 273.15
    #############################
    TB = VistaScan.ReadChannel(9)
    Z = VistaScan.ReadChannel(-2)
    
    SweepDataArr[Counter, :] = [Bias, Temp, TB, ResistanceTip, CurrentTip, VTwo, PowerTip, Z]

    Counter += 1
    time.sleep(WaitTime)

EndTime = time.time()
VistaScan.WriteChannel(65, 0)

#SweepDataFile = open("SweepData.txt","w").close() #Clear the file
#SweepDataFile = open("SweepData.txt","w+") #Open the file
#SweepDataFile.close()
print("Loop Time: ", EndTime - StartTime)
print("Total Points: ", Counter)

#Display the data
#SweepDataFile = open("SweepData.txt", "r")
#SweepDataArr = np.loadtxt(SweepDataFile)

Bias = SweepDataArr[:,0]
TB = SweepDataArr[:,2]
Temp = SweepDataArr[:,1]
RTip = SweepDataArr[:,3]
ITip = SweepDataArr[:,4]
VTip = SweepDataArr[:,5]
PTip = SweepDataArr[:,6]
Z = SweepDataArr[:,7]

plt.subplot(3, 2, 1)
plt.plot(Temp, TB, 'ko-')
plt.title('T-B vs. Temp')
plt.xlabel('Temp')
plt.ylabel('T-B')

plt.subplot(3, 2, 2)
plt.plot(Bias, RTip, 'r.-')
plt.title('Resistance of Tip vs. Voltage')
plt.xlabel('Bias')
plt.ylabel('RTip')

plt.subplot(3, 2, 3)
plt.plot(VTip, ITip, 'r.-')
plt.title('I-V Curve for Tip')
plt.xlabel('Voltage Drop Across Tip')
plt.ylabel('Current Through Tip (mA)')

plt.subplot(3, 2, 4)
plt.plot(Bias, PTip, 'r.-')
plt.title('Power vs. Bias')
plt.xlabel('Bias')
plt.ylabel('Power (mW)')

plt.subplot(3, 2, 5)
plt.plot(Temp, Z, 'r.-')
plt.title('HeadZ vs. Temp')
plt.xlabel('Temp')
plt.ylabel('HeadZ (nm)')

plt.show()


#SweepDataFile.close()


result = VistaScan.Disconnect();
print('VistaScan disconnect result: ', result)