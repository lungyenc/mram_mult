# mram_mult
This package provides the binarized matrix multiplication on MRAM cells. Set up the MRAM parameters in the MramSettings file.
Example usage:

import mram_mult.MramMultSingleBit

test = MramMultSingleBit(4, 3)   # create an 4x3 mram array that stores the w matrix

w = np.random.random((4, 3))
for i in range(4):
    for j in range(3):
        w[i, j] = 1 if w[i, j] < 0.5 else -1
print(w)
x = np.random.random((1, 4))
for i in range(testXR):
    for j in range(testXC):
        x[i, j] = 1 if x[i, j] < 0.5 else -1   
print(x) 
y = test.multXW(x, w)
print(y)
