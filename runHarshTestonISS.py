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



# get all sss games here
all_sss_games = []
for filename in os.listdir(f'data/25_SSS_games1/'):
    if("POST" in filename):
        with open(f"data/25_SSS_games1/{filename}", 'rb') as f:
            post_sss_game = pickle.load(f)
            all_sss_games.append(post_sss_game)

            

# try out the first ones
for game_sss in all_sss_games:
    
        try_game_sss = deepcopy(game_sss)
        try_game_sss.environment_type = "Harsh"
        try_game_sss.put_food(challenge=True)
        
        game_sss, data_sss, endstate, _ = simulate(game=try_game_sss,
                                                   cycles=20000,
                                                   have_agents_list=False,
                                                   type="regular")
        
        file_name = randint(1000, 10000) 
        pickle.dump(game_sss, open(
            f"data/25_H_SSS/pickledGamePOST_{file_name}.pic", "wb"))
        write_json_to_folder(data_sss, "25_H_SSS", file_name)
        visualizePopulation(
            f"data/25_H_SSS/output_{file_name}.js", smooth=False)
            



# import sys
# from utils.Agent import Agent
# from utils.Field import Field
# from utils.Food import Food
# from utils.Game import Game
# from utils.Simulate import *
# from utils.Visualize import *
# from typing import Dict
# from random import randint, randrange
# import numpy as np
# from matplotlib import colors
# from matplotlib import pyplot as plt

# from utils.tools import *
# import os
# import matplotlib


# # get all iss games here
# all_iss_games = []
# for filename in os.listdir(f'data/25_ISS_games1/'):
#     if("POST" in filename):
#         with open(f"data/25_ISS_games1/{filename}", 'rb') as f:
#             post_iss_game = pickle.load(f)
#             all_iss_games.append(post_iss_game)
            
# # get all sss games here
# all_sss_games = []
# for filename in os.listdir(f'data/25_SSS_games1/'):
#     if("POST" in filename):
#         with open(f"data/25_SSS_games1/{filename}", 'rb') as f:
#             post_sss_game = pickle.load(f)
#             all_sss_games.append(post_sss_game)
            

# # try out the first ones
# game_iss = all_iss_games[0]
# try_game_iss = deepcopy(game_iss)
# try_game_iss.give=0.25
# try_game_iss.keep=0.75
# # try out the first ones
# game_sss = all_sss_games[0]
# try_game_sss = deepcopy(game_sss)
# try_game_sss.give=0.25
# try_game_sss.keep=0.75

# try_game_iss.environment_type = "Harsh"
# try_game_sss.environment_type = "Harsh"

# try_game_iss.put_food(challenge=True)
# _, data_iss, _, _ = simulate(game=try_game_iss, cycles=20000, have_agents_list=False, type="regular")

# # i = 0
# # print(iss_game.environment_type)
# # for x in range(100):
# #     for y in range(100):
# #         if(isinstance(iss_game.field.array[x,y], Agent)):
# #             i += 1
# # print(i)

# try_game_sss.put_food(challenge=True)
# _, data_sss, _, _ = simulate(game=try_game_sss, cycles=20000, have_agents_list=False, type="regular")


# legends = []
# fig = plt.figure
# ax = plt.axes()

# pop=[]
# for key in data_iss:
#     if key =="header":
#         continue
#     pop.append(data_iss[key]['pop'])
# iss, = ax.plot(pop)
# iss.set_label("ISS")

# pop=[]
# for key in data_sss:
#     if key =="header":
#         continue
#     pop.append(data_sss[key]['pop'])
# sss, = ax.plot(pop)
# sss.set_label("SSS")

# plt.legend()
# ax.set_title("ISS and SSS Simulations on Harsh Environment=2.5%", fontdict = {'fontsize' : 20})
# plt.xticks( rotation='vertical')
# plt.savefig('data/figures/ISS and SSS Simulations on Harsh Environment 20000', dpi=300, bbox_inches='tight')



