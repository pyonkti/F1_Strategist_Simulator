# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 00:14:26 2020

@author: Billy
"""

import numpy as np
import matplotlib.pyplot as plt
import random

xHamMediumNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,30]
xHamMediumNew = np.array(xHamMediumNew)
yHamMediumNew = [0,1051,2215,3292,4150,4867,5660,6170,6998,7631,8839,9398,10030,10680,10396,10607,10942,11776,12518,12991,10000,4000]
yHamMediumNew = np.array(yHamMediumNew)

xHamMediumUsed = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,30]
xHamMediumUsed = np.array(xHamMediumUsed)
yHamMediumUsed = [0,381,1409,2458,3484,4623,5877,7162,8118,9340,10280,11025,11972,12539,13133,13674,14079,14641,14895,15067,15100,11000,2000]
yHamMediumUsed = np.array(yHamMediumUsed)

xHamHardNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]
xHamHardNew = np.array(xHamHardNew)
yHamHardNew = [0,-252,-1005,-1617,-1797,-1994,-2213,-2042,-2219,-1957,-929,334,1487,2338,3300,4377,5707,6744,8023,9548,10433,11580,12453,13296,14017,15009,16106,17231,18552,19732,	20792,21359,22008,21214,21804,21722,20673]
yHamHardNew = np.array(yHamHardNew)

xSaiSoftNew = [0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
xSaiSoftNew = np.array(xSaiSoftNew)
ySaiSoftNew = [0,933,1782,2278,3360,4817,6315,6716,7497,8410,9661,10607,11260,11096,10547,9900,8534,7996]
ySaiSoftNew = np.array(ySaiSoftNew)

x2 = np.linspace(0, 40, 20)
x3 = np.linspace(0, 60, 20)
def func(x, a, b,c):
    return a*np.sqrt(x)*(b*np.square(x)+c)

def lapTimeUsedMedium(lap):
    p = np.polyfit(xHamMediumUsed , yHamMediumUsed , 4) 
    
    """
    remove following section before using onestop()/twostop()
    """
    
    yvals = p[0]*x2**4 + p[1]*x2**3 + p[2]*x2**2 + p[3]*x2 + p[4]  
    plt.plot(x2, yvals, 'k', label='used medium')
    plt.scatter(xHamMediumUsed , yHamMediumUsed)
    plt.legend()
    
    deltaTime = 4*p[0]*lap**3 + 3*p[1]*lap**2 + 2*p[2]*lap + p[3]
    finalTime = 99550 - deltaTime
    deviation = 500 * random.normalvariate(0, 1)
    return(finalTime+deviation)
    
def lapTimeNewSoft(lap):
    p = np.polyfit(xSaiSoftNew , ySaiSoftNew , 4)
    
    """
    remove following section before using onestop()/twostop()
    """
    
    yvals = p[0]*x2**4 + p[1]*x2**3 + p[2]*x2**2 + p[3]*x2 + p[4]  
    plt.plot(x2, yvals, 'r', label='new soft')
    plt.scatter(xSaiSoftNew , ySaiSoftNew)
    plt.legend()
    
    deltaTime = 4*p[0]*lap**3 + 3*p[1]*lap**2 + 2*p[2]*lap + p[3]
    finalTime = 97300 - deltaTime
    deviation = 500 * random.normalvariate(0, 1)
    return(finalTime+deviation)

def lapTimeNewMedium(lap):
    p = np.polyfit(xHamMediumNew , yHamMediumNew , 4) 
    
    """
    remove following section before using onestop()/twostop()
    """
    
    yvals = p[0]*x2**4 + p[1]*x2**3 + p[2]*x2**2 + p[3]*x2 + p[4]  
    plt.plot(x2, yvals, 'y', label='new medium')
    plt.scatter(xHamMediumNew , yHamMediumNew)
    plt.legend() 
    
    deltaTime = 4*p[0]*lap**3 + 3*p[1]*lap**2 + 2*p[2]*lap + p[3]
    finalTime = 97300 - deltaTime
    deviation = 500 * random.normalvariate(0, 1)
    return(finalTime+deviation)
    
def lapTimeNewHard(lap):
    p = np.polyfit(xHamHardNew , yHamHardNew , 4) 
    
    """
    remove following section before using onestop()/twostop()
    """

    yvals = p[0]*x2**4 + p[1]*x2**3 + p[2]*x2**2 + p[3]*x2 + p[4]  
    plt.plot(x2, yvals, 'b', label='new hard')
    plt.scatter(xHamHardNew,yHamHardNew)
    plt.legend()
    
    deltaTime = 4*p[0]*lap**3 + 3*p[1]*lap**2 + 2*p[2]*lap + p[3]
    finalTime = 98000 - deltaTime
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
    timeConsumption = 215100
    for i in range(3,23):
        timeConsumption += lapTimeUsedMedium(i)
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(22), "hard", "in")
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(22), "hard", "out")
    for i in range(2,34):
        timeConsumption += lapTimeNewHard(i)
    print(timeConsumption)

def twoStop():
    timeConsumption = 215100
    for i in range(3,14):
        timeConsumption += lapTimeUsedMedium(i)
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(13), "hard", "in")
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(13), "hard", "out")    
    for i in range(2,23):
        timeConsumption += lapTimeNewHard(i)
    timeConsumption += pitTimeGenerate(lapTimeNewHard(22), "medium", "in")
    timeConsumption += pitTimeGenerate(lapTimeNewHard(22), "medium", "out")   
    for i in range(2,20):
        timeConsumption += lapTimeNewMedium(i)
    print(timeConsumption)
    
def main():
    #oneStop()
    #twoStop()
    lapTimeUsedMedium(10)
    lapTimeNewSoft(10)
    lapTimeNewMedium(10)
    lapTimeNewHard(10)
    
if __name__ == '__main__':
    main()