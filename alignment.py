import numpy as np

#SSDAlign performs ssd between image1 and image2, and then aligns them.
#It does it in the nested for loop style.
def ssdAlign(rollImg, baseImg):
    # numRows = baseImg.shape[0]
    # numCols = baseImg.shape[1]
    numRows = 35 #suggested window size by assignment
    numCols = 35

    minSSD = False
    currRollImg = rollImg
    bestAligned = False
    # use roll to brute force try matches.
    for i in range(-numRows, numRows-1):
        for j in range(-numCols, numCols-1):
            if (i == 0 or j == 0):
                continue
            #make sure to roll both x and y in order to get all combos
            rolledImg = np.roll(currRollImg, (i, j), axis=(0, 1))
            ssd = np.sum((rolledImg-baseImg)**2) #apply SSD formula
            # cases where minSSD are replaced
            if (minSSD == False or ssd<minSSD):
                minSSD = ssd
                # save where the best alignment is in coordination with base input
                bestAligned = [i, j] #this is the rows/columns moved. scale comes in at the pyramid lvl
                #bestAligned = rolledImg

    print("best alignment movements are:", bestAligned)
    return (bestAligned, minSSD)


