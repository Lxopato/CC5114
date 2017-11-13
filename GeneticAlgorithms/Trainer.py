from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping

early_stopper = EarlyStopping(patience=5)


def get_mnist():
    nb_classes = 10
    batch_size = 64
    input_shape = (784,)

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(60000, 784)
    x_test = x_test.reshape(10000, 784)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    y_train = to_categorical(y_train, nb_classes)
    y_test = to_categorical(y_test, nb_classes)

    return nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test


def get_model(network, nb_classes, input_shape):
    nb_layers = network['nb_layers']
    nb_neurons = network['nb_neurons']
    activation = network['activation']
    optimizer = network['optimizer']

    model = Sequential()

    for i in range(nb_layers):
        if i == 0:
            model.add(Dense(nb_neurons, activation=activation, input_shape=input_shape))
        else:
            model.add(Dense(nb_neurons, activation=activation))

    model.add(Dense(nb_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model


def train_and_score(network):
    nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test = get_mnist()
    model = get_model(network, nb_classes, input_shape)
    model.fit(x_train, y_train, batch_size=batch_size, epochs=10000, verbose=0, validation_data=(x_test, y_test), callbacks=[early_stopper])
    score = model.evaluate(x_test, y_test, verbose=0)
    return score[1]
