from NeuralNetwork import NeuralNetwork

n_inputs = 2  # Number Of Inputs
n_hiddenlayers = 1  # Number Of Hidden Layers
n_neurons_in_hlayers = 1  # Number of Neurons in the Hidden Layers
n_outputs = 1  # Number of outputs

network = NeuralNetwork(n_inputs, n_hiddenlayers, n_neurons_in_hlayers, n_outputs)


def train(test_set, expected, n_epoch):
    for epoch in range(n_epoch):
        sum_error = 0
        i = 0
        for item in test_set:
            outputs = network.forward_propagate(item)
            sum_error += sum([(expected[i][j]-outputs[j])**2 for j in range(len(expected[i]))])
            network.back_propagate_error(expected[i])
            network.update_weights(item)
        print('>epoch=%d, lrate=%.3f , error=%.3f' % (epoch, 0.01,sum_error))

train([[0,0],[0,1],[1,0],[1,1]], [[0],[1],[1],[1]], 500)