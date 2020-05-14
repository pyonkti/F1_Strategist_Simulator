# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 20:24:40 2020

@author: Billy
"""

import pandas as pd
import re
from matplotlib import pyplot as plt 
import numpy as np
                                                                                                                                                                                                                                                               
lapTime = pd.read_csv(".\learn\lap_times.csv")
driverInfo = pd.read_csv(".\learn\drivers.csv")
driverInfo= driverInfo.drop(columns= ['driverRef','number','forename','surname','dob','nationality','url'], axis=1)
tyreChoice = pd.read_csv(".\learn\\tyre.csv")
merged = driverInfo.merge(lapTime, left_on='driverId', right_on = 'driverId', how = 'right')
merged = merged.drop(columns= ['driverId'], axis=1)
merged = merged.merge(tyreChoice, how = 'right')
raceTuple = (862,882,903,928,950,970,991)
yearTuple = ("2012","2013","2014","2015","2016","2017","2018")
raceDict = dict(zip(raceTuple,yearTuple))
overtakeList = list()
overtakeAdvList = list()
allGapList = list()
allAdvList = list()
costOfOvertakeList = list()
costOfBeOvertakenList = list()

def tyreCondition(currentLap,inputDataFrame,lastPitDict,pitTimesDict):
    allTyreChoice = list()
    for i in range(len(set(inputDataFrame['code']))):
        for key,value in pitTimesDict.items():
            if key == inputDataFrame['code'][i]:
                expectedLapsOnTyre = re.search(r'\d+',str(inputDataFrame.iloc[i,6+value])).group()
                currentTyre = re.search(r'^[a-zA-Z]*\s*[a-zA-Z]*',str(inputDataFrame.iloc[i,6+value])).group()
                if currentLap == lastPitDict[key] + int(expectedLapsOnTyre):
                    allTyreChoice.append(str(currentLap-lastPitDict[key])+" "+currentTyre+'\033[35m PIT\033[0m')
                else:
                    allTyreChoice.append(str(currentLap-lastPitDict[key])+" "+currentTyre)
                if currentLap == lastPitDict[key] + int(expectedLapsOnTyre):
                    pitTimesDict[key] += 1
                    lastPitDict[key] = currentLap
    return allTyreChoice

def timeGap(currentLap,inputDataFrame,timeCostDict):
    timeGapList = list()
    for i in range(len(set(inputDataFrame['code']))):
        for key,value in timeCostDict.items():
            if key == inputDataFrame['code'][i]:
                currentLapTime = inputDataFrame.iloc[i,5]
                if currentLap == 1:
                    timeCostDict[key] = currentLapTime
                else:
                    timeCostDict[key] += currentLapTime
                timeStamp = timeCostDict[key] - timeCostDict[inputDataFrame['code'][0]]
                timeGapList.append(timeStamp)
    return timeGapList

def allGap(timeGapList,lapTimeList):
    for i in range(len(timeGapList)-1):
        if (timeGapList[i+1]-timeGapList[i] < 1000) & (lapTimeList[i]-lapTimeList[i+1] > 0) & (lapTimeList[i]-lapTimeList[i+1] < 2000) :
            allGapList.append(timeGapList[i+1]-timeGapList[i])
            
def allAdv(lapTimeList,timeGapList):
    for i in range(len(lapTimeList)-1):
        if (lapTimeList[i]-lapTimeList[i+1] < 2000) & (lapTimeList[i]-lapTimeList[i+1] > 0) & (timeGapList[i+1]-timeGapList[i] < 1000):
            allAdvList.append(lapTimeList[i]-lapTimeList[i+1])
    

def lastLapTime(inputDataFrame,lastLapDict):
    lastLapTimeList = list()
    for i in range(len(set(inputDataFrame['code']))):
        for key,value in lastLapDict.items():
            if key == inputDataFrame['code'][i]:
                lastLapDict[key] = inputDataFrame.iloc[i,5]                
                lastLapTimeList.append(lastLapDict[key])
    return lastLapTimeList

def getResult(raceId):
    lastOrder = list()
    tempTyreConditionList = list()
    lastLapTimeList = list()
    raceData = merged[merged['raceId'].isin([raceId])]
    raceData = raceData.reset_index(drop=True)
    codeTuple = tuple(set(raceData['code']))
    lastPitLapTuple = (0,)*len(codeTuple)
    timeCostDict = dict(zip(codeTuple,lastPitLapTuple))
    lastLapDict = dict(zip(codeTuple,lastPitLapTuple))
    lastPitDict = dict(zip(codeTuple,lastPitLapTuple))
    pitTimesDict = dict(zip(codeTuple,lastPitLapTuple))
    for i in set(raceData.lap):
        lapResult = raceData[raceData['lap'].isin([i])]
        lapResult = lapResult.sort_values('position')
        lapResult = lapResult.reset_index(drop=True)
        if i == 1:
            lastOrder = tuple(lapResult['code'])
            lastLapTimeList = lastLapTime(lapResult,lastLapDict)
            lastTimeGapList = timeGap(i,lapResult,timeCostDict)
            tempTyreConditionList = tyreCondition(i,lapResult,lastPitDict,pitTimesDict)
            allGap(lastTimeGapList,lapResult['milliseconds'])
            allAdv(lapResult['milliseconds'],lastTimeGapList)
            continue
        else:
            thisTyreConditionList = tyreCondition(i,lapResult,lastPitDict,pitTimesDict)
            tempCodeList = lapResult['code'].values.tolist()
            tempTimeList = lapResult['milliseconds'].values.tolist()
            for cPosition, cDriver in enumerate(tuple(lapResult['code'])):
                for lPosition, lDriver in enumerate(lastOrder):
                    if cDriver == lDriver and lPosition-cPosition >= 1:
                        if lPosition >= len(lapResult['code']) or lastOrder[lPosition-1] not in tempCodeList or tempCodeList.index(lastOrder[lPosition-1])-lPosition > 1 or tempCodeList.index(lastOrder[lPosition-1])-tempCodeList.index(cDriver) <= 0 or "PIT" in thisTyreConditionList[tempCodeList.index(lastOrder[lPosition-1])] or "PIT" in tempTyreConditionList[lPosition-1]:
                            continue
                        else:
                            overtakeList.append(lastTimeGapList[lPosition]-lastTimeGapList[lPosition-1])
                            overtakeAdvList.append(lastLapTimeList[lPosition-1]-lastLapTimeList[lPosition])
                            if i == 2:
                                continue
                            else:
                                costOfOvertakeList.append(tempTimeList[cPosition]- lastLapTimeList[lPosition])
                                costOfBeOvertakenList.append(tempTimeList[tempCodeList.index(lastOrder[lPosition-1])]- lastLapTimeList[lPosition-1])
        lastLapTimeList = lastLapTime(lapResult,lastLapDict)
        lastTimeGapList = timeGap(i,lapResult,timeCostDict)
        tempTyreConditionList = thisTyreConditionList  
        allGap(lastTimeGapList,lapResult['milliseconds'])
        allAdv(lapResult['milliseconds'],lastTimeGapList)         
        lastOrder = tuple(lapResult['code'])
    data = np.array(overtakeList) 
    bins = np.linspace(0, 1000, num=20, endpoint=True, retstep=False, dtype=None)
    countOvertakeGap,bins = np.histogram(data, bins)
    data = np.array(allGapList) 
    countGap,bins = np.histogram(data, bins)   
    possibilityOnGapList = np.array(countOvertakeGap) / np.array(countGap)
    plt.title("F1 Shanghai: Overtake possibility distribution in relation to the gap between drivers from 2012 to "+raceDict[raceId]) 
    x = np.arange(50, 1000, 50).tolist()
    y = possibilityOnGapList
    plt.plot(x, y, 'ro-')
    plt.xlabel('milliseconds (gap) with width of 100ms')
    plt.ylabel('overtake possibility under the circumstance')
    fileName = str("F:/Programming/thesis/GapPossibility/"+raceDict[raceId]+"gapOvertakePossibility.eps")
    plt.savefig(fileName)
    plt.show()
    
    data = np.array(overtakeAdvList) 
    countOvertakeAdv,bins = np.histogram(data, bins)
    data = np.array(allAdvList) 
    countAdv,bins = np.histogram(data, bins)   
    possibilityOnAdvList = np.array(countOvertakeAdv) / np.array(countAdv)
    plt.title("F1 Shanghai: Overtake possibility distribution in relation to the lap time advantage between drivers from 2012 to "+raceDict[raceId]) 
    x = np.arange(0, 1900, 100).tolist()
    y = possibilityOnAdvList
    plt.plot(x, y, 'ro-')
    plt.xlabel('milliseconds (advantage) with width of 100ms')
    plt.ylabel('overtake possibility under the circumstance')
    fileName = str("F:/Programming/thesis/LapTimeAdvPossibility/"+raceDict[raceId]+"lapTimeAdvOvertakePossibility.eps")
    plt.savefig(fileName)
    plt.show()
    
    data = np.array(costOfOvertakeList) 
    bins = np.linspace(-1000, 2000, num=30, endpoint=True, retstep=False, dtype=None)
    countOvertakeCost,bins = np.histogram(data, bins)
    data = np.true_divide(countOvertakeCost, len(overtakeList))
    sumData = list()
    for i in range(0,len(data)):
        sumData.append(sum(data[0:i+1]))
    print(sumData)
    x = np.arange(-900, 2000, 100).tolist()
    plt.scatter(x, sumData) 
    plt.title("F1 Shanghai: Time cost of Overtaking from 2012 to "+raceDict[raceId]) 
    plt.xlabel('milliseconds')
    plt.ylabel('numbers')
    fileName = str("F:/Programming/thesis/CostofOvertaking/"+raceDict[raceId]+"CostofOvertaking.eps")
    plt.savefig(fileName)
    plt.show()
    
    data = np.array(costOfBeOvertakenList) 
    countBeOvertakeCost,bins = np.histogram(data, bins)
    data = np.true_divide(countBeOvertakeCost, len(overtakeList))
    sumData = list()
    for i in range(0,len(data)):
        sumData.append(sum(data[0:i+1]))
    print(sumData)
    x = np.arange(-900, 2000, 100).tolist()
    plt.scatter(x, sumData) 
    plt.title("F1 Shanghai: Time cost of being Overtook from 2012 to "+raceDict[raceId]) 
    plt.xlabel('milliseconds')
    plt.ylabel('numbers')
    fileName = str("F:/Programming/thesis/CostofBeingOvertook/"+raceDict[raceId]+"CostofBeingOvertook.eps")
    plt.savefig(fileName)
    plt.show()

    print(len(overtakeList)," overtakes in all\n")
    
    
def main():
    getResult(862)
    getResult(882)
    getResult(903)
    getResult(928)
    getResult(950)
    getResult(970)
    getResult(991)
       
if __name__ == '__main__':
    main()