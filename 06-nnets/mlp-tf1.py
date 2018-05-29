#!/usr/bin/pyton

import csv
import numpy as np

X = []
Y = []

# read in feature data
with open('wheat-seeds.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        X.append([float(f) if f else 0.0 for f in row[:-1]])
        y = [0., 0., 0.]
        y[int(row[-1])-1] = 1.0
        Y.append(y)

X = np.array(X)
Y = np.array(Y)

# partition data in train ({X,Y}tr) and test ({X,Y}te)
nte = 10
Xtr = X[:-nte]
Ytr = Y[:-nte]
Xte = X[-nte:]
Yte = Y[-nte:]


import tensorflow as tf

inputs = 7  # see wheat-seed.csv
hidden = 25
outputs = 3  # one-hot encoding of three classes (line 14)

x_ = tf.placeholder(tf.float32, [None, inputs])

# hidden
W1 = tf.Variable(tf.random_normal([inputs, hidden], stddev=0.01))
b1 = tf.Variable(tf.zeros([hidden]))
y1 = tf.nn.sigmoid(tf.matmul(x_, W1) + b1)

# output
W2 = tf.Variable(tf.zeros([hidden, outputs]))
b2 = tf.Variable(tf.zeros([outputs]))
y2 = tf.nn.softmax(tf.matmul(y1, W2) + b2)

#output
pred_y = tf.argmax(y2, 1)
y_ = tf.placeholder(tf.float32, [None, outputs])


# training
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y2), 
	reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.2).minimize(cross_entropy)


with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())

	for _ in range(10000):
		p = np.random.permutation(len(Xtr))
		x_batch = Xtr[p]
		y_batch = Ytr[p]
		sess.run(train_step, feed_dict={x_: x_batch, y_: y_batch})

	Ypred = sess.run(y2, feed_dict={x_: Xte})
	correct_prediction = tf.equal(tf.argmax(Yte, 1), tf.argmax(Ypred, 1))

	print Yte, Ypred, sess.run(correct_prediction)
