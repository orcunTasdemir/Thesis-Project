import sys
import numpy as np
from random import uniform
import random

class Layer_Dense:
    """Class for dense layer
    """
    def __init__(self, n_inputs, n_neurons):
        """Constructor for the dense layer

        Args:
            n_inputs (int): Number of inputs to the network
            n_neurons (int): Number of neurons receiving the input on the layer
        """
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        """Forward function takes in an input and takes the dot product of it with weights and finally adds up the biases
        so that the layer passes on the new values to the next layer

        Args:
            inputs (np.ndarray): A numpy array of values that are the input to the layer.
        """
        self.output = np.dot(inputs, self.weights) + self.biases


class Activation_ReLU:
    """Rectified linear activation function class
    """
    def forward(self, inputs):
        """Puts the inputs through the ReLu function and creates an output

        Args:
            inputs (np.ndarray): A numpy array of values that are the input to the layer.
        """
        self.output = np.maximum(0, inputs)


class Activation_Softmax:
    """Softmax activation function class
    """
    def forward(self, inputs):
        """puts the data through the function and creates output

        Args:
            inputs (np.ndarray): A numpy array of values that are the input to the layer.
        """
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities


class AgentNeuralNetwork:
    """Neural network class for the Agent
    """
    def __init__(self):
        """The constructor for the neural network
        """
        # first layer
        self.dense1 = Layer_Dense(2, 5)
        self.activation1 = Activation_ReLU()
        # second layer
        self.dense2 = Layer_Dense(5, 2)
        self.activation2 = Activation_Softmax()
        self.layers = [self.dense1, self.dense2]

    def run_network(self, input):
        """Function that runs the network every cycle of the game so the Agent can make a decision about where to move next.

        Args:
            input (np.ndarray): A numpy array of values that are the input to the layer. The first input to the ANN is distance and angle of the food respectively. ([distance, angle])

        Returns:
            np.ndarray : A numpy array of shape (2,). We decide whether to move, whether to turn left, or turn right through this resulting array.
        """
        self.dense1.forward(input)
        self.activation1.forward(self.dense1.output)
        self.dense2.forward(self.activation1.output)
        self.activation2.forward(self.dense2.output)
        return_val = self.activation2.output
        return return_val

    def genetic_mutation(self):
        """Function that mutates the neural network when the offspring is being created.
        """
        if(uniform(0,1) < 0.20):
            for layer in self.layers:
                for weight in np.nditer(layer.weights, op_flags=["readwrite"]):
                    # 50 percent chance
                    if np.random.randn() > 0.85:
                        weight[...] += 0.10 *(1 if random.random() < 0.5 else -1)
                for bias in np.nditer(layer.biases, op_flags=["readwrite"]):
                    # 50 percent chance
                    if np.random.randn() > 0.85:
                        bias[...] += 0.10 *(1 if random.random() < 0.5 else -1)
                        
                    
                    
                    
# Changed the plus to multiply
