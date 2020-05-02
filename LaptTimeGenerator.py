# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 00:14:26 2020

@author: Billy
"""

import numpy as np
import matplotlib.pyplot as plt
import random

xHamMediumNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
xHamMediumNew = np.array(xHamMediumNew)
yHamMediumNew = [0,1051,2215,3292,4150,4867,5660,6170,6998,7631,8839,9398,10030,10680,10396,10607,10942,11776,12518,12991]
yHamMediumNew = np.array(yHamMediumNew)

xHamMediumUsed = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
xHamMediumUsed = np.array(xHamMediumUsed)
yHamMediumUsed = [0,381,1409,2458,3484,4623,5877,7162,8118,9340,10280,11025,11972,12539,13133,13674,14079,14641,14895,15067]
yHamMediumUsed = np.array(yHamMediumUsed)

xHamHardNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,40,50]
xHamHardNew = np.array(xHamHardNew)
yHamHardNew = [0,-252,-1005,-1617,-1797,-1994,-2213,-2042,-2219,-1957,-929,334,1487,2338,3300,4377,5707,6744,8023,9548,10433,11580,12453,13296,14017,15009,16106,17231,18552,19732,	20792,21359,22008,21214,21804,21722,20673,12000,-21000]
yHamHardNew = np.array(yHamHardNew)

x2 = np.linspace(0, 60, 20)

def func(x, a, b,c):
    return a*np.sqrt(x)*(b*np.square(x)+c)

def lapTimeUsedMedium(lap):
    p = np.polyfit(xHamMediumUsed , yHamMediumUsed , 3) 
    """
    yvals = p[0]*x2**3 + p[1]*x2**2 + p[2]*x2 + p[3]
    plt.plot(x2, yvals, 'r')
    plt.scatter(xHamMediumUsed , yHamMediumUsed)
    plt.show()
    """
    deltaTime = 3*p[0]*lap**2 + 2*p[1]*lap + p[2]
    finalTime = 99550 - deltaTime
    deviation = 500 * random.normalvariate(0, 1)
    return(finalTime+deviation)

def lapTimeNewMedium(lap):
    p = np.polyfit(xHamMediumNew , yHamMediumNew , 3) 
    """
    yvals = p[0]*x2**3 + p[1]*x2**2 + p[2]*x2 + p[3]
    plt.plot(x2, yvals, 'r')
    plt.scatter(xHamMediumNew , yHamMediumNew)
    plt.show()
    """
    deltaTime = 3*p[0]*lap**2 + 2*p[1]*lap + p[2]
    finalTime = 97100 - deltaTime
    deviation = 500 * random.normalvariate(0, 1)
    return(finalTime+deviation)
    
def lapTimeNewHard(lap):
    p = np.polyfit(xHamHardNew , yHamHardNew , 3) 
    """
    yvals = p[0]*x2**3 + p[1]*x2**2 + p[2]*x2 + p[3]
   
    plt.plot(x2, yvals, 'r')
    plt.scatter(xHamHardNew,yHamHardNew)
    """
    deltaTime = 3*p[0]*lap**2 + 2*p[1]*lap + p[2]
    finalTime = 97300 - deltaTime
    deviation = 500 * random.normalvariate(0, 1)
    return(finalTime+deviation)
    
def pitTimeGenerate(lastLapTime, newTyre, condition):
    if condition == 'in':
        pitInTime = lastLapTime + lastLapTime * 0.045 + 100 * random.normalvariate(0, 0.618)
        return pitInTime
    if condition == 'out':
        laneTime = 22544 + 1500 * random.normalvariate(0, 0.618)
        if newTyre == "medium":
            pitOuTtime = lapTimeNewMedium(2) * 0.97 + 500 * random.normalvariate(0, 1)
        if newTyre == "hard":
            pitOuTtime = lapTimeNewHard(2) * 0.97 + 500 * random.normalvariate(0, 1)
        return (laneTime+pitOuTtime)
    
def oneStop():
    timeConsumption = 0
    for i in range(2,24):
        timeConsumption += lapTimeUsedMedium(i)
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(23), "hard", "in")
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(23), "hard", "out")
    for i in range(2,34):
        timeConsumption += lapTimeNewHard(i)
    print(timeConsumption)

def twoStop():
    timeConsumption = 0
    for i in range(2,15):
        timeConsumption += lapTimeUsedMedium(i)
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(14), "hard", "in")
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(14), "hard", "out")    
    for i in range(2,23):
        timeConsumption += lapTimeNewHard(i)
    timeConsumption += pitTimeGenerate(lapTimeNewHard(22), "medium", "in")
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(22), "medium", "out")   
    for i in range(2,20):
        timeConsumption += lapTimeNewMedium(i)
    print(timeConsumption)
    
def main():
    oneStop()
    twoStop()
    
if __name__ == '__main__':
    main()