#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 12:21:52 2022

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

class Encode:
    def __init__(self, DCTObj):
        self.X_q = DCTObj.coeffs_quantized
        self.N = DCTObj.N
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
                #print("zcount: {}" .format(zcount))
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
if __name__ == "__main__":
    pass
