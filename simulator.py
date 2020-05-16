# -*- coding: utf-8 -*-
"""
Created on Fri May 15 23:59:39 2020

@author: Billy
"""
import fastTeamLapTimeGenerator as hamLTG
import overtake as otkCalculator
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
pd.set_option('display.max_columns',None)
pd.set_option('display.width', 1000)    

class Race(object):
    raceId = 0                                                                  # the ID that tell what race it is
    codes = tuple()                                                             # Tuple used for initiating other dictionaries
    lastPitLap = tuple()                                                        # Tuple created for initiatng variables
    pitTimes = dict()                                                           # How many times the racer had pitted
    lastLap = tuple()                                                           # Stores last lap number
    currentTime = 0                                                             # Stores current time by accumulting
    renewOrder = 0                                                              # Predicted location for the next lap
    dropRacer = list()                                                          # Racers that will not be racing in the next lap
    fastDrivers = list()                                                        # Operable and modeled six racers 
    timeCosts = dict()                                                          # Time counter from the start to the next lap
    lap = dict()                                                                # Current lap 
    lastPit = dict()                                                            # Stores the lap where the last pit happens
    driverNextLapTime = dict() 
    driverLastLapTime = dict()
    raceData = 0                                                                # Specific race data for one mathch
    endFlag = False                                                             # Whether user called for quit or not
    pauseFlag = False                                                           # Whether user called pause or not
    raceEndFlag = False                                                         # Wheter the race is ended or not
    dropFlag = False
    sortFlag = False    
    lateInstructionFlag = False                                                 # Whether too late for giving instruction at this lap or not

    """
    The output result for every update
    """
    result = pd.DataFrame(columns=('code', 'raceId', 'lap', 'position', 'time', 'milliseconds','totalTimeCost','timeGap','selfComparison','tyreCondition')) 
    
    def __init__(self, raceId, choosenDriver):
        
        """
        class variables initiation
        """
        self.player = choosenDriver
        self.raceId = raceId
        self.raceData = merged[merged['raceId'].isin([raceId])] 
        self.raceData = self.raceData.reset_index(drop=True)
        self.codes = tuple(set(self.raceData['code']))
        self.lastPitLap = (0,)*len(self.codes)
        self.timeCosts = dict(zip(self.codes,self.lastPitLap))
        self.lastLap = (1,)*len(self.codes)
        self.lap = dict(zip(self.codes,self.lastLap))
        self.lastPit = dict(zip(self.codes,self.lastPitLap))
        self.pitTimes = dict(zip(self.codes,self.lastPitLap))
        self.driverLastLapTime = dict(zip(self.codes,self.lastPitLap))
        self.driverNextLapTime = dict(zip(self.codes,self.lastPitLap))
        self.fastDrivers = ["HAM","BOT","LEC","VET","VER","GAS"]
        
        if self.player == 'GAS':
            tyreChoice.loc[(tyreChoice['code']== choosenDriver) & (tyreChoice['raceId']==self.raceId), 2] =  'Used soft (56)'
        else:
            tyreChoice.loc[(tyreChoice['code']== choosenDriver) & (tyreChoice['raceId']==self.raceId), 2] =  'Used medium (56)'
        
        """
        Preload first lap statistics before started
        """
        
        firstLap = self.raceData[self.raceData['lap'].isin([1])]
        firstLap = firstLap.reset_index(drop=True)
        for i in range(len(set(firstLap['code']))):
            if firstLap['code'][i] in self.fastDrivers:
                if firstLap['code'][i] == "GAS":
                    currentLapTime = int(hamLTG.startOff(int(hamLTG.lapTimeUsedSoft(2,firstLap['code'][i])),firstLap['code'][i]))
                else:
                    currentLapTime = int(hamLTG.startOff(int(hamLTG.lapTimeUsedMedium(2,firstLap['code'][i])),firstLap['code'][i]))
                self.timeCosts[firstLap['code'][i]] = currentLapTime
                self.driverLastLapTime[firstLap['code'][i]] = currentLapTime
                self.driverNextLapTime[firstLap['code'][i]] = currentLapTime
                self.raceData.loc[(self.raceData['code']== firstLap['code'][i]) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lap[firstLap['code'][i]]), 'milliseconds'] =  currentLapTime
                continue
            for key,value in self.timeCosts.items():
                if key == firstLap['code'][i]:
                    currentLapTime = firstLap.iloc[i,5]
                    self.timeCosts[key] = currentLapTime
                    self.driverLastLapTime[key] = currentLapTime  
        self.timeCosts = dict(sorted(self.timeCosts.items(), key=lambda x: x[1]))
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            print("You can now give instructions to "+ self.player +" by pressing \"P\" at any time.")
            print("The race is about to Start. Press \"ENTER\" to launch. Press \"Q\" at any time to quit")
            print("Good Luck!")
            listener.join()    
        
    def output(self,racerInput,key):
        temp = {col: racerInput[col].tolist() for col in racerInput.columns}
        for tempKey, value in temp.items():
            temp[tempKey] = str(temp[tempKey]).strip('[]').strip('\'')
        temp['totalTimeCost'] = self.timeCosts[key]
        temp['timeGap'] = ''
        self.renewOrder = self.findPosition(temp)
        emptyFlag = True
        for i, resultKey in enumerate(self.result['code'].tolist()):
            if key == resultKey:
                emptyFlag = False
                negativeFlag = False
                selfTimeStamp = int(temp['milliseconds'])-self.driverLastLapTime[key]
                self.driverLastLapTime[key] = int(temp['milliseconds'])
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
                temp['time'] = str(self.timeTransformer(int(temp['milliseconds'])))
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
        for key,value in self.pitTimes.items():
            if key == inputDataFrame.iloc[0,0]:
                driverTyreInfo = tyreChoice[tyreChoice['raceId'].isin([self.raceId]) & tyreChoice['code'].isin([key])]
                expectedLapsOnTyre = re.search(r'\d+',str(driverTyreInfo.iloc[0,2+value])).group()
                currentTyre = re.search(r'^[a-zA-Z]*\s*[a-zA-Z]*',str(driverTyreInfo.iloc[0,2+value])).group()
                if int(inputDataFrame.iloc[0,2]) == self.lastPit[key] + int(expectedLapsOnTyre):
                    allTyreChoice = str(int(inputDataFrame.iloc[0,2])-self.lastPit[key])+" "+currentTyre+'\033[35m PIT\033[0m'
                    self.pitTimes[key] += 1
                    self.lastPit[key] = int(inputDataFrame.iloc[0,2])
                else:
                    allTyreChoice = str(int(inputDataFrame.iloc[0,2])-self.lastPit[key])+" "+currentTyre 
        return allTyreChoice  
    
    def timeTransformer(self,inputTime):
        inputTime /= 1000
        timearr = datetime.fromtimestamp(inputTime)
        otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
        outputTime = str(otherStyleTime)
        return outputTime
        
    def fun_timer(self,event):
        if self.pauseFlag:
            event.wait()
        self.dropFlag = False
        self.sortFlag = False
        for key,value in self.timeCosts.items():
            if (self.currentTime >= value):
                self.sortFlag = True
                thisLap = self.raceData[self.raceData['lap'].isin([self.lap[key]])]
                thisLap = thisLap.reset_index(drop=True)
                if(self.lap[key] == 56):
                    self.raceEndFlag = True
                self.output(thisLap[thisLap['code'] == key], key)
                self.endJudgement(key)
                self.nextLap(key)
        if self.dropFlag:
            tempNameList = list()
            for racer in self.dropRacer:
                if(self.lap[racer] == 56):
                    tempNameList.append(racer)
                del self.timeCosts[racer]
                del self.lap[racer]
            self.dropRacer = list()
        if self.sortFlag:
            self.timeCosts = dict(sorted(self.timeCosts.items(), key=lambda x: x[1]))
        if not self.endFlag:
            self.currentTime += 1000
            self.timer = threading.Timer(0.0001, self.fun_timer,args=(self.event,))
            self.timer.start()
        else:
            self.timer.cancel()
            
    def endJudgement(self,key):
        if((key == self.player) & (self.raceEndFlag)):
            position = list(self.result['code']).index(self.player)+1
            print("The race ended. You are "+ str(position))
            k = Controller()
            k.press('q')
            k.release('q')
            
    def nextLap(self,key):
        nextLap = self.raceData[self.raceData['lap'].isin([self.lap[key]+1])]
        nextLap = nextLap.reset_index(drop=True)
        if key in set(nextLap['code']):
            if key in self.fastDrivers:
                if (self.lap[key] == self.lastPit[key]):
                    outLapTime = self.raceData[(self.raceData['code'] == key) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lap[key]+1)].iloc[0,5]
                    self.timeCosts[key] += outLapTime
                    self.driverNextLapTime[key] = outLapTime
                    self.lap[key] += 1                                  
                elif self.lap[key] == 1:
                    if key == "GAS":
                        self.driverNextLapTime[key] = int(hamLTG.virtualSafetyCar(int(hamLTG.lapTimeUsedSoft(2,key)),key))
                    else:
                        self.driverNextLapTime[key] = int(hamLTG.virtualSafetyCar(int(hamLTG.lapTimeUsedMedium(2,key)),key))
                    self.raceData.loc[(self.raceData['code']== key) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lap[key]+1), 'milliseconds'] =  self.driverNextLapTime[key]
                    self.timeCosts[key] += self.driverNextLapTime[key]
                    self.lap[key] += 1                                                       
                else:
                    driverTyreInfo = tyreChoice[tyreChoice['raceId'].isin([self.raceId]) & tyreChoice['code'].isin([key])]
                    currentTyre = str(re.search(r'^[a-zA-Z]*\s*[a-zA-Z]*',str(driverTyreInfo.iloc[0,2+self.pitTimes[key]])).group())
                    expectedLapsOnTyre = int(re.search(r'\d+',str(driverTyreInfo.iloc[0,2+self.pitTimes[key]])).group())
                    currentTyre = currentTyre.strip()
                    if currentTyre == 'Used medium':
                        self.driverNextLapTime[key] = int(hamLTG.lapTimeUsedMedium(self.lap[key]-self.lastPit[key]+1,key))
                    elif currentTyre == 'Used soft':
                        self.driverNextLapTime[key] = int(hamLTG.lapTimeUsedSoft(self.lap[key]-self.lastPit[key]+1,key))
                    elif currentTyre == 'Soft': 
                        self.driverNextLapTime[key] = int(hamLTG.lapTimeNewSoft(self.lap[key]-self.lastPit[key]+1,key))
                    elif currentTyre == 'Medium':
                        self.driverNextLapTime[key] = int(hamLTG.lapTimeNewMedium(self.lap[key]-self.lastPit[key]+1,key))
                    elif currentTyre == 'Hard':
                        self.driverNextLapTime[key] = int(hamLTG.lapTimeNewHard(self.lap[key]-self.lastPit[key]+1,key))
                    if self.lap[key]-self.lastPit[key] == expectedLapsOnTyre-1:
                         self.driverNextLapTime[key] = int(hamLTG.pitTimeGenerate(self.driverNextLapTime[key],'','in',key))
                    self.overtake(key)
                    self.raceData.loc[(self.raceData['code']== key) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lap[key]+1), 'milliseconds'] =  self.driverNextLapTime[key]
                    self.timeCosts[key] += self.driverNextLapTime[key]
                    self.lap[key] += 1                       
            else:
                self.driverNextLapTime[key] = nextLap[nextLap['code'] == key].iloc[0,5]
                self.timeCosts[key] += nextLap[nextLap['code'] == key].iloc[0,5]
                self.lap[key] += 1
        else:
            self.dropFlag = True
            self.dropRacer.append(key)
    
    def overtake(self,key):
        pursuerLoc = pd.Index(list(self.result['code'])).get_loc(key)
        leader = str(self.result.iloc[pursuerLoc-1,0])
        gap = int(self.result.iloc[pursuerLoc,6]-self.result.iloc[pursuerLoc-1,6])
        adv = int(self.driverNextLapTime[leader]-self.driverNextLapTime[key])  
        if (adv-gap > 0) and gap < 1000 and not (self.lap[leader] == self.lastPit[leader] + 1) and not pursuerLoc == 0:
            overtakeCompensation = otkCalculator.overtakeJudgement(gap,adv)
            self.driverNextLapTime[key] += overtakeCompensation['pursuer']
            self.driverNextLapTime[leader] += overtakeCompensation['leader']
            self.timeCosts[leader] += overtakeCompensation['leader']                         
    
    event = threading.Event()
    timer = threading.Timer(0, fun_timer,args=(event,))
    
    def pitTimeGenerator(self,tyreType):
        self.pauseFlag = False
        driverTyreInfo = tyreChoice[tyreChoice['raceId'].isin([self.raceId]) & tyreChoice['code'].isin([self.player])]
        expectedLapsOnTyre = self.lap[self.player]-self.lastPit[self.player]
        currentTyre = re.search(r'^[a-zA-Z]*\s*[a-zA-Z]*',str(driverTyreInfo.iloc[0,2+self.pitTimes[self.player]])).group()
        changePosition = str('stint'+ str(int(1+self.pitTimes[self.player])))
        replaceString = currentTyre + " (" + str(expectedLapsOnTyre) +")"
        tyreChoice.loc[(tyreChoice['code']== self.player) & (tyreChoice['raceId']==self.raceId), changePosition] =  replaceString
        changePosition = str('stint'+ str(int(2+self.pitTimes[self.player])))
        replaceString = tyreType + " (56)"
        tyreChoice.loc[(tyreChoice['code']== self.player) & (tyreChoice['raceId']==self.raceId), changePosition] =  replaceString
        pitInTime  = hamLTG.pitTimeGenerate(self.driverNextLapTime[self.player],tyreType,'in',self.player)
        self.timeCosts[self.player] += (pitInTime-self.driverNextLapTime[self.player])
        self.driverNextLapTime[self.player] = pitInTime              
        pitOutTime  = hamLTG.pitTimeGenerate(self.driverNextLapTime[self.player],tyreType,'out',self.player)
        self.raceData.loc[(self.raceData['code']== self.player) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lap[self.player]), 'milliseconds'] =  pitInTime
        self.raceData.loc[(self.raceData['code']== self.player) & (self.raceData['raceId']==self.raceId) & (self.raceData['lap']==self.lap[self.player]+1), 'milliseconds'] =  pitOutTime
        self.event.set()
    
    """
    Keyboard Monitor
    """       
        
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
        if key == Key.esc and self.pauseFlag and self.lateInstructionFlag:
            self.pauseFlag = False
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
                if self.timeCosts[self.player] - self.currentTime <= 8000:
                    self.pauseFlag = True
                    self.lateInstructionFlag = True
                    print("Too close to the pit lane, give instruction in the next lap please.")
                    print("Press \"ESC\" to continue")
                else :
                    self.pauseFlag = True
                    print("Press \"1\" for Soft,\"2\" for Medium, \"3\" for Hard. Press \"ESC\" to continue")
                return True
        else:
            return True
        

def main():
    race2019 = Race(1012,"GAS")    
    
if __name__ == '__main__':
    main()