import sys
import numpy as np
import matplotlib
import nnfs 
from nnfs.datasets import spiral_data

#softmax is exponentiation
# and normalization

np.random.seed(0)

class Layer_Dense:

    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities

class AgentNeuralNetwork:
    def __init__(self):
        #first layer
        self.dense1 = Layer_Dense(2,5)
        self.activation1 = Activation_ReLU()

        #second layer
        self.dense2 = Layer_Dense(5,2)
        self.activation2 = Activation_Softmax()
        self.layers = [self.dense1, self.dense2]

    def run_network(self, input):
        self.dense1.forward(input)
        self.activation1.forward(self.dense1.output)
        self.dense2.forward(self.activation1.output)
        self.activation2.forward(self.dense2.output)
        return_val = self.activation2.output
        return return_val

    def genetic_mutation(self):
        chance_to_mutate = np.random.rand()
        for layer in self.layers:
            for weight in np.nditer(layer.weights, op_flags=['readwrite']):
                if np.random.randn() > 0:
                    weight[...] = 0.10 * np.random.randn()
            for bias in np.nditer(layer.biases, op_flags=['readwrite']):
                if np.random.randn() > 0:
                    bias[...] = 0.10 * np.random.randn()


# a = AgentNeuralNetwork()
# output = a.run_network(np.array([1,2]))
# print("\noutput: ", output)
# print("\nweights of dense1 before mutation: ", a.dense1.weights)
# print("\nweights of dense1 biases before mutation: ", a.dense1.biases)
# print("\nweights of bias2 before mutation: ", a.dense2.weights)
# print("\nweights of dense2 biases before mutation: ", a.dense2.biases)

# a.genetic_mutation()

# print("\nweights of dense1 after mutation: ", a.dense1.weights)
# print("\nweights of dense1 biases after mutation: ", a.dense1.biases)
# print("\nweights of bias2 after mutation: ", a.dense2.weights)
# print("\nweights of dense2 biases after mutation: ", a.dense2.biases)



# print("weights of dense1 after mutation: \n", a.dense1.weights)
# for neuron in a.dense1.weights:
#     for weight in neuron:
#         a.dense1.weights = 1
#         print("\n", weight)

# for neuron in a.dense1.weights:
#     for weight in neuron:
#         weight = 1
# print(a.dense1.weights)
# X, y = spiral_data(samples=100, classes=3)

# dense1 = Layer_Dense(2, 3)
# activation1 = Activation_ReLU()

# dense2 = Layer_Dense(3, 3)
# activation2 = Activation_Softmax()

# dense1.forward(X)
# activation1.forward(dense1.output)

# dense2.forward(activation1.output)
# activation2.forward(dense2.output)

# print(activation2.output[:5])






# print("Python: ", sys.version)
# print("Numpy: ", np.__version__)
# print("Matplotlib: ", matplotlib.__version__)

# inputs = [[1, 2, 3, 2.5],
#             [2.0, 5.0, -1.0, 2.0],
#             [-1.5, 2.7, 3.3, -0.8]]

# ####################################            
# weights = [[0.2, 0.8, -0.5, 1.0],
#             [0.5, -0.91, 0.26, -0.5],
#             [-0.26, -0.27, 0.17, 0.87]]
# biases1 = [2, 3, 0.5]

# ####################################
# weights2 = [[0.1, -0.14, 0.5],
#             [-0.5, 0.12, -0.33],
#             [-0.44, 0.73, -0.13]]

# biases2 = [-1, 2, -0.5]
# ####################################

# layer1_outputs = np.dot(inputs, np.array(weights).T) + biases1

# layer2_outputs = np.dot(layer1_outputs, np.array(weights2).T) + biases2


# print(layer1_outputs)
# print(layer2_outputs)