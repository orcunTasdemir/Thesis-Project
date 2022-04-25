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
from matplotlib import colors, pyplot
from utils.tools import *
import os
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')



# Food capturing test to see their learning
extinction = True
while(extinction):
    game = Game(game_type="ISS", environment_type="Temperate", give=0.45, keep=0.55)
    
    game.init_agents()
    game.populate()
    game.put_food()
    game_out, simulation_data, _, iss_agents_list = simulate(game, 20000, have_agents_list=True, type="regular") 
    print(simulation_data["header"]["Overpopulation"])
    if(simulation_data["header"]["extinction"] == False):
        extinction = False

extinction = True
while(extinction):
    game2 = Game(game_type="SSS", environment_type="Temperate", give=0.45, keep=0.55)
    game2.init_agents()
    game2.populate()
    game2.put_food()
    game_out, simulation_data, _, sss_agents_list = simulate(game2, 20000, have_agents_list=True, type="regular")
    print(simulation_data["header"]["extinction"])
    if(simulation_data["header"]["extinction"] == False):
        extinction = False
    

if(not(os.path.isdir(f"data/agent_lists_from_games"))):
        os.makedirs(f"data/agent_lists_from_games")
        

with open("data/agent_lists_from_games/ agent_lists.txt", "w+") as outfile:
    outfile.write("\nISS_agent_list:\n")
    outfile.write("\n".join(str(item) for item in iss_agents_list)) 
    outfile.write("\nSSS_agent_list:\n")
    outfile.write("\n".join(str(item) for item in sss_agents_list))
    
iss_record, sss_record = run_test(iss_agents_list, sss_agents_list, duration=100, environment="Test")

if(not(os.path.isdir(f"data/food_capturing_test"))):
        os.makedirs(f"data/food_capturing_test")


with open("data/food_capturing_test/food_cap_test_results.txt", "w+") as outfile:
    outfile.write("\nISS_record:\n")
    outfile.write("\n".join(str(item) for item in iss_record)) 
    outfile.write("\nSSS_record:\n")
    outfile.write("\n".join(str(item) for item in sss_record))
    
length = len(iss_record)
cycles = [x for x in range(20001)]

fig = plt.figure
ax = plt.axes()
iss, = ax.plot(cycles[:length], iss_record[:length], color="blue")
iss.set_label("ISS agents")
sss, = ax.plot(cycles[:length], sss_record[:length], color="red")
sss.set_label("SSS agents")
plt.title("ISS vs SSS Food Capturing Ability", fontdict = {'fontsize' : 20})
plt.legend()
plt.savefig('data/figures/capture_ability_test', dpi=300, bbox_inches='tight')



