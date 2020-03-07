# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
 
import pandas as pd
import re 
import time
from pynput import keyboard
from pynput.keyboard import Key
from datetime import datetime
                                                                                                                                                                                                                                                               
lapTime = pd.read_csv(".\learn\lap_times.csv",skiprows=range(1,428568),nrows=1115)
lapTime= lapTime.drop(columns= ['raceId'], axis=1)
driverInfo = pd.read_csv(".\learn\drivers.csv")
driverInfo= driverInfo.drop(columns= ['driverRef','number','forename','surname','dob','nationality','url'], axis=1)
tyreChoice = pd.read_csv(".\learn\\tyre.csv")
merged = driverInfo.merge(lapTime, left_on='driverId', right_on = 'driverId', how = 'right')
merged = merged.drop(columns= ['driverId'], axis=1)
merged = merged.merge(tyreChoice, left_on='code', right_on = 'code', how = 'right')
codeTuple = tuple(set(merged['code']))
lastPitLapTuple = (0,)*20
lastPitDict = dict(zip(codeTuple,lastPitLapTuple))
pitTimesDict = dict(zip(codeTuple,lastPitLapTuple))
timeCostDict = dict(zip(codeTuple,lastPitLapTuple))
driverLastLapTimeDict = dict(zip(codeTuple,lastPitLapTuple))
endFlag = False

print("The race starts! Press Enter to check lap 1\n")

def on_press(key):
    pass
    
def on_release(key):
    if key == Key.enter:
        return False 
    if key.char == 'q':
        global endFlag
        endFlag = True
        return False
    
def tyreCondition(currentLap,inputDataFrame):
    allTyreChoice = list()
    for i in range(len(set(inputDataFrame['code']))):
        for key,value in pitTimesDict.items():
            if key == inputDataFrame['code'][i]:
                expectedLapsOnTyre = re.search(r'\d+',str(inputDataFrame.iloc[i,8+value])).group()
                currentTyre = re.search(r'^[a-zA-Z]*\s*[a-zA-Z]*',str(inputDataFrame.iloc[i,8+value])).group()
                if currentLap == lastPitDict[key] + int(expectedLapsOnTyre):
                    allTyreChoice.append(str(currentLap-lastPitDict[key])+" "+currentTyre+'\033[35m PIT\033[0m')
                else:
                    allTyreChoice.append(str(currentLap-lastPitDict[key])+" "+currentTyre)
                if currentLap == lastPitDict[key] + int(expectedLapsOnTyre):
                    pitTimesDict[key] += 1
                    lastPitDict[key] = currentLap
    return allTyreChoice

def timeGap(currentLap,inputDataFrame):
    timeGapList = list()
    for i in range(len(set(inputDataFrame['code']))):
        for key,value in timeCostDict.items():
            if key == inputDataFrame['code'][i]:
                currentLapTime = inputDataFrame.iloc[i,4]
                if currentLap == 1:
                    timeCostDict[key] = currentLapTime
                else:
                    timeCostDict[key] += currentLapTime
                timeStamp = timeCostDict[key] - timeCostDict[inputDataFrame['code'][0]]
                timeStamp /= 1000.0
                timearr = datetime.fromtimestamp(timeStamp)
                otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
                timeGapList.append("+"+otherStyleTime)
    return timeGapList

def selfTimeComparison(currentLap,inputDataFrame):
    timeComparisonList = list()
    for i in range(len(set(inputDataFrame['code']))):
        for key,value in driverLastLapTimeDict.items():
            if key == inputDataFrame['code'][i]:
                if currentLap == 1:
                    timeComparisonList.append('+00.00')
                    driverLastLapTimeDict[key] = inputDataFrame.iloc[i,4]
                else:
                    negativeFlag = False
                    timeStamp = inputDataFrame.iloc[i,4] - driverLastLapTimeDict[key]
                    timeStamp /= 1000.0
                    if timeStamp < 0:
                        timeStamp = -timeStamp
                        negativeFlag = True               
                    timearr = datetime.fromtimestamp(timeStamp)
                    otherStyleTime = datetime.strftime(timearr,"%M:%S.%f")[:-3]
                    if negativeFlag:
                        timeComparisonList.append('\033[32m'+'-'+ otherStyleTime  +'\033[0m')
                    else:
                        timeComparisonList.append('\033[31m'+'+'+ otherStyleTime +'\033[0m')
                    driverLastLapTimeDict[key] = inputDataFrame.iloc[i,4]
    return timeComparisonList
    
    
def nextLap(currentLap):
    result = merged[merged['lap'].isin([currentLap])]
    result = result.sort_values('position')
    result = result.reset_index(drop=True)
    tyreConditionList = tyreCondition(currentLap,result)
    timeGapList = timeGap(currentLap,result)
    driverSelfComparisonList = selfTimeComparison(currentLap,result)
    result['time gap'] = timeGapList
    result['self comparison'] = driverSelfComparisonList
    result['tyres'] = tyreConditionList
    result = result.drop(columns= ['milliseconds','stint1','stint2','stint3'], axis=1)
    print(result)
    print("\nPress Enter to check next lap or press Q to quit\n")

def main():
    i = 1
    for i in set(merged.lap):
        with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
                listener.join()
        
        if endFlag == True:
            break
        nextLap(i)
        i+=1
        
if __name__ == '__main__':
    main()
