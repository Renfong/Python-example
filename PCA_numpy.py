
"""
To do PCA by numpy package
ref:
https://stackoverflow.com/questions/13224362/principal-component-analysis-pca-in-python/49629816#49629816

@author: renfong

"""

import numpy as np
import matplotlib.pyplot as plt
import hyperspy.api as hs

from numpy import argsort
from numpy.linalg import eigh

#%% load data
data = hs.load('t1.dm3').data


#%% define pca
def pca(data, pc_count = None):
    """
    Principal component analysis using eigenvalues
    note: this mean-centers and auto-scales the data (in-place)
    """

    C = np.dot(data.T, data)       # covariance matrix
    E, V = eigh(C)
    key = argsort(E)[::-1][:pc_count]
    E, V = E[key], V[:, key]
    U = data @ V  # equvalent to np.dot(data, V)

    return U, E, V

#%% reconstruction
U, _, V = pca(data, 3)
recons = U @ V.T

""" visualize """
ch = 80
plt.figure()
plt.plot(data[ch,:], label='Raw')
plt.plot(recons[ch,:], label='PCA')
plt.legend()
plt.xlim([800,1800])
plt.ylim([data[ch,1850], data[ch,750]])
plt.show()
