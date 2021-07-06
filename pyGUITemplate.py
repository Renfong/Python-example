# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 22:38:21 2021

@author: renfo
"""
import tkinter as tk
import os
from tkinter import filedialog


root = tk.Tk()
root.geometry("600x600+200+200")

def GetFolder():
    mainfolder = filedialog.askdirectory()
    os.chdir(mainfolder)
    FolderEntry.insert(0, mainfolder)

GetFolderBtn = tk.Button(root, text = "Select a folder", command=GetFolder)
GetFolderBtn.grid(row=0, column=0, padx=20, pady=10)
FolderEntry = tk.Entry(root)
FolderEntry.grid(row=0, column=1, columnspan=3, padx=120, pady=10, sticky='W')
root.mainloop()