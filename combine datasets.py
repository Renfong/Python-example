# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 17:43:22 2021

An example to show how to combine all dataframe together
key functions:
  --> index_col : combine the dataframe quickly
  --> interp1d  : unify the x-axis

@author: renfo
"""
import numpy as np
import pandas as pd
import glob

from scipy.interpolate import interp1d

#%% import data and put them together
files = glob.glob("*.csv")

# columns: xx, y1, y2, y3
ds = []
for f in files:
    # to simplify the code by using "index_col"
    df = pd.read_csv(f, index_col="xx") 
    ds.append(df)

#%% determine the x range of all datasets
xMax = np.inf
for i in range(len(ds)):
    xMax = min(xMax, ds[i].index.max())
    print("ds%i -> xx[-1:]=%.2f, xMax=%.2f"%(i, ds[i].index.max(), xMax))

# or (Comprehensions)
# xMax = min([d.index.max() for d in ds])

#%% unify the x-axis , the new values are "cubic" interpolated
xnew = np.arange(xMax, step=.1)
ds2 = []        # put all the dataframe together

for d in ds:
    df2 = {"xx":xnew}
    for col in d.columns:
        f = interp1d(d.index, d[col],kind='cubic')
        df2[col]=f(xnew)
    df2 = pd.DataFrame(df2)
    df2 = df2.set_index("xx")   # to simplify the code
    ds2.append(df2)

#%% merge together
df_avg = ds2[0]*0
for i in np.arange(len(ds2)):
    df_avg += ds2[i]
    
df_avg /= len(ds2)
df_avg.to_csv("ds_avg.csv")