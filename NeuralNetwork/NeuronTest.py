import unittest

import Neuron


class MyTestCase(unittest.TestCase):
    def setUp(self):
        neuron = Neuron(3, [4, 5, 6], 0.5)



if __name__ == '__main__':
    unittest.main()
