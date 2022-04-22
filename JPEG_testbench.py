#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 09:40:27 2022

@author: rahelmizrahi
"""
import numpy as np
from math import ceil
COEFF_WIDTH = 3
from  scipy import fftpack

coeffs = np.array([
                [0,0,0],
                [1,1,1],
                [2,2,2],
                ])

data = np.array([
    [9,9,9,9,9,9,9],
    [8,8,8,8,8,8,8],
    [7,7,7,7,7,7,7],
    [6,6,6,6,6,6,6],
    [5,5,5,5,5,5,5],
    ])

def replicateRow(rowVector): 
    #horizontally concatenate a numpy row vector to itself
    #for JPEG, we want to replicate  rowVector ceil(N/COEFF_WIDTH) times, wehre N = number of columns in Image
    xBlocks = ceil(data.shape[1]/float(COEFF_WIDTH))
    rowCopies = np.zeros(shape = (0,0))
    for i in range(xBlocks):
        rowCopies = np.append(rowCopies, rowVector)
    
    #flatten the 2D list of lists to 1d list 
    return rowCopies.flatten()

def replicate() : #this function makes (M/COEFF_WIDTH) x (N/COEFF_WIDTH) blocks of coefficient matrices. 
    yBlocks = ceil(data.shape[0]/float(COEFF_WIDTH))
    coeffGrid = replicateRow(coeffs[0,:]).T
    for i in range(1, yBlocks+1):
        row = replicateRow(coeffs[i,:]).T
        coeffGrid = np.vstack((coeffGrid, row))
    return coeffGrid

def dct2(a):
    return fftpack.dct( fftpack.dct( a, axis=0, norm='ortho' ), axis=1, norm='ortho' )
 
def genCoeffs(size): #size is a tuple
c = np.zeros(size)
    N2 = size[1]
    N1 = size[0]
    K1 = [_ for _ in range(N1)]
    K2 = [_ for _ in range(N2)]
        
    for i in range(N1):
        for j in range(N2):
            c[i][j] = cos( (np.pi / N2) * (j + 1/2) * ) * cos( ) 
if __name__ == "__main__":
    T = np.array([
                    [0,0,0],
                    [1,1,1],
                    [2,2,2],
                    ])
    
    data = np.array([
        [9,9,9,9,9,9,9],
        [8,8,8,8,8,8,8],
        [7,7,7,7,7,7,7],
        [6,6,6,6,6,6,6],
        [5,5,5,5,5,5,5],
        ])
    
    yBlocks = ceil(data.shape[0]/float(COEFF_WIDTH))
    xBlocks = ceil(data.shape[1]/float(COEFF_WIDTH))
    N = 3
    imsize = data.shape
    dct = np.zeros(imsize)
    
    x = dct2(data)
   