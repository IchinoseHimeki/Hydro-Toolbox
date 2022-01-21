# -*- coding: utf-8 -*-
'''
File: Pipe_Pressure.py
File Created: 2021-08-06 14:08:44 
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 15:02:46
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: Matplotlib
Description: This is barely support program， considering to be done.
'''

import matplotlib.pyplot as plt
import os
from math import sqrt
import numpy as np

from matplotlib import rcParams
params={'font.family':'serif',
        'font.serif':'STSong',
        'font.weight':'normal', #or 'blod'
        'font.size':'12',#or large,small
        }
rcParams.update(params)

path=os.getcwd()
d=0.01 # Diameter of leaked point
l=4000.0 # Length of the pipe
p0=100.0 # Starting pressure
deltap=0.1 # Stepping of pressure
g=9.8 # Gravity constant
pi=3.141592653589793 # Pi

def waterheadCalc(length,d): # Calculate specific water head
    px_qx=[]
    py_qy=[]
    x=length
    y=l-length
    A=pi*pow(d,2)/4
    if(y<0):
        raise Exception("The length is too long for this pipe!")
    for i in np.arange(p0,0.0,-deltap):
        px=i
        py=i
        # vx=sqrt(px*2*g*d/(lambdaCalc(0.6,d)*x))
        # vy=sqrt(py*2*g*d/(lambdaCalc(0.6,d)*y))
        # qx=vx*A*1000
        # qy=vy*A*1000
        vx=px*d/(lambdaCalc(0.6,d)*x)
        vy=py*d/(lambdaCalc(0.6,d)*y)
        px_qx.append([px,vx])
        py_qy.append([py,vy])
    return [px_qx,py_qy]

def piperesACalc(v,d): # A λ Calculation program, which will be ignored in later work
    A=0.001736/(pow(d,5.3))
    k=0.852*pow((1+0.867/v),0.3)
    if v >= 1.2:
        return A
    else:
        return k*A
    
def lambdaCalc(v,d):
    lambdaValue=piperesACalc(v,d)*pow(pi,2)*g*pow(d,5)/8
    print(lambdaValue)
    return lambdaValue

# def mathPrint(data,length): # Original print method, could easily adapt to multi-processing
#     fig, ax = plt.subplots()
#     datax=[]
#     datay=[]
#     p=[]
#     n_p=[]
#     for i in range(len(data[0])):
#         p.append(data[0][i][0])
#         datax.append(data[0][i][1]+data[1][i][1])
#         datay.append(data[1][i][1]+data[0][i][1])
#         n_p.append(-data[0][i][0])
#     ax.spines[["bottom"]].set_position(("data", 0))
#     ax.spines[["top", "right"]].set_visible(False)
#     ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
#     ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
#     ax.plot(datax,p,label="X端")
#     ax.plot(datay,n_p,label="Y端")
#     # ax.plot(p,datax,label="X端")
#     # ax.plot(p,datay,label="Y端")
#     ax.invert_xaxis()
#     ax.set_ylabel("P (m)")
#     ax.set_xlabel("Q (L/s)")
#     ax.set_title('漏点在距离左端 '+str(length)+'m 处两端压强与漏点流量的关系图',fontsize=18)
#     ax.legend()
#     plt.savefig(path+"\\pic"+str(length)+".png")

def mathPrint(length,d):
    do_l=True
    do_d=False
    fig, ax = plt.subplots()
    alldata_l=[]
    alldata_d=[]
    color=["b","g","r","c","m","#66ccff","#39c5bb","#114514","#191981","#984432"]
    if do_l:
        for l in length:
            data=waterheadCalc(l,0.1)
            datax=[]
            datay=[]
            p=[]
            n_p=[]
            for i in range(len(data[0])):
                p.append(data[0][i][0])
                datax.append(data[0][i][1])
                datay.append(data[1][i][1])
                n_p.append(-data[0][i][0])
            alldata_l.append([p,datax,datay,n_p])
    if do_d:
        for k in d:
            data=waterheadCalc(1000,k)
            datax=[]
            datay=[]
            p=[]
            n_p=[]
            for i in range(len(data[0])):
                p.append(data[0][i][0])
                datax.append(data[0][i][1])
                datay.append(data[1][i][1])
                n_p.append(-data[0][i][0])
            alldata_d.append([p,datax,datay,n_p])
    ax.spines[["bottom"]].set_position(("data", 0))
    ax.spines[["top", "right"]].set_visible(False)
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
    if do_l:
        for l in range(len(length)):
            ax.plot(alldata_l[l][1],alldata_l[l][0],label=str(length[l])+"m",c=color[l])
            ax.plot(alldata_l[l][2],alldata_l[l][3],label="_"+str(length[l])+"m",c=color[l])
            ax.set_title('漏点在距离左端 '+str(length)+'m 处两端压强与漏点流量的关系图',fontsize=18)
    if do_d:
        for l in range(len(d)):
            ax.plot(alldata_d[l][1],alldata_d[l][0],label=str(d[l])+"m",c=color[l])
            ax.plot(alldata_d[l][2],alldata_d[l][3],label="_"+str(d[l])+"m",c=color[l])
            ax.set_title('漏点在距离左端1000m,直径为 '+str(d)+'m 处两端压强与漏点流量的关系图',fontsize=18)
    # ax.plot(p,datax,label="X端")
    # ax.plot(p,datay,label="Y端")
    # ax.invert_xaxis()
    ax.set_ylabel("P (m)")
    ax.set_xlabel(r"$\frac{v^2}{2g}$(m)")
    ax.legend()
    plt.savefig(path+"\\length"+str(length)+".png")

mathPrint([500,1000,1500,2000],[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])