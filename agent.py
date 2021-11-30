
from sentdexANN import *

#this is how we create an agent

class Agent():
    #facing directions for the agent so that
    #we are informed where their next movement is going to be
    facing_directions = [0,1,2,3]
    #init method is the constructor for the agent
    def __init__(self, energy : int = 30.0):
        self.name = "agent" #this will change in init agents
        self.neuralNetwork = AgentNeuralNetwork() #all agents have a neural network
        self.energy = energy #agents are born with 30 energy
        self.age = 0 #age starts from 0
        self.x = None #the x coordinate for the agent
        self.y = None #the y coordinate for the agent
        self.facing_direction = None #facing direction is going to be one of 0, 1, 2, 3

# a = Agent()
# a.x = 3
# print(a.x)

# b = Agent()
# print(b.x)