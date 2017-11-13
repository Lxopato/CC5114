import random
import logging
from GeneticAlgorithms.Trainer import train_and_score


class Network:

    def __init__(self, nn_param_choices=None):
        self.accuracy = 0.
        self.nn_param_choices = nn_param_choices
        self.network = {}

    def create_random(self):
        for key in self.nn_param_choices:
            self.network[key] = random.choice(self.nn_param_choices[key])

    def create_set(self, network):
        self.network = network

    def train(self):
        if self.accuracy ==0.:
            self.accuracy = train_and_score(self.network)

    def print_network_info(self):
        logging.info(self.network)
        logging.info("Network Accuracy: %.2f%%" % (self.accuracy * 100))

