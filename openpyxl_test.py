# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 15:03:17 2021

An example shows how to write pd.DataFram into excel through openpyxl

@author: renfo
"""

import pandas as pd
import numpy as np
import random
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import os

mainfolder = os.getcwd()
os.chdir(mainfolder)

# generate a dataframe
data = {
    "position":["Top", "Mid", "Btm"]*3,
    # random.gauss(mu, sig)
    "A":np.array([ random.gauss(3,1.2) for x in range(9) ]),
    "B":np.array([ random.gauss(8,0.5) for x in range(9) ]),
    "C":np.array([ random.gauss(48,1.5) for x in range(9) ]),
}

df = pd.DataFrame(data)

# write pd.DataFrame into excel via openpyxl
wb = openpyxl.Workbook()
ws = wb.active
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

wb.save("pandas_openpyxl.xlsx")