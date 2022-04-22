#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:08:35 2022

@author: rahelmizrahi
"""
import numpy as np
from math import ceil
from  scipy import fftpack
from PIL import Image, ImageOps

class DCT:
    def __init__(self, inPath =  None, data = None , compressionLevel = None, N = None):
        if inPath != None:
            self.inPath = inPath
            self.data = np.asarray(ImageOps.grayscale(Image.open(inPath))) 
        elif inPath == None and len(data) > 0:
            self.data = data 
        
        else: 
            print("error! you need to provide data either in the form of a filepath or actual data")
        
        self.data = self.data -128
        if N != None:
            self.N = N # sections off the image into blocks of NxN
        else: 
            self.N = 8
        self.yBlocks = ceil(self.data.shape[0]/float(self.N))
        self.xBlocks = ceil(self.data.shape[1]/float(self.N))
        
        self.compressionLevel = compressionLevel
        self.T = self._T() #coeffs
        self.DCT_Image = self.DCT_Image() #gets the DCT coeffs for matrix of size (yBlocks * N ) x (xBlocks * N)
        
        

    def _replicate(self) : #this function makes (m/N) x (n/N) blocks of coefficient matrices. 
    #N is the width of the coeefficent matrix T
        yBlocks = self.yBlocks
        coeffGrid = self._replicateRow(self.T[0,:]).T
        for i in range(1, yBlocks * self.N):
            rowIdx = i % self.N
            row = self._replicateRow(self.T[rowIdx,:]).T
            coeffGrid = np.vstack((coeffGrid, row))
        return coeffGrid
    
    def _replicateRow(self, rowVector): 
        #horizontally concatenate a numpy row vector to itself
        #for JPEG, we want to replicate  rowVector ceil(N/COEFF_WIDTH) times, wehre N = number of columns in Image
        xBlocks = self.xBlocks
        rowCopies = np.zeros(shape = (0,0))
        for i in range(xBlocks):
            rowCopies = np.append(rowCopies, rowVector)
        #flatten the 2D list of lists to 1d list 
        return rowCopies.flatten()
    
    #computes DCT entires for the whole image
    #to do this, we make a grid of (M/COEFF_WIDTH) x (N/COEFF_WIDTH) blocks of coefficient matrices.
    #we do this so the grid dimensions match the image dimensions 
    #and we can compute the DCT in one fell swoop. 
    def DCT_Image(self): 
        yBlocks = self.yBlocks
        xBlocks = self.xBlocks
        N = self.N
        T = self.T
        dct = np.zeros((self.yBlocks * self.N  , self.xBlocks * self.N  )) 
        dataPadded = self.pad() #pad the image so each dimensions is divisible by N
        for i in range(0, yBlocks*N , N):
            for j in range(0, xBlocks*N, N ):
                dct[i: i + N, j: j + N] = T * dataPadded[i: i + N, j: j + N] * T.T
                #FIXME : this works, need to add quantization step here 3/10/2022
                ''' 
                debug 
                print("{}, {}".format(i,j))
                np.set_printoptions(precision=)
                print(dct[i: i + N, j: j + N])
                '''
        
        return  dct
        
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
    
        
    
    def _T(self):
        N = self.N
        T = np.zeros(shape= (N,N))
        for i in range(N):
            for j in range(N):  
                if i == 0:
                    T[i][j] = 1/np.sqrt(N)
                else:
                    T[i][j] = np.sqrt(2/N) *np.cos( ((2*j + 1) * i * np.pi) / (2*N) )
        return T


if __name__ == "__main__":
    ''' test1: data dims < 8 '''
    data = np.array([
        [9,9,9,9,9,9,9],
        [8,8,8,8,8,8,8],
        [7,7,7,7,7,7,7],
        [6,6,6,6,6,6,6],
        [5,5,5,5,5,5,5],
        ])
    ''' test2: data dims  = 8 '''
    data=  np.random.randint(5, size=(8, 8))
    data = np.full((8,8), 255)
    
    myDCT = DCT(data = data)
    freqs = myDCT.DCT_Image
    
    ''' test3: data is an image  '''
    '''
    path = "peppers.png"
    
    x = DCT(inPath = path)
    
    
    freqs = x.DCT_Image
    #display the frequencies
    Img = Image.fromarray( freqs , 'L')
    Img.show()
    '''
    
    
    