#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 13:18:33 2022

@author: rahelmizrahi
"""

#coeffs = [-30, 2, -5, 0, -2, 1, -2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
coeffs = [1,0,0,0,0,0, 8, 0,0, 1]
''' run length encoding'''
def rle(coeffs):
    i = 0
    rle = []
    
    while i < len(coeffs):
        dontAppend = False
        zcount = 0
        if i == 0:
            i = i + 1
            continue
        else:
            while coeffs[i] == 0:
                zcount += 1
                i +=1 
                if i == len(coeffs) : 
                    break
            thresh = 4
            if zcount >= thresh:
                dontAppend = True
                expandedTuples = fix((zcount, coeffs[i]), thresh)
                for tup in expandedTuples:
                    rle.append(tup)
                i+=1
            else:
                if i < len(coeffs) and dontAppend == False:
                    rle.append((zcount, coeffs[i]))
                    i += 1
                else: #boundary checking
                    break
    rle.append((0,0))
    return rle

def fix(tupleVal, thresh):
    numChunks = int(tupleVal[0]/thresh)
    rem = tupleVal[0] % thresh + 1
    zeroCountValues = [i*thresh - 1 for i in range(1,numChunks+1)]
    tuples = []
    for zc in zeroCountValues:
        tuples.append((zc, 0))
    tuples.append((rem, tupleVal[1]))
    return tuples

bla = fix((16, 8), 4)
bla2 = rle(coeffs)