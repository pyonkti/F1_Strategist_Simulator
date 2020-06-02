# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:23:24 2020

@author: Billy
"""

from scipy.optimize import curve_fit
import numpy as np
from matplotlib import pyplot as plt 
import random


costOfOverlap = [2291, 4041, -642, 561, 942, 550, 457, -446, 699, 479, 520, 149, -1598, -704, 283, 136, 119, -364, 1787, 381, -556, 108, 416, -607, -215, 356, -986, 416, 338, -421, 432, 346, 393, -247, -59, -329, 226, -577, -170, -290, -107, -132, 50, -295, -85, 288, 6, -55, 251, 8, 641, 414, 374, 294, 844, 184, 522, -65, 871, -173, -38, 898, 42, -47, -138, 369, 214, 259, 495, 1053, 1053, 862, 564, -567, -198, -1443, -410, 279, 251, -606, 198, -1045, -229, 568, 373, -412, -32, 95, 286, -36, -208, -432, -481, 113, -39, 405, 519, 252, -153, -582, -111, -37, -104, -455, 1124, 32, -403, -421, -183, 597, 939, -298, -7, -2, -122, 486, -186, -299, 384, -399, -291, -173, 613, -469, 612, 532, 1000, 764, -578, 230, 165, 273, 413, 226, 303, 35, -322, -223, -104, 35, 157, 539, -188, 185, 211, 784, -85, -57, 59, 210, 201, 190, 153, -558, -47, 463, -455, -50, 713, 1335, -1184, 137, 214, 341, -20, -38, 333, -41, -237, -561, 345, 569, -898, -410, 685, -275, -407, 28, -643, -1262, -1230, -1678, -152, -392, -2410, -3293, 1194, 828, 230, 197, 626, 1144, 3541, 619, 735, -689, -16, 623, 394, 232, -2305, -669, 937, 1433, -56]
costOfOverlap = np.array(costOfOverlap)

costOfBeOverlapped = [6277, 52770, 1084, 6184, 2003, 1279, -2327, 1713, -13, 1255, 659, 1783, 825, 1521, 1359, -387, 3033, 3033, 537, -3193, 2691, -1842, 1617, 1328, 2357, -1616, 1652, 1898, 1778, 2107, 1557, 2418, 1532, 441, 1062, 1888, -52, 1615, 3809, 3809, -2173, -1478, 535, 43534, 43534, -43806, 1262, -385, 1113, -918, 974, 651, 1531, 2701, -154, -1589, -757, -1112, 64, 817, 1114, 1258, -527, 1937, 1937, 655, -2886, 1493, -359, 1679, 2519, 14050, 1307, -1443, 28, -13250, 4376, 2202, 1585, 2102, -691, -79, 841, 157, 20996, 1257, 1814, -2171, 2563, 641, 1161, -1800, 735, 836, 1437, 1552, 2133, -1830, 1600, 1100, -1664, 992, 1872, 834, -919, -172, 407, 3168, 589, -3106, 1655, 1108, -205, 1835, 1838, -1574, 1696, 100, 790, 1002, 380, 1414, 1139, 1865, 1640, -258, 2660, 728, 1024, 2261, 2603, 1876, 1582, 480, 1557, 409, -1996, 2298, -891, 1116, 2010, 1209, 1278, 1779, 2083, -1585, -1108, 1231, 51, 1708, 1620, 1620, 3563, 3563, 3563, 3563, 3563, 3222, -4073, -4073, -4073, -1621, -790, -1517, 1774, -1305, 2582, 1755, 1819, -173, 1528, 1467, 801, 2643, 4608, 7110, 7110, 7110, 7110, 7110, 7110, -11093, -11093, -11093, -248, -248, 3541, 3541, 3541, 3541, 6422, 6422, 6422, 807, 807, -1320, -1320, -1320, -1320]
costOfBeOverlapped = np.array(costOfBeOverlapped)

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
yCostofOverlap = funcCostofOverlap(xCostOverlapLinear,aCostOlping,bCostOlping,cCostOlping)
plot1=plt.plot(xCostOverlapScatter, costOfOverlap, '*',label='original values')
plot2=plt.plot(xCostOverlapLinear, yCostofOverlap, 'r',label='curve_fit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.title('CostOfOverlapping(Inverse funciton)')
plt.show()

yCostofBeOverlapped = funcCostofBeingOverlapped(xCostOverlapLinear2)
plot1=plt.plot(xCostOverlapScatter2, costOfBeOverlapped, '*',label='original values')
plot2=plt.plot(xCostOverlapLinear2, yCostofBeOverlapped, 'r',label='curve_fit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
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