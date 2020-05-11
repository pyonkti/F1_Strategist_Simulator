# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 18:54:32 2020

@author: Billy

"""

import HamLapTimeGenerator as HamLTG
import threading
import pandas as pd
import re
from datetime import datetime
from pynput import keyboard
from pynput.keyboard import Key, Controller


lapTime = pd.read_csv("./learn/lap_times.csv")
driverInfo = pd.read_csv("./learn/drivers.csv")
driverInfo= driverInfo.drop(columns= ['driverRef','number','forename','surname','dob','nationality','url'], axis=1)
tyreChoice = pd.read_csv("./learn/tyre.csv")
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
    fastDriversList = list()
    timeCostDict = dict()
    lastLapTuple = tuple()
    lapDict = dict()
    pitTimesDict = dict()
    lastPitDict = dict()
    driverNextLapTimeDict = dict()
    driverLastLapTimeDict = dict()
    raceData = 0
    endFlag = False
    pauseFlag = False
    raceEndFlag = False
    lateInstructionFlag = False

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
    
    def output(self,racerInput,key):
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
                selfTimeStamp /= 1000
                if selfTimeStamp < 0:
                    selfTimeStamp = -selfTimeStamp
                    negativeFlag = True               
                timearr = datetime.fromtimestamp(selfTimeStamp)
                otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
                if negativeFlag:
                    temp['selfComparison']='\033[32m'+'-'+ otherStyleTime  +'\033[0m'
                else:
                    temp['selfComparison']='\033[31m'+'+'+ otherStyleTime  +'\033[0m'
                timeStamp = int(temp['milliseconds'])
                timeStamp /= 1000
                timearr = datetime.fromtimestamp(timeStamp)
                otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
                outputTime = str(otherStyleTime)
                temp['time'] = outputTime
                self.result = self.result[self.result.code != key]
                df1 = self.result.loc[:self.renewOrder-1]
                df2 = self.result.loc[self.renewOrder:]
                df3 = pd.DataFrame([temp])
                df3['tyreCondition'] = self.tyreCondition(df3)
                self.result = df1.append(df3, ignore_index = True).append(df2, ignore_index = True)
        if emptyFlag:
            temp['tyreCondition'] = self.tyreCondition(pd.DataFrame([temp])) 
            temp['selfComparison'] = '+00.00'
            timeStamp = int(temp['milliseconds'])
            timeStamp /= 1000
            timearr = datetime.fromtimestamp(timeStamp)
            otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
            outputTime = str(otherStyleTime)
            temp['time'] = outputTime
            self.result.loc[self.renewOrder] = temp
        gapTimeStamp = int(temp['totalTimeCost']) - int(self.result.iloc[0,6])
        gapTimeStamp /= 1000
        timearr = datetime.fromtimestamp(gapTimeStamp)
        otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
        timeGap = str("+"+otherStyleTime)
        self.result.iloc[self.renewOrder,7] = timeGap   
        print(self.result[['code','lap','time','milliseconds','timeGap','selfComparison','tyreCondition']])
        
    def fun_timer(self,event):
        if self.pauseFlag:
            event.wait()
        dropFlag = False
        sortFlag = False
        for key,value in self.timeCostDict.items():
            if (self.currentTime >= value):
                sortFlag = True
                thisLap = self.raceData[self.raceData['lap'].isin([self.lapDict[key]])]
                thisLap = thisLap.reset_index(drop=True)
                if self.renewOrder == 0:
                    self.codeTuple = tuple(set(thisLap['code']))
                if(self.lapDict[key] == 56):
                    self.raceEndFlag = True
                self.output(thisLap[thisLap['code'] == key], key)
                if((key == 'HAM') & (self.raceEndFlag)):
                    position = list(self.result['code']).index('HAM')+1
                    print("The race ended. You are "+ str(position))
                    k = Controller()
                    k.press('q')
                    k.release('q')
                nextLap = self.raceData[self.raceData['lap'].isin([self.lapDict[key]+1])]
                nextLap = nextLap.reset_index(drop=True)
                if key in set(nextLap['code']):
                    if key in self.fastDriversList:
                        if (self.lapDict[key] - self.lastPitDict[key] == 0):
                            outLapTime = self.raceData[(self.raceData['code'] == key) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lapDict[key]+1)].iloc[0,5]
                            self.timeCostDict[key] += outLapTime
                            self.driverNextLapTimeDict[key] = outLapTime
                            self.lapDict[key] += 1                                  
                        elif self.lapDict[key] == 1:
                            self.driverNextLapTimeDict[key] = int(HamLTG.virtualSafetyCar(int(HamLTG.lapTimeUsedMedium(2,key)),key))
                            self.raceData.loc[(self.raceData['code']== key) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lapDict[key]+1), 'milliseconds'] =  self.driverNextLapTimeDict[key]
                            self.timeCostDict[key] += self.driverNextLapTimeDict[key]
                            self.lapDict[key] += 1                                                       
                        else:
                            driverTyreInfo = tyreChoice[tyreChoice['raceId'].isin([self.raceId]) & tyreChoice['code'].isin([key])]
                            currentTyre = str(re.search(r'^[a-zA-Z]*\s*[a-zA-Z]*',str(driverTyreInfo.iloc[0,2+self.pitTimesDict[key]])).group())
                            currentTyre = currentTyre.strip()
                            if currentTyre == 'Used medium':
                                self.driverNextLapTimeDict[key] = int(HamLTG.lapTimeUsedMedium(self.lapDict[key]-self.lastPitDict[key]+1,key))
                                self.raceData.loc[(self.raceData['code']== key) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lapDict[key]+1), 'milliseconds'] =  self.driverNextLapTimeDict[key]
                                self.timeCostDict[key] += self.driverNextLapTimeDict[key]
                                self.lapDict[key] += 1
                            elif currentTyre == 'Soft': 
                                self.driverNextLapTimeDict[key] = int(HamLTG.lapTimeNewSoft(self.lapDict[key]-self.lastPitDict[key]+1,key))
                                self.raceData.loc[(self.raceData['code']== key) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lapDict[key]+1), 'milliseconds'] =  self.driverNextLapTimeDict[key]
                                self.timeCostDict[key] += self.driverNextLapTimeDict[key]
                                self.lapDict[key] += 1
                            elif currentTyre == 'Medium':
                                self.driverNextLapTimeDict[key] = int(HamLTG.lapTimeNewMedium(self.lapDict[key]-self.lastPitDict[key]+1,key))
                                self.raceData.loc[(self.raceData['code']== key) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lapDict[key]+1), 'milliseconds'] =  self.driverNextLapTimeDict[key]
                                self.timeCostDict[key] += self.driverNextLapTimeDict[key]
                                self.lapDict[key] += 1
                            elif currentTyre == 'Hard':
                                self.driverNextLapTimeDict[key] = int(HamLTG.lapTimeNewHard(self.lapDict[key]-self.lastPitDict[key]+1,key))
                                self.raceData.loc[(self.raceData['code']== key) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lapDict[key]+1), 'milliseconds'] =  self.driverNextLapTimeDict[key]
                                self.timeCostDict[key] += self.driverNextLapTimeDict[key]
                                self.lapDict[key] += 1
                    else:
                        self.driverNextLapTimeDict[key] = nextLap[nextLap['code'] == key].iloc[0,5]
                        self.timeCostDict[key] += nextLap[nextLap['code'] == key].iloc[0,5]
                        self.lapDict[key] += 1
                else:
                    dropFlag = True
                    self.dropRacer.append(key)

        if dropFlag:
            tempNameList = list()
            for racer in self.dropRacer:
                if(self.lapDict[racer] == 56):
                    tempNameList.append(racer)
                del self.timeCostDict[racer]
                del self.lapDict[racer]
            self.dropRacer = list()

        if sortFlag:
            self.timeCostDict = dict(sorted(self.timeCostDict.items(), key=lambda x: x[1]))
        if not self.endFlag:
            self.currentTime += 1000
            self.timer = threading.Timer(0.0001, self.fun_timer,args=(self.event,))
            self.timer.start()
        else:
            self.timer.cancel()
        
    event = threading.Event()
    timer = threading.Timer(0, fun_timer,args=(event,))
    def pitTimeGenerator(self,tyreType):
        self.pauseFlag = False
        driverTyreInfo = tyreChoice[tyreChoice['raceId'].isin([self.raceId]) & tyreChoice['code'].isin(['HAM'])]
        expectedLapsOnTyre = self.lapDict['HAM']-self.lastPitDict['HAM']
        currentTyre = re.search(r'^[a-zA-Z]*\s*[a-zA-Z]*',str(driverTyreInfo.iloc[0,2+self.pitTimesDict['HAM']])).group()
        changePosition = str('stint'+ str(int(1+self.pitTimesDict['HAM'])))
        replaceString = currentTyre + " (" + str(expectedLapsOnTyre) +")"
        tyreChoice.loc[(tyreChoice['code']== 'HAM') & (tyreChoice['raceId']==self.raceId), changePosition] =  replaceString
        changePosition = str('stint'+ str(int(2+self.pitTimesDict['HAM'])))
        replaceString = tyreType + " (56)"
        tyreChoice.loc[(tyreChoice['code']== 'HAM') & (tyreChoice['raceId']==self.raceId), changePosition] =  replaceString
        pitInTime  = HamLTG.pitTimeGenerate(self.driverNextLapTimeDict['HAM'],tyreType,'in','HAM')
        self.timeCostDict['HAM'] += (pitInTime-self.driverNextLapTimeDict['HAM'])
        self.driverNextLapTimeDict['HAM'] = pitInTime              
        pitOutTime  = HamLTG.pitTimeGenerate(self.driverNextLapTimeDict['HAM'],tyreType,'out','HAM')
        self.raceData.loc[(self.raceData['code']== 'HAM') & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lapDict['HAM']), 'milliseconds'] =  pitInTime
        self.raceData.loc[(self.raceData['code']== 'HAM') & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lapDict['HAM']+1), 'milliseconds'] =  pitOutTime
        self.event.set()
        
        
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
        if key == Key.esc and self.lateInstructionFlag:
            self.lateInstructionFlag = False
            self.event.set()
            return True
        if key.char is not None:
            if key.char == '1' and self.pauseFlag:
                self.pitTimeGenerator('Soft')
                return True
            elif key.char == '2' and self.pauseFlag:
                self.pitTimeGenerator('Medium')
                return True
            elif key.char == '3' and self.pauseFlag:
                self.pitTimeGenerator('Hard')
                return True
            if key.char == 'q':
                self.endFlag = True
                return False
            if key.char == 'p':
                self.event.clear()
                if self.timeCostDict['HAM'] - self.currentTime <= 8000:
                    self.lateInstructionFlag = True
                    print("Too close to the pit lane, give instruction in the next lap please.")
                    print("Press \"ESC\" to continue")
                else :
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
        self.driverNextLapTimeDict = dict(zip(self.codeTuple,self.lastPitLapTuple))
        self.fastDriversList = ["HAM","BOT","LEC","VET"]
        
        firstLap = self.raceData[self.raceData['lap'].isin([1])]
        firstLap = firstLap.reset_index(drop=True)
        for i in range(len(set(firstLap['code']))):
            if firstLap['code'][i] in self.fastDriversList:
                currentLapTime = int(HamLTG.startOff(int(HamLTG.lapTimeUsedMedium(2,firstLap['code'][i])),firstLap['code'][i]))
                self.timeCostDict[firstLap['code'][i]] = currentLapTime
                self.driverLastLapTimeDict[firstLap['code'][i]] = currentLapTime
                self.driverNextLapTimeDict[firstLap['code'][i]] = currentLapTime
                self.raceData.loc[(self.raceData['code']== firstLap['code'][i]) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lapDict[firstLap['code'][i]]), 'milliseconds'] =  currentLapTime
                continue
            for key,value in self.timeCostDict.items():
                if key == firstLap['code'][i]:
                    currentLapTime = firstLap.iloc[i,5]
                    self.timeCostDict[key] = currentLapTime
                    self.driverLastLapTimeDict[key] = currentLapTime
        self.timeCostDict = dict(sorted(self.timeCostDict.items(), key=lambda x: x[1]))
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            print("You can now give instructions to Lewis Hamilton(HAM) by pressing \"P\" at any time.")
            print("The race is about to Start. Press \"ENTER\" to launch. Press \"Q\" at any time to quit")
            print("Good Luck!")
            listener.join()

def main():
    race2019 = Race(1012)    
    
if __name__ == '__main__':
    main()