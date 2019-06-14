#!/usr/bin/python


import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense

with open('admission.asc') as f:
    xs = list()
    ys = list()
    for l in f:
        x1, x2, y = l.strip().split()
        xs.append(map(float, [x1, x2]))
        ys.append(int(y))

xs = np.array(xs)
ys = keras.utils.to_categorical(np.array(ys))


# partition, randomly
perm = np.random.permutation(len(xs))
n = 72
x_train = xs[perm[:n]]
y_train = ys[perm[:n]]

x_test = xs[perm[n:]]
y_test = ys[perm[n:]]


model = Sequential()

model.add(Dense(units=12, activation='relu', input_dim=2))
model.add(Dense(units=4, activation='sigmoid'))
model.add(Dense(units=8, activation='tanh'))
model.add(Dense(units=2, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True))

model.fit(x_train, y_train, epochs=10, batch_size=4)

loss_and_metrics = model.evaluate(x_test, y_test, batch_size=4)
classes = model.predict(x_test, batch_size=4)

loss_and_metrics
classes