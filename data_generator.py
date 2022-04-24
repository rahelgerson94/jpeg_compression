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
def cosImage(numRows, numCols):
    c = [i for i in range(0,numCols)]
    r = [i for i in range(0,numRows)]
    C,R = np.meshgrid(r,c)
    wr =  0.25*pi # digital freq in the row dimension
    wc =  0.5 *pi # digital freq in the col dimension
    data =  30*cos(wr*R+wc*C) + 60*cos(wr*R+wc*C)
    return data.T

def baseImage( ):
    data0 = np.array([
         [0,0,0,0,0,0,0, 0],
         [0,0,20,50,20,0,0, 0],
         [0,7,50,90,50,7,0, 0],
         [0,0,20,50,20,0,0, 0]
         ])
    return data0

def multiplyBaseImage( baseImage, mult):
    for i in range(0,mult):
        data = np.vstack((baseImage, baseImage))
        data = np.hstack((baseImage, baseImage))
    return data
    
if __name__ == "__main__":
    pass
    # img1 = baseImage()
    # img = multiplyBaseImage(img1, 2)
    
   
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
    
