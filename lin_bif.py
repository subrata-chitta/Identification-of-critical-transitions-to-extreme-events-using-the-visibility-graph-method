# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:16:41 2025

@author: slkki
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib qt5
import scipy.io as sio
# from scipy.io import loadmat
from collections import OrderedDict
from collections import Counter
from scipy.integrate import odeint
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import scipy.stats as stats
import math


f1= lambda x:math.sin(w1*x)
def f(y,t):
    dy = np.empty(2,float)
    u = y[0]
    v = y[1]
    h=f1(t)
    dy[0] = v  
    dy[1] = -al*u*v-gam*u-bt*u**3+amp*h 
    return dy

al=0.45
bt=0.50
gam=-0.50
amp=0.20    
q=np.arange(0.642,0.643,0.00001)
for i in q:
    w1=i
    print(i)
    file_1 = open('Linard_th.txt', 'a')
    y0 = np.zeros(2,float)
    y0[0]=0.5
    y0[1]=-0.5

    tf =300000
    tt = np.linspace(0, tf, tf*10)
    [sol,info] = odeint(f,y0,tt,full_output=1,printmessg=1)
    l = 1000000
    xx=sol[l:,1]
    xx=np.array(xx)
    peaks, _ = find_peaks(xx)
    uni = np.unique(xx[peaks])
    z = np.mean(xx[peaks])+6*np.std(xx[peaks])
    file_1.write("%s %s\n" % (str(w1), str(z)))
    file_1.close()
    for l in range(len(uni)):
        file_2 = open('Linard_peaks_all.txt', 'a')
        file_2.write("%s %s\n" % (str(w1), str(uni[l])))
        file_2.close()
