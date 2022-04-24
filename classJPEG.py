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
from math import ceil, floor
from  scipy import fftpack
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import pprint

from DCT import DCT
from image import image
from Encode import Encode
from Decode import Decode
import data_generator as data_gen

class JPEG:
    def __init__(self, data , N = None):
        if N is not None:
            self.N = N
        else:
            self.N = 8
        self.ImageObject = image(data = data, N = self.N)
        self.encoded_dcts = self.encodeLoop()
        #self.encodeLoop()
        
        '''
        self.entropy_encoded_list = [] 
        
        self.dctObject = DCT(self.ImageObject)
        self.DCTBlocks = DCT.dctLoop()
        self.EncodeObject = Encode(self.dctObject)
        
        rle = None
        self.DecodeObject = Decode(self.EncodeObject, rle ) #FIXME
        
        self.DCTBlocks = self.dctLoop( )
        '''
        
    '''loop over the rows, cols of image
        get the DCT of each 8x8 block
        return encoded dcts of each block
       this is the main wrapper function 
    '''   
    def encodeLoop(self): 
        encoded_dcts = []
        rowBlocks = self.ImageObject.yBlocks
        colBlocks = self.ImageObject.xBlocks
        N = self.N
        for y in range(0, rowBlocks):
            
            for x in range(0,colBlocks): #iterate horizontally
                col_left = x*N
                col_right = col_left + 8
                row_low = y*N
                row_high = row_low + 8
                #print(x_low, x_hi)
                print(y)
                currBlock = data[ row_low: row_high, col_left: col_right]
                #print( " ({}, {} ) , ({}, {} )".format(row_low, row_high, col_left, col_right))
                
                imgObj = image(data = currBlock)                
                dct = DCT(imgObj)  
                E = Encode(dct)
                zz = E.zigzag() 
                rle = E.rle(zz)
                encoded_dcts.append(rle)
        return encoded_dcts     
    def decodeLoop(self):
        imData = []
        for rle in self.encoded_dcts:
            D = Decode(self.ImageObject.origShape, rle)
            invRle = D.inverse_rle() #FIXME  produces a 1xm*n array not a 1 x 64 array
            invZZ = D.inverse_zigzag() #produces an 8x8 block
            imDataBlock = D.idct2(invZZ)
            imData.append(imDataBlock )
        return
        
if __name__ == "__main__":
    ''' test1: data dims < 8 '''
    '''
    img1 = data_gen.baseImage()
    data = data_gen.multiplyBaseImage(img1, 2)
    '''
    data = data_gen.cosImage(16, 32)
    plt.matshow(data)
    plt.title('image')
    plt.colorbar() 
    
    jpeg = JPEG(data)
    encoded_dcts = jpeg.encodeLoop() #verified 4/23
    imData1d = jpeg.decodeLoop( )
    
    
    