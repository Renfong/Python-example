# -*- coding: utf-8 -*-
"""
2021/07/31
@author: renfong
"""
import tkinter as tk
import os
from tkinter import filedialog
import data_process as dp

#%% ========================================================
# define window size
root = tk.Tk()
root.geometry("600x300+200+200")
root.title("Renfong")

#%% ========================================================
# Create section 1
frame1 = tk.LabelFrame(root,text="Section 1", borderwidth=2)
frame1.pack(fill="x", padx=10)

# select a folder and save a figure in it
def GetFolder():
    mainfolder = filedialog.askdirectory()
    os.chdir(mainfolder)
    FolderEntry.insert(0, mainfolder)

GetFolderBtn = tk.Button(frame1, text = "Select folder", command=GetFolder)
GetFolderBtn.grid(row=0, column=0, padx=15, pady=10)
FolderEntry = tk.Entry(frame1, width=75)
FolderEntry.grid(row=0, column=1, padx=5, pady=10, sticky='WE')


def btn1_response():
    mainfolder = FolderEntry.get()
    dp.btn1(mainfolder)

Btn1 = tk.Button(root, text = "Do Function 1", command=btn1_response)
Btn1.pack(fill="x", padx=20)


#%% ========================================================
# Create section 2
frame2 = tk.LabelFrame(root,text="Section 2", borderwidth=2)
frame2.pack(fill="x", padx=10)

# nth folder
tk.Label(frame2,text="Site : ").grid(pady=5, row=0, column=0)
SiteEntry = tk.Entry(frame2, width=10)
SiteEntry.grid(pady=5, row=0, column=1)

# files
tk.Label(frame2, text="Position : ").grid(pady=2, row=1, column=0)
PosEntry = tk.Entry(frame2, width=10)
PosEntry.grid(pady=2, row=1, column=1)

# ROI
tk.Label(frame2, text="start pixel : ").grid(pady=2, row=2, column=0)
SPEntry = tk.Entry(frame2, width=10)
SPEntry.grid(pady=2, row=2, column=1)
tk.Label(frame2, text="Range : ").grid(pady=2, row=2, column=2)
RNGEntry = tk.Entry(frame2, width=10)
RNGEntry.grid(pady=2, row=2, column=3)

# process
def btn2_response():
    site = "SITE"+SiteEntry.get()
    pos = PosEntry.get()
    sp = SPEntry.get()
    rng = RNGEntry.get()
    dp.btn2(site, pos, sp, rng)
    
Btn2 = tk.Button(root, text= "Do Function 2", command=btn2_response)
Btn2.pack(fill="x", padx=20)

#%% ========================================================
# Create section 3
frame3 = tk.LabelFrame(root,text="Section 3", borderwidth=2)
frame3.pack(fill="both", padx=10, expand="yes")

def btn3_response():
    dp.btn3(FolderEntry.get())

Btn2 = tk.Button(frame3, text= "Do Function 3", command=btn3_response)
Btn2.pack(fill="x", padx=10, pady=10)

#%% ========================================================
root.mainloop()
