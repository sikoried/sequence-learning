#!/usr/bin/python

# nnet forward pass and error backpropagation

import csv
import numpy as np
from random import seed, random, choice

X = []
Y = []

# read in feature data
with open('wheat-seeds.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        X.append([float(f) if f else 0.0 for f in row[:-1]])
        y = [0, 0, 0]
        y[int(row[-1])-1] = 1
        Y.append(y)

X = np.array(X)
Y = np.array(Y)

# partition data in train ({X,Y}tr) and test ({X,Y}te)
nte = 10
Xtr = X[:-nte]
Ytr = Y[:-nte]
Xte = X[-nte:]
Yte = Y[-nte:]


# nonlinearity: Sigmoid, and its derivative
def nonlin(x, deriv=False):
	if deriv:
		return x * (1 - x)
	else:
		return 1. / (1. + np.exp(-x))


# inner layer is a matrix (outputs, inputs+1)
# to add the bias term
def mkinner(inputs, outputs):
	return np.random.rand(outputs, inputs+1)


#def softmax(x):
#    e_x = np.exp(x)
#    return e_x / e_x.sum()

# compute a forward pass, store the activations
# forward pass per node is 
#   act = nonlin(b + sum_i w_i x_i)
#       = nonlin(dot([w_0, ..., w_d, bias], [x_0, ..., x_d, 1]))
def forward(x, layers):
	acts = []
	for l in layers:
		act = np.matmul(l, np.append(x, 1))
		x = nonlin(a)
	return acts


