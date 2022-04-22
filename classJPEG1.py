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

from DCT import DCT
from image import image
from Encode import Encode
from Decode import Decode






        
if __name__ == "__main__":
    ''' test1: data dims < 8 '''
    
    c = [i for i in range(0,25)]
    r = [i for i in range(0,33)]
    C,R = np.meshgrid(r,c)
    wr =  0.25*pi # digital freq in the row dimension
    wc =  0.5 *pi # digital freq in the col dimension
    data =  30*cos(wr*R+wc*C) + 60*cos(wr*R+wc*C)
    
    plt.matshow(data)
    plt.title('image')
    plt.colorbar() 
    
    '''make image obj '''
    imgObj = image(data = data)
    
    '''make DCT obj '''
    X= DCT(imgObj)
    X_q = X.downsample()
    plt.matshow(abs(X.coeffs1)) #my DCT 
    plt.title('my DCT output')
    plt.colorbar() 
    
    plt.matshow((X.coeffs)) # python's built in DCT. 
    plt.title('pythons DCT output')
    plt.colorbar() 
   
    ''' Encode'''
    E = Encode(X)
    
    zz = E.zigzag() # #verified 4/21 for 1 case
    rle = E.rle(zz)
    
    #D = Decode(X.coeffs.shape, rle)
    ''' Decode'''
    D = Decode(X, rle)
    inv_rle = D.inverse_rle() #verified 4/21 for 1 case
    arr = D.inverse_zigzag() #verified 4/21 for 1 case
    x = (zz == inv_rle)
    
    ''' inverse DCT'''
    I = X.idct2(arr)
    plt.matshow(I)
    plt.colorbar() 
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
    
    
    