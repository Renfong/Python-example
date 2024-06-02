# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 19:24:03 2024

@author: renfo
"""

import os
import hyperspy.api as hs
import matplotlib.pyplot as plt

mainfolder = r"C:\Users\renfo\Desktop\EDS test"
os.chdir(mainfolder)

fileName = "Demo.bcf"
edsMap = hs.load(fileName)

#%%
sp = edsMap[2].sum()
ax = sp.axes_manager[0].axis
data = sp.data

plt.figure(dpi=150)
plt.plot(ax,data)
plt.show()