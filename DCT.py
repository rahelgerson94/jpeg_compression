#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 12:21:29 2022

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

class DCT: 
    def __init__(self, imageObj , N = None):
        self.imageObj = imageObj
        self.N = imageObj.N
        #self.coeffs = fftpack.dct(self.) #built in quantization 
        self.coeffs = fftpack.dct(fftpack.dct(imageObj.data, axis=0), axis=1) #this works 4/19
        #self.coeffs1 = self.DCT()
        self.coeffs1 = self.dct2(imageObj.data) #this works 4/19
        self.coeffs_quantized = self.downsample()
        #self.downsample
    '''
    def downsample(self, thresh):
        
        maxFreq = np.amax(self.coeffs)
        ind = np.abs(self.coeffs) >= thresh*maxFreq
        X_q = self.coeffs * ind
        return X_q
        #return  10*(np.round_(self.coeffs)/10)
    '''
    def downsample(self, thresh = None):
        if thresh == None:
            thresh = 0.75
        sorted_coeffs = np.sort(np.abs(self.coeffs.reshape(-1)))[::-1] #flattens and sorts X; largest coeffs in front; shape = (mxn), 1. 
        numCoeffs2keep = int( (1 - thresh) * len (sorted_coeffs)) #keep only the largest numCoeffs2keep 
        coeffs2keep = sorted_coeffs[0:numCoeffs2keep] 
        thresh = coeffs2keep[-1] #we want coeffs of at least this value
        row, col = np.where(self.coeffs >= thresh) #get the rows and cols where this condition is met
        listOfCoordinates = list(zip(row, col)) #get exact coords where this condition is met
        X_q = np.zeros((self.coeffs.shape)) 
        for coord in listOfCoordinates:
            X_q[coord[0], coord[1]] = self.coeffs[coord[0], coord[1]]
        return X_q  
    
    
    def dctLoop(self): 
        DCTblocks= []
        yblocks = self.ImageObject.yBlocks
        xblocks = self.ImageObject.xBlocks
        for x in range(0, xBlocks):
            for y in range(0,yBlocks): #iterate horizontally
                x_low = x*N
                x_hi = x*N + 8
                #print(x_low, x_hi)
                currBlock = data[x_low: x_hi, (y*N): (y*N) + N]
                DCTblocks.append(self.dct2(currBlock))
        return DCTBlocks            
    
                
    def dct2(self, im_data):
        
        N = self.N
        a = empty([N,N],float)
        X = empty([N,N],float)
    
        for i in range(N):
            a[i,:] = self.dct(im_data[i,:])
        for j in range(N):
            X[:,j] = self.dct(a[:,j])
        return X
    
    def dct(self, x):
        N = len(x)
        y = empty(2*N,float)
        y[:N] = x[:]
        y[N:] = x[::-1]
    
        X = rfft(y)
        phi = exp(-1j*pi*arange(N)/(2*N))
        return real(phi*X[:N])
   
    
    
if __name__ == "__main__":
    pass