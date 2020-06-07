# -*- coding: utf-8 -*-
"""
Created on Tue May 12 19:04:32 2020

Overtake Logistic Part

@author: Billy
"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import random

gapPossibility = [1.0, 1.25, 1.0, 0.41666667, 0.75, 0.48484848, 0.71428571, 0.36538462, 0.34328358, 0.25714286, 0.35616438, 0.22666667, 0.19277108, 0.15873016, 0.11428571, 0.31707317, 0.16129032, 0.11538462, 0.2]
gapPossibility = np.array(gapPossibility)

advPossibility = [0.13131313, 0.1, 0.21538462, 0.15384615, 0.11764706, 0.13888889, 0.11111111, 0.32142857, 0.28571429, 0.26086957, 0.34782609, 0.25, 0.33333333, 0.26666667, 0.2, 0.18181818, 0.1875, 0.45, 0.5]
advPossibility = np.array(advPossibility)

costOfOvertake = [0.013888888888888888, 0.03819444444444445, 0.059027777777777776, 0.08680555555555555, 0.10069444444444445, 0.1388888888888889, 0.1736111111111111, 0.2361111111111111, 0.2743055555555556, 0.3263888888888889, 0.36458333333333337, 0.4340277777777778, 0.4791666666666667, 0.5243055555555556, 0.5520833333333334, 0.5659722222222222, 0.5902777777777778, 0.6180555555555556, 0.6319444444444444, 0.6458333333333333, 0.6527777777777777, 0.6597222222222221, 0.6666666666666665, 0.6736111111111109, 0.6770833333333331, 0.6805555555555554, 0.690972222222222, 0.6944444444444442, 0.6979166666666664]
costOfOvertake = np.array(costOfOvertake)

costofBeingOvertake = [0.010416666666666666, 0.017361111111111112, 0.024305555555555556, 0.03819444444444445, 0.04166666666666667, 0.06597222222222222, 0.06944444444444445, 0.08680555555555555, 0.10763888888888888, 0.12152777777777776, 0.13194444444444442, 0.14236111111111108, 0.17361111111111108, 0.23958333333333331, 0.3055555555555555, 0.36111111111111105, 0.41319444444444436, 0.48263888888888884, 0.5416666666666666, 0.6006944444444444, 0.6284722222222222, 0.6701388888888888, 0.6909722222222222, 0.7152777777777778, 0.732638888888889, 0.7500000000000001, 0.7812500000000001, 0.7847222222222223, 0.7986111111111112]
costofBeingOvertake= np.array(costofBeingOvertake)

xGapScatter = np.arange(0, 950, 50).tolist()
xGapLinear = np.linspace(0, 1000, 100)
xAdvScatter = np.arange(0, 1900, 100).tolist()
xAdvLinear = np.linspace(0, 2000, 100)

xCostOvertakeScatter = np.arange(-1000, 1900, 100).tolist()
xCostOvertakeLinear = np.linspace(-1000, 3000, 100)

def funcGap(x,a,b,c):
    return a/(x+b)+c

def funcCostofOvertake(x,a,b,c):
    result = a*np.exp(-np.exp(-b*(x-c)))
    return result

def funcCostofOvertakeReverse(x,a,b,c):
    result = c-np.log(-np.log(x/a))/b
    return result

def funcCostofBeingOvertake(x):
    result = 0.04655+(0.8645-0.04655)*np.exp(-np.exp(-0.001922*(x-563.1)))
    return result

def funcCostofBeingOvertakeReverse(x):
    result = 563.1-np.log(np.log((0.8645-0.04655)/(x-0.04655)))/0.001922
    return result

popt, pcov = curve_fit(funcCostofOvertake, xCostOvertakeScatter, costOfOvertake)
aCostOtking=popt[0]
bCostOtking=popt[1]
cCostOtking=popt[2]

"""
Following part is for drawing Curve fitted result for the Time cost of Overtaking and Being overtaken
"""

"""
yCostofOvertake = funcCostofOvertake(xCostOvertakeLinear,aCostOtking,bCostOtking,cCostOtking)
plot1=plt.plot(xCostOvertakeScatter, costOfOvertake, '*',label='original values')
plot2=plt.plot(xCostOvertakeLinear, yCostofOvertake, 'r',label='curve_fit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.title('Cost Of Overtaking')
plt.show()

yCostofBeOvertake = funcCostofBeingOvertake(xCostOvertakeLinear)
plot1=plt.plot(xCostOvertakeScatter, costofBeingOvertake, '*',label='original values')
plot2=plt.plot(xCostOvertakeLinear, yCostofBeOvertake, 'r',label='curve_fit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.title('Cost Of Being Overtaken')
plt.show()
"""

popt, pcov = curve_fit(funcGap, xGapScatter , gapPossibility)
aGap=popt[0]
bGap=popt[1]
cGap=popt[2]
yGap=funcGap(xGapLinear,aGap,bGap,cGap)

pAdv = np.polyfit(xAdvScatter , advPossibility , 3) 
def funcAdv(x):
    return pAdv[0]*x**3 + pAdv[1]*x**2 + pAdv[2]*x + pAdv[3]

"""
Following part is for drawing Curve fitted result for Overtake Probability on GAP and Lap Time Adv
"""

"""
plot1=plt.plot(xGapScatter, gapPossibility, '*',label='original values')
plot2=plt.plot(xGapLinear, yGap, 'r',label='curve_fit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.title('Possibility Scatter by Accumulation(GAP)')
plt.show()

yAdv = pAdv[0]*xAdvLinear**3 + pAdv[1]*xAdvLinear**2 + pAdv[2]*xAdvLinear + pAdv[3]
plt.plot(xAdvLinear, yAdv, 'r')
plt.scatter(xAdvScatter , advPossibility)
plt.title('Possibility Scatter by Accumulation(ADV)')
plt.show()
"""

def overtakeJudgement(gap,adv):
    overtakeResult = {"pursuer":0,"leader":0}  
    if adv < 1250:
        randomNumber = random.random()
        if (randomNumber <= funcGap(gap,aGap,bGap,cGap)):
            randomNumber = random.uniform(0.01,0.7)
            timeCostofOvertaker = int(funcCostofOvertakeReverse(randomNumber,aCostOtking,bCostOtking,cCostOtking))
            if timeCostofOvertaker < 0:
                timeCostofOvertaker = 0
            randomNumber = random.uniform(0.047,0.86)
            timeCostofLeader = int(funcCostofBeingOvertakeReverse(randomNumber))
            if  timeCostofLeader < 0:
                timeCostofLeader = 0
            overtakeResult['pursuer'] = timeCostofOvertaker
            overtakeResult['leader'] = timeCostofLeader
            return(overtakeResult)
        else:
            randomNumber = random.uniform(0.4,0.5)
            timeCostofOvertaker = int(funcCostofOvertakeReverse(randomNumber,aCostOtking,bCostOtking,cCostOtking))
            randomNumber = random.uniform(0.09,0.86)
            timeCostofLeader = int(funcCostofBeingOvertakeReverse(randomNumber))
            if timeCostofOvertaker - (adv-gap) <= 100:
                overtakeResult['pursuer'] = timeCostofLeader + adv-(gap-int(100 + 20 * random.normalvariate(0, 0.618))) 
            else:
                overtakeResult['pursuer'] = timeCostofLeader + adv-(gap-timeCostofOvertaker)  
            overtakeResult['leader'] = timeCostofLeader
            return(overtakeResult)
    else:
        gapFactor = funcGap(gap,aGap,bGap,cGap)
        advFactor = funcAdv(adv)
        randomNumber = random.random()
        if advFactor > gapFactor:         
            if (randomNumber <= advFactor):
                randomNumber = random.uniform(0.01,0.71)
                timeCostofOvertaker = int(funcCostofOvertakeReverse(randomNumber,aCostOtking,bCostOtking,cCostOtking))
                if timeCostofOvertaker < 0:
                    timeCostofOvertaker = 0
                randomNumber = random.uniform(0.047,0.86)
                timeCostofLeader = int(funcCostofBeingOvertakeReverse(randomNumber))
                if  timeCostofLeader < 0:
                    timeCostofLeader = 0
                overtakeResult['pursuer'] = timeCostofOvertaker
                overtakeResult['leader'] = timeCostofLeader
                return(overtakeResult)
            else:
                randomNumber = random.uniform(0.4,0.5)
                timeCostofOvertaker = int(funcCostofOvertakeReverse(randomNumber,aCostOtking,bCostOtking,cCostOtking))
                randomNumber = random.uniform(0.09,0.86)
                timeCostofLeader = int(funcCostofBeingOvertakeReverse(randomNumber))
                if timeCostofOvertaker - (adv-gap) <= 100:
                    overtakeResult['pursuer'] = timeCostofLeader + adv-(gap-int(100 + 20 * random.normalvariate(0, 0.618))) 
                else:
                    overtakeResult['pursuer'] = timeCostofLeader + adv-(gap-timeCostofOvertaker)  
                overtakeResult['leader'] = timeCostofLeader
                return(overtakeResult)
        else:
            if (randomNumber <= gapFactor):
                randomNumber = random.uniform(0.01,0.71)
                timeCostofOvertaker = int(funcCostofOvertakeReverse(randomNumber,aCostOtking,bCostOtking,cCostOtking))
                if timeCostofOvertaker < 0:
                    timeCostofOvertaker = 0
                randomNumber = random.uniform(0.047,0.86)
                timeCostofLeader = int(funcCostofBeingOvertakeReverse(randomNumber))
                if  timeCostofLeader < 0:
                    timeCostofLeader = 0
                overtakeResult['pursuer'] = timeCostofOvertaker
                overtakeResult['leader'] = timeCostofLeader
                return(overtakeResult)
            else:
                randomNumber = random.uniform(0.4,0.5)
                timeCostofOvertaker = int(funcCostofOvertakeReverse(randomNumber,aCostOtking,bCostOtking,cCostOtking))
                randomNumber = random.uniform(0.09,0.86)
                timeCostofLeader = int(funcCostofBeingOvertakeReverse(randomNumber))
                if timeCostofOvertaker - (adv-gap) <= 100:
                    overtakeResult['pursuer'] = timeCostofLeader + adv-(gap-int(100 + 20 * random.normalvariate(0, 0.618))) 
                else:
                    overtakeResult['pursuer'] = timeCostofLeader + adv-(gap-timeCostofOvertaker)  
                overtakeResult['leader'] = timeCostofLeader
                return(overtakeResult)