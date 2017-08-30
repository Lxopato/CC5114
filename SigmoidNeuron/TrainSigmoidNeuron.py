from SigmoidNeuron import *
from matplotlib import pyplot as plt
import random

#Variables for creating the function the Neuron will analize
epsilon = 0.1
slope = -2
axis_cut = 3
leftlimit = -25
rightlimit = 25
leftpoint = slope* leftlimit + axis_cut
rightpoint = slope* rightlimit + axis_cut
success_rate = []

#Creation of the number of training sessions and tests the Neuron will have
training_sessions = 1000 #Modify for increase/decrease the number of training sessions, higher numbers will take more time to execute
after_training_points = 1000 #Modify for increase/decrease the number of points to be tested


#Training
for i in range(training_sessions):
    neuron = SigmoidNeuron()
    neuron.setBias(1)
    neuron.setWeights([1, 1])
    error=0
    for j in range(i):
        anX = random.uniform(leftlimit, rightlimit)
        anY = random.uniform(leftlimit, rightlimit)
        expected = 0

        if (slope*anX + axis_cut) >= anY:
            expected = 1

        neuron.setInputs([anX,anY])
        neuron.train(expected)

    for k in range(after_training_points):
        anX = random.uniform(leftlimit, rightlimit)
        anY = random.uniform(leftlimit, rightlimit)
        expected = 0
        if (slope * anX + axis_cut) >= anY:
            expected = 1

        neuron.setInputs([anX, anY])
        if (expected+epsilon) < neuron.feed() or neuron.feed() < (expected-epsilon):
            error += 1

    success_rate.append((after_training_points-error) / after_training_points)

#Create the final plot
X = []
Y = []
redX = []
redY = []
blueX = []
blueY = []

for i in range(after_training_points):
    X.append(random.uniform(leftlimit, rightlimit))
    Y.append(random.uniform(leftlimit, rightlimit))

    neuron.setInputs([X[i],Y[i]])
    if neuron.feed() >= 0.5:
        redX.append(X[i])
        redY.append(Y[i])
    else:
        blueX.append(X[i])
        blueY.append(Y[i])

#ScatterPlot
scatter =plt.figure()
scatter.suptitle('Test')
plt.scatter(redX, redY, color='r')
plt.scatter(blueX, blueY, color='b')
plt.plot([leftlimit,rightlimit],[leftpoint,rightpoint])

#Success Rate Plot
success = plt.figure()
success.suptitle('Success Rate')
plt.plot(range(training_sessions),success_rate)

#Show both plots
plt.show()
