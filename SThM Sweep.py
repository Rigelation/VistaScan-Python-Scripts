# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:58:44 2019

@author: Will Morrison
"""

import VistaScan
import time
import numpy as np
import matplotlib.pyplot as plt


EndTemp = 200
StepSize = 30 #mV
Resistor = 1000 #Ohms
WaitTime = 0.001 #Time between measurements in seconds
TBLimit = 40 #Amount of T-B change at which to stop the sweep (mV)

SweepDataFile = open("SweepData.txt","w").close()
SweepDataFile = open("SweepData.txt","w+")
Temp = 29 #Need to initialize for loop
Counter = 1

VistaScan.Connect()
VistaScan.SetFeedbackParameter_Bias(0)
MinTB = VistaScan.ReadChannel(9) - TBLimit

#Sweep the temperature and record the data
while Temp < EndTemp and VistaScan.ReadChannel(9) > MinTB:
    if (Counter * StepSize) > 9500:
        break
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
    
    VistaScan.SetFeedbackParameter_Bias(Counter * StepSize)
    Counter = Counter + 1
    print(Temp, "  ", VistaScan.ReadChannel(9))
    SweepDataFile.write(str(VistaScan.GetFeedbackParameter_Bias()))
    SweepDataFile.write("\t")
    SweepDataFile.write(str(Temp))
    SweepDataFile.write("\t")
    SweepDataFile.write(str(VistaScan.ReadChannel(9))) #T-B
    SweepDataFile.write("\t")
    SweepDataFile.write(str(ResistanceTip))
    SweepDataFile.write("\t")
    SweepDataFile.write(str(CurrentTip))
    SweepDataFile.write("\t")
    SweepDataFile.write(str(VTwo))
    SweepDataFile.write("\t")
    SweepDataFile.write(str(VistaScan.ReadChannel(-2))) #AFMHead-Z
    SweepDataFile.write("\t")
    SweepDataFile.write(str(PowerTip)) 
    SweepDataFile.write("\n")
    time.sleep(WaitTime)

VistaScan.SetFeedbackParameter_Bias(0)
SweepDataFile.close()

#Display the data
SweepDataFile = open("SweepData.txt", "r")
SweepDataArr = np.loadtxt(SweepDataFile)

Bias = SweepDataArr[:,0]
TB = SweepDataArr[:,2]
Temp = SweepDataArr[:,1]
RTip = SweepDataArr[:,3]
ITip = SweepDataArr[:,4]
VTip = SweepDataArr[:,5]
HeadZ = SweepDataArr[:,6]
PTip = SweepDataArr[:,7]

plt.subplot(2, 2, 1)
plt.plot(Temp, TB, 'ko-')
plt.title('T-B vs. Temp')
plt.xlabel('Temp')
plt.ylabel('T-B')

plt.subplot(2, 2, 2)
plt.plot(Bias, RTip, 'r.-')
plt.title('Resistance of Tip vs. Voltage')
plt.xlabel('Bias')
plt.ylabel('RTip')

plt.subplot(2, 2, 3)
plt.plot(VTip, ITip, 'r.-')
plt.title('I-V Curve for Tip')
plt.xlabel('Voltage Drop Across Tip')
plt.ylabel('Current Through Tip (mA)')

plt.subplot(2, 2, 4)
plt.plot(Bias, PTip, 'r.-')
plt.title('Power vs. Bias')
plt.xlabel('Bias')
plt.ylabel('Power (mW)')

plt.show()


SweepDataFile.close()


result = VistaScan.Disconnect();
print('VistaScan disconnect result: ', result)