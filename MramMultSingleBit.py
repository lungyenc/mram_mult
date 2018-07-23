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
import matplotlib.pyplot as plt
import MramSettings as ms

class MramMultSingleBit:

    def __init__(self, nRow=None, nCol=None):
        self.nRow = nRow    # number of rows for the MRAM array
        self.nCol = nCol    # number of cols for the MRAM array
        self.wCon = np.zeros((self.nRow, self.nCol, 2))  # conductance array
        self.wCon[:, :, 1] = np.random.normal(ms.cpM, ms.cpStd, 
        (self.nRow, self.nCol))
        self.wCon[:, :, 0] = np.random.normal(ms.capM, ms.capStd, 
        (self.nRow, self.nCol))      
        print(self.wCon)

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
            raise ValueError('The dimensions of the W, X matrix dont match')
        # Multiplication
        y = np.zeros((x0, w1))
        for k in range(x0):
            for n in range(w1):
                # Conductance summation
                acc = 0.
                for m in range(w0):
                    acc += self.wCon[m, n, int((w[m, n]*x[k, m]+1)/2)]
                # Perfect ADC readout
                accShift = acc - self.nRow * ms.capM - 0.5*ms.md
                diff = accShift // ms.md
                if (diff >= 0 and diff <= self.nRow-2):
                    y[k, n] = -self.nRow + 2*diff + 2
                elif (diff <0):
                    y[k, n] = -self.nRow
                else:
                    y[k, n] = self.nRow
                print(str(k)+' '+str(n)+' '+str(m)+' '+str(acc)+' '+str(accShift)+' '+str(diff)+' '+str(ms.md)+' '+str(y[k,n]))
        return y

### Class Test ###
if __name__ == '__main__':
    testR = 16
    testC = 2
    testXR = 1
    testXC = testR
    test = MramMultSingleBit(testR, testC)
    # tes2 = MramMultSingleBit.fromW(np.zeros((3,2)))
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

