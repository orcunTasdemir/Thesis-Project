import numpy as np
from utils.ANN import AgentNeuralNetwork
from random import randint, choice
from copy import deepcopy
from math import *
import math
import random
from utils.tools import *
####################################################################################################################
class Agent:
    """Agent class constructs the agent that plays the survival strategy game
    """
    isSSS : bool = False
    numKids : int = 0
    perimeter : int = 3
    numberInPerimeter : int = 0
    facing_directions : list = [0, 1, 2, 3]    
    name: str = "agent"
    energy: float = 30.0
    lifeSpan : int = 350
    reproductionSpan : int = 50
    x: int = None
    y: int = None
    facing_direction: int = None
    impact_strength : float = 0.0
    overrideReproductionSpan : bool = True
    reproduceAtEnergy : int = 120
    social_gene : float = 0.0
    last_age_reproduced : int = 0
    def __init__(self,
                 isSSS = isSSS,
                 name=name,
                 neural_network : AgentNeuralNetwork = AgentNeuralNetwork(),
                 energy=energy,
                 lifeSpan=lifeSpan,
                 reproductionSpan=reproductionSpan,
                 age=randint(0,200),
                 x=x,
                 y=y,
                 facing_direction=facing_direction,
                 impact_strength=impact_strength,
                 reproduceAtEnergy=reproduceAtEnergy,
                 social_gene=social_gene,
                 numberInPerimeter=numberInPerimeter,
                 perimeter=perimeter,
                 last_age_reproduced=last_age_reproduced,
                 numKids = 0
                 ):
        """Constructor for the Agent object

        Args:
            name (str, optional): Name of the agent. Defaults to name.
            neural_network (AgentNeuralNetwork, optional): Neural network that dictates the movement of the agent.
            The networks is a (2,5,2) simple neural network with biases and mutation chances. Defaults to AgentNeuralNetwork().
            energy (float, optional): The amount of energy the agent starts its life with. Defaults to energy.
            lifeSpan (int, optional): The maximum number of years the agent can stay alive. Defaults to lifeSpan.
            reproductionSpan (int, optional): Number of years by which the agent can periodically reproduce. This variable is being overwritten due to the overPopulation issue with another energy based reproduction indicator. (From Ron Sun, 2006) Defaults to reproductionSpan.
            age (int, optional): Agents age. Defaults to a random integer between 0 and 40 to make the population change more homogenious.[randint(0,40).]
            x (int, optional): X coordinate of the Agent. Defaults to x.
            y (int, optional): Y coordinate of the Agent. Defaults to y.
            facing_direction (int, optional): 0 is down, 1 is left, 2 is up, 3 is right, facing direction indicates where the Agent is looking at. Defaults to facing_direction.
            impact_strength (float, optional): The current strength the Agent have as a coefficient for how much impact they will create for others aronud them. This is dictated by their age, energy level, and how many times they reproduced.
            numKids (int, optinal): Number of offspring an Agent had is being recorded in this variable as it informs their social status.
            reproduceAtEnergy (int, optional): The energy that the agent is required to be at to be able to reproduce given there is room in the society.
            
        """
        
        self.isSSS=isSSS,
        self.name = name
        self.neuralNetwork = AgentNeuralNetwork()
        self.energy = energy
        self.lifeSpan =lifeSpan,
        self.reproductionSpan = reproductionSpan,
        self.age = randint(0,40)
        self.x = x
        self.y = y
        self.facing_direction = facing_direction
        self.impact_strength = impact_strength
        self.reproduceAtEnergy = reproduceAtEnergy
        self.social_gene = random.uniform(-1,1)
        self.numberInPerimeter=numberInPerimeter
        self.perimeter=perimeter
        self.last_age_reproduced=last_age_reproduced
        self.numKids = numKids
####################################################################################################################    
    def move(self, move_instructions : np.ndarray, edge : int = 100): 
            
        if move_instructions[0][1] <= 0.3:  # for turn left
            self.facing_direction = Agent.facing_directions[(self.facing_direction - 1) % 4]
        elif move_instructions[0][1] >= 0.7:  # for turn right
            self.facing_direction = Agent.facing_directions[(self.facing_direction + 1) % 4]        
        move = False
        if move_instructions[0][0] > 0.5:
            move = True
        return move
####################################################################################################################   
    def reproduce(self):
        
        half_energy = (self.energy) / 2
        self.energy = half_energy
        offspring = Agent(energy=half_energy, age=0)
        offspring.isSSS = deepcopy(self.isSSS)
        offspring.neuralNetwork = deepcopy(self.neuralNetwork)
        offspring.neuralNetwork.genetic_mutation()
        # print(offspring.neuralNetwork.dense1.weights)
        offspring.social_gene = deepcopy(self.social_gene)
        offspring.mutateSocial()
        offspring.facing_direction = choice(Agent.facing_directions)
        return offspring
####################################################################################################################
    def mutateSocial(self):
        if(np.random.randn() > 0.85):
            self.social_gene += (self.social_gene * (0.10 * randint(-1,1)))
            
####################################################################################################################    
    def angle_agent_food(self, find_x: int, find_y: int):  # for thte angle of the food
        agent_x = self.x
        agent_y = self.y
        fd = self.facing_direction
        food_x = find_x
        food_y = find_y
        d1 = agent_x - food_x
        d2 = agent_y - food_y
        if d1 == 0:
            if d2 == 0:
                deg = 0
            else:
                deg = 0 if agent_y > food_y else 180
        elif d2 == 0:
            deg = 90 if agent_x < food_x else 270
        else:
            deg = math.atan(d2 / d1) / pi * 180
            lowering = agent_y < food_y
            if (lowering and deg < 0) or (not lowering and deg > 0):
                deg += 270
            else:
                deg += 90
                
        deg -= fd*(90)
        deg = deg % 360
        # print("HERE")
        return mapRange(deg, 0.0, 360.0, 1.0, -1.0)
    
