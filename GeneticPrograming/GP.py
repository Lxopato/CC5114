from GeneticPrograming import AST
import random
import logging


###########
# GLOBAL VARIABLES
###########

POPULATION = 20
MAX_DEPTH = 5
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8
EXPECTED_VALUE = 87
GENERATIONS = 200
VALUES = [x+1 for x in range(9)]

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
    filename='GP results.txt'
)


def generate_population(length, depth, values):
    """
    Generate the first generation
    :param length: Size of the population
    :param depth: Max depth of trees
    :param values: Values to be used to get the result
    :return: First Population
    """
    genes = []
    while len(genes) < length:
        tree = AST.Tree(random.randint(1, depth), values).create_tree()
        genes.append(tree)
    return genes


def fitness_func(individual):
    """
    Fitness function for individuals
    :param individual: Individual of the population
    :return: Fitness rate
    """
    return (EXPECTED_VALUE - individual.eval())**2


def get_fitness(population):
    """
    Get the fitness of the entire population
    :param population: Population to be measured
    :return: Fitness and real fitness
    """
    fitness = []
    r_fitness = []
    for individual in population:
        r = fitness_func(individual)
        r_fitness.append(r)
        fitness.append(1./r)
    return fitness, r_fitness


def normalize_fitness(fitness):
    """
    Normalizes the fitness of the population
    :param fitness: Fitness of the population
    :return: Normalized Fitness
    """
    total = sum(fitness)
    if total != 0:
        return [fit / total for fit in fitness]
    else:
        return 0


def select(population, n_fitness):
    """
    Select the best individuals of a population from their fitness
    :param population: current population
    :param n_fitness: fitness of te population
    :return: best individuals
    """
    ordered_pair = [(x, y) for x, y in sorted(zip(population, n_fitness), key=lambda pair: pair[1], reverse=True)]
    acc_fitness = [ordered_pair[0][1]]
    for i in range(1, len(ordered_pair)):
        acc_fitness.append(acc_fitness[i - 1] + ordered_pair[i][1])

    parents = []

    for _ in range(POPULATION):
        index1 = get_random(acc_fitness)
        index2 = get_random(acc_fitness)
        parents.append(ordered_pair[index1][0])
        parents.append(ordered_pair[index2][0])
    return parents


def get_random(acc_fitness):
    """
    Get a random individual of the population
    :param acc_fitness:
    :return:
    """
    n = random.random()
    if n <= acc_fitness[0]:
        return 0
    for i in range(1, len(acc_fitness) - 1):
        if acc_fitness[i] > n:
            return i - 1
    return len(acc_fitness) - 1


def crossover(mother, father):
    """
    Crossover between 2 individuals to get one if the chance is correct
    :param mother: First individual
    :param father: Second Individual
    :return: New individual
    """
    chance = random.random()
    if chance <= CROSSOVER_RATE:
        child = mother.copy()
        random.choice(child.serialize()).replace(random.choice(father.serialize()).copy())
    else:
        if fitness_func(mother) < fitness_func(father):
            child = father.copy()
        else:
            child = mother.copy()

    return child

def create_new_population(parents):
    """
    Creates a new population from a previous one
    :param parents: Current population
    :return: New population
    """
    i=0
    new_pop = []
    while i < len(parents):
        mother = parents[i]
        father = parents[i+1]
        i += 2
        new_pop.append(crossover(mother, father))
    return new_pop


if __name__ == "__main__":
    best_fit = []
    population = generate_population(POPULATION, MAX_DEPTH, VALUES)
    fitness, r_fitness = get_fitness(population)
    best = population[fitness.index(max(fitness))]
    for _ in range(GENERATIONS):
        logging.info("                     ")
        logging.info("Generation %d of %d" % (_+1, GENERATIONS))
        best_fit.append(min(r_fitness))
        logging.info("The best result is: %d" % (best.eval()))
        logging.info("The fitness is: %d" % (best_fit[-1]))
        logging.info("The equation is:" + str(best))
        logging.info("                     ")
        if best.eval() == EXPECTED_VALUE:
            break
        n_fitness = normalize_fitness(fitness)
        parents = select(population, n_fitness)
        population = create_new_population(parents)
        fitness, real_fitness = get_fitness(population)
        best = population[fitness.index(max(fitness))]


