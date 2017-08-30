import unittest
from SigmoidNeuron import *
import matplotlib as plt

class MyTestCase(unittest.TestCase):

    def test_bias(self):
        neuron = SigmoidNeuron()
        neuron.setBias(5)
        self.assertEqual(neuron.bias, 5)

    def test_inputs(self):
        neuron=SigmoidNeuron()
        neuron.setInputs([0,1,1,0])
        self.assertEqual(neuron.inputs,[0,1,1,0])

    def test_weights(self):
        neuron= SigmoidNeuron()
        neuron.setWeights([12,35])
        self.assertEqual(neuron.weights,[12,35])

    def test_feed(self):
        neuron = SigmoidNeuron()
        neuron.setWeights([12,35])
        neuron.setInputs([1,0])
        neuron.setBias(-14)
        self.assertTrue(neuron.feed()<0.5)

    def learn_50_times(self):
        neuron = SigmoidNeuron()
        neuron.setBias()
        neuron.setInputs([1,1])
        neuron.setWeights([0,0])
        neuron.setBias(1)


    def learn_100_times(self):
        neuron = SigmoidNeuron()

    def learn_200_times(self):
        neuron = SigmoidNeuron()




if __name__ == '__main__':
    unittest.main()
