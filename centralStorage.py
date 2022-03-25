from agent import Agent
from game import *
from field import Field
from food import Food
from simulate import simulate
from visualize import *
from typing import Dict
import random
import numpy as np
from matplotlib import colors, pyplot 


#create a game with the field and agents we have now
game = Game(field = Field(100), agents = dict(), environment_type = "Temperate")
# print(game.environment_type)

def run_simulations(game: Game, num_agents : int = 150, cycles : int = 20000, num_of_sims : int = 1):

    #create the agents  
    game.init_agents(num_agents)
    #populate the field with the agents
    game.populate()
    #put food on the field
    game.put_food(True)

    print(game)



    print("##########::SIMULATION::##########")
    for x in range(num_of_sims):
        simulate(game, cycles)
    print(game.agents)
    visualizeGame(game)

run_simulations(game, 150, 1200, 50)
# #Visualize population
visualizePopulation("output/output_0.out")

# game = Game(field = Field(2), agents = dict(), environment_type = "Harsh")
# #create the agents  
# game.init_agents(1)
# #populate the field with the agents
# game.populate()
# #put food on the field
# game.put_food(True)

# print(game.agents['agent1'].x)
# print(game.agents['agent1'].y)
# print(game.field.array[game.agents['agent1'].x, game.agents['agent1'].y])