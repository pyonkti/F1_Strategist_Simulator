# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 18:54:32 2020

@author: Billy
"""

import threading
import time
import pandas as pd

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

class Race(object):
    codeTuple = tuple()
    lastPitLapTuple = tuple()
    timeCostDict = dict()
    lastLapTuple = tuple()
    lapDict = dict()
    raceData = 0
    currentTime = 0
    renewOrder = 0
    result = pd.DataFrame(columns=('code', 'raceId', 'lap', 'position', 'time', 'milliseconds', 'stint1', 'stint2', 'stint3', 'stint4', 'stint5', 'stint6','totalTimeCost'))
    
    def findPosition(self,newestRecord):
        if len(self.result['lap']) == 0:
            return 0
        else:
            for i, value in enumerate(self.result['lap'].tolist()):
                if newestRecord['lap'] > value :
                    return i
            return len(set(self.result['code']))
                    
    
    def output(self,racerInput,key): 
        temp = {col: racerInput[col].tolist() for col in racerInput.columns}
        for tempKey, value in temp.items():
            temp[tempKey] = str(temp[tempKey]).strip('[]').strip('\'')
        temp['totalTimeCost'] = self.timeCostDict[key]
        self.renewOrder = self.findPosition(temp) 
        emptyFlag = True
        for i, resultKey in enumerate(self.result['code'].tolist()):
            if key == resultKey:
                emptyFlag = False
                self.result = self.result[self.result.code != key]
                df1 = self.result.loc[:self.renewOrder-1]
                df2 = self.result.loc[self.renewOrder:]
                df3 = pd.DataFrame([temp])
                self.result = df1.append(df3, ignore_index = True).append(df2, ignore_index = True)
                print(self.result)
        if emptyFlag:
             self.result.loc[self.renewOrder] = temp
             print(self.result)
                
                
        
    def fun_timer(self): 
        dropFlag = False
        dropRacer = list()
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
                    self.timeCostDict[key] += nextLap[nextLap['code'] == key].iloc[0,5]
                    self.lapDict[key] += 1
                else:
                    dropFlag = True
                    dropRacer.append(key)
        if dropFlag:
            for racer in dropRacer:
                del self.timeCostDict[racer]
                del self.lapDict[racer]
                
        self.currentTime += 100
        self.timer = threading.Timer(0.0001, self.fun_timer)
        self.timer.start()
        
    timer = threading.Timer(0, fun_timer)
        
    def __init__(self, raceId):
        self.raceId = raceId
        self.raceData = merged[merged['raceId'].isin([raceId])]
        self.raceData = self.raceData.reset_index(drop=True)
        self.codeTuple = tuple(set(self.raceData['code']))
        self.lastPitLapTuple = (0,)*len(self.codeTuple)
        self.timeCostDict = dict(zip(self.codeTuple,self.lastPitLapTuple))
        self.lastLapTuple = (1,)*len(self.codeTuple)
        self.lapDict = dict(zip(self.codeTuple,self.lastLapTuple))
        firstLap = self.raceData[self.raceData['lap'].isin([1])]
        firstLap = firstLap.reset_index(drop=True)
        for i in range(len(set(firstLap['code']))):
            for key,value in self.timeCostDict.items():
                if key == firstLap['code'][i]:
                    currentLapTime = firstLap.iloc[i,5]
                    self.timeCostDict[key] = currentLapTime
        self.timer = threading.Timer(0, self.fun_timer)
        self.timer.start()
        time.sleep(100)
        self.timer.cancel()
    
        
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
    race2018 = Race(970)    
if __name__ == '__main__':
    main()
    

