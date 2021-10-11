# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 19:56:31 2021

an example to show the gaussian distribution random

@author: renfo
"""

from random import gauss
import numpy as np
import pandas as pd

table = {"mu0":[], "mu":[], "sig0":[], "sig":[]}
for i in range(10):
    mu0 = 5
    sig0 = 0.8
    counts = 5
    values = []
    for c in range(counts):
        values.append(gauss(mu0, sig0))
    
    values = np.array(values)
    table["mu0"].append(mu0)
    table["mu"].append(values.mean())
    table["sig0"].append(sig0)
    table["sig"].append(values.std())

df = pd.DataFrame(table)
print(df)
    