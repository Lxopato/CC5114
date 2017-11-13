import logging
from GeneticAlgorithms.NetworkGenerator import NetworkGenerator
from tqdm import tqdm

###############################
# FIELDS THAT CAN BE MODIFIED #
###############################

# NETWORK ARCHITECTURE
N_NEURONS = [2, 4, 6, 8]  # Possible number of neurons in each layer. MUST BE A LIST OF INTEGERS!!!
N_LAYERS = [1, 2]  # Possible Number of layers in each network. MUST BE A LIST OF INTEGERS!!!

# POPULATION ATTRIBUTES
GENERATIONS = 10  # Number of generations
POPULATION = 5  # Number of networks in each generation.
MUTATE_CHANCE = 0.2  # Chance that a random network will be mutated
RANDOM_SELECT = 0.1  # Chance that a rejected network makes to de next generation
RETAIN = 0.4  # % of population that remains in each generation


################
# DO NOT TOUCH #
################

# Configuration for logging file to read the results in each generation
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
    filename='log.txt'
)


def train_networks(networks):
    prog_bar = tqdm(total=len(networks))
    for network in networks:
        network.train()
        prog_bar.update(1)
    prog_bar.close()


def get_average_accuracy(networks):
    total_accuracy = 0
    for network in networks:
        total_accuracy += network.accuracy

    return total_accuracy / len(networks)


def generate(generations, population, nn_param_choices):
    optimizer = NetworkGenerator(nn_param_choices, MUTATE_CHANCE, RANDOM_SELECT, RETAIN)
    networks = optimizer.create_population(population)

    for i in range(generations):
        logging.info("***Doing generation %d of %d***" %
                     (i + 1, generations))

        train_networks(networks)
        average_accuracy = get_average_accuracy(networks)
        logging.info("Generation average: %.2f%%" % (average_accuracy * 100))
        logging.info('-'*50)

        if i != generations - 1:
            networks = optimizer.evolve(networks)

        networks = sorted(networks, key=lambda x: x.accuracy, reverse=True)
        print_networks(networks[:5])


def print_networks(networks):
    logging.info('-'*50)
    logging.info("Top 5 networks for this generation:")
    for network in networks:
        network.print_network_info()


def main():
    nn_param_choices = {
        'nb_neurons': N_NEURONS,
        'nb_layers': N_LAYERS,
        'activation': ['relu', 'elu', 'tanh', 'sigmoid'],
        'optimizer': ['rmsprop', 'adam', 'sgd', 'adagrad',
                      'adadelta', 'adamax', 'nadam'],
    }

    logging.info("***Evolving %d generations with population %d***" %
                 (GENERATIONS, POPULATION))

    generate(GENERATIONS, POPULATION, nn_param_choices)

if __name__ == '__main__':
    main()