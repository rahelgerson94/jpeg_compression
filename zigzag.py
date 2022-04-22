#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 16:40:43 2022

@author: rahelmizrahi
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 16:38:33 2022

@author: rahelmizrahi
"""

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

def zigzag(matrix):
    #initializing the variables
    #----------------------------------
    h = 0
    v = 0

    vmin = 0
    hmin = 0

    vmax = matrix.shape[0]
    hmax = matrix.shape[1]
    
    #print(vmax ,hmax )

    i = 0

/Users/rahelmizrahi/Desktop/ece533/ece533_image_compression/ece533_image_compression_codes/untitled5.py
    output = np.zeros(( vmax * hmax))
    #----------------------------------

    while ((v < vmax) and (h < hmax)):
    	
        if ((h + v) % 2) == 0:                 # going up
            
            if (v == vmin):
            	#print(1)
                output[i] = matrix[v, h]        # if we got to the first line

                if (h == hmax):
                    v = v + 1
                else:
                    h = h + 1                        

                i = i + 1

            elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
            	#print(2)
            	output[i] = matrix[v, h] 
            	v = v + 1
            	i = i + 1

            elif ((v > vmin) and (h < hmax -1 )):    # all other cases
            	#print(3)
            	output[i] = matrix[v, h] 
            	v = v - 1
            	h = h + 1
            	i = i + 1

        
        else:                                    # going down

        	if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
        		#print(4)
        		output[i] = matrix[v, h] 
        		h = h + 1
        		i = i + 1
        
        	elif (h == hmin):                  # if we got to the first column
        		#print(5)
        		output[i] = matrix[v, h] 

        		if (v == vmax -1):
        			h = h + 1
        		else:
        			v = v + 1

        		i = i + 1

        	elif ((v < vmax -1) and (h > hmin)):     # all other cases
        		#print(6)
        		output[i] = matrix[v, h] 
        		v = v + 1
        		h = h - 1
        		i = i + 1




        if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
        	#print(7)        	
        	output[i] = matrix[v, h] 
        	break

    #print ('v:',v,', h:',h,', i:',i)
    return output




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
    
