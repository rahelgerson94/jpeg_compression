#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 15:41:23 2022

@author: rahelmizrahi
"""

from PIL import Image, ImageOps
import numpy as np

class JPEG:
    def __init__(self,inPath, compressionLevel = None, N = 8):
        self.inPath = inPath
        self.compressionLevel = compressionLevel
        self.DFT = np.zeros(shape= (8,8))
        self.data = np.asarray(ImageOps.grayscale(Image.open(inPath))) - 128
        self.N = 8 # sections off the image into blocks of NxN
        
    def DFT(self):
        pass
    
    def DFT8x8(self, M): #compute DFT entires for an 8x8 block of pixels
    #M is an 8x8 subsection of the image. 
        T = self.T()
        D = T * M * T.T
        return D
    
    def T(self):
        T = np.zeros(shape= (8,8))
        N = self.N
        for i in range(N):
            for j in range(N):  
                if i == 0:
                    T[i][j] = 1/np.sqrt(N)
                else:
                    T[i][j] = np.sqrt(2/N) *np.cos( ((2*j + 1) * i * np.pi) / (2*N) )
        return T
    
    def quantize(self):
        pass
    def decode(self):
        pass
    def encode(self):
        pass


if __name__ == "__main__":
    
    path = "toast.png"
    #image = Image.open(path)
    #img = np.asarray(ImageOps.grayscale(Image.open(path))) # read image as grayscale. Set second parameter to 1 if rgb is required 
    test = JPEG(path)
    
    
    
    
    
    
    
    