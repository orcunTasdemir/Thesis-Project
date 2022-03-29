from agent import Agent
from game import *
from field import Field
from food import Food
from simulate import simulate
from visualize import *
from typing import Dict
from random import randint, randrange
import numpy as np
from matplotlib import colors, pyplot 


def run_simulations(num_of_sims : int = 2,
                    num_agents : int = 50,
                    cycles : int = 1000,
                    environment_type : str = "Super-Harsh",
                    game_type : str = "SSS",
                    field_size : int = 100):

    print("########## :: SIMULATION INITIATED :: ##########")
    for i in range(num_of_sims):
        file_num = randrange(1000, 10000)
        #create a game with the field and agents we have now
        game = Game(field = Field(field_size),
                        agents = dict(),
                        environment_type = environment_type,
                        game_type = game_type)
        # print(game.environment_type)

        #create the agents  
        game.init_agents(num_agents)
        #populate the field with the agents
        game.populate()
        #put food on the field
        game.put_food(init=True)

        print(game)
        
        simulate(game, cycles, file_num)
        
        #print(game.agents)
        
        # Visualize the game and save it under the games/ folder
        visualizeGame(game, file_num)
        
        address = "output/output_"+ str(file_num)+ ".out"
        #graph of the populations
        visualizePopulation(address, file_num)
        

run_simulations(1, 150, 700, "Harsh")
# #Visualize population
#visualizePopulation("output/output_0.out")

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