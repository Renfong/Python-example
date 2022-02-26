# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 21:36:28 2022

@author: renfong
"""

import numpy as np
import matplotlib.pyplot as plt

# ref
# https://www.statology.org/cdf-python/

def CDF_Stack(data, labels):
    colors = ["steelblue","mediumvioletred","limegreen","goldenrod"]
    ci = 0
    alpha=0.2
    plt.figure(dpi=150)
    for i in np.arange(len(data)):
        x = np.sort(data[i])
        #calculate CDF values
        y = 100. * np.arange(len(data[i])) / (len(data[i])-1)
        plt.plot(x, y,"-",color=colors[ci], label=labels[i])
        plt.fill_between(x, y,color=colors[ci], alpha=alpha)
        ci += 1
    plt.ylabel("CDF (%)", fontsize=14)
    plt.xlabel("Distance (m)", fontsize=14)
    plt.ylim(bottom=0)
    plt.legend(loc=2)
    plt.show()


# example
data = []
labels = []
data.append(np.random.normal(loc=4.2, scale=0.5, size=30))
labels.append("Series 1")
data.append(np.random.normal(loc=4.7, scale=0.9, size=20))
labels.append("Series 2")
data.append(np.random.normal(loc=4.5, scale=0.4, size=60))
labels.append("Series 3")
data.append(np.random.normal(loc=4.5, scale=0.8, size=15))
labels.append("Series 4")

CDF_Stack(data, labels)
