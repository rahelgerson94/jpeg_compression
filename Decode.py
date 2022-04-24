#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 12:22:32 2022

@author: rahelmizrahi
"""
import numpy as np 
from numpy import empty,arange,exp,real,imag,pi
from numpy import fft, cos, sin, pi, sqrt
from numpy.fft import rfft,irfft
from math import ceil
from  scipy import fftpack
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import pprint
class Decode:
    def __init__(self, origShape, rle, N):
        ''' rle_data is the list of tuples 
            origDims: original dimensions of dctmatrix, 
            which equal the dimensions of the image
        '''
        self.rle_data = rle
        self.array = [] # output of inverse run-length encoding
        self.DCTMatrix = np.zeros(()) #output of inverse zigzag
        self.origShape = origShape #orig
        self.N = N
   
    #turn 1d arr to 2d matrix
    def  inverse_zigzag(self): 
        vmax = self.N
        hmax = self.N
        h = 0
        v = 0
        vmin = 0
        hmin = 0
        
        output = np.zeros((vmax, hmax))
        i = 0
        dct1d = self.inverse_rle()
        while (v < vmax) and (h < hmax):
            if ((h + v) % 2) == 0:                 # going up
                
                if (v == vmin):
                    output[v, h] = dct1d[i]        # if we got to the first line

                    if (h == hmax):
                        v = v + 1
                    else:
                        h = h + 1                        
    
                    i = i + 1

                elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
                    output[v, h] = dct1d[i] 
                    v = v + 1
                    i = i + 1

                elif ((v > vmin) and (h < hmax -1 )):    # all other cases
                    output[v, h] = dct1d[i] 
                    v = v - 1
                    h = h + 1
                    i = i + 1

            else:                                    # going down

                if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
                    output[v, h] = dct1d[i] 
                    h = h + 1
                    i = i + 1
            
                elif (h == hmin):                  # if we got to the first column
                    output[v, h] = dct1d[i] 
                    if (v == vmax -1):
                        h = h + 1
                    else:
                        v = v + 1
                    i = i + 1
                elif((v < vmax -1) and (h > hmin)):     # all other cases
                    output[v, h] = dct1d[i] 
                    v = v + 1
                    h = h - 1
                    i = i + 1
            if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
                output[v, h] = dct1d[i] 
                break
        return output
    
    def inverse_rle(self):
        DCTarray = []
        EOB = False
        totLength = self.origShape[0] * self.origShape[1] 
        print(totLength )
        for i, tup in enumerate(self.rle_data):
            tmpList = self.expand(tup)
            for val in tmpList:
                
                DCTarray.append(val)
        #we need to subtract 2 from the total length b/c 
        #we dropped the DC coeff, and the zigzag algorithm adds a zero 
        DCTarray = self.addRemainingZeros(DCTarray, totLength )
        
        return np.array(DCTarray, dtype = np.float32)
        
    def expand(self, tup):
        arr = []
        numZeros = tup[0]
        val = tup[1]
        for z in range(numZeros):
            arr.append(0)
        if val != 0:
            arr.append(val)
        return arr
        
    def addRemainingZeros( self, l, totLength ):
        length = len(l)
        numZ = totLength - length
        for z in range(0,numZ):
            l.append(0)
        return l
    
    def idct(self, a):
        N = len(a)
        c = empty(N+1,complex)
    
        phi = exp(1j*pi*arange(N)/(2*N))
        c[:N] = phi*a
        c[N] = 0.0
        return irfft(c)[:N]
    
    def idct2(self, coeff_data):
        #b - self.
        M = coeff_data.shape[0]
        N = coeff_data.shape[1]
        a = empty([M,N],float)
        y = empty([M,N],float)
    
        for i in range(M):
            a[i,:] = self.idct(coeff_data[i,:])
        for j in range(N):
            y[:,j] = self.idct(a[:,j])
        return y
    
if __name__ == "__main__":

    pass