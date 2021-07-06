# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 14:31:14 2019

map gui ver 2


@author: Renfong
"""


#%% import packages
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from hyperspy.api import load as hs_load
from tkinter import filedialog
from tkinter import ttk, messagebox # themed tk
from sklearn.cluster import KMeans
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.axes_grid1 import make_axes_locatable

#%% User function
def elbow_test(datum,n):
    distortions=[]
    for i in range(1,n+1):
        km=KMeans(n_clusters=i,
                  init='k-means++',
                  n_init=10,
                  max_iter=300,
                  random_state=0)
        km.fit(datum)
        distortions.append(km.inertia_)
    return distortions

def MLLS(target,ref):
    coeff=(target.dot(ref.T)).dot(np.linalg.inv(ref.dot(ref.T)))
    return coeff

def kMLLS(datum,ref,tolerance):
	it=0
	maxiter=100
	component=np.zeros([datum.shape[0],ref.shape[0]])
	ref_refined=ref
	for i in range(datum.shape[0]):
		component[i,:]=MLLS(datum[i,:],ref)	
	while (component>1+tolerance).any():
		if it>=maxiter:
			break
		it+=1
		# component refinement
		for i in range(ref.shape[0]):
			ref_refined[i,:]=datum[component[:,i]>1-tolerance,:].mean(axis=0)
		
		for i in range(datum.shape[0]):
			component[i,:]=MLLS(datum[i,:],ref_refined)         
	return component, ref_refined 

#%% GUI function
def BrowseFunc():
    global si, datum, ex, sy, sx, sz
    filename=filedialog.askopenfilename(title='Select SI file',
                                     filetypes=(('dm files','*.dm3'),
                                                ('dm files','*.dm4'),
                                                ('hspy files','*.hspy')))
    fname.set(filename)
    si=hs_load(fname.get())
    dataset=si.data
    ex=si.axes_manager[-1].axis
    
    [sy, sx, sz] = dataset.shape
    datum=dataset.reshape([sy*sx,sz])


def ElbowFunc(n=10):
    global si, datum, ex
    try:
        distortions=elbow_test(datum,n)
        f=plt.figure(figsize=(9.5,5), dpi=100)
        a=f.add_subplot(111)
        a.plot(np.arange(1,n+1),distortions,'-o')
        plt.xticks(ticks=np.arange(1,n+1))
        plt.xlabel('clusters')
        plt.ylabel('distortions')
        plt.title('Elbow Test', fontsize=18)
        f.tight_layout()
        canvas=FigureCanvasTkAgg(f,tab1)
        canvas.get_tk_widget().grid(row=1,column=0,columnspan=2,stick='W')
        
        toolbar_frame = tk.Frame(tab1)
        toolbar_frame.grid(row=2,column=0,columnspan=2,stick='W')
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
    except:
         messagebox.showinfo(title='Error', message='Select a dm file.')


def KMLLSFunc():
    global si, datum, ex, components, refs
    try:
        km=KMeans(n_clusters=val_k.get(),
                  init='k-means++',
                  n_init=10,
                  max_iter=300,
                  random_state=0)
        km.fit(datum)
        refs=km.cluster_centers_
        components, refs = kMLLS(datum,refs,tolerance=0.1)
        
            
        f2,ax=plt.subplots(1,val_k.get(),figsize=(9.5,3),dpi=100)
        ax=ax.ravel()
        for i in range(val_k.get()):
            ax[i].plot(ex,refs[i,:])
            ax[i].tick_params(axis='both', which='major', labelsize=6)
            ax[i].set_yticks([])
            ax[i].set_xlabel('Energy loss (eV)',fontsize=8)
            ax[i].set_xlim([ex[0],ex[-1]])
            ax[i].set_title('Endmember %i'%(i+1))
        f2.tight_layout()
        
        canvas2=FigureCanvasTkAgg(f2,subframe22)
        canvas2.get_tk_widget().grid(row=0,column=0,columnspan=3,stick='W')
        toolbar2_frame = tk.Frame(subframe22)
        toolbar2_frame.grid(row=1,column=0,columnspan=3,stick='W')
        toolbar2 = NavigationToolbar2Tk(canvas2, toolbar2_frame)
        toolbar2.update()
        
    except:
        messagebox.showinfo(title='Error', message='Select a dm file.')


def MapFunc():
    try:
        i=int(Select_em.get())-1
        f3, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5,5),dpi=100)
        ax1.plot(ex,refs[i,:])
        ax1.tick_params(axis='both', which='major', labelsize=6)
        ax1.set_yticks([])
        ax1.set_xlabel('Energy loss (eV)',fontsize=8)
        ax1.set_xlabel('Energy loss (eV)',fontsize=8)
        ax1.set_xlim([ex[0],ex[-1]])
        ax1.set_title('Endmember %i'%(i+1),fontsize=12)
        
        fig32=ax2.imshow(components[:,i].reshape([sy,sx]),
                      cmap=Select_cmap.get())
        ax2.set_yticks([])
        ax2.set_xticks([])
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(fig32,cax=cax)
        f3.tight_layout()

        canvas3=FigureCanvasTkAgg(f3,subframe32)
        canvas3.get_tk_widget().grid(row=0,column=0,columnspan=3,stick='W')
        toolbar3_frame = tk.Frame(subframe32)
        toolbar3_frame.grid(row=1,column=0,columnspan=3,stick='W')
        toolbar3 = NavigationToolbar2Tk(canvas3, toolbar3_frame)
        toolbar3.update()

    except:
        messagebox.showinfo(title='Error', message='Select a dm file.')

def UpdateValFun():
    val_list=np.arange(val_k.get())
    val_list=[str(i+1) for i in val_list]
    Select_em['values']=val_list
    
    
#%% GUI Layout
gui=tk.Tk()
gui.geometry('1000x680+550+100')
#gui.iconbitmap(r'.\tk.ico')
gui.title('kMLLS Maps')


#%% =====================  Layout ===================== %%#
#%% ---------- frame 1 ----------
frame1 = tk.Frame(gui)
frame1.pack()

BrowseButton = ttk.Button(frame1, text='Browse', command = BrowseFunc )
BrowseButton.grid(row=0,column=0,stick='W')

fname=tk.StringVar(value='Select a dm files')
entry_box1=ttk.Entry(frame1,width=125, textvariable=fname)
entry_box1.grid(row=0,column=1)

#%% ---------- frame 2 ----------
frame2 = tk.Frame(gui)
frame2.pack()

## tab_bar
tab_parent=ttk.Notebook(frame2,width=960,height=600)
tab1=ttk.Frame(tab_parent)
tab2=ttk.Frame(tab_parent)
tab3=ttk.Frame(tab_parent)
tab_parent.add(tab1, text=' Elbow ')
tab_parent.add(tab2,text=' kMLLS ')
tab_parent.add(tab3,text='  Map  ')
tab_parent.pack(expand=1, fill='both')

## tab1 : Elobw test
elbowbutton = ttk.Button(tab1, text='Elbow',command=ElbowFunc)
elbowbutton.grid(row=0,column=0,stick='W')

#%% tab 2 : kMLLS tab
subframe21=tk.Frame(tab2)
subframe21.pack(anchor='w')
subframe22=tk.Frame(tab2)
subframe22.pack(anchor='w')


label21=tk.Label(subframe21,text=' Endmember : ',width=15)
label21.grid(row=0,column=0,stick='W')

val_k=tk.IntVar(value=3)
entry_label1=ttk.Entry(subframe21,width=5,textvariable=val_k)
entry_label1.grid(row=0,column=1,stick='W')

kmbutton = ttk.Button(subframe21, text='  kMLLS  ',command=KMLLSFunc,width=10)
kmbutton.grid(row=3,column=0,columnspan=2,stick='W')

#%% tab 3 : mapping
subframe31=tk.Frame(tab3)
subframe31.pack(anchor='w')
subframe32=tk.Frame(tab3)
subframe32.pack(anchor='w')

label31=tk.Label(subframe31,text='  Select an endmember : ', width=25)
label31.grid(row=0,column=0,stick='W')
Select_em = ttk.Combobox(subframe31,width=15, postcommand=UpdateValFun)
Select_em.grid(row=0,column=1,stick='W')

label32=tk.Label(subframe31,text='  Select colormap : ', width=25)
label32.grid(row=1,column=0,sticky='W')
cmap_list=['plasma','viridis','ocean', 'gist_earth', 'nipy_spectral' ,
			'Reds' , 'Blues', 'Greens', 'Oranges', 'Greys',
			'Pastel1', 'Accent' , 'Dark2' , 'Set2' , 'Set3',
			'tab10', 'tab20', 'tab20b']
Select_cmap = ttk.Combobox(subframe31,values=cmap_list,width=15)
Select_cmap.grid(row=1,column=1,stick='W')
Select_cmap.current(0)

mapbutton = ttk.Button(subframe31,text='  Plot  ',command=MapFunc,width=10)
mapbutton.grid(row=3,column=0,columnspan=2,stick='W')

#%% ---------- frame 3 ----------
frame3 = tk.Frame(gui)
frame3.pack()
label99=tk.Label(frame3,text='ver 1.0 ', width=25)
label99.pack( side='right')
#%% run
gui.mainloop()