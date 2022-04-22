class Decode:
    def __init__(self, origDims, encodedData):
        ''' encodedData is the list of tuples 
            origDims: original dimensions of dctmatrix, 
            which equal the dimensions of the image
        '''
        self.encodedData = encodedData
        self.array = [] # output of inverse run-length encoding
        self.DCTMatrix = np.zeros(()) #output of inverse zigzag
        self.origDims = origDims #orig
    
    def  inverse_zigzag(self):
        vmax = self.origDims[0]
        hmax = self.origDims[1]
        h = 0
        v = 0
        vmin = 0
        hmin = 0
        
        output = np.zeros((vmax, hmax))
        i = 0

        while (v < vmax) and (h < hmax):
            if ((h + v) % 2) == 0:                 # going up
                
                if (v == vmin):
                    output[v, h] = self.encodedData[i]        # if we got to the first line

                    if (h == hmax):
                        v = v + 1
                    else:
                        h = h + 1                        
    
                    i = i + 1

                elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
                    output[v, h] = self.encodedData[i] 
                    v = v + 1
                    i = i + 1

                elif ((v > vmin) and (h < hmax -1 )):    # all other cases
                    output[v, h] = self.encodedData[i] 
                    v = v - 1
                    h = h + 1
                    i = i + 1

            else:                                    # going down

                if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
                    output[v, h] = self.encodedData[i] 
                    h = h + 1
                    i = i + 1
            
                elif (h == hmin):                  # if we got to the first column
                    output[v, h] = self.encodedData[i] 
                    if (v == vmax -1):
                        h = h + 1
                    else:
                        v = v + 1
                    i = i + 1
                elif((v < vmax -1) and (h > hmin)):     # all other cases
                    output[v, h] = self.encodedData[i] 
                    v = v + 1
                    h = h - 1
                    i = i + 1
            if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
                output[v, h] = self.encodedData[i] 
                break
        return output
    