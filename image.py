#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 12:22:52 2022

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

class image:
    def __init__(self, inPath =  None, data = None, N = None):
        ''' image stuff '''
        if inPath != None:
            self.inPath = inPath
            self.data = np.asarray(ImageOps.grayscale(Image.open(inPath))) 
        elif inPath == None and len(data) > 0:
            self.data = data 
        
        else: 
            print("error! you need to provide data either in the form of a filepath or actual data")
        if N == None:
            self.N = 8
        else:
            self.N = N
        #self.data = self.data -128
        
        self.yBlocks = ceil(self.data.shape[0]/float(self.N)) #num blocks in the row direction
        self.xBlocks = ceil(self.data.shape[1]/float(self.N)) #num blocks in the col direction
        self.origShape = self.data.shape
        
        # need to pad the data here if either dim of image isn't divisible by 8. 
        '''
        if self.xBlocks % self.N != 0 or self.yBlocks % self.N != 0:
            self.data = self.pad()
        '''  
    
    def pad(self): # need to pad data with zeros so M and N (number of columns)  are divisible N (coefficent with)
        numPadsx =  self.xBlocks * self.N - self.data.shape[1] #number of zeroes to pad in the x direction
        numPadsy = self.yBlocks * self.N - self.data.shape[0]
        
        dataPadded = np.zeros((self.yBlocks * self.N  , self.xBlocks * self.N  )) #make an empty array, which will  hold the new padded array
        
        for idx,row in enumerate(self.data):
            dataPadded[idx] = np.hstack((row, np.zeros(numPadsx)))
        #end padding in the x direction
        #now, pad in the y direction
        i = idx
        for i in range(i, i + numPadsy):
            dataPadded[i] = np.zeros(self.xBlocks * self.N)
        return dataPadded
    def unpad(self):
        pass
                
if __name__ == "__main__":
    pass