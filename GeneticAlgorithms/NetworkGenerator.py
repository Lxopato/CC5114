import random
from GeneticAlgorithms.GeneticNetwork import Network
from functools import reduce
from operator import add


class NetworkGenerator:

    def __init__(self, nn_param_choices, mutate_chance, random_select, retain):
        self.mutate_chance = mutate_chance
        self.random_select = random_select
        self.retain = retain
        self.nn_param_choices = nn_param_choices

    def create_population(self, count):
        population = []
        for _ in range(0, count):
            network = Network(self.nn_param_choices)
            network.create_random()
            population.append(network)

        return population

    @staticmethod
    def fitness(network):
        return network.accuracy

    def grade(self, population):
        suma = reduce(add, (self.fitness(network) for network in population))
        return suma / float((len(population)))

    def breed(self, mother, father):
        children = []

        for _ in range(2):
            child = {}
            for param in self.nn_param_choices:
                child[param] = random.choice([mother.network[param], father.network[param]])

            network = Network(self.nn_param_choices)
            network.create_set(child)
            if self.mutate_chance > random.random():
                network = self.mutate(network)
            children.append(network)
        return children

    def mutate(self, network):
        mutation = random.choice(list(self.nn_param_choices.keys()))
        network.network[mutation] = random.choice(self.nn_param_choices[mutation])
        return network

    def evolve(self, population):
        graded = [(self.fitness(network), network) for network in population]
        graded = [x[1] for x in sorted(graded, key=lambda x:x[0], reverse=True)]
        retain_length = int(len(graded)*self.retain)
        parents = graded[:retain_length]

        for individual in graded[retain_length:]:
            if self.random_select > random.random():
                parents.append(individual)

        parents_length = len(parents)
        desired_length = len(population) - parents_length
        children = []

        while len(children) < desired_length:
            father = random.randint(0, parents_length - 1)
            mother = random.randint(0, parents_length - 1)
            if mother != father:
                father = parents[father]
                mother = parents[mother]

                sons = self.breed(mother, father)

                for son in sons:
                    if len(children) < desired_length:
                        children.append(son)
        parents.extend(children)
        return parents
