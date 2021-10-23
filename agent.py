
from numpy import double
from neuralNetwork import NeuralNetwork

#this is how we create an agent, the agent is an abstract datatype

class Agent:
    #init method is the constructor for the agent
    def __init__(self, energy : double = 30):
        self.neuralNetwork = NeuralNetwork
        self.energy = energy #agents are born with 30 energy
        self.age = 0 #age starts from 0
        self.x = None #the x coordinate for the agent
        self.y = None #the y coordinate for the agent

