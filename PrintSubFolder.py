# -*- coding: utf-8 -*-
"""
Created on Wed May  4 22:44:35 2022

@author: renfo
"""

import tkinter as tk
import tkinter.ttk as ttk
import os
import glob

root = tk.Tk()
root.title("ScreenShotter")
root.geometry("150x80")

mainfolder = r"C:\Users\renfo\Desktop\mainfoler"
os.chdir(mainfolder)
folders = glob.glob("*")
folders = [fo for fo in folders if os.path.isdir(os.path.join(mainfolder,fo))]

var = tk.StringVar()
cb = ttk.Combobox(root,textvariable=var, value=folders)
cb.current(0)
cb.pack(pady=10)

def printSelection():
    path = os.path.join(mainfolder,var.get())
    print(path)

btn = tk.Button(root, text="Print", command=printSelection)
btn.pack(pady=10,anchor=tk.S,side=tk.BOTTOM)


root.mainloop()