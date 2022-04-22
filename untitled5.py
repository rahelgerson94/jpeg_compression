#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Zigzag scan of a matrix
# Argument is a two-dimensional matrix of any size,
# not strictly a square one.
# Function returns a 1-by-(m*n) array,
# where m and n are sizes of an matrix matrix,
# consisting of its items scanned by a zigzag method.
#
# Matlab Code:
# Alexey S. Sokolov a.k.a. nICKEL, Moscow, Russia
# June 2007
# alex.nickel@gmail.com

import numpy as np




# Inverse zigzag scan of a matrix
# Arguments are: a 1-by-m*n array, 
# where m & n are vertical & horizontal sizes of an output matrix.
# Function returns a two-dimensional matrix of defined sizes,
# consisting of matrix array items gathered by a zigzag method.
#
# Matlab Code:
# Alexey S. Sokolov a.k.a. nICKEL, Moscow, Russia
# June 2007
# alex.nickel@gmail.com


def inverse_zigzag(matrix, vmax, hmax):
	
	#print matrix.shape

	# initializing the variables
	#----------------------------------
    h = 0
    v = 0

    vmin = 0
    hmin = 0

    output = np.zeros((vmax, hmax))

    i = 0
    while ((v < vmax) and (h < hmax)): 
        if ((h + v) % 2) == 0:                 # going up
            
            if (v == vmin):
                output[v, h] = matrix[i]        # if we got to the first line

                if (h == hmax):
                    v = v + 1
                else:
                    h = h + 1                        

                i = i + 1

        elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
            output[v, h] = matrix[i] 
            v = v + 1
            i = i + 1

        elif ((v > vmin) and (h < hmax -1 )):    # all other cases
            output[v, h] = matrix[i] 
            v = v - 1
            h = h + 1
            i = i + 1

        
        else:                                    # going down

            if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
                output[v, h] = matrix[i] 
                h = h + 1
                i = i + 1
        
            elif (h == hmin):                  # if we got to the first column
                output[v, h] = matrix[i] 
                if (v == vmax -1):
                    h = h + 1
                else:
                    v = v + 1
                i = i + 1
            elif((v < vmax -1) and (h > hmin)):     # all other cases
                output[v, h] = matrix[i] 
                v = v + 1
                h = h - 1
                i = i + 1




        if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
            output[v, h] = matrix[i] 
            break


    return output

if __name__ == "__main__":
    matrix = np.array([
        [1, 2, 3, 4], 
        [6, 7, 8, 9], 
        [11, 12, 13, 14], 
        [16, 17, 18, 19], 
        [1, 2, 3, 4]])
    zz = zigzag(matrix)
    Iz = inverse_zigzag(zz, 4, 4)
    
