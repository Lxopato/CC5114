from NeuralNetwork.NeuralNetwork import NeuralNetwork as nn
import Pong

#NETWORK ARCHITECTURE
N_INPUTS = 5
N_HIDDEN_LAYERS = 1
N_NEURONS_IN_HLAYERS = 6
N_OUTPUTS = 3

#TRAINING ATTRIBUTES
LEARNING_RATE = 0.05
N_EPOCH = 1000


def create_network():
    network = nn(N_INPUTS, N_HIDDEN_LAYERS, N_NEURONS_IN_HLAYERS, N_OUTPUTS)
    return network


def output_fix(output):
    action = [0, 0, 0]
    action[output.index(max(output))] = 1
    return action


def single_normalizer(data):
    data[0] = (data[0])/470
    data[1] = (data[1] - 40)/390
    data[2] = (data[2] + 1)/2
    data[3] = (data[3] + 1)/2
    data[4] = (data[4] - 40)/340
    return data


def get_data(dat):
    data = []
    for row in dat:
        data.append(row[:-1])
    return data


def get_results(data):
    results = []
    for row in data:
        results.append(row[-1])
    return results


def train_network(network):
    game = Pong.Pong()
    data = game.start_game()
    first = True
    while True:
        if first:
            data, reset = game.play(output_fix(network.forward_propagate(single_normalizer(data))))
            first = False

        data, reset = game.play(output_fix(network.forward_propagate(single_normalizer(data))))
        if reset:
            print("Training Network...")
            dat = get_data(data)
            for i in range(len(data)):
                dat[i] = single_normalizer(dat[i])
            expected = get_results(data)
            network.train(dat, expected, N_EPOCH, LEARNING_RATE)
            game.restart_game()
            data = game.start_game()


def main():
    network = create_network()
    train_network(network)

if __name__ == "__main__":
    main()
