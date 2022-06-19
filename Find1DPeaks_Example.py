# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 21:10:32 2022

Find 1D peak maximum in python

ref:
https://www.statology.org/numpy-shift/
https://stackoverflow.com/questions/65154833/how-to-find-peak-positions-local-maxima

@author: renfo
"""

import numpy as np
import matplotlib.pyplot as plt

def ArrOffset(src, offset):
    dst = np.empty_like(src)
    if (offset>0):
        dst[offset:] = src[:-offset]
        dst[:offset] = src[0]
        
    elif (offset<0):
        dst[offset:] = src[offset+1]
        dst[:offset] = src[-offset:]
        
    else:
        dst[:] = src
    
    return dst
  

def Find1DPeaks(y, win):
    y2 = y*0+1
    for dy in np.arange(-win,win+1):
        offset = ArrOffset(y,dy)
        mk = (y>=offset)
        y2 = y2*mk
    pkInd = np.where(y2==1)
    return y2, pkInd
    

        
# test
x = np.arange(0,100.1,step=.1)
y = 5*np.exp(-1*(x-35)**2/10)
y += 3*np.exp(-1*(x-75)**2/25)

y2, pkInd = FindPeaks(y, 3)

plt.figure()
plt.plot(x,y)
plt.plot(x,y2)
plt.show()
