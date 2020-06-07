# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 00:14:26 2020

Time Generator

@author: Billy
"""

import numpy as np
import matplotlib.pyplot as plt
import random


newSoftReferenceDict = {"HAM": 95800, "BOT": 95860, "LEC": 95670, "VET": 95870, "VER": 96120, "GAS":96680}
newMediumReferenceDict = {"HAM": 96800,"BOT": 96860, "LEC": 96670, "VET": 96870, "VER": 97120, "GAS":97680}
usedMediumReferenceDict = {"HAM": 99550, "BOT": 99760, "LEC": 100410, "VET": 100205, "VER": 100340}
newHardReferenceDict = {"HAM": 98000, "BOT": 98235, "LEC": 98300, "VET": 98385, "VER": 98883, "GAS": 99579}
usedSoftReferenceDict = {"GAS": 100880}

startOffFactorDict = {"HAM": 1.085, "BOT": 1.10, "LEC": 1.116, "VET": 1.123, "VER": 1.136, "GAS": 1.143}

pitLaneTimeDict = {"HAM": 23130, "BOT": 23130, "LEC": 23053, "VET": 23053, "VER": 22605, "GAS": 22605}

xHamMediumNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,30]
xHamMediumNew = np.array(xHamMediumNew)
yHamMediumNew = [0,751,1615,2392,2950,3367,3860,4070,4598,4931,5839,6098,6430,6780,6196,6107,6142,6676,7118,7291,1200,-8000]
yHamMediumNew = np.array(yHamMediumNew)

xVetMediumNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,25,30]
xVetMediumNew = np.array(xVetMediumNew)
yVetMediumNew = [0,2034,2406,2664,2836,3060,3595,3817,4326,4945,5798,5912,6355,6249,6661,6483,6884,7300,7302,7297,6219,300,-10000]
yVetMediumNew = np.array(yVetMediumNew)

xVerMediumNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25,30]
xVerMediumNew = np.array(xVerMediumNew)
yVerMediumNew = [0,344,765,668,1129,1787,2404,2898,3330,4238,5215,6102,6583,6837,7334,7835,8216,8331,7854,7299,7123,6197,500,-8000]
yVerMediumNew = np.array(yVerMediumNew)

xHamMediumUsed = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,30]
xHamMediumUsed = np.array(xHamMediumUsed)
yHamMediumUsed = [0,1431,2459,3508,4534,5673,6927,8212,9168,10390,11330,12075,13022,13589,14183,14724,15129,15691,15945,16117,16150,11050,-1950]
yHamMediumUsed = np.array(yHamMediumUsed)

xVetMediumUsed = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,25,30]
xVetMediumUsed = np.array(xVetMediumUsed)
yVetMediumUsed = [0,1562,2875,4104,5470,6563,7835,9084,10383,11479,12191,12522,13294,13737,14286,14701,16130,10020,-3000]
yVetMediumUsed = np.array(yVetMediumUsed)

xVerMediumUsed = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,20,25,30]
xVerMediumUsed = np.array(xVerMediumUsed)
yVerMediumUsed = [0,1137,2402,3879,5065,6403,7752,8984,10148,10990,11260,11895,12763,13640,14204,16130,10020,-3000]
yVerMediumUsed = np.array(yVerMediumUsed)

xHamHardNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,40,50]
xHamHardNew = np.array(xHamHardNew)
yHamHardNew = [0,449,396,485,1006,1510,1991,2863,3387,4349,6077,8041,9895,11447,13110,14887,16918,18655,20634,22860,24446,26293,27866,29410,30831,32524,34322,36148,38170,40050,41811,43078,44428,44334,45625,46244,45896,30000,0]
yHamHardNew = np.array(yHamHardNew)

xVetHardNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,40,50]
xVetHardNew = np.array(xVetHardNew)
yVetHardNew = [0,307,109,54,433,795,1134,1866,2248,3071,4663,6493,8212,9628,11155,12797,14694,16296,18141,20234,21684,23397,24834,26242,27526,29083,30746,32437,34325,36071,37697,38827,40040,39801,40954,41432,40937,25000,-5500]
yVetHardNew = np.array(yVetHardNew)

xVerHardNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,40,50]
xVerHardNew = np.array(xVerHardNew)
yVerHardNew = [0,275,43,-46,302,633,940,1643,1994,2788,4356,6162,7857,9247,10749,12367,14241,15819,17641,19712,21136,22824,24236,25618,26876,28408,30046,31713,33578,35300,36901,38003,39189,38915,40041,40488,39957,23000,-7000]
yVerHardNew = np.array(yVerHardNew)

xHamSoftNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,30]
xHamSoftNew = np.array(xHamSoftNew)
yHamSoftNew = [0,200,1014,1746,2137,3095,4416,5777,6076,6743,7537,8659,9485,10318,11038,11482,11443,11967,11937,11800,5000,-10000]
yHamSoftNew = np.array(yHamSoftNew)

xVetSoftNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,30]
xVetSoftNew = np.array(xVetSoftNew)
yVetSoftNew = [0,200,718,1154,1247,1909,2936,4003,4003,4373,4871,5698,6228,6765,7188,7334,6996,7223,6894,6500,-500,-20000]
yVetSoftNew = np.array(yVetSoftNew)

xVerSoftNew = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,30]
xVerSoftNew = np.array(xVerSoftNew)
yVerSoftNew = [0,200,453,623,448,846,1611,2416,2149,2253,2486,3049,3314,3586,3744,3623,3015,2975,2376,2000,-5000,-30000]
yVerSoftNew = np.array(yVerSoftNew)

xGasSoftUsed = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,20,25,30]
xGasSoftUsed = np.array(xGasSoftUsed)
yGasSoftUsed = [0,1059,1952,3112,4022,5031,6105,7258,8418,9426,10137,11019,11994,12951,13800,14666,15129,15000,9000,-8000]
yGasSoftUsed = np.array(yGasSoftUsed)

x2 = np.linspace(0, 40, 20)

p_usedSoft = np.polyfit(xGasSoftUsed, yGasSoftUsed, 4)

p_usedMedium_Ham = np.polyfit(xHamMediumUsed , yHamMediumUsed , 4) 
p_newSoft_Ham = np.polyfit(xHamSoftNew , yHamSoftNew , 4)
p_newMedium_Ham = np.polyfit(xHamMediumNew , yHamMediumNew , 4) 
p_newHard_Ham = np.polyfit(xHamHardNew , yHamHardNew , 4)

p_usedMedium_Vet = np.polyfit(xVetMediumUsed , yVetMediumUsed , 4) 
p_newMedium_Vet = np.polyfit(xVetMediumNew , yVetMediumNew , 4) 
p_newHard_Vet = np.polyfit(xVetHardNew , yVetHardNew , 4)  
p_newSoft_Vet = np.polyfit(xVetSoftNew , yVetSoftNew , 4)

p_usedMedium_Ver = np.polyfit(xVerMediumUsed , yVerMediumUsed , 4) 
p_newMedium_Ver = np.polyfit(xVerMediumNew , yVerMediumNew , 4) 
p_newHard_Ver = np.polyfit(xVerHardNew , yVerHardNew , 4) 
p_newSoft_Ver = np.polyfit(xVerSoftNew , yVerSoftNew , 4)

usedMediumDict = {"HAM": p_usedMedium_Ham, "BOT": p_usedMedium_Ham, "LEC": p_usedMedium_Vet, "VET": p_usedMedium_Vet, "VER": p_usedMedium_Ver, "GAS": p_usedMedium_Ver} 
newMediumDict = {"HAM": p_newMedium_Ham, "BOT": p_newMedium_Ham, "LEC": p_newMedium_Vet, "VET": p_newMedium_Vet, "VER": p_newMedium_Ver, "GAS": p_newMedium_Ver} 
newHardDict = {"HAM": p_newHard_Ham, "BOT": p_newHard_Ham, "LEC": p_newHard_Vet, "VET": p_newHard_Vet, "VER": p_newHard_Ver, "GAS": p_newHard_Ver} 
newSoftDict = {"HAM": p_newSoft_Ham, "BOT": p_newSoft_Ham, "LEC": p_newSoft_Vet, "VET": p_newSoft_Vet, "VER": p_newSoft_Ver, "GAS": p_newSoft_Ver} 

def lapTimeUsedMedium(lap,key):
    
    """
    #remove following section before using onestop()/twostop()

    yvals = usedMediumDict[key][0]*x2**4 + usedMediumDict[key][1]*x2**3 + usedMediumDict[key][2]*x2**2 + usedMediumDict[key][3]*x2 + usedMediumDict[key][4]
    plt.plot(x2, yvals, 'k', label='used medium')
    plt.scatter(xHamMediumUsed , yHamMediumUsed)
    plt.legend()
    """   
    
    deltaTime = 4*usedMediumDict[key][0]*lap**3 + 3*usedMediumDict[key][1]*lap**2 + 2*usedMediumDict[key][2]*lap + usedMediumDict[key][3]
    finalTime = usedMediumReferenceDict[key] - deltaTime
    deviation = 200 * random.normalvariate(0, 0.674)
    return(finalTime+deviation)
    
def lapTimeNewSoft(lap,key):
   
    """
    #remove following section before using onestop()/twostop()
         
    yvals = newSoftDict[key][0]*x2**4 + newSoftDict[key][1]*x2**3 + newSoftDict[key][2]*x2**2 + newSoftDict[key][3]*x2 + newSoftDict[key][4]  
    plt.plot(x2, yvals, 'r', label='new soft')
    plt.scatter(xVetSoftNew , yVetSoftNew)
    plt.legend() 
    """
    
    deltaTime = 4*newSoftDict[key][0]*lap**3 + 3*newSoftDict[key][1]*lap**2 + 2*newSoftDict[key][2]*lap + newSoftDict[key][3]
    finalTime = newSoftReferenceDict[key] - deltaTime
    deviation = 220 * random.normalvariate(0, 0.674)
    return(finalTime+deviation)
    
def lapTimeUsedSoft(lap,key):
    
    """
    #remove following section before using onestop()/twostop()
         
    yvals = p_usedSoft[0]*x2**4 + p_usedSoft[1]*x2**3 + p_usedSoft[2]*x2**2 + p_usedSoft[3]*x2 + p_usedSoft[4]  
    plt.plot(x2, yvals, 'r', label='new soft')
    plt.scatter(xSaiSoftNew , ySaiSoftNew)
    plt.legend()
    """   
    
    deltaTime = 4*p_usedSoft[0]*lap**3 + 3*p_usedSoft[1]*lap**2 + 2*p_usedSoft[2]*lap + p_usedSoft[3]
    finalTime = usedSoftReferenceDict[key] - deltaTime
    deviation = 350 * random.normalvariate(0, 0.674)
    return(finalTime+deviation)    

def lapTimeNewMedium(lap,key):

    """
    #remove following section before using onestop()/twostop()
   
    yvals = newMediumDict[key][0]*x2**4 + newMediumDict[key][1]*x2**3 + newMediumDict[key][2]*x2**2 + newMediumDict[key][3]*x2 + newMediumDict[key][4]  
    plt.plot(x2, yvals, 'y', label='new medium')
    plt.scatter(xHamMediumNew , yHamMediumNew)
    plt.legend() 
    """
    
    deltaTime = 4*newMediumDict[key][0]*lap**3 + 3*newMediumDict[key][1]*lap**2 + 2*newMediumDict[key][2]*lap + newMediumDict[key][3]
    finalTime = newMediumReferenceDict[key] - deltaTime
    deviation = 350 * random.normalvariate(0, 0.674)
    return(finalTime+deviation)
    
def lapTimeNewHard(lap,key):

    """
    #remove following section before using onestop()/twostop()
    x2 = np.linspace(0, 60, 20)
    yvals = newHardDict[key][0]*x2**4 + newHardDict[key][1]*x2**3 + newHardDict[key][2]*x2**2 + newHardDict[key][3]*x2 + newHardDict[key][4]  
    plt.plot(x2, yvals, 'b', label='new hard')
    plt.scatter(xHamHardNew,yHamHardNew)
    plt.legend()
    """
    
    deltaTime = 4*newHardDict[key][0]*lap**3 + 3*newHardDict[key][1]*lap**2 + 2*newHardDict[key][2]*lap + newHardDict[key][3]
    finalTime = newHardReferenceDict[key] - deltaTime
    deviation = 320 * random.normalvariate(0, 1)
    return(finalTime+deviation)
    
def pitTimeGenerate(lastLapTime, newTyre, condition, key):
    if condition == 'in':
        pitInTime = lastLapTime + lastLapTime * 0.045 + 300 * random.normalvariate(0, 0.674)
        return int(pitInTime)
    if condition == 'out':
        laneTime = pitLaneTimeDict[key] + 750 * random.normalvariate(0, 0.674)
        pitOutTime =  int()
        if newTyre == 'Soft':
            pitOutTime = lapTimeNewSoft(2,key) * 0.97 + 220 * random.normalvariate(0, 0.674)
        if newTyre == 'Medium':
            pitOutTime = lapTimeNewMedium(2,key) * 0.97 + 350 * random.normalvariate(0, 0.674)
        if newTyre == 'Hard':
            pitOutTime = lapTimeNewHard(2,key) * 0.97 + 320 * random.normalvariate(0, 0.674)
        temp = {"lane":laneTime, "out":pitOutTime}
        return temp
    
def startOff(laptime,key):
    return startOffFactorDict[key] * laptime + 200 * random.normalvariate(0, 0.674)#1.10569 comes from HAM/BOT/lEC/VET when first lap divided by the third lap and then take the average
    
def virtualSafetyCar(expectedLaptime,currentTime,vscStart,vscLast,key):
    factor = 127700/expectedLaptime #according to the rules of Virtual Safety Car, the gap of all cars would be maintained by following a reference lap which is roughly 30% slower than the leader.
    if 0 <= currentTime-vscStart < vscLast:
        affectedTime = vscStart + vscLast-currentTime
        if affectedTime > expectedLaptime:
            return 127700 + 200 * random.normalvariate(0, 1)
    else:
        affectedTime = 0
    return expectedLaptime- affectedTime + affectedTime*factor + 200 * random.normalvariate(0, 1)

"""
For individual running test 
"""

"""      
def oneStop():
    timeConsumption = 0
    firstLap = startOff(lapTimeUsedMedium(2,"HAM"),"HAM") 
    secondLap = virtualSafetyCar(lapTimeUsedMedium(2,"HAM"),"HAM")
    timeConsumption += firstLap
    timeConsumption += secondLap
    for i in range(3,23):
        timeConsumption += lapTimeUsedMedium(i,"HAM")
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(22,"HAM"), "Hard", "in","HAM")
    timeConsumption += pitTimeGenerate(lapTimeUsedMedium(22,"HAM"), "Hard", "out","HAM")
    for i in range(2,34):
        timeConsumption += lapTimeNewHard(i,"HAM")
    print(timeConsumption)

