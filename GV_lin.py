# -*- coding: utf-8 -*-
"""
Created on Thu May 22 16:16:58 2025

@author: Subrata
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

def visibility_graph(time_series):
    """
    Constructs a Visibility Graph (VG) from a time series.

    Parameters:
        time_series (list or np.array): The input time series.

    Returns:
        G (networkx.Graph): The visibility graph.
    """
    n = len(time_series)
    G = nx.Graph()

    # Add nodes
    for i in range(n):
        G.add_node(i, value=time_series[i])

    # Check visibility condition and add edges
    for i in range(n):
        for j in range(i + 1, n):
            visible = True
            for k in range(i + 1, j):
                # Visibility condition
                if time_series[k] >= time_series[i] + (time_series[j] - time_series[i]) * (k - i) / (j - i):
                    visible = False
                    break
            if visible:
                G.add_edge(i, j)

    return G


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
av_d=[]
d_max=[]
cluster=[]
av_path=[] 
q=np.arange(0.642,0.643,0.00001)
for i in q:
    w1=i
    print(i)
    y0 = np.zeros(2,float)
    y0[0]=0.5
    y0[1]=-0.5

    tf = 200000
    tt = np.linspace(0, tf, tf*10)
    [sol,info] = odeint(f,y0,tt,full_output=1,printmessg=1)
    l=50000
    peaks, _ = find_peaks(sol[l:,1])
    time_series = np.array(sol[l:,1])[peaks]
    VG = visibility_graph(time_series)
    #A=nx.to_numpy_array(VG)
    Gcc= sorted(nx.connected_components(VG), key=len, reverse=True)
    G0=VG.subgraph(Gcc[0])
    deg=G0.degree()
        #v=Counter(deg)
    deg=G0.degree()
    d1=np.array(deg)
    degree=d1[:,1]
    av_d.append(np.mean(degree))
    d_max.append(np.max(degree))
    cluster.append(nx.average_clustering(G0))
    av_path.append(nx.average_shortest_path_length(G0))
    
plt.figure()
plt.plot(q,av_d,'r.-')
plt.plot(q,d_max,'b.-')
plt.plot(q,cluster,'g.-')
plt.plot(q,av_path,'m.-')
