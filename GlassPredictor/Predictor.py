from NeuralNetwork.NeuralNetwork import NeuralNetwork as nn
from GlassPredictor.DataNormalization import DataNormalizer
from GlassPredictor.CSVparser import CSVparser
from matplotlib import pyplot as plt
import numpy as np

normalizer = DataNormalizer()
'''
TEST SET
'''
test = CSVparser('testset.csv')
data_test = normalizer.normalize_data(test.get_data())
results_test_binary = normalizer.data_to_binary_array(test.get_results())
'''
DATA SET
'''
glasses = CSVparser('data.csv')
data = normalizer.normalize_data(glasses.get_data())
expected_binary = normalizer.data_to_binary_array(glasses.get_results())
'''
VARIABLES PARA LA EJECUCIÓN DEL TEST, ESTAS PUEDEN SER MODIFICADAS 
'''
n_epoch= 10000 # Número base de epochs, se recomienda no usar más de 10.000 ya que con una base de 100.000 el test puede tardar horas
learning_rate = 0.3 #Learning Rate para la red
n_inputs = 9 #Número de inputs de la red
n_hidden_layers= 2 # Número de Hidden Layers de la red
n_neurons_in_hidden = 9 # Número de neuronas en las Hidden Layers, debe ser un número
n_outputs = 7 # Número de neuronas en el output layer

'''
TEST. DO NOT TOUCH
'''
epoch=[]
accuracy=[]
for i in range(10):
    network = nn(n_inputs, n_hidden_layers, n_neurons_in_hidden, n_outputs)
    network.train(data_test, results_test_binary, (i+1)*n_epoch, learning_rate)
    correct = 0
    total = 0
    j = 0
    for item in data:
        result = network.forward_propagate(item)
        lel = np.around(result) == expected_binary[j]
        if lel.all():
            correct+=1
        j += 1
        total += 1
    epoch.append((i+1)*10000)
    accuracy.append(correct/total)

k=plt.figure()
plt.plot(epoch,accuracy)
k.suptitle("TEST" )
plt.xlabel("Número de epochs")
plt.ylabel("% de acierto")
plt.show()
