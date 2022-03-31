import sys
import numpy as np

# No seed is being used


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
        # first layer
        self.dense1 = Layer_Dense(2, 5)
        self.activation1 = Activation_ReLU()

        # second layer
        self.dense2 = Layer_Dense(5, 2)
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
        for layer in self.layers:
            for weight in np.nditer(layer.weights, op_flags=["readwrite"]):
                if np.random.randn() > 0:
                    weight[...] += 0.10 * np.random.randn()
            for bias in np.nditer(layer.biases, op_flags=["readwrite"]):
                if np.random.randn() > 0:
                    bias[...] += 0.10 * np.random.randn()
