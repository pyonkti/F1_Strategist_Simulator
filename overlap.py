# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:23:24 2020

Overlap Logistic Part

@author: Billy
"""

from scipy.optimize import curve_fit
import numpy as np
from matplotlib import pyplot as plt 
import random

costOfOverlap = [0.00975609756097561, 0.00975609756097561, 0.014634146341463414, 0.04390243902439024, 0.07804878048780488, 0.15121951219512195, 0.1902439024390244, 0.25365853658536586, 0.3121951219512195, 0.424390243902439, 0.47804878048780486, 0.5707317073170731, 0.6390243902439023, 0.7170731707317072, 0.7707317073170731, 0.824390243902439, 0.8439024390243902, 0.8682926829268293, 0.8926829268292683, 0.9073170731707317, 0.9170731707317074, 0.9219512195121952, 0.926829268292683, 0.9317073170731708, 0.9317073170731708, 0.9317073170731708, 0.9365853658536586, 0.9365853658536586, 0.9365853658536586]
costOfOverlap = np.array(costOfOverlap)

costOfBeOverlapped = [0.03015075376884422, 0.04522613065326633, 0.09045226130653267, 0.12562814070351758, 0.1608040201005025, 0.24120603015075376, 0.3065326633165829, 0.37688442211055273, 0.5125628140703518, 0.5879396984924623, 0.6180904522613065, 0.6633165829145728, 0.6733668341708543, 0.6834170854271358, 0.7286432160804021, 0.7386934673366835, 0.7386934673366835, 0.7437185929648242, 0.748743718592965, 0.748743718592965, 0.748743718592965, 0.748743718592965, 0.748743718592965, 0.7738693467336685, 0.7738693467336685, 0.7738693467336685, 0.8040201005025127, 0.8040201005025127, 0.8040201005025127]
costOfBeOverlapped = np.array(costOfBeOverlapped)

xCostOverlapScatter = np.arange(-1000, 1900, 100).tolist()
xCostOverlapScatter2 = np.arange(-1000, 7700, 300).tolist()
xCostOverlapLinear = np.linspace(-1000, 3000, 100)
xCostOverlapLinear2 = np.linspace(-1000, 7700, 300)

def funcCostofOverlap(x,a,b,c):
    result = a*np.exp(-np.exp(-b*(x-c)))
    return result

def funcCostofOverlapReverse(x,a,b,c):
    result = c-np.log(-np.log(x/a))/b
    return result

def funcCostofBeingOverlapped(x):
    result = 0.04516+(0.7748-0.04516)*np.exp(-np.exp(- 0.00107*(x-1048)))
    return result

def funcCostofBeingOverlappedReverse(x):
    result = 1048-np.log(np.log((0.774-0.04516)/(x-0.04516)))/0.00107
    return result

popt, pcov = curve_fit(funcCostofOverlap, xCostOverlapScatter, costOfOverlap)
aCostOlping=popt[0]
bCostOlping=popt[1]
cCostOlping=popt[2]


"""
Following part is for drawing Curve fitted result for the Time cost of Overlapping and Being overlapped
"""

"""
yCostofOverlap = funcCostofOverlap(xCostOverlapLinear,aCostOlping,bCostOlping,cCostOlping)
plot1=plt.plot(xCostOverlapScatter, costOfOverlap, '*',label='original values')
plot2=plt.plot(xCostOverlapLinear, yCostofOverlap, 'r',label='curve_fit values')
plt.xlabel('milliseconds')
plt.ylabel('probability')
plt.title('CostOfOverlapping(Inverse funciton)')
plt.show()

yCostofBeOverlapped = funcCostofBeingOverlapped(xCostOverlapLinear2)
plot1=plt.plot(xCostOverlapScatter2, costOfBeOverlapped, '*',label='original values')
plot2=plt.plot(xCostOverlapLinear2, yCostofBeOverlapped, 'r',label='curve_fit values')
plt.xlabel('milliseconds')
plt.ylabel('probability')
plt.title('CostOfBeingOverlapped(Inverse funciton)')
plt.show()
"""

def overlapJudgement():
    overlapResult = {"fast":0,"slow":0}  
    randomNumber = random.uniform(0.0025,0.96)
    timeCostofOverlapper = int(funcCostofOverlapReverse(randomNumber,aCostOlping,bCostOlping,cCostOlping))
    randomNumber = random.uniform(0.046,0.774)
    timeCostofBeOverlapper = int(funcCostofBeingOverlappedReverse(randomNumber))
    if timeCostofOverlapper < 0:
        overlapResult['fast'] = 0
        if timeCostofBeOverlapper < 0:
            overlapResult['slow'] = 0
        else:
            overlapResult['slow'] = int(timeCostofBeOverlapper)
    else:
        overlapResult['fast'] = int(timeCostofOverlapper)
        if timeCostofBeOverlapper < 0:
            overlapResult['slow'] = 0
        else:
            overlapResult['slow'] = int(timeCostofBeOverlapper)
    return (overlapResult)