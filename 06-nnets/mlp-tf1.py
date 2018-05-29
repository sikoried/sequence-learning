#!/usr/bin/pyton

import csv

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


import tensorflow as tf

inputs = len(Xtr[0])
hidden = 25
output = 3

x = tf.placeholder(tf.float32, [None, inputs])

# hidden
W1 = tf.Variable(tf.zeros([inputs, hidden]))
b1 = tf.Variable(tf.zeros([hidden]))
y1 = tf.nn.sigmoid(tf.matmul(x, W1) + b1)

# output
W2 = tf.Variable(tf.zeros([hidden, 3]))
b2 = tf.Variable(tf.zeros([3]))
y2 = tf.nn.softmax(tf.matmul(y1, W2) + b2)

#output
y = y2
y_ = tf.placeholder(tf.float32, [None, 3])


# training
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), 
	reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.2).minimize(cross_entropy)

with tf.InteractiveSession() as sess:
	tf.global_variables_initializer().run()

	for _ in range(10000):
	  batch_xs, batch_ys = mnist.train.next_batch(100)
	  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

	correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

	print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: 
	mnist.test.labels}))