import unittest
from NeuralNetwork import NeuralNetwork as nn
import numpy as np


class MyTestCase(unittest.TestCase):

    def test_AND(self):
        network= nn(2,1,1,1)
        set =[[0,0],[0,1],[1,0],[1,1]]
        expected = [[0],[0],[0],[1]]
        n_epoch = 300000
        network.train(set,expected,n_epoch,0.1)
        self.assertEqual(np.around(network.forward_propagate([0, 0])), [0])
        self.assertEqual(np.around(network.forward_propagate([0, 1])), [0])
        self.assertEqual(np.around(network.forward_propagate([1, 0])), [0])
        self.assertEqual(np.around(network.forward_propagate([1, 1])), [1])

    def test_OR(self):
        network = nn(2, 1, 1, 1)
        set = [[0, 0], [0, 1], [1, 0], [1, 1]]
        expected = [[0], [1], [1], [1]]
        n_epoch = 300000
        network.train(set, expected, n_epoch,0.1)
        self.assertEqual(np.around(network.forward_propagate([0, 0])), [0])
        self.assertEqual(np.around(network.forward_propagate([0, 1])), [1])
        self.assertEqual(np.around(network.forward_propagate([1, 0])), [1])
        self.assertEqual(np.around(network.forward_propagate([1, 1])), [1])

    def test_XOR(self):
        network = nn(2, 1, 2, 1)
        set = [[0, 0], [0, 1], [1, 0], [1, 1]]
        expected = [[0], [1], [1], [0]]
        n_epoch = 300000
        network.train(set, expected, n_epoch,0.1)
        self.assertEqual(np.around(network.forward_propagate([0, 0])), [0])
        self.assertEqual(np.around(network.forward_propagate([0, 1])), [1])
        self.assertEqual(np.around(network.forward_propagate([1, 0])), [1])
        self.assertEqual(np.around(network.forward_propagate([1, 1])), [0])


if __name__ == '__main__':
    unittest.main()
