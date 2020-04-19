# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 23:47:16 2020

@author: Billy
"""

import threading
import time
import pandas as pd
import re
import sys
sys.setrecursionlimit(10000)
from datetime import datetime

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
pd.set_option('display.max_columns',None)
pd.set_option('display.width', 1000)    

overlapCostList = list()
beOverlapCostList = list()

class Race(object):
    codeTuple = tuple()
    lastPitLapTuple = tuple()
    pursuerList = list()
    headerList = list()
    timeCostDict = dict()
    lastLapTuple = tuple()
    lapDict = dict()
    pitTimesDict = dict()
    lastPitDict = dict()
    driverLastLapTimeDict = dict()
    raceData = 0
    currentTime = 0
    renewOrder = 0
    currentLap = 0
    dropRacer = list()
    result = pd.DataFrame(columns=('code', 'raceId', 'lap', 'position', 'time', 'milliseconds', 'stint1', 'stint2', 'stint3', 'stint4', 'stint5', 'stint6','totalTimeCost','timeGap','selfComparison','tyreCondition'))
    
    def overLapping(self,currentRacer):
        currentPosition = tuple(self.result['code']).index(currentRacer)
        for key in tuple(self.result['code']):
            nextLap = self.raceData[self.raceData['lap'].isin([int(self.result.iloc[currentPosition,2])+1])]
            headerPosition = tuple(self.result['code']).index(key)
            if key not in tuple(nextLap['code']):
                continue
            if tuple(self.result['code']).index(key) <= currentPosition:
                continue
            if "PIT" in self.result.iloc[headerPosition,15]:
                continue
            if int(self.result.iloc[headerPosition,2]) == self.lastPitDict[key] + 1:
                continue
            if int(self.result.iloc[headerPosition,2]) + 1 == self.lastPitDict[key] + int(re.search(r'\d+',str(self.result.iloc[headerPosition,6+self.pitTimesDict[key]])).group()):
                continue
            if int(self.result.iloc[currentPosition,2]) + 1 == self.lastPitDict[currentRacer] + int(re.search(r'\d+',str(self.result.iloc[currentPosition,6+self.pitTimesDict[currentRacer]])).group()):
                continue
            if int(self.result.iloc[currentPosition,2]) == self.lastPitDict[currentRacer] + 1:
                continue
            if "PIT" in self.result.iloc[currentPosition,15]:
                continue
            else:
                nextLaptimePursuer = nextLap[nextLap['code'].isin([currentRacer])].iloc[0,5]
                timeDelta = self.timeCostDict[key] - self.currentTime
                if timeDelta > nextLaptimePursuer:
                    self.pursuerList.append(currentRacer)
                    self.headerList.append(key)
                    #headerList.append(key)
                    #lapList.append(self.result.iloc[tuple(self.result['code']).index(key),2])
                
    def tyreCondition(self,inputDataFrame):
        allTyreChoice = str()
        for key,value in self.pitTimesDict.items():
            if key == inputDataFrame.iloc[0,0]:
                expectedLapsOnTyre = re.search(r'\d+',str(inputDataFrame.iloc[0,6+value])).group()
                currentTyre = re.search(r'^[a-zA-Z]*\s*[a-zA-Z]*',str(inputDataFrame.iloc[0,6+value])).group()
                if int(inputDataFrame.iloc[0,2]) == self.lastPitDict[key] + int(expectedLapsOnTyre):
                    allTyreChoice = str(int(inputDataFrame.iloc[0,2])-self.lastPitDict[key])+" "+currentTyre+'\033[35m PIT\033[0m'
                    self.pitTimesDict[key] += 1
                    self.lastPitDict[key] = int(inputDataFrame.iloc[0,2])
                else:
                    allTyreChoice = str(int(inputDataFrame.iloc[0,2])-self.lastPitDict[key])+" "+currentTyre 
        return allTyreChoice
    
    def findPosition(self,newestRecord):
        if len(self.result['lap']) == 0:
            return 0
        else:
            for i, value in enumerate(self.result['lap'].tolist()):
                if int(newestRecord['lap']) > int(value) :
                    return i
            return len(set(self.result['code']))
                    
    
    def output(self,racerInput,key): 
        dropFlag = False
        for value in self.dropRacer:
            dropFlag = True
            self.result = self.result[self.result.code != value]
        if dropFlag:
            self.dropRacer = list()
        temp = {col: racerInput[col].tolist() for col in racerInput.columns}
        for tempKey, value in temp.items():
            temp[tempKey] = str(temp[tempKey]).strip('[]').strip('\'')
        temp['totalTimeCost'] = self.timeCostDict[key]
        temp['timeGap'] = ''
        self.renewOrder = self.findPosition(temp) 
        emptyFlag = True
        for i, resultKey in enumerate(self.result['code'].tolist()):
            if key == resultKey:
                emptyFlag = False
                negativeFlag = False
                selfTimeStamp = int(temp['milliseconds'])-self.driverLastLapTimeDict[key]
                for value in self.pursuerList:
                    if key == value :
                        overlapCostList.append(selfTimeStamp)
                        self.pursuerList.remove(key)
                for value in self.headerList:
                    if key == value :
                        beOverlapCostList.append(selfTimeStamp)
                        self.headerList.remove(key)
                self.driverLastLapTimeDict[key] = int(temp['milliseconds'])
                selfTimeStamp /= 1000.0
                if selfTimeStamp < 0:
                    selfTimeStamp = -selfTimeStamp
                    negativeFlag = True               
                timearr = datetime.fromtimestamp(selfTimeStamp)
                otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
                if negativeFlag:
                    temp['selfComparison']='\033[32m'+'-'+ otherStyleTime  +'\033[0m'
                else:
                    temp['selfComparison']='\033[31m'+'+'+ otherStyleTime  +'\033[0m'
                self.result = self.result[self.result.code != key]
                df1 = self.result.loc[:self.renewOrder-1]
                df2 = self.result.loc[self.renewOrder:]
                df3 = pd.DataFrame([temp])
                df3['tyreCondition'] = self.tyreCondition(df3)
                self.result = df1.append(df3, ignore_index = True).append(df2, ignore_index = True)
        if emptyFlag:
            temp['tyreCondition'] = self.tyreCondition(pd.DataFrame([temp])) 
            temp['selfComparison'] = '+00.00'
            self.driverLastLapTimeDict[key] = int(temp['milliseconds'])
            self.result.loc[self.renewOrder] = temp
        timeStamp = temp['totalTimeCost'] - int(self.result.iloc[0,12])
        timeStamp /= 1000.0
        timearr = datetime.fromtimestamp(timeStamp)
        otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
        timeGap = str("+"+otherStyleTime)
        self.result.iloc[self.renewOrder,13] = timeGap   
        #print(self.result[['code','lap','position','time','timeGap','selfComparison','tyreCondition']])
              
                
        
    def fun_timer(self): 
        dropFlag = False
        for key,value in self.timeCostDict.items():
            if self.currentTime >= value:
                thisLap = self.raceData[self.raceData['lap'].isin([self.lapDict[key]])]
                thisLap = thisLap.reset_index(drop=True)
                if self.renewOrder == 0:
                    self.codeTuple = tuple(set(thisLap['code']))      
                self.output(thisLap[thisLap['code'] == key], key)
                nextLap = self.raceData[self.raceData['lap'].isin([self.lapDict[key]+1])]
                nextLap = nextLap.reset_index(drop=True)
                if key in set(nextLap['code']):
                    nextLaptime = nextLap[nextLap['code'] == key].iloc[0,5]
                    self.timeCostDict[key] += nextLaptime
                    self.lapDict[key] += 1
                    self.overLapping(key)
                else:
                    dropFlag = True
                    self.dropRacer.append(key)
        if dropFlag:
            for racer in self.dropRacer:
                del self.timeCostDict[racer]
                del self.lapDict[racer]
        
        if len(tuple(self.result['code'])) == 0:
            self.currentLap = 1
        else:
            self.currentLap = self.lapDict[tuple(self.result['code'])[0]]
        self.currentTime += 100
        
        
    def __init__(self, raceId):
        self.raceId = raceId
        self.raceData = merged[merged['raceId'].isin([raceId])]
        self.raceData = self.raceData.reset_index(drop=True)
        self.codeTuple = tuple(set(self.raceData['code']))
        self.lastPitLapTuple = (0,)*len(self.codeTuple)
        self.timeCostDict = dict(zip(self.codeTuple,self.lastPitLapTuple))
        self.lastLapTuple = (1,)*len(self.codeTuple)
        self.lapDict = dict(zip(self.codeTuple,self.lastLapTuple))
        self.lastPitDict = dict(zip(self.codeTuple,self.lastPitLapTuple))
        self.pitTimesDict = dict(zip(self.codeTuple,self.lastPitLapTuple))
        self.driverLastLapTimeDict = dict(zip(self.codeTuple,self.lastPitLapTuple))
        firstLap = self.raceData[self.raceData['lap'].isin([1])]
        firstLap = firstLap.reset_index(drop=True)
        for i in range(len(set(firstLap['code']))):
            for key,value in self.timeCostDict.items():
                if key == firstLap['code'][i]:
                    currentLapTime = firstLap.iloc[i,5]
                    self.timeCostDict[key] = currentLapTime
        while self.currentLap < len(set(self.raceData['lap'])):
                self.fun_timer()
    
        
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
                    timeStamp = timeCostDict[key]
                    timeGapList.append(timeStamp)
        return timeGapList


def main():
    race2018 = Race(862) 
    print(overlapCostList)
    print(beOverlapCostList)
    
if __name__ == '__main__':
    main()