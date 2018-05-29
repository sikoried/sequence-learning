#!/usr/bin/python

import numpy as np

def nonlin(x,deriv=False):
    if deriv:
        return x*(1-x)
    else:
        return 1/(1+np.exp(-x))
    
X = np.array([[0,0,1],
            [0,1,1],
            [1,0,1],
            [1,1,1],
            [2,2,1],
            [0,0,1]])
                
y = np.array([[0],
			[1],
			[1],
			[0],[0],[0]])

# seed the NRG for reproducible results
np.random.seed(1)

# randomly initialize our weights with mean 0
#layer0 = 2 * np.random.rand(4, 3) - 1  # mean weight 0
#layer1 = 2 * np.random.rand(1, 4) - 1

# for exact compatibility with the original script nnet2_orig.py
# to maintain the same rand() calls
# but then save transposeds.
layer0 = 2 * np.random.rand(3, 4) - 1  # mean weight 0
layer1 = 2 * np.random.rand(4, 1) - 1

layer0 = layer0.T
layer1 = layer1.T

learning_rate = 1

for j in xrange(60000):

	# Feed forward through layers 0, 1, and 2
    l0 = X.T
    l1 = nonlin(np.matmul(layer0, l0))
    l2 = nonlin(np.matmul(layer1, l1))

    # how much did we miss the target value?
    l2_error = y.T - l2
    
    if (j% 10000) == 0:
        print "Error:" + str(np.mean(np.abs(l2_error)))
        
    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l2_delta = l2_error * nonlin(l2, deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l1_error = np.matmul(layer1.T, l2_delta)
    
    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l1_delta = l1_error * nonlin(l1, deriv=True)

    # sum up the partial contributions by each sample to form
    # the final gradient
    layer1 += (learning_rate * np.matmul(l2_delta, l1.T))
    layer0 += (learning_rate * np.matmul(l1_delta, l0.T))

print layer0, layer1