def twoStop():
    timeConsumption = 0
    firstLap = startOff(lapTimeUsedMedium(2,"HAM"),"HAM")
    print(int(firstLap))
    secondLap = virtualSafetyCar(lapTimeUsedMedium(2,"HAM"),"HAM")
    print(int(secondLap))
    timeConsumption += firstLap
    timeConsumption += secondLap
    for i in range(3,22):
        temp = lapTimeUsedMedium(i,"HAM")
        timeConsumption += temp 
        print(int(temp))
    temp = pitTimeGenerate(lapTimeUsedMedium(21,"HAM"), "Hard", "in","HAM")
    print(int(temp))
    timeConsumption += temp
    temp = pitTimeGenerate(lapTimeUsedMedium(21,"HAM"), "Hard", "out","HAM")    
    print(int(temp))
    timeConsumption += temp
    for i in range(2,14):
        temp = lapTimeNewHard(i,"HAM")
        print(int(temp))
        timeConsumption += temp
    temp = pitTimeGenerate(lapTimeNewHard(22,"HAM"), "Medium", "in","HAM")
    print(int(temp))
    timeConsumption += temp
    temp = pitTimeGenerate(lapTimeNewHard(22,"HAM"), "Medium", "out","HAM")   
    print(int(temp))
    timeConsumption += temp   
    for i in range(2,21):
        temp = lapTimeNewMedium(i,"HAM")
        timeConsumption += temp
        print(int(temp))
    print(timeConsumption)

def main():
    #oneStop()
    #twoStop()
    
if __name__ == '__main__':
    main()
"""