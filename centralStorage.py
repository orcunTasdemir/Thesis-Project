from agent import Agent
from game import *
from field import Field
from food import Food
from visualize import *
from simulate import simulate
from typing import Dict
import random
import numpy as np
from matplotlib import colors, pyplot


#create a game with the field and agents we have now
game = Game()
print(game.agents)


# #create field
game.initField(100)

# #create the agents  
game.initAgents(150)

# #populate the field with the agents
# game.populate()

# #put food on the field
#game.putFood("Temperate")


# #simulate(game, 1)

# #visualize
# visualize(game)