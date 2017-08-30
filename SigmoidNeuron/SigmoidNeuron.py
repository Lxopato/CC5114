from math import exp


class SigmoidNeuron(object):
    def __init__(self):
        self.weights = []
        self.inputs = []
        self.bias = 0
        self.learningconstant = 0.01
        self.epsilion = 0.1

    def setWeights (self,someweights):
        self.weights = someweights

    def setInputs (self,someinputs):
        self.inputs = someinputs

    def setBias(self,aBias):
        self.bias = aBias

    def feed(self):
        if(len(self.weights) != len(self.inputs)):
            raise
        else:
            lel = 0
            for i in range(len(self.weights)):
                lel += self.weights[i]*self.inputs[i]
            return 1/(1 + exp(-lel-self.bias))

    def train(self, expected):

        if(self.feed() > (expected+self.epsilion)) or (self.feed() < (expected-self.epsilion)):
            if (self.feed() < expected - self.epsilion):
                for i in range(len(self.weights)):
                    self.weights[i]+= self.inputs[i]* self.learningconstant
            else:
                for i in range(len(self.weights)):
                    self.weights[i] -= self.inputs[i] * self.learningconstant


