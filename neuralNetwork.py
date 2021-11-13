import numpy as np
import pandas as pd
import random
from random import sample
import keras
from keras.models import Sequential
from keras.layers import Dense
from scipy.stats import truncnorm

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    """
    This method helps us get a normal distribution for our genetic mutations

    Args:
        mean (int, optional): Mena for the ND. Defaults to 0.
        sd (int, optional): standard deviation for the ND. Defaults to 1.
        low (int, optional): Low cut point I want for the truncation. Defaults to 0.
        upp (int, optional): High cut point I want for the truncation. Defaults to 10.

    Returns:
        [type]: a truncnorm object
    """
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
        


class NeuralNetwork():
    """
    Neural network for the food gathering agents
    the input layer is going to have a dimension of 2 for
    the angle and the distance of the food
    """
    

    def __init__(self):
        """
        Print method for the neuralNetwork class
        """
        self.model = Sequential()
        #adding the input layer, we will also have a 3 dimensional hidden layer
        self.model.add(Dense(5, input_dim=2, activation="relu", kernel_initializer= "random_normal"))
        #adding the output layer
        self.model.add(Dense(2, activation="sigmoid", kernel_initializer="random_normal"))
        #self.num_of_mutations = num_of_mutations

        #example distances for the agent to perceive
        # data1 = np.array([[1, 2]]) #one units to the right, 2 units down
        # data2 = np.array([-1, -2]) #one units to the left, 2 units up
    
    def genetic_mutation(self):
        """
        Genetically mutates the neuralNetwork object so that the offspring has slightly different genome
        """
        #we will generate mutation chances and mutations from a truncated normal dicstribution function
        mutation_chance_generate = get_truncated_normal(mean = 0.5, sd = 1, low = 0, upp = 1)
        mutation_generate = get_truncated_normal(mean = 0.0, sd = 1, low = -1, upp = 1)
        
        for layer in self.model.layers:
            #for the first layer
            #first, get the weights from the first layer
            old_weights = layer.weights[0]
            #flatten them so we can iterate through them
            old_flat_weights = old_weights.numpy().flatten()
            #initialize the new weights array 
            new_flat_weights = np.copy(old_flat_weights)
            #mutate genes and populate the new_flat_weights array with the new genes
            for i in range(0, len(old_flat_weights) -1):
                if mutation_chance_generate.rvs() >= 0.5:
                    new_flat_weights[i] = mutation_generate.rvs()
            #reshape them back, we need the shape information first
            shape = layer.weights[0].shape
            new_weights = new_flat_weights.reshape(shape)
            #append with the biases that we discarded before
            new_weights_full = [new_weights, layer.weights[1].numpy()]
            #set the new weight set of the layer to be this
            layer.set_weights(new_weights_full)

# n = NeuralNetwork()
# print("n summmary: ", n.model.summary())
# m = NeuralNetwork()
# print("m summmary: ", m.model.summary())
# print("n weights: ", n.model.get_weights())

# n.genetic_mutation()
# #print("n summmary after mutation: ", n.model.summary())
# print("n weights after mutation: ", n.model.get_weights())
