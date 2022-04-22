#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 09:33:00 2022

@author: rahelmizrahi
"""

def reverse(matrix,  i,  j,  k,  col,  x) :
    if (j >= 0 and k < col):
        reverse(matrix, i, j - 1, k + 1, col, x)
        x.append(matrix[j][k])
        #  Display element
        return x

def reverseP(matrix,  i,  j,  k,  col) :
    print(j,k)
    if (j >= 0 and k < col) :
        reverseP(matrix, i, j - 1, k + 1, col)
        #  Display element
        print(matrix[j][k], end =" ")        
matrix = [
    [1, 2, 3, 4], 
    [6, 7, 8, 9], 
    [11, 12, 13, 14], 
    [16, 17, 18, 19], 
    [1, 2, 3, 4]]
col = 4
i = 1
j = 4
k = 1
x = reverse(matrix, i, j, k, col, [])
#reverseP(matrix, i, j, k, col)