#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 09:06:32 2022

@author: rahelmizrahi
"""

#  Python 3 program for
#  Zigzag traversal of matrix

#  Display reverse order elements
def reverse(matrix,  i,  j,  k,  col) :
    if (j >= 0 and k < col) :
        reverse(matrix, i, j - 1, k + 1, col)
        #  Display element
        print(matrix[j][k], end =" ")


def zigzag(matrix):
    #  Auxiliary variables
    x = []
    i = 0
    j = 0
    k = 0
    counter = 0
    #  Get the length number of rows
    #  And number of columns
    row = len(matrix)
    col = len(matrix[0])
    #  First half which contain element of top left triangle
    while (i < row) :
        if (counter % 2 == 0) :
            j = 0
            while (j <= i and j < col and i - j >= 0) :
                #  Display element
                print(matrix[i - j][j], end =" ")
                x.append(matrix[i - j][j])
                j += 1
        else :
            j = i
            k = 0
            while (j >= 0 and j < col and k <= i) :
                #  Display element
                print(matrix[k][j], end =" ")
                x.append(matrix[k][j])
                
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
                print(matrix[j][k], end =" ")
                x.append(matrix[j][k])
                j -= 1
                k += 1
        else :
            reverse(matrix, i, row - 1, i, col)
        counter += 1
        i += 1

def main() :
    matrix = [
        [1, 2, 3, 4], 
        [6, 7, 8, 9], 
        [11, 12, 13, 14], 
        [16, 17, 18, 19], 
        [1, 2, 3, 4]
    ]
    #  Test
    zigzag(matrix)


if __name__=="__main__":
    main()