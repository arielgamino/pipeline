from tensorflow.python import debug as tf_debug

import tensorflow as tf
from tensorflow.python.client import timeline
import numpy as np

tf.logging.set_verbosity(tf.logging.INFO)

x_train = np.random.rand(100000).astype(np.float32)
print(x_train)

noise = np.random.normal(scale=0.01, size=len(x_train))

y_train = x_train * 0.1 + 0.3 + noise
print(y_train)

# Create some fake test/validation data
x_test = np.random.rand(len(x_train)).astype(np.float32)
print(x_test)

noise = np.random.normal(scale=0.01, size=len(x_train))

y_test = x_test * 0.1 + 0.3 + noise
print(y_test)

W = tf.get_variable(shape=[], name='weights')
print(W)

b = tf.get_variable(shape=[], name='bias')
print(b)

x_observed = tf.placeholder(shape=[None], dtype=tf.float32, name='x_observed')
print(x_observed)

y_pred = W * x_observed + b
print (y_pred)

init_op = tf.global_variables_initializer()
print(init_op)

config = tf.ConfigProto(
  log_device_placement=True,
)

sess = tf.Session(config=config)
sess = tf_debug.LocalCLIDebugWrapperSession(sess)

with tf.device("/device:XLA_GPU:0"):
  sess.run(init_op)

def test(x, y):
  return sess.run(loss_op, feed_dict={x_observed: x, y_observed: y})

y_observed = tf.placeholder(shape=[None], dtype=tf.float32, name='y_observed')
print(y_observed)

loss_op = tf.reduce_mean(tf.square(y_pred - y_observed))

    # Create an optimizer.
optimizer_op = tf.train.GradientDescentOptimizer(0.5)

    # Create an operation that minimizes loss.
train_op = optimizer_op.minimize(loss_op)

    # 'loss', 'optimizer' and 'train' are.
print("loss:", loss_op)
print("optimizer:", optimizer_op)
print("train:", train_op)

print("W: %f" % sess.run(W))
print("b: %f" % sess.run(b))