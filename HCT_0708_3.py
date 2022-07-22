#!/usr/bin/env python
# coding: utf-8

#      Sample No ; 
#      HCT level ; 
#      Channel number ;
#      Voltage ;

# In[114]:


from __future__ import unicode_literals, print_function
from prompt_toolkit import print_formatted_text, HTML
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import expanduser
plt.rcParams['font.size'] = 16
plt.rcParams['axes.linewidth'] = 2
from tkinter import messagebox
from scipy.interpolate import splrep, splev
plt.style.use('seaborn-whitegrid')
plt.rc('grid', color='b', linestyle='solid')
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error 
import re 
from tkinter import messagebox as mb


# In[52]:


#os.chdir('../')
#os.chdir('../')
#os.getcwd()


# In[123]:


req_files=[]
def to_excel(channel,hct):
    global req_files
    req_files=[]
    sample_list=[]
    d = '.'
    subdirs2 = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    for folder in subdirs2[1:]:
        files2=[]
        for subdir, dirs, files in os.walk(r'./'):
            for filename in files:
                if (filename.endswith(".txt")) & (filename.startswith("HCT "+str(hct)[0]) & (filename[-5] == str(channel))):
                            files2.append(os.path.abspath(os.path.join(subdir, filename)))
        for filename in files2:
            if (folder[3:] in filename):
                 if(filename[-5] == str(channel)):
                        sample_list.append(folder[3:])
                        req_files.append(filename)
    d = {}
    for i in range(len(req_files)):
        df = pd.read_csv(req_files[0], sep=" ", names=['current','time','Serial','Y','voltage'])
        df = df[["current","time","voltage"]]
        #df2 = pd.concat([df2, df], axis=1,keys=['s1', 's2'])
        d[sample_list[i]] = df
    final_df = (pd.concat(d.values(), axis=1, keys=d.keys()))
    final_df.to_csv("HCT_%d_Channel_%s.csv" % (int(hct), str(channel)))
    mb.showinfo('Info','File saved as: HCT_%d_Channel_%s.csv' % (int(hct), str(channel)))  


# In[124]:


import tkinter as tk
from tkinter import ttk 
from tkinter import *
import scipy.signal
from random import random

plot_list=[]
colors = ['r', 'c', 'hotpink', 'g', 'y', 'c', 'k']
s,h,c,v = [0],[0],[0],[0]

def show_entry_fields():
    fig = plt.figure(figsize=(20,7))
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    a=[var1.get(),var2.get(),var3.get(),var4.get()]
    for k in range(4):
        if(a[k]):
            s[0]= (d['plot'+str(k+1)][0])
            h[0]=(d['plot'+str(k+1)][1])
            c[0]=(d['plot'+str(k+1)][2])
            v[0]=(d['plot'+str(k+1)][3])
            i=0
            #print(h)
            os.chdir(s[i])
            #os.chdir(str(h[i]))
            files2=[]
            for subdir, dirs, files in os.walk(r'./'):
                for filename in files:
                    if (filename.endswith(".txt") & filename.startswith('HCT '+str(h[i]))):
                            #files2.append(filename)
                            files2.append(os.path.abspath(os.path.join(subdir, filename)))
            #print(files2)
            bool_var = False
            channel_taken = c[i]
            for j in range(len(files2)):
                #print (j)
                if (files2[j][-5]) == c[i]:
                    bool_var=True 
                    df = pd.read_csv(files2[j], sep="\t", names=['current','time','Serial','Y','voltage'])
            if not bool_var:
                #print(files2)
                channel_taken = str(files2[0][-5])
                print("Channel specified not available, taking channel", channel_taken )
            df = pd.read_csv(files2[0], sep=" ", names=['current','time','Serial','Y','voltage'])
            df2 = df.loc[df["voltage"]==v[i]]
            df2 = df2.reset_index(drop=True)
            df3 = df2[["Serial","current"]]
            #print(df2)
            slope = pd.Series(np.gradient(df3.current), df3.index, name='slope')
            #print(slope)
            xdata= df2.index.to_numpy()
            ydata= df2["current"].to_numpy()
            ydata2 = slope.to_numpy()
            xdata1 = xdata.astype(np.float64)
            ydata1 = ydata.astype(np.float64)
            ydata2 = ydata2.astype(np.float64)
            
            def func(x, a, b, c):
                return a * np.exp(-b * x) + c

            popt, pcov = curve_fit(func, xdata1, ydata1/1000, maxfev=5000)
            stdevs = np.sqrt(np.diag(pcov))
            print('For Plot (' + str(s[i]) + ') HCT(' + str(h[i]) + ') Ch' + str(channel_taken))
            print("Parameters:   ", popt)
            print("Std Dev:   ", stdevs)
            print ("Mean square error:   ", '%.7f' % mean_squared_error(ydata1,func(xdata1, *popt)) )
            print()
            dydx = scipy.signal.savgol_filter(ydata1, window_length=11, polyorder=2, deriv=1)
            ax1.plot(xdata1, ydata1,linewidth=3,c = (colors[k]), label='Sample(' + str(s[i]) + ') HCT(' + str(h[i]) + ') Ch' + str(channel_taken))
            #plt.figure()
            ax2.plot(xdata1, (dydx*10),linewidth=3,c = (colors[k]), label='Sample(' + str(s[i]) + ') HCT(' + str(h[i]) + ') Ch' + str(channel_taken))
            ax1.set_xlabel('Serial Number',fontsize= 20)
            ax1.set_ylabel('Current',fontsize= 20)
            ax2.set_xlabel('Serial Number',fontsize= 20)
            ax2.set_ylabel('Derivative',fontsize= 20)            
            ax1.set_title("Actual curves",fontsize= 20)
            ax2.set_title("Derivative plot",fontsize= 20)
            ax1.legend()
            ax2.legend()
            os.chdir('../')
            #os.chdir('../')
        else:
            pass
    ax1.grid(b=True,  color='lightgray', linestyle='-')
    ax2.grid(b=True,  color='lightgray', linestyle='-')
    plt.show()

