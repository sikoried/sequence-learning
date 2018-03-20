#!/usr/bin/python

from __future__ import print_function, division
import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as mpl


num_epochs = 100
total_series_length = 920
truncated_backprop_length = 15
state_size = 4
num_classes = 4
batch_size = 5
num_batches = total_series_length//batch_size//truncated_backprop_length
num_layers = 3

def fizz_buzz_encode(i):
    if   i % 15 == 0: return 3
    elif i % 5  == 0: return 2
    elif i % 3  == 0: return 1
    else:             return 0

def generateData():
    x = np.array(range(101, 2**10-3))
    y = np.array(map(fizz_buzz_encode, range(101, 2**10-3)))
    x = x.reshape((batch_size, -1))  # The first index changing slowest, subseries as rows
    y = y.reshape((batch_size, -1))

    return (x, y)

batchX_placeholder = tf.placeholder(tf.float32, [batch_size, truncated_backprop_length])
batchY_placeholder = tf.placeholder(tf.int32, [batch_size, truncated_backprop_length])


init_state = tf.placeholder(tf.float32, [num_layers, 2, batch_size, state_size])

state_per_layer_list = tf.unstack(init_state, axis=0)
rnn_tuple_state = tuple(
    [tf.nn.rnn_cell.LSTMStateTuple(state_per_layer_list[idx][0], state_per_layer_list[idx][1])
     for idx in range(num_layers)]
)

W2 = tf.Variable(np.random.rand(state_size, num_classes),dtype=tf.float32)
b2 = tf.Variable(np.zeros((1, num_classes)), dtype=tf.float32)

# Unpack columns
# inputs_series = tf.split(value=batchX_placeholder, num_or_size_splits=truncated_backprop_length, axis=1)
labels_series = tf.unstack(batchY_placeholder, axis=1)

# Forward passes
stacked_rnn = []
for iiLyr in range(num_layers):
    stacked_rnn.append(tf.nn.rnn_cell.LSTMCell(state_size, state_is_tuple=True))

multiLyr_cell = tf.nn.rnn_cell.MultiRNNCell(stacked_rnn, state_is_tuple=True)


states_series, current_state = tf.nn.dynamic_rnn(cell=multiLyr_cell, inputs=tf.expand_dims(batchX_placeholder, -1), initial_state=rnn_tuple_state)
states_series = tf.reshape(states_series, [-1, state_size])

logits = tf.matmul(states_series, W2) + b2 #Broadcasted addition
labels = tf.reshape(batchY_placeholder, [-1])

logits_series = tf.unstack(tf.reshape(logits, [batch_size, truncated_backprop_length, num_classes]), axis=1)
predictions_series = [tf.nn.softmax(logit) for logit in logits_series]

losses = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels)

# losses = [tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels) for logits, labels in zip(logits_series,labels_series)]
total_loss = tf.reduce_mean(losses)

train_step = tf.train.AdagradOptimizer(0.3).minimize(total_loss)

def plot(loss_list, predictions_series, batchX, batchY):
    mpl.subplot(2, 3, 1)
    mpl.cla()
    mpl.plot(loss_list)

    for batch_series_idx in range(5):
        one_hot_output_series = np.array(predictions_series)[:, batch_series_idx, :]
        single_output_series = np.array([(1 if out[0] < 0.5 else 0) for out in one_hot_output_series])

        mpl.subplot(2, 3, batch_series_idx + 2)
        mpl.cla()
        mpl.axis([0, truncated_backprop_length, 0, 2])
        left_offset = range(truncated_backprop_length)
        mpl.bar(left_offset, batchX[batch_series_idx, :], width=1, color="blue")
        mpl.bar(left_offset, batchY[batch_series_idx, :] * 0.5, width=1, color="red")
        mpl.bar(left_offset, single_output_series * 0.3, width=1, color="green")

    mpl.draw()
    mpl.pause(0.0001)


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    mpl.ion()
    mpl.figure()
    mpl.show()
    loss_list = []

    for epoch_idx in range(num_epochs):
        x,y = generateData()

        _current_state = np.zeros((num_layers, 2, batch_size, state_size))

        print("New data, epoch", epoch_idx)

        for batch_idx in range(num_batches):
            start_idx = batch_idx * truncated_backprop_length
            end_idx = start_idx + truncated_backprop_length

            batchX = x[:,start_idx:end_idx]
            batchY = y[:,start_idx:end_idx]

            _total_loss, _train_step, _current_state, _predictions_series,_logits_series, _labels_series = sess.run(
                [total_loss, train_step, current_state, predictions_series, logits_series, labels_series],
                feed_dict={
                    batchX_placeholder: batchX,
                    batchY_placeholder: batchY,
                    init_state: _current_state
                })

            # _current_cell_state, _current_hidden_state = _current_state

            loss_list.append(_total_loss)

            if batch_idx%100 == 0:
                print("Step",batch_idx, "Batch loss", _total_loss)
                plot(loss_list, _predictions_series, batchX, batchY)

    # todo: evaluate model for series 1..100

mpl.ioff()
mpl.show()