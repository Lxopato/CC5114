from NeuralNetwork.NeuralNetwork import NeuralNetwork as nn
from GlassPredictor.DataNormalization import DataNormalizer
from GlassPredictor.CSVparser import CSVparser
from matplotlib import pyplot as plt
import numpy as np

normalizer = DataNormalizer()
delta = 0.01

'''
TEST SET
'''
test = CSVparser('testset.csv')
data_test = normalizer.normalize_data(test.get_data())
results_test = normalizer.normalize_data(test.get_results())
results_test_binary = normalizer.data_to_binary_array(test.get_results())
'''
DATA SET
'''
glasses = CSVparser('data.csv')
data = normalizer.normalize_data(glasses.get_data())
expected = normalizer.normalize_data(glasses.get_results())
expected_binary = normalizer.data_to_binary_array(glasses.get_results())


'''
TEST PARA UNA RED CON 9 INPUTS Y 1 SALIDA NORMALIZADA con Learning Rate de 0.1. 
'''
epoch=[]
accuracy=[]
for i in range(10):
    network = nn(9, 1, 9, 1)
    network.train(data_test, results_test, (i+1)*100, 0.1)
    correct=0
    total=0
    j=0
    for item in data:
        result = network.forward_propagate(item)
        if expected[j][0]-delta < result[0] < expected[j][0] + delta:
            correct += 1
        j+=1
        total+=1
    epoch.append((i+1)*100)
    accuracy.append(correct/total)

f=plt.figure(1)
plt.plot(epoch,accuracy)
f.suptitle("9 Inputs, 1 Salida Normalizada, Learning Rate = 0.1")
plt.xlabel("Número de epochs")
plt.ylabel("% de acierto")

'''
TEST PARA UNA RED CON 9 INPUTS Y 7 OUTPUTS con Learning Rate de 0.1. 
'''
epoch=[]
accuracy=[]
for i in range(10):
    network = nn(9, 1, 9, 7)
    network.train(data_test, results_test_binary, (i+1)*10000, 0.1)
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

k=plt.figure(2)
plt.plot(epoch,accuracy)
k.suptitle("9 Inputs, 7 Outputs, Learning Rate = 0.1")
plt.xlabel("Número de epochs")
plt.ylabel("% de acierto")


'''
TEST PARA UNA RED CON 9 INPUTS Y 7 OUTPUTS con Learning Rate de 0.3. 
'''
epoch=[]
accuracy=[]
for i in range(10):
    network = nn(9, 1, 9, 7)
    network.train(data_test, results_test_binary, (i+1)*10000, 0.3)
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

l=plt.figure(3)
plt.plot(epoch,accuracy)
l.suptitle("9 Inputs, 7 Outputs, Learning Rate = 0.3")
plt.xlabel("Número de epochs")
plt.ylabel("% de acierto")

'''
TEST PARA UNA RED CON 9 INPUTS Y 7 OUTPUTS con Learning Rate de 0.5. 
'''
epoch=[]
accuracy=[]
for i in range(10):
    network = nn(9, 1, 9, 7)
    network.train(data_test, results_test_binary, (i+1)*10000, 0.5)
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

m=plt.figure(4)
plt.plot(epoch,accuracy)
m.suptitle("9 Inputs, 7 Outputs, Learning Rate = 0.5")
plt.xlabel("Número de epochs")
plt.ylabel("% de acierto")
plt.show()