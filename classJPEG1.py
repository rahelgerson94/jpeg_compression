#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:08:35 2022

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
        #self.coeffs = fftpack.dct(self.x) #built in quantization 
        self.coeffs = fftpack.dct(fftpack.dct(data, axis=0), axis=1) #this works 4/19
        #self.coeffs1 = self.DCT()
        self.coeffs1 = self.dct2() #this works 4/19
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
    
    def DCT(self): #FIXME doesn't work
        data = self.x - 128
        M, N = self.x.shape # (img x, img y)
        dct = np.zeros((M,N),dtype=complex)
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
                dct[i,j] = ci*cj*tempSum
        return dct
    def dct2(self):
        M = self.x.shape[0]
        N = self.x.shape[1]
        a = empty([M,N],float)
        X = empty([M,N],float)
    
        for i in range(M):
            a[i,:] = self.dct(self.x[i,:])
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
   
    def idct(self, a):
        N = len(a)
        c = empty(N+1,complex)
    
        phi = exp(1j*pi*arange(N)/(2*N))
        c[:N] = phi*a
        c[N] = 0.0
        return irfft(c)[:N]
    
    def idct2(self):
        #b - self.X
        M = self.coeffs.shape[0]
        N = self.coeffs.shape[1]
        a = empty([M,N],float)
        y = empty([M,N],float)
    
        for i in range(M):
            a[i,:] = self.idct(self.X[i,:])
        for j in range(N):
            y[:,j] = self.idct(a[:,j])
        return y

class Encode:
    def __init__(self, DCTObj):
        self.X_q = DCTObj.coeffs_quantized
        self.N = X.N
        self.origShape = self.X_q.shape
 
    def zigzag(self):
        h = 0
        v = 0
        vmin = 0
        hmin = 0
        vmax = self.X_q.shape[0]
        hmax = self.X_q.shape[1]
        i = 0
        
        output = np.zeros(( vmax * hmax), dtype = np.float32)
        while ((v < vmax) and (h < hmax)):
        	
            if ((h + v) % 2) == 0:                 # going up
                
                if (v == vmin):
                	#print(1)
                    output[i] = self.X_q[v, h]        # if we got to the first line

                    if (h == hmax):
                        v = v + 1
                    else:
                        h = h + 1                        

                    i = i + 1

                elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
                	#print(2)
                	output[i] = self.X_q[v, h] 
                	v = v + 1
                	i = i + 1

                elif ((v > vmin) and (h < hmax -1 )):    # all other cases
                	#print(3)
                	output[i] = self.X_q[v, h] 
                	v = v - 1
                	h = h + 1
                	i = i + 1

            else:                                    # going down

            	if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
            		#print(4)
            		output[i] = self.X_q[v, h] 
            		h = h + 1
            		i = i + 1
            
            	elif (h == hmin):                  # if we got to the first column
            		#print(5)
            		output[i] = self.X_q[v, h] 

            		if (v == vmax -1):
            			h = h + 1
            		else:
            			v = v + 1

            		i = i + 1

            	elif ((v < vmax -1) and (h > hmin)):     # all other cases
            		#print(6)
            		output[i] = self.X_q[v, h] 
            		v = v + 1
            		h = h - 1
            		i = i + 1

            if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
            	#print(7)        	
            	output[i] = self.X_q[v, h] 
            	break

        return output
    ''' run length encoding'''
    def rle(self, coeffs):
        i = 0
        rle = []
        thresh = 16
        while i < len(coeffs):
            
            dontAppend = False
            zcount = 0
            # if i == 0: #skip the dc coeff
            #     i = i + 1
            #     continue
            #else:
            while coeffs[i] == 0:
                zcount += 1
                print("zcount: {}" .format(zcount))
                i +=1 
                if i == len(coeffs) : 
                    break
            
            if zcount >= thresh:
                if i < len(coeffs):
                    dontAppend = True
                    expandedTuples = self.fix((zcount, coeffs[i]), thresh)
                    for tup in expandedTuples:
                        rle.append(tup)
                    i+=1
                else:
                    rle.append((0,0))
                    return rle
            else:
                if i < len(coeffs) and dontAppend == False:
                    rle.append((zcount, coeffs[i]))
                    i += 1
                    
                else: #boundary checking
                    break
    
        return rle

    def fix(self, tupleVal, thresh):
        numChunks = int(tupleVal[0]/thresh)
        rem = tupleVal[0] % thresh + 1
        zeroCountValues = [i*thresh - 1 for i in range(1,numChunks+1)]
        tuples = []
        for zc in zeroCountValues:
            tuples.append((zc, 0))
        tuples.append((rem, tupleVal[1]))
        return tuples

class Decode:
    def __init__(self, DCTobj, rle):
        ''' rle_data is the list of tuples 
            origDims: original dimensions of dctmatrix, 
            which equal the dimensions of the image
        '''
        self.rle_data = rle
        self.array = [] # output of inverse run-length encoding
        self.DCTMatrix = np.zeros(()) #output of inverse zigzag
        self.origShape = X.coeffs.shape #orig
   
    #turn 1d arr to 2d matrix
    def  inverse_zigzag(self): 
        vmax = self.origShape[0]
        hmax = self.origShape[1]
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

        
if __name__ == "__main__":
    ''' test1: data dims < 8 '''
    
    
    plt.matshow(data)
    
    imgObj = image(data = data)
    X= DCT(imgObj)
    X_q = X.downsample()
    plt.matshow(abs(X.coeffs1)) #my DCT 
    plt.matshow((X.coeffs)) # python's built in DCT. 
    
    E = Encode(X)
    
    zz = E.zigzag() # #verified 4/21 for 1 case
    rle = E.rle(zz)
    
    #D = Decode(X.coeffs.shape, rle)
    D = Decode(X, rle)
    inv_rle = D.inverse_rle() #verified 4/21 for 1 case
    arr = D.inverse_zigzag() #verified 4/21 for 1 case
    x = (zz == inv_rle)
    
    ''' test2: data dims  = 8 '''
    
    
    
    ''' test3: data is an image  '''
    '''
    path = "peppers.png"
    
    x = DCT(inPath = path)
    
    
    freqs = x.DCT_Image
    #display the frequencies
    Img = Image.fromarray( freqs , 'L')
    Img.show()
    '''
    
    
    