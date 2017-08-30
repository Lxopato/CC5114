import unittest
from NeuralNetwork import NeuralNetwork
#  n_inputs, n_hiddenlayers, n_neurons_in_layers, n_outputs

class MyTestCase(unittest.TestCase):

    def Test_AND(self):
        network= NeuralNetwork(2,1,1,1)
        set=[[0,0],[0,1],[1,0],[1,1]]
        expected = [[0],[0],[0],[1]]
        n_epoch = 500
        network.train(set,expected,n_epoch)

if __name__ == '__main__':
    unittest.main()
