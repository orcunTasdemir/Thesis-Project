import sys
from utils.Agent import Agent
from utils.Field import Field
from utils.Food import Food
from utils.Game import Game
from utils.Simulate import *
from utils.Visualize import *
from typing import Dict
from random import randint, randrange
import numpy as np
from matplotlib import colors
from matplotlib import pyplot as plt

from utils.tools import *
import os
import matplotlib

# here we are trying to get agents from a ISS and another SSS game, put them in the same game and track their individual populations
all_iss_games = []
for filename in os.listdir(f'data/25_ISS_games1/'):
    if("POST" in filename):
        with open(f"data/25_ISS_games1/{filename}", 'rb') as f:
            post_iss_game = pickle.load(f)
            all_iss_games.append(post_iss_game)
            
            
all_sss_games = []
for filename in os.listdir(f'data/25_SSS_games1/'):
    if("POST" in filename):
        with open(f"data/25_SSS_games1/{filename}", 'rb') as f:
            post_sss_game = pickle.load(f)
            all_sss_games.append(post_sss_game)
          
for i in range(0,26):            
    #get one game each 
    game_iss = all_iss_games[i]
    game_sss = all_sss_games[i]

    # get the iss game
    try_game_iss = deepcopy(game_iss)
    try_game_iss.environment_type = "Harsh"
    try_game_iss.put_food(challenge=True)
    # set all ISS agents to be iss so that I can keep track of the population seperately
    for agent_name in try_game_iss.agents:
        try_game_iss.agents[agent_name].isSSS = False
        
    # get the sss game 
    try_game_sss = deepcopy(game_sss)
    try_game_sss.environment_type = "Harsh"
    try_game_sss.put_food(challenge=True)
    # set all SSS agents to be sss so that I can keep track of the population seperately
    for agent_name in try_game_sss.agents:
        try_game_sss.agents[agent_name].isSSS = True

    iss_a = dict(list(try_game_iss.agents.items())[len(try_game_iss.agents)//2:])
    sss_a = dict(list(try_game_sss.agents.items())[len(try_game_sss.agents)//2:])
    # add the ss agents to the iss_game
    agents_dict = dict(iss_a, **sss_a)


    # create a brand new game with these agents
    game = Game(
                agents=agents_dict, #all agents are in it
                environment_type="Harsh",
                game_type="Competition",
                food_energy=32,
                agent_energy=30,
                num_of_first_gen=len(agents_dict),
                overrideReproductionSpan=True,
                give=0.45,
                keep=0.55
            )

    game.agents = agents_dict
    game.populate_for_competition()
    game.put_food(challenge=True)

    # run special simulation for competition on this iss_game with both populations in it
    game_post, game_data, _, _ = simulate(game, 20000)

    filenum = random.randint(1000, 10000)

    write_json_to_folder(game_data, "compTest", filenum)

        