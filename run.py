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


# game1 = Game()
# game1.init_agents()
# game1.populate()
# game1.put_food()


# def finding_optimal_energy_levels():
#     folder_name = "data/optimal_energy_levels"
#     if(os.path.isdir(folder_name)):
#             for f in os.listdir(folder_name):
#                 os.remove(f"{folder_name}/{f}")
#     else:
#         os.mkdir(folder_name)
#     p_food_nums = [8,9,10,11,12,13,14,15,16]
#     p_food_energy = [32,31,28,25,23,21,20,18,17]
#     i = 0
#     for food_num in range(len(p_food_nums)):
#         food_num = p_food_nums[i]
#         Game.environment_types["Temperate"] = food_num
#         food_energy = p_food_energy[i]
#         i += 1
#         run_simulations(
#             folder_name= f"optimal_energy_levels/I{food_num}T{food_num}F{food_energy}C1A50",
#             num_of_sims=5,
#             num_of_first_gen=Game.num_of_first_gen,
#             environment_type="Temperate",
#             game_type="ISS",
#             food_energy=food_energy,
#             agent_energy=Agent.energy,
#             cycles=20000,
#         )

# finding_optimal_energy_levels()
# run_simulations(
#                 folder_name= f"energyAnalysis",
#                 num_of_sims=1,
#                 num_of_first_gen=150,
#                 environment_type="Temperate",
#                 game_type="ISS",
#                 food_energy=20,
#                 agent_energy=20,
#                 cycles=20)

# no question about energy, there is no way we use energy because then there is no cumulation, because then the population spikes and stays there.
# we are also only using halving the energies because we need to be awarding the individuals and if individual wiht 1 energy reproduced they deserve to die.
# we shouldnt use more than 20 percent of field as food because then there is no sufficient hardship for the agents to develop.
# Agent energy should start low so that we see an initial dip in the population.
#

# visualizePopulation("data/realValues/output_2699.js", smooth=False)

# def correlation():
#     i = 0
#     all_results = []
#     total_energy = 16000.0
#     for food_en in range(4, 50, 2):
#         ten_repeat = []
#         for i in range(10):
#             print(i)
#             Game.environment_types['Temperate'] = (total_energy/food_en)/100
#             game1 = Game()
#             game1.food_energy = food_en
#             game1.popLimit = 800
#             game1.num_of_first_gen = 150
#             game1.init_agents()
#             game1.populate()
#             game1.put_food(init=True)
#             game2, result, _ = simulate(game1, 20000)
#             ten_repeat.append([result["numFood"], result['foodEnergy'], result['lastCycle']])
#         all_results.append(ten_repeat)
#     jsonn = json.dumps(all_results)
#     return jsonn

# result_of_10_repoeat_correlation = correlation()

# with open("data/correlation_results.txt") as f:
#     f.write(result_of_10_repoeat_correlation)

# print(result_of_10_repoeat_correlation)


# def run_energy_over_percentage_analysis():
#     total_energy = 16000.0
#     for food_en in range(4, 50, 2):
#         Game.environment_types['Temperate'] = (total_energy/food_en)/100
#         run_simulations(
#             folder_name= f"energyOverPercentageAnalysis",
#             file_name = f"FE{food_en}FP{(total_energy/food_en)/100}",
#             num_of_sims=1,
#             num_of_first_gen=150,
#             environment_type="Temperate",
#             game_type="ISS",
#             food_energy=food_en,
#             cycles=20000)

# run_energy_over_percentage_analysis()

# run_simulations(folder_name= f"ISS vs. SSS Single run",
#                 num_of_sims=1,
#                 num_of_first_gen=150,
#                 environment_type="Temperate",
#                 game_type="ISS",
#                 food_energy=32,
#                 agent_energy=30,
#                 cycles=20000,
# #                 allow_extinction=False)

run_simulations(folder_name="SIT_P0.5_2000s",
                num_of_sims=1,
                num_of_first_gen=150,
                environment_type="Temperate",
                game_type="SIT",
                food_energy=32,
                agent_energy=30,
                cycles=10000,
                allow_extinction=False,
                type="regular",
                give=0.45,
                keep=0.55,
                have_agents_list=False)


# run_simulations(folder_name= "oneSSSoneISSwithagentLists",
#                 num_of_sims=1,
#                 num_of_first_gen=150,
#                 environment_type="Temperate",
#                 game_type="SSS",
#                 food_energy=32,
#                 agent_energy=30,
#                 cycles=20000,
#                 allow_extinction=False,
#                 have_agents_list = True,
#                 type="regular")


# def run_energy_analysis_below5():
#     for food_en in range(5, 1, -1):
#         for agent_en in range(5, 1, -1):
#             run_simulations(
#                 folder_name= f"energyAnalysisbelow5Desktop",
#                 file_name = f"FE{food_en}AE{agent_en}",
#                 num_of_sims=1,
#                 num_of_first_gen=150,
#                 environment_type="Temperate",
#                 game_type="ISS",
#                 food_energy=food_en,
#                 agent_energy=agent_en,
#                 cycles=2000,
#                 tries=5)

# run_energy_analysis_below5()

# game = Game(game_type="ISS", environment_type="Temperate")
# game.init_agents()
# game.populate()
# game.put_food()
# game_out, simulation_data, _, iss_agents_list = simulate(game, 20000)

# game = Game(game_type="SSS", environment_type="Temperate")
# game.init_agents()
# game.populate()
# game.put_food()
# game_out, simulation_data, _, sss_agents_list = simulate(game, 20000)

# from utils.Simulate import run_test
# iss_record, sss_record = run_test(iss_agents_list, sss_agents_list, duration=200, environment="Test")
# # os.mkdir('data/learning_test')
# with open("data/learning_test/test_results_1.txt", "w+") as outfile:
#     outfile.write("\nISS_record:\n")
#     outfile.write("\n".join(str(item) for item in iss_record))
#     outfile.write("\nSSS_record:\n")
#     outfile.write("\n".join(str(item) for item in sss_record))


# Food capturing test to see their learning

# game = Game(game_type="ISS", environment_type="Temperate")
# game.init_agents()
# game.populate()
# game.put_food()
# game_out, simulation_data, _, iss_agents_list = simulate(game, 20000, have_agents_list=True)

# game = Game(game_type="SSS", environment_type="Temperate")
# game.init_agents()
# game.populate()
# game.put_food()
# game_out, simulation_data, _, sss_agents_list = simulate(game, 20000, have_agents_list=True)

# if(not(os.path.isdir(f"data/agent_lists_from_games"))):
#         os.makedirs(f"data/agent_lists_from_games")


# with open("data/agent_lists_from_games/ agent_lists.txt", "w+") as outfile:
#     outfile.write("\nISS_agent_list:\n")
#     outfile.write("\n".join(str(item) for item in iss_agents_list))
#     outfile.write("\nSSS_agent_list:\n")
#     outfile.write("\n".join(str(item) for item in sss_agents_list))
