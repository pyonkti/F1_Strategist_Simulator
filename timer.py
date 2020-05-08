# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 18:54:32 2020

@author: Billy

"""

import HamLapTimeGenerator as HamLTG
import threading
import time
import pandas as pd
import re
from datetime import datetime
from pynput import keyboard
from pynput.keyboard import Key


lapTime = pd.read_csv(".\learn\lap_times.csv")
driverInfo = pd.read_csv(".\learn\drivers.csv")
driverInfo= driverInfo.drop(columns= ['driverRef','number','forename','surname','dob','nationality','url'], axis=1)
tyreChoice = pd.read_csv(".\learn\\tyre.csv")
merged = driverInfo.merge(lapTime, left_on='driverId', right_on = 'driverId', how = 'right')
merged = merged.drop(columns= ['driverId'], axis=1)
#merged = merged.merge(tyreChoice, how = 'right')
raceTuple = (862,882,903,928,950,970,991,1012)
yearTuple = ("2012","2013","2014","2015","2016","2017","2018","2019")
raceDict = dict(zip(raceTuple,yearTuple))
pd.set_option('display.max_columns',None)
pd.set_option('display.width', 1000)    

class Race(object):
    codeTuple = tuple()
    lastPitLapTuple = tuple()
    currentTime = 0
    renewOrder = 0
    dropRacer = list()
    timeCostDict = dict()
    lastLapTuple = tuple()
    lapDict = dict()
    pitTimesDict = dict()
    lastPitDict = dict()
    driverLastLapTimeDict = dict()
    raceData = 0
    endFlag = False
    pauseFlag = False
    result = pd.DataFrame(columns=('code', 'raceId', 'lap', 'position', 'time', 'milliseconds','totalTimeCost','timeGap','selfComparison','tyreCondition'))
    
    def findPosition(self,newestRecord):
        if len(self.result['lap']) == 0:
            return 0
        else:
            for i, value in enumerate(self.result['lap'].tolist()):
                if int(newestRecord['lap']) > int(value) :
                    return i
            return len(set(self.result['code']))
        
    def tyreCondition(self,inputDataFrame):
        allTyreChoice = str()
        for key,value in self.pitTimesDict.items():
            if key == inputDataFrame.iloc[0,0]:
                driverTyreInfo = tyreChoice[tyreChoice['raceId'].isin([self.raceId]) & tyreChoice['code'].isin([key])]
                expectedLapsOnTyre = re.search(r'\d+',str(driverTyreInfo.iloc[0,2+value])).group()
                currentTyre = re.search(r'^[a-zA-Z]*\s*[a-zA-Z]*',str(driverTyreInfo.iloc[0,2+value])).group()
                if int(inputDataFrame.iloc[0,2]) == self.lastPitDict[key] + int(expectedLapsOnTyre):
                    allTyreChoice = str(int(inputDataFrame.iloc[0,2])-self.lastPitDict[key])+" "+currentTyre+'\033[35m PIT\033[0m'
                    self.pitTimesDict[key] += 1
                    self.lastPitDict[key] = int(inputDataFrame.iloc[0,2])
                else:
                    allTyreChoice = str(int(inputDataFrame.iloc[0,2])-self.lastPitDict[key])+" "+currentTyre 
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
                    timeStamp = timeCostDict[key]
                    timeGapList.append(timeStamp)
        return timeGapList                    
    
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
            temp['milliseconds'] = self.driverLastLapTimeDict[key]
            timeStamp = temp['milliseconds']
            timeStamp /= 1000.0
            timearr = datetime.fromtimestamp(timeStamp)
            otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
            outputTime = str(otherStyleTime)
            temp['time'] = outputTime
            self.result.loc[self.renewOrder] = temp
        timeStamp = temp['totalTimeCost'] - int(self.result.iloc[0,6])
        timeStamp /= 1000.0
        timearr = datetime.fromtimestamp(timeStamp)
        otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
        timeGap = str("+"+otherStyleTime)
        self.result.iloc[self.renewOrder,7] = timeGap   
        print(self.result[['code','lap','time','timeGap','selfComparison','tyreCondition']])
        
    def fun_timer(self,event):
        if self.pauseFlag:
            event.wait()
        dropFlag = False
        for key,value in self.timeCostDict.items():
            if self.currentTime >= value:
                thisLap = self.raceData[self.raceData['lap'].isin([self.lapDict[key]])]
                thisLap = thisLap.reset_index(drop=True)
                if self.renewOrder == 0:
                    self.codeTuple = tuple(set(thisLap['code']))
                racerInput = thisLap[thisLap['code'] == key]
                racerInput.iloc
                self.output(thisLap[thisLap['code'] == key], key)
                nextLap = self.raceData[self.raceData['lap'].isin([self.lapDict[key]+1])]
                nextLap = nextLap.reset_index(drop=True)
                if key in set(nextLap['code']):
                    self.timeCostDict[key] += nextLap[nextLap['code'] == key].iloc[0,5]
                    self.lapDict[key] += 1
                else:
                    dropFlag = True
                    self.dropRacer.append(key)
        if dropFlag:
            for racer in self.dropRacer:
                del self.timeCostDict[racer]
                del self.lapDict[racer]
        if not self.endFlag:
            self.currentTime += 100
            self.timer = threading.Timer(0.0001, self.fun_timer,args=(self.event,))
            self.timer.start()
        else:
            self.timer.cancel()
        
    event = threading.Event()
    timer = threading.Timer(0, fun_timer,args=(event,))
    
    def on_press(self,key):
        pass
    
    def on_release(self,key):
        if key == Key.enter:
            self.timer = threading.Timer(0, self.fun_timer, args =(self.event,))
            self.timer.start()
            if self.endFlag:
                self.timer.cancel()
            return True 
        if key == Key.esc and self.pauseFlag:
            self.pauseFlag = False
            self.event.set()
            return True
        if key.char == 'q':
            self.endFlag = True
            return False
        if key.char == 'p':
            self.event.clear()
            self.pauseFlag = True
            print("Press \"1\" for Soft,\"2\" for Medium, \"3\" for Hard. Press \"ESC\" to continue")
            return True
        else:
            return True
        
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
            if firstLap['code'][i] == "HAM":
                currentLapTime = HamLTG.startOff(int(HamLTG.lapTimeUsedMedium(2)))
                self.timeCostDict[firstLap['code'][i]] = currentLapTime
                self.driverLastLapTimeDict[firstLap['code'][i]] = currentLapTime
                continue
            for key,value in self.timeCostDict.items():
                if key == firstLap['code'][i]:
                    currentLapTime = firstLap.iloc[i,5]
                    self.timeCostDict[key] = currentLapTime
                    self.driverLastLapTimeDict[key] = currentLapTime
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            print("The race is about to Start. Press \"ENTER\" to launch. Press \"Q\" at any time to quit")
            listener.join()

def main():
    race2019 = Race(1012)    
    
if __name__ == '__main__':
    main()
    

