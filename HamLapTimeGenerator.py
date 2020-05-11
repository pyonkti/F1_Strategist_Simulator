# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 00:14:26 2020

@author: Billy
"""

import numpy as np
import matplotlib.pyplot as plt
import random

newSoftReferenceDict = {"HAM": 97300, "BOT": 97360, "LEC": 97170, "VET": 97370}
newMediumReferenceDict = {"HAM": 97300,"BOT": 97360, "LEC": 97170, "VET": 97370}
usedMediumReferenceDict = {"HAM": 99550, "BOT": 99760, "LEC": 100410, "VET": 100205}
newHardReferenceDict = {"HAM": 98000, "BOT": 98235, "LEC": 98300, "VET": 98385}

startOffFactorDict = {"HAM": 1.085, "BOT": 1.10, "LEC": 1.116, "VET": 1.123}

vscAffectedTimeDict = {"HAM": 45000, "BOT": 43016, "LEC": 41346, "VET": 40674}

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

def lapTimeUsedMedium(lap,key):
    p = np.polyfit(xHamMediumUsed , yHamMediumUsed , 4) 
    
    """
    remove following section before using onestop()/twostop()

    yvals = p[0]*x2**4 + p[1]*x2**3 + p[2]*x2**2 + p[3]*x2 + p[4]  
    plt.plot(x2, yvals, 'k', label='used medium')
    plt.scatter(xHamMediumUsed , yHamMediumUsed)
    plt.legend()
    """   
    
    deltaTime = 4*p[0]*lap**3 + 3*p[1]*lap**2 + 2*p[2]*lap + p[3]
    finalTime = usedMediumReferenceDict[key] - deltaTime
    deviation = 200 * random.normalvariate(0, 1)
    return(finalTime+deviation)
    
def lapTimeNewSoft(lap,key):
    p = np.polyfit(xSaiSoftNew , ySaiSoftNew , 4)
    
    """
    remove following section before using onestop()/twostop()
         
    yvals = p[0]*x2**4 + p[1]*x2**3 + p[2]*x2**2 + p[3]*x2 + p[4]  
    plt.plot(x2, yvals, 'r', label='new soft')
    plt.scatter(xSaiSoftNew , ySaiSoftNew)
    plt.legend()
    """   
    
    deltaTime = 4*p[0]*lap**3 + 3*p[1]*lap**2 + 2*p[2]*lap + p[3]
    finalTime = newSoftReferenceDict[key] - deltaTime
    deviation = 200 * random.normalvariate(0, 1)
    return(finalTime+deviation)

def lapTimeNewMedium(lap,key):
    p = np.polyfit(xHamMediumNew , yHamMediumNew , 4) 
    
    """
    remove following section before using onestop()/twostop()
   
    yvals = p[0]*x2**4 + p[1]*x2**3 + p[2]*x2**2 + p[3]*x2 + p[4]  
    plt.plot(x2, yvals, 'y', label='new medium')
    plt.scatter(xHamMediumNew , yHamMediumNew)
    plt.legend() 
    """    
    
    deltaTime = 4*p[0]*lap**3 + 3*p[1]*lap**2 + 2*p[2]*lap + p[3]
    finalTime = newMediumReferenceDict[key] - deltaTime
    deviation = 200 * random.normalvariate(0, 1)
    return(finalTime+deviation)
    
def lapTimeNewHard(lap,key):
    p = np.polyfit(xHamHardNew , yHamHardNew , 4) 
    
    """
    remove following section before using onestop()/twostop()

    yvals = p[0]*x2**4 + p[1]*x2**3 + p[2]*x2**2 + p[3]*x2 + p[4]  
    plt.plot(x2, yvals, 'b', label='new hard')
    plt.scatter(xHamHardNew,yHamHardNew)
    plt.legend()
    """    
    
    deltaTime = 4*p[0]*lap**3 + 3*p[1]*lap**2 + 2*p[2]*lap + p[3]
    finalTime = newHardReferenceDict[key] - deltaTime
    deviation = 500 * random.normalvariate(0, 1)
    return(finalTime+deviation)
    
def pitTimeGenerate(lastLapTime, newTyre, condition, key):
    if condition == 'in':
        pitInTime = lastLapTime + lastLapTime * 0.045 + 100 * random.normalvariate(0, 0.618)
        return int(pitInTime)
    if condition == 'out':
        laneTime = 22544 + 1500 * random.normalvariate(0, 0.618)
        if newTyre == "Soft":
            pitOuTtime = lapTimeNewSoft(2,key) * 0.97 + 100 * random.normalvariate(0, 1)
        if newTyre == "Medium":
            pitOuTtime = lapTimeNewMedium(2,key) * 0.97 + 100 * random.normalvariate(0, 1)
        if newTyre == "Hard":
            pitOuTtime = lapTimeNewHard(2,key) * 0.97 + 100 * random.normalvariate(0, 1)
        return (int(laneTime+pitOuTtime))
    
def startOff(laptime,key):
    return startOffFactorDict[key] * laptime #1.10569 comes from HAM/BOT/lEC/VET when first lap divided by the third lap and then take the average
    
def virtualSafetyCar(expectedLaptime,key):
    factor = 127700/expectedLaptime #according to the rules of Virtual Safety Car, the gap of all cars would be maintained by following a reference lap which is roughly 30% slower than the leader.
    return expectedLaptime-vscAffectedTimeDict[key]/factor + vscAffectedTimeDict[key] + 100 * random.normalvariate(0, 1)
    
"""    
def oneStop():
    timeConsumption = 0
    firstLap = startOff(lapTimeUsedMedium(2)) + 200 * random.normalvariate(0, 1)
    secondLap = virtualSafetyCar(lapTimeUsedMedium(2),45000) + 200 * random.normalvariate(0, 1)
    timeConsumption += firstLap
    timeConsumption += secondLap
    for i in range(3,23):
        timeConsumption += lapTimeUsedMedium(i)
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(22), "hard", "in")
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(22), "hard", "out")
    for i in range(2,34):
        timeConsumption += lapTimeNewHard(i)
    print(timeConsumption)

def twoStop():
    timeConsumption = 0
    firstLap = startOff(lapTimeUsedMedium(2)) + 100 * random.normalvariate(0, 1)
    secondLap = virtualSafetyCar(lapTimeUsedMedium(2),45000)
    timeConsumption += firstLap
    timeConsumption += secondLap
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
    oneStop()
    twoStop()
    
if __name__ == '__main__':
    main()
"""