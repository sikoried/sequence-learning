---
template: page
title: Neural Networks
permalink: 06/nnets/
mathjax: true
---

# Python and Numpy

If you haven't worked with python, here's an [extensive tutorial](http://cs231n.github.io/python-numpy-tutorial/).

If you worked with python before, you could proceed right to the [numpy tutorial](https://docs.scipy.org/doc/numpy/user/quickstart.html).


# Rosenblatt's Perceptron (1958)

Wow, neural nets are old... checkout Rosenblatt's [original publication](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.335.3398&rep=rep1&type=pdf).


## The Math

The decision function of the perceptron is

$$
\hat y = \text{sgn}(\mathbf{\alpha}^T \mathbf{x} + \alpha_0) .
$$

The loss function is 

$$
\mathrm{L}(\alpha_0, \mathbf{\alpha}) = -\sum_{x_i \in \mathrm{M}} y_i (\mathbf{\alpha}^T \mathbf{x}_i + \alpha_0) 
$$

where $\mathrm{M}$ are the misclassified samples.

If you minimize the loss with respect to the parameters, you end up with iterative update formulae for the bias ($\alpha_0$) and decision boundary ($\mathbf{\alpha}$):

$$
\alpha_0^{(k+1)} = \alpha_0^{(k)} + \lambda \cdot y_i ,
$$

$$
\mathbf{\alpha}^{(k+1)}= \mathbf{\alpha}^{(k)} + \lambda \cdot y_i \cdot \mathbf{x}_i .
$$


## The Code

Let's lift this formulation to python.
First, let's load the [data]({{site.baseurl}}/06-nnets/admission.zip); we need to read the CSV columns, and parse the fields to numeric values

```python
import csv
import numpy as np

X = []
Y = []

# read in feature data
with open('admission.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        X.append(np.array([float(f) for f in row[:-1]]))
        Y.append(float(row[-1]))
```

We need to partition the data into training and test:

```python
# partition data in train ({X,Y}tr) and test ({X,Y}te)
nte = 10
Xtr = X[:-nte]
Ytr = Y[:-nte]
Xte = X[-nte:]
Yte = Y[-nte:]
```

If we define the parameters of the perceptron as $\alpha_0$ and $\mathbf{\alpha}$, we can make predictions about feature data:

```python
a0 = 0
a = np.zeros(len(Xtr[0]))  # dimension of our data?

def pred(x):
	return a0 + np.dot(a, x)
```

Note that `numpy` has all the linear algebra magic implemented for us, no need to do `for`-loops etc.


Given sample data ($xs$) with labels ($ys$), we can compute the loss (see above):

```python
def loss(xs, ys):
	l = 0
	for x, y in zip(xs, ys):
		p = pred(x)

		# misclassified?
		if y * p < 0:
			l -= (y * p)
	return l
```

We're all set, so let's do some iterations!

```python
rate = 1.0  # learning rate, if you like...

iters = 1000
while iters > 0:
	# take a random sample
	i = random.choice(range(len(Xtr)))
	x = Xtr[i]
	y = Ytr[i]

	# predict
	yhat = pred(x)
	print x, y, yhat

	if y * yhat < 0:
		a0 = a0 + rate * y    # easy: all scalars.
		a = a + rate * y * x  # numpy ftw! element-wise ops
		print a0, a

	# print training and test loss
	print loss(Xtr, Ytr), loss(Xte, Yte)
	
	iters -= 1

# all done
print a0, a
```

## Lessons Learned

- Use numpy to do the math, eg. `dot`, `matmul`, `zeros`, `norm`, _etc._
- The vector/matrix notation can be confusing in numpy; practice will help you write neat code!

See the complete solution: [perceptron.py]({{site.baseurl}}/06-nnets/perceptron.py).


# Multi-layer Perceptron and Backpropagation

Now lets move from a single perceptron to a more general formulation and train using _error backpropagation_.
The following is based on this [excellent tutorial](https://iamtrask.github.io/2015/07/12/basic-python-network/).


## Prelims

The math is described in the [slides]({{site.baseurl}}/06-nnets/sl-mlp.pdf), but here's two key takeaways:

- We'll use the [sigmoid](https://en.wikipedia.org/wiki/Sigmoid_function) function as non-linearity:
	$$
	\sigma (x) = \frac{1}{1+e^{-x}}
	$$
- ...because it is so easy to differentiate:
	$$
	\frac{d\sigma (x)}{d(x)} = \sigma (x)\cdot (1-\sigma(x)) .
	$$
- For the output layer, people often use the [softmax](https://en.wikipedia.org/wiki/Softmax_function) function if they have more than one output node.


## A Toy Problem

Consider the mapping from input to (target) output:

|Inputs|Output|
|-------|-----|
| 0 0 1	| 0 |
| 1 1 1 | 1 |
| 1 0 1 | 1 |
| 0 1 1 | 0 |

Note that we add the third column with ones to the input to capture the bias:

$$
\hat y = \text{sgn}(\mathbf{\alpha}^T \mathbf{x} + \alpha_0) = 
	\text{sgn}\left(\left< \begin{pmatrix}\alpha_0 \\ \mathbf{\alpha}\end{pmatrix}, \begin{pmatrix}1 \\ \mathbf{x}\end{pmatrix} \right>\right)
$$

Unfortunately, this can't be linearly separated with a basic perceptron (which you can confirm visually).


## More Neurons, More Layers

A _multi-layer peceptron (MLP)_, or more fashionable, a _deep neural network (DNN)_, is a network of multiple perceptrons.
In Rosenblatt's perceptron above, we used the signum function, for DNNs, we typically chose the sigmoid function due to its convenient derivative:

```python
def nonlin(x, deriv=False):
	if deriv:
		return x * (1 - x)
	else:
		return 1 / (1 + np.exp(-x))
```

Note how smart numpy is: if you input a vector or matrix, it will apply everything element-wise!
Back to our XOR toy problem:

```python
X = np.array([[0,0,1],
			[0,1,1],
			[1,0,1],
			[1,1,1]])
                
y = np.array([[0],
			[1],
			[1],
			[0]])
```

Now we want to feed the inputs to a hidden layer with four neurons (perceptrons).
We'll connect every input to every node ("fully connected"), so each node will have three weights.
Remember that for the single neuron, we need to compute the dot product between weights and input, and then apply the non-linearity.

$$
y_k = f(\mathbf{w}_k^T \mathbf{x}) , k = 1, ..., 4
$$

If you define $f$ to be applied element-wise, you can use _matrix notation:_

$$
\mathbf{y} = f(W \mathbf{x})
$$

where $W^T = (\mathbf{w_1} \mathbf{w_2} \mathbf{w_3} \mathbf{w_4})$, ie. the rows $k$ of $W$ are the $\mathbf{w}_k$.
If you summarize all your data points in a matrix $X^T = (\mathbf{x}_1 \dots \mathbf{x}_n)$, ie. a matrix where the rows $i$ are the samples $\mathbf{x}_i$, you can compute all neuron activations in a single mathematical operation:

$$
W X^T = \begin{pmatrix}
	\mathbf{w}_1^T \mathbf{x}_1 & \cdots & \mathbf{w}_1^T \mathbf{x}_N \\ 
	\vdots & \ddots & \vdots \\ 
	\mathbf{w}_L^T \mathbf{x}_1 & \cdots & \mathbf{w}_L^T \mathbf{x}_N
\end{pmatrix}
$$

for $N$ samples and $L$ layers.

After feeding the input to the hidden layer, we'll have three outputs, which we will _feed forward_ the output layer (hence the name "feed forward networks" and "forward pass").

Let's prepare our network, by creating a hidden and an out put layer, each with neurons with random weights:

```python
layer0 = 2 * np.random.rand(4, 3) - 1  # mean weight 0
layer1 = 2 * np.random.rand(1, 4) - 1
```

The forward pass through a network is straight forward:

```python
# input; one *column* per sample
l0 = X.T

# l1 has N colums (samples) and 4 rows (neurons at L1)
l1 = nonlin(np.matmul(layer0, l0))

# l2 has N colums, 1 row (single output node at L2)
l2 = nonlin(np.matmul(layer1, l1))
```

The error is the difference between the target (in `y`) and the prediction (in `l2`).
For the output layer, this difference is weighted by the derivative at this point.
For hidden layers, we propagate the error in parts.
In the end, we sum up all the contributions by the samples for one neuron.

```python
l2_error = y.T - l2
    
# N columns, 1 row: how much did each sample contribute?
l2_delta = l2_error * nonlin(l2, deriv=True)

# how much did each l1 value contribute to the l2 error (according to the weights)?
# N colums, 4 rows (neurons)
l1_error = np.matmul(layer1.T, l2_delta)

# how much weight for this error? --> derivative!
l1_delta = l1_error * nonlin(l1, deriv=True)

# sum up the partial contributions by each sample to form
# the final gradient
layer1 += (learning_rate * np.matmul(l2_delta, l1.T))
layer0 += (learning_rate * np.matmul(l1_delta, l0.T))
```

This was a single backpropagation iteration, in which we considered all features; this is called an _epoch_.
You can also batch the features ("minibatches") by drawing random subsets from the data.
In this case, an update after a batch is done is an _iteration_, and an _epoch_ is once all features have been visited once.


See the complete solution: [mlp-basic.py]({{site.baseurl}}/06-nnets/mlp-basic.py).
For the special case of a single neuron (ie. a _perceptron_), the algorithm behaves almost identical to the Rosenblatt update above (see [perceptron-nonlinear.py]({{site.baseurl}}/06-nnets/perceptron-nonlinear.py)).


# TensorFlow

Here's a [gentle introduction to TensorFlow](https://michelleful.github.io/PyCon2017/#/).

Build a TF network to work with the [Wheat Seeds]({{site.baseurl}}/06-nnets/wheat-seeds.zip) data:

```python
import csv
import numpy as np

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

# convert to numpy arrays
X = np.array(X)
Y = np.array(Y)

# partition data in train ({X,Y}tr) and test ({X,Y}te)
nte = 10
Xtr = X[:-nte]
Ytr = Y[:-nte]
Xte = X[-nte:]
Yte = Y[-nte:]
```

Here are a few hints to get started:

```python
import tensorflow as tf

# define variables
X = tf.placeholder("float", [None, 14])  # 14-dim input
Y = tf.placeholder("float", [None, 4])   # 4-dom output

# create a variable of [rows, cols] and random init
W = tf.Variable(tf.random_normal(shape, stddev=0.01))

# example of fully connected layer with sigmoid
W1 = tf.Variable(tf.random_normal(shape, stddev=0.01))
y1 = tf.nn.sigmoid(tf.matmul(X, W1))

# example with softmax
W2 = tf.Variable(tf.random_normal(shape, stddev=0.01))
y2 = tf.nn.softmax(tf.matmul(y1, W2))

# cross-entropy loss function
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y2, labels=Y))

# training optimizer
train_op = tf.train.GradientDescentOptimizer(0.05).minimize(cost)

# make predictions with model by argmaxing over the output
predict_op = tf.argmax(y2, 1)

# work with a session...
with tf.Session() as sess:
	# ...to train
	sess.run(train_op, feed_dict={X: ..., Y: ...})

	# ...to test
	teY = sess.run(predict_op, feed_dict={X: ...})
```

See the solution: [mlp-tf1.py]({{site.baseurl}}/06-nnets/mlp-tf1.py)



# Pseudo-Sequences: Fizz-Buzz

_Adapted from [Joel Grus: Fizz Buzz in Tensorflow](http://joelgrus.com/2016/05/23/fizz-buzz-in-tensorflow/)._

Do you know [_fizz buzz_](https://en.wikipedia.org/wiki/Fizz_buzz)?
It is a game played in early school years to practice 101, where players would call out the numbers starting from 1, but instead say _fizz_ if the number is divisible by 3, _buzz_ if divisible by 5, or _fizzbuzz_ if divisible by both.

For example:

> 1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, Fizz Buzz, 16, 17, Fizz, 19, Buzz, Fizz, 22, 23, Fizz, Buzz, 26, Fizz, 28, 29, Fizz Buzz, 31, 32, Fizz, 34, Buzz, Fizz, ...

We're looking to make predictions for the numbers 1...100 (`range(1, 100)`), so use numbers `range(101, 2**14)` to train.

Build a simple TF network, train and evaluate!

Hints:

```python
# represent each input by an array of its binary digits
def binary_encode(i, num_digits):
    return np.array([i >> d & 1 for d in range(num_digits)])

# one-hot encoding of an integer (used to generate training data)
def fizz_buzz_encode(i):
    if   i % 15 == 0: return np.array([0, 0, 0, 1])
    elif i % 5  == 0: return np.array([0, 0, 1, 0])
    elif i % 3  == 0: return np.array([0, 1, 0, 0])
    else:             return np.array([1, 0, 0, 0])
```

See the solution: [fizzbuzz.py]({{site.baseurl}}/06-nnets/fizzbuzz.py)


# Homework: Hotwords Recognition in TensorFlow

Please work your way through the TensorFlow [hotword recognition tutorial](https://www.tensorflow.org/tutorials/audio_recognition) (you need to install [bazel](https://www.bazel.build/), Google's build tool, e.g. using homebrew on a Mac or using your package manager on linux).
