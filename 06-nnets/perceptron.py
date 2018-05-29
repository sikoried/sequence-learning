#!/usr/bin/python

# Perceptron learning

import csv
import numpy as np
import random

X = []
Y = []

# read in feature data
with open('admission.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        X.append(np.array([float(f) for f in row[:-1]]))
        Y.append(float(row[-1]))

# partition data in train ({X,Y}tr) and test ({X,Y}te)
nte = 10
Xtr = X[:-nte]
Ytr = Y[:-nte]
Xte = X[-nte:]
Yte = Y[-nte:]


def pred(a0, a, x):
	return a0 + np.dot(a, x)


def loss(a0, a, xs, ys):
	l = 0
	for x, y in zip(xs, ys):
		p = pred(a0, a, x)
		if y * p < 0:
			l -= (y * p)
	return l


# learning rate
lr = 1

# init alpha
alpha0 = 0
alpha = np.zeros(len(Xtr[0]))

cur_loss = loss(alpha0, alpha, Xtr, Ytr)
iters = 1000
while iters > 0:
	i = random.choice(range(len(Xtr)))
	x = Xtr[i]
	y = Ytr[i]

	# predict
	yhat = pred(alpha0, alpha, x)
	print x, y, yhat

	if y * yhat <= 0:
		alpha0 = alpha0 + lr * y
		alpha = alpha + lr * y * x
		print alpha0, alpha

	loss_tr, loss_te = loss(alpha0, alpha, Xtr, Ytr), loss(alpha0, alpha, Xte, Yte)
	
	print loss_tr, loss_te
	iters -= 1

print alpha0, alpha
