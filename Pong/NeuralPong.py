import tensorflow as tf
import cv2
import Pong
import numpy as np
import random
from collections import deque

#Actions for Paddle, 0 to stay, 1 to move up and 2 to move down
ACTIONS = 3

#Frames for training
EXPLORE = 500000
OBSERVE = 50000

#Frames Storage
REPLAY_MEMORY = 1000000



def createNetwork():
    #Create Layers
    layer1_weights = tf.Variable(tf.zeros([8, 8, 4, 32]))
    layer1_bias = tf.Variable(tf.zeros([32]))

    layer2_weights = tf.Variable(tf.zeros([4, 4, 32, 64]))
    layer2_bias = tf.Variable(tf.zeros([64]))

    layer3_weights = tf.Variable(tf.zeros([3, 3, 64, 64]))
    layer3_bias = tf.Variable(tf.zeros([64]))

    layer4_weights = tf.Variable(tf.zeros([3136, 784]))
    layer4_bias = tf.Variable(tf.zeros([784]))

    outputlayer_weights = tf.Variable(tf.zeros([784, ACTIONS]))
    outputlayer_bias = tf.Variable(tf.zeros([ACTIONS]))

    #Define input
    input = tf.placeholder("float", [None, 84, 84, 4])

    #Create Convolutional Network
    layer1 = tf.nn.relu(tf.nn.conv2d(input, layer1_weights, strides=[1, 4, 4, 1], padding="VALID") + layer1_bias)
    layer2 = tf.nn.relu(tf.nn.conv2d(layer1, layer2_weights, strides=[1, 2, 2, 1], padding="VALID") + layer2_bias)
    layer3 = tf.nn.relu(tf.nn.conv2d(layer2, layer3_weights, strides=[1, 1, 1, 1], padding="VALID") + layer3_bias)
    layer3_flat = tf.reshape(layer3, [-1, 3136])
    layer4 = tf.nn.relu(tf.matmul(layer3_flat, layer4_weights) + layer4_bias)
    output = tf.matmul(layer4, outputlayer_weights) + outputlayer_bias

    return input, output


def trainNetwork(input, output, session):

    # Queue for storing data
    queue = deque()

    #Argmax calculated by outputs
    argmax = tf.placeholder("float", [None, ACTIONS])
    #Ground truth
    gt = tf.placeholder("float", [None])

    action = tf.reduce_sum(tf.multiply(output, argmax))
    # Cost function
    cost = tf.reduce_mean(tf.square(action - gt))
    # Optimization function
    train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)

    # Initialize Pong
    game = Pong.Pong()

    # Get data from image
    frame = game.getPresentFrame()
    frame = cv2.cvtColor(cv2.resize(frame, (84, 84)), cv2.COLOR_BGR2GRAY)
    ret, frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)
    inp_t = np.stack((frame, frame, frame, frame), axis=2)

    session.run(tf.global_variables_initializer())

    frame = 0
    epsilon = 1.0

    # Training
    while (True):

        # Output Tensor
        out_t = output.eval(feed_dict={input: [inp_t]})[0]
        # Argmax function
        argmax_t = np.zeros([ACTIONS])

        if (random.random() <= epsilon):
            maxIndex = random.randrange(ACTIONS)
        else:
            maxIndex = np.argmax(out_t)
        argmax_t[maxIndex] = 1

        if epsilon > 0.5:
            epsilon -= 0.5 / EXPLORE

        # Reward Tensor
        reward_t, frame = game.getNextFrame(argmax_t)

        # Get data from image
        frame = cv2.cvtColor(cv2.resize(frame, (84, 84)), cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)
        frame = np.reshape(frame, (84, 84, 1))

        #Input Tensor
        inp_t1 = np.append(frame, inp_t[:, :, 0:3], axis=2)

        #Append data
        queue.append((inp_t, argmax_t, reward_t, inp_t1))

        # Renew data when we got out of memory
        if len(queue) > REPLAY_MEMORY:
            queue.popleft()

        # Training
        if frame > OBSERVE:
            # Get 32 random values from Memory to train
            minibatch = random.sample(queue, 32)

            inp_batch = [d[0] for d in minibatch]
            argmax_batch = [d[1] for d in minibatch]
            reward_batch = [d[2] for d in minibatch]
            inp_t1_batch = [d[3] for d in minibatch]
            gt_batch = []
            out_batch = output.eval(feed_dict={input: inp_t1_batch})

            # Add Values
            for i in range(0, len(minibatch)):
                gt_batch.append(reward_batch[i] + 0.99 * np.max(out_batch[i]))

            # Train on values
            train_step.run(feed_dict={
                gt: gt_batch,
                argmax: argmax_batch,
                input: inp_batch
            })

        # Update Input Tensor
        inp_t = inp_t1
        frame += 1

        print("FRAME", frame, "/ EPSILON", epsilon, "/ ACTION", maxIndex, "/ REWARD", reward_t)


def main():
    session = tf.InteractiveSession()
    input, output = createNetwork()
    trainNetwork(input, output, session)

if __name__ == "__main__":
    main()