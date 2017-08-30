import random


class Neuron:

    def __init__(self, n_inputs):
        self.n_inputs = n_inputs
        self.set_weights([random.uniform(0,1) for x in range(0, n_inputs+1)])

    def set_weights(self, weights):
        self.weights = weights

    def sum(self,inputs):
        return sum(val*self.weights[i] for i,val in enumerate(inputs))
