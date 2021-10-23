import numpy as np
import pandas as pd

import keras
from keras.models import Sequential
from keras.layers import Dense

class NeuralNetwork:
    #Neural network for the food gathering agents
    #the input layer is going to have a dimension of 2 for
    #the angle and the distance of the food
    model = Sequential()
    #adding the input layer, we will also have a 3 dimensional hidden layer
    model.add(Dense(5, input_dim=2, activation="relu"))
    #adding the output layer
    model.add(Dense(2, activation="softmax"))

    #example distances for the agent to perceive
    # data1 = np.array([[1, 2]]) #one units to the right, 2 units down
    # data2 = np.array([-1, -2]) #one units to the left, 2 units up