d = {'plot1': ['257_2',30,5,50], 'plot2': ['257_3',50,5,50],'plot3': ['257_2',30,5,50],'plot4': ['257_2',30,5,50]}

def show_info(plot_str):
    e1.delete(0, tk.END)
    e1.insert(10, d[plot_str][0])
    e2.delete(0, tk.END) 
    e2.insert(10, d[plot_str][1])
    e3.delete(0, tk.END)
    e3.insert(10, d[plot_str][2])
    e4.delete(0, tk.END)   
    e4.insert(10, d[plot_str][3])
    
def store_val():
    d['plot'+str(var.get())]=[str(e1.get()),int(e2.get()),int(e3.get()),int(e4.get())]
    
master = tk.Tk()

tk.Label(master, text="Sample File").grid(row=0,column=0,padx=10)
tk.Label(master, text="HCT").grid(row=1,column=0,padx=10)

e1 = tk.Entry(master)
e2 = tk.Entry(master)
e1.insert(10, '257_1')
e2.insert(10, 30)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tk.Label(master, text="Channel").grid(row=0,column=2,padx=10)
tk.Label(master, text="Voltage").grid(row=1,column=2,padx=10)

e3 = tk.Entry(master)
e4 = tk.Entry(master)
e3.insert(10, 5)
e4.insert(10, 50)

e3.grid(row=0, column=3 )
e4.grid(row=1, column=3 )


var = IntVar()
var.set(1)
Radiobutton(master, text="Plot 1", variable=var, value=1, command=lambda:show_info('plot1')).grid(row=2, 
                                                               column=0, 
                                                               sticky=tk.N, padx=5,
                                                               pady=20)
Radiobutton(master, text="Plot 2", variable=var, value=2, command=lambda:show_info('plot2')).grid(row=2, 
                                                               column=1, 
                                                               sticky=tk.N, padx=5,
                                                               pady=20)
Radiobutton(master, text="Plot 3", variable=var, value=3, command=lambda:show_info('plot3')).grid(row=2, 
                                                               column=2, 
                                                               sticky=tk.N, padx=5,
                                                               pady=20)
Radiobutton(master, text="Plot 4", variable=var, value=4, command=lambda:show_info('plot4')).grid(row=2, 
                                                               column=3, 
                                                               sticky=tk.N, padx=5,
                                                               pady=20)

var1 = IntVar()
var1.set(True)
Checkbutton(master, text="Plot 1", variable=var1).grid(row=3,column=0,pady=10)
var2 = IntVar()
var2.set(True)
Checkbutton(master, text="Plot 2", variable=var2).grid(row=3,column=1,pady=10)
var3 = IntVar()
Checkbutton(master, text="Plot 3", variable=var3).grid(row=3,column=2,pady=10)
var4 = IntVar()
Checkbutton(master, text="Plot 4", variable=var4).grid(row=3,column=3,pady=10)


tk.Button(master, text='Store', command=store_val,width=6,height=3).grid( row=0,
                                                               column=8, 
                                                                padx=10,
                                                               pady=10)
tk.Button(master, text='PLOT', command=show_entry_fields,width=6,height=3).grid( row=0,
                                                               column=10, 
                                                                padx=10,
                                                               pady=10)
tk.Label(master, text="Channel").grid(row=5,column=0,padx=10,pady=10)
tk.Label(master, text="HCT").grid(row=5,column=2,padx=10,pady=10)

e5 = tk.Entry(master)
e6 = tk.Entry(master)
e5.insert(10, 0)
e6.insert(10, 30)
e5.grid(row=5, column=1,pady=10)
e6.grid(row=5, column=3,pady=10)

tk.Button(master, text='To Excel', command=lambda:to_excel(e5.get(),e6.get()), width=10).grid( row=5,
                                                               column=5, 
                                                                padx=10,
                                                               pady=10)
master.mainloop()


# In[17]:


#os.chdir('../')
#os.chdir('../')
#os.getcwd()

