# MramMultSingleBit.py
# This class samples an MRAM array with varations and provides multiplication
# function assuming ideal read out circuits.
# ---------------
# File dependecy:
# [1] MramSettings.py # MRAM cell parameters
# ---------------
# Lung-Yen Chen
# lungyenc@princeton.edu

import sys
import math
import numpy as np
import mram_mult.MramSettings as ms


class MramMultSingleBit:

    def __init__(self, nRow=None, nCol=None):
        self.nRow = nRow    # number of rows for the MRAM array
        self.nCol = nCol    # number of cols for the MRAM array
        self.wCon = np.zeros((self.nRow, self.nCol, 4))  # conductance array
        for i in range(2,4):
            self.wCon[:, :, i] = np.random.normal(ms.cpM, ms.cpStd, 
            (self.nRow, self.nCol))
        for i in range(2):
            self.wCon[:, :, i] = np.random.normal(ms.capM, ms.capStd, 
            (self.nRow, self.nCol))      

    @classmethod
    def fromW(cls, w):
        return cls(np.size(w, 0), np.size(w,1))

    def multXW(self, x, w):
        # Check matrix dimension
        w0 = np.size(w, 0)
        w1 = np.size(w, 1)
        x0 = np.size(x, 0)
        x1 = np.size(x, 1)
        if (self.nRow != w0 or self.nCol != w1):
            raise ValueError('The dimension of the W matrix is not the same as '
            'the Mram cell size')
        if (w0 != x1):
            raise ValueError('The dimensions of the W, X matrix do not match')
        # Matrix Mapping
        # w mapping
        wM = np.zeros((2*w0, w1))
        for m in range(w0):
            for n in range(w1):
                if (w[m, n] == 1):
                    wM[2*m, n] = (self.wCon[m, n, 2] + self.wCon[m, n, 0])/2
                    wM[2*m+1, n] = (self.wCon[m, n, 2] - self.wCon[m, n, 0])/2
                else:
                    wM[2*m, n] = (self.wCon[m, n, 3] + self.wCon[m, n, 1])/2
                    wM[2*m+1, n] = (-self.wCon[m, n, 3] + self.wCon[m, n, 1])/2
        print(wM)
        # x mapping
        xM = np.zeros((x0, 2*x1))
        for k in range(x0):
            for m in range(x1):
                if (x[k, m] == 1):
                    xM[k, 2*m] = 1
                    xM[k, 2*m+1] = 1
                else:
                    xM[k, 2*m] = 1
                    xM[k, 2*m+1] = -1               
        print(xM)     
        # Multiplication
        y = np.dot(xM, wM)
        print(y)
        # Perfect ADC readout
        for k in range(x0):
            for n in range(w1):
                accShift = y[k, n] - self.nRow * ms.capM - 0.5*ms.md
                diff = accShift // ms.md
                if (diff >= 0 and diff <= self.nRow-2):
                    y[k, n] = -self.nRow + 2*diff + 2
                elif (diff <0):
                    y[k, n] = -self.nRow
                else:
                    y[k, n] = self.nRow
        return y

### Class Test ###
if __name__ == '__main__':   
    testR = 128
    testC = 3
    testXR = 1
    testXC = testR
    test = MramMultSingleBit(testR, testC)
    w = np.random.random((testR, testC))
    for i in range(testR):
        for j in range(testC):
            w[i, j] = 1 if w[i, j] < 0.5 else -1
    print(w)
    x = np.random.random((testXR, testXC))
    for i in range(testXR):
        for j in range(testXC):
            x[i, j] = 1 if x[i, j] < 0.5 else -1   
    print(x) 
    y = test.multXW(x, w)
    print(y)
    print(np.dot(x, w))

