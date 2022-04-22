#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:08:35 2022

@author: rahelmizrahi
"""
import numpy as np 
from numpy import fft, cos, sin, pi, sqrt
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
        
        self.yBlocks = ceil(self.data.shape[0]/float(self.N))
        self.xBlocks = ceil(self.data.shape[1]/float(self.N))
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
                
class DCT: 
    def __init__(self, image_obj , N = None):
        self.x = image_obj.data
        self.N = image_obj.N
        self.coeffs = fftpack.dct(self.x) #built in quantization 
        self.coeffs1 = self.DCT()
        #self.downsample
    '''
    def downsample(self, thresh):
        
        maxFreq = np.amax(self.coeffs)
        ind = np.abs(self.coeffs) >= thresh*maxFreq
        X_q = self.coeffs * ind
        return X_q
        #return  10*(np.round_(self.coeffs)/10)
    '''
    def downsample(self, thresh):
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
    
    def DCT(self): #FIXME doesn't work
        data = self.x - 128
        M, N = self.x.shape # (img x, img y)
        dft2d = np.zeros((M,N),dtype=complex)
        for i in range(M):
            for j in range(N):
                if i == 0: 
                    ci = 1/sqrt(M)
                else:
                    ci = sqrt(2)/sqrt(M)
                if j == 0: 
                    cj = 1/sqrt(N)
                else :
                    cj = sqrt(2)/sqrt(N)
                
                tempSum = 0
                for x in range(M):
                    for y in range(N):
                        #e = cmath.exp(- 2j * np.pi * ((k * m) / M + (l * n) / N))
                        cos = np.cos(((2*x + 1) * i * pi)/ 2* M ) * np.cos(((2*y + 1) * j * pi)/ 2*N )
                        
                        #if x == 0 and y == 6:
                            #print(x,y)
                        tempSum +=  data[x,y] * cos
                dft2d[i,j] = ci*cj*tempSum

        return dft2d

class Encode:
    def __init__(self, X):
        self.X = X.coeffs
   
    def reverse(self,  i,  j,  k,  col,  x) :
        if (j >= 0 and k < col):
            self.reverse( i, j - 1, k + 1, col, x)
            x.append(self.X[j][k])
            #  Display element
            return x
 
    def zigzag(self):
        #  Auxiliary variables
        x = []
        i = 0
        j = 0
        k = 0
        counter = 0
        #  Get the length number of rows
        #  And number of columns
        row = len(self.X)
        col = len(self.X[0])
        #  First half which contain element of top left triangle
        while (i < row) :
            if (counter % 2 == 0) :
                j = 0
                while (j <= i and j < col and i - j >= 0) :
                    #  Display element
                    print(self.X[i - j][j], end =" ")
                    x.append(self.X[i - j][j])
                    j += 1
            else :
                j = i
                k = 0
                while (j >= 0 and j < col and k <= i) :
                    #  Display element
                    print(self.X[k][j], end =" ")
                    x.append(self.X[k][j])
                    
                    j -= 1
                    k += 1
            i += 1
            counter += 1
        #  Display remaining bottom right triangle
        i = 1
        while (i < col) :
            if (counter % 2 == 0) :
                j = row - 1
                k = i
                while (j >= 0 and k < col) :
                    #  Display element
                    #print(self.X[k][j], end =" ")
                    x.append(self.X[j][k])
                    j -= 1
                    k += 1
            else :
                x1 = self.reverse( i, row - 1, i, col, [])
                for ii in x1:
                    x.append(ii)
            counter += 1
            i += 1
        return x
        
if __name__ == "__main__":
    ''' test1: data dims < 8 '''
    data = np.array([
        [9,9,9,9,9,9,9],
        [8,8,8,8,8,8,8],
        [7,7,7,7,7,7,7],
        [6,6,6,6,6,6,6],
        [5,5,5,5,5,5,5],
        ])
    
    data = np.array([
        [0,0,0,20,0,0,0],
        [0,0,20,50,20,0,0],
        [0,7,50,90,50,7,0],
        [0,0,20,50,20,0,0],
        [0,0,0,20,0,0,0],
        ])
    plt.matshow(data)
    
    imgObj = image(data = data)
    X= DCT(imgObj)
    E = Encode(X)
    #plt.matshow(abs(X.coeffs1))
    #plt.matshow((X.coeffs))
    X_q = X.downsample(0.75)
    
    plt.matshow(X_q)
    zz = E.zigzag()
    ''' test2: data dims  = 8 '''
    data=  np.random.randint(5, size=(8, 8))
    data = np.full((8,8), 255)
    
    
    
    
    ''' test3: data is an image  '''
    '''
    path = "peppers.png"
    
    x = DCT(inPath = path)
    
    
    freqs = x.DCT_Image
    #display the frequencies
    Img = Image.fromarray( freqs , 'L')
    Img.show()
    '''
    
    
    