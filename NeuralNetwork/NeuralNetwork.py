import numpy as np


class Neuron:

    def __init__(self, n_inputs):
        '''
        Constructor para la clase Neuron
        :param n_inputs: Número de inputs para la neurona
        '''
        self.n_inputs = n_inputs
        self.set_weights([np.random.uniform(0,1) for _ in range(0, n_inputs+1)]) # +1 for Bias value
        self.output = 0
        self.delta = 0


    def set_weights(self, weights):
        '''
        Setea los pesos de la neurona
        :param weights: Valores de los pesos
        '''
        self.weights = weights

    def sum(self, inputs):
        '''
        Suma de la ponderación entre cada peso y el input recibido
        :param inputs: Arreglo de Inputs que llegan a la neurona
        :return: Suma de las ponderaciones entre los pesos e inputs correspondientes
        '''
        return sum(val * self.weights[i] for i, val in enumerate(inputs)) # Does not include Bias


class NeuralLayer:

    def __init__(self, n_neurons, n_inputs):
        '''
        Constructor para la clase NeuralLayer
        :param n_neurons: Número de neuronas que contrendrá la capa
        :param n_inputs: Número de inputs que recibirá cada neurona en la capa
        '''
        self.n_neurons = n_neurons
        self.neurons = [Neuron(n_inputs) for _ in range(0, self.n_neurons)]


class NeuralNetwork:
    def __init__(self, n_inputs, n_hiddenlayers, n_neurons_in_layers, n_outputs):
        '''
        Constructor para la clase NeuralNetwork
        :param n_inputs: Número de inputs que recibirá la capa
        :param n_hiddenlayers: Número de Hidden Layers
        :param n_neurons_in_layers: Número de neuronas que contendrá cada Hidden Layer
        :param n_outputs: Número de neuronas en el Output Layer
        '''
        self.n_inputs = n_inputs
        self.n_hiddenlayers = n_hiddenlayers
        self.n_neurons_in_layers = n_neurons_in_layers
        self.n_outputs = n_outputs
        self.layers=list()

        self.initialize_network()

    def initialize_network(self):
        '''
        Método que inicializa una Red Neuronal dado los parámetros del constructor
        :return: Red Neuronal con los parámetros deseados
        '''
        if self.n_hiddenlayers>0:
            self.layers = [NeuralLayer(self.n_neurons_in_layers, self.n_inputs)] # First Hidden Layer
            self.layers += [NeuralLayer(self.n_neurons_in_layers, self.n_neurons_in_layers) for _ in range(0, self.n_hiddenlayers-1)] # Other Hidden Layers
            self.layers += [NeuralLayer(self.n_outputs,self.n_neurons_in_layers)] # Output Layer
        else:
            self.layers = [NeuralLayer(self.n_outputs, self.n_inputs)]

    def get_weights(self):
        '''
        Obtiene todos los pesos dentro de la red
        :return: Pesos de la red
        '''
        weights = []

        for layer in self.layers:
            for neuron in layer.neurons:
                weights += neuron.weights

        return weights

    def sigmoid(self, activation):
        '''
        Función continua que retorna un valor entre 0 y 1
        :param activation: Ponderación entre los inputs y pesos de una neurona
        :return: Output de la neurona
        '''
        return 1/(1+np.exp(-activation))

    def forward_propagate(self, inputs):
        '''
        Metódo de Forward Propagate para la red neuronal
        :param inputs: Inputs de la red
        :return: Output de la red
        '''
        lel=inputs
        for layer in self.layers:
            outputs = []
            for neuron in layer.neurons:
                total = neuron.sum(lel)-neuron.weights[-1]
                neuron.output = self.sigmoid(total)
                outputs.append(neuron.output)
            lel = outputs
        return outputs

    def back_propagate_error(self,expected):
        '''
        Método de Back propagate error para la red neuronal
        :param expected: Valores esperados para el Output Layer
        '''
        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]
            errors = list()
            if i != len(self.layers)-1:
                for j in range(len(layer.neurons)):
                    error = 0.0
                    previouslayer = self.layers[i+1]
                    for neuron in previouslayer.neurons:
                        error += (neuron.weights[j]*neuron.delta)
                    errors.append(error)

            else:

                for j in range(len(layer.neurons)):
                    neuron = layer.neurons[j]
                    errors.append(expected[j]-neuron.output)

            for j in range(len(layer.neurons)):
                neuron = layer.neurons[j]
                neuron.delta = errors[j]*(neuron.output*(1.0 - neuron.output))

    def update_weights(self, inputs, learning_rate):
        '''
        Actualización de pesos y bias para la red
        :param inputs: Inputs de la red
        :param learning_rate: Tasa de Aprendizaje
        '''
        lel = inputs
        for i in range(len(self.layers)):
            if i != 0:
                lel = []
                for neuron in self.layers[i-1].neurons:
                    lel.append(neuron.output)

            for neuron in self.layers[i].neurons:
                for j in range(len(lel)):
                    neuron.weights[j]+= learning_rate*neuron.delta*lel[j]
                neuron.weights[-1]-= learning_rate*neuron.delta

    def train(self, test_set, expected_set,n_epoch,learning_rate):
        '''
        Método de entrenamiento para la red neuronal
        :param test_set: Inputs de test
        :param expected_set: Outputs esperados para el input de test
        :param n_epoch: Número de entrenamientos de la red
        :param learning_rate: Tasa de aprendizaje
        '''
        for epoch in range(n_epoch):
            sum_error = 0
            j = 0
            for item in test_set:
                noutputs = self.forward_propagate(item)
                sum_error += sum([(expected_set[j][i]-noutputs[i])**2 for i in range(len(expected_set[j]))])
                self.back_propagate_error(expected_set[j])
                self.update_weights(item,learning_rate)
                j+=1
        print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, learning_rate, sum_error))