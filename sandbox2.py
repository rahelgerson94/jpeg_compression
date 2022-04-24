#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 13:46:37 2022

@author: rahelmizrahi
"""

import numpy as np 
from numpy import pi, cos, sin
from math import ceil
import matplotlib.pyplot as plt

N = 8

c = [i for i in range(0,24)]
r = [i for i in range(0,32)]
C,R = np.meshgrid(r,c)
wr =  0.25*pi # digital freq in the row dimension
wc =  0.5 *pi # digital freq in the col dimension
data =  30*cos(wr*R+wc*C) + 60*cos(wr*R+wc*C)


data0 = np.array([
     [0,0,0,20,0,0,0, 0],
     [0,0,20,50,20,0,0, 0],
     [0,7,50,90,50,7,0, 0],
     [0,0,20,50,20,0,0, 0]
     ])
data = data0
#data is 4x8
for i in range(0,2):
    data = np.vstack((data, data))
    data = np.hstack((data, data))
#data is 32x32

plt.matshow(data)

xBlocks = ceil(data.shape[0]/float(N))
yBlocks = ceil(data.shape[1]/float(N))

bla = []
for x in range(0, xBlocks):
    for y in range(1,yBlocks+1): #iterate horizontally
        x_low = x*N
        x_hi = x*N + 8
        print(x_low, x_hi)
        B = data[x_low: x_hi, (y*N): (y*N) + N]
        bla.append(B)
        

'''
plt.matshow(data[12:20, 20: 28])
plt.matshow(data[0:5, 0:7])

for i,b in enumerate(bla):
    print(i)
    plt.matshow(b)
    
for x in range(0, xBlocks): 
    r_low = x
    r_high = x+ N 
    
    col_left = y
    col_right = y+ N
    B = data[r_low: r_high, col_left: col_right]
    bla.append(B)
'''