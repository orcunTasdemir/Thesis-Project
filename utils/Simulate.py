import os
from typing import Dict
import numpy as np
from utils.Agent import Agent
from utils.Field import Field
from utils.Food import Food
from random import randint, choice
from math import pi
from utils.Game import Game
from utils.tools import *
from copy import deepcopy
import pickle
from utils.Visualize import *
from random import uniform


def simulate(game: Game, cycles: int = 20000, have_agents_list: bool = False, type: str = "regular"):
    if(game.game_type == "SSS"):
        return simulate_SSS(game, cycles, have_agents_list, type)
    elif(game.game_type == "VOLUN_SSS"):
        return simulate_SSS(game, cycles, have_agents_list, type, True) #true for voluntary
    elif(game.game_type == "SIT"):
        return simulate_SIT(game, cycles, have_agents_list, type, True) #true for voluntary
    elif(game.game_type == "ISS"):
        return simulate_ISS(game, cycles, have_agents_list, type)
    elif(game.game_type == "Competition"):
        return simulate_Competition(game, cycles, have_agents_list, type)


def simulate_ISS(game: Game, cycles=20000, have_agents_list: bool = False, type: str = "regular"):
    """Simulates a given game for the given number of cycles
    Args:
        game (Game): Game passed to the simulation
        cycles (int, optional): Number of cycles for the simulation to run.
        Defaults to 20000.
    """
    Overpopulation = False

    SIMULATION_DATA = {"header":
                       {
                           "gameType": game.game_type,
                           "gameEnvironment": game.environment_type,
                           "totalCycles": cycles,
                           "foodEnergy": game.food_energy,
                           "numFood": int(((Game.environment_types[game.environment_type])/100)*game.field.size*game.field.size),
                           "agentEnergy": game.agent_energy,
                           "numFirstGen": game.num_of_first_gen,
                           "overrideReproductionSpan": game.overrideReproductionSpan,
                           "popLimit": game.popLimit,
                           "Overpopulation": False,
                           "extinction": False,
                           "lastCycle": 0
                       }
                       }
    CYCLE_DATA = {}
    size = game.field.size
    offspring_dict = {}
    offspringName = int(game.num_of_first_gen + 1)
    deleted_agents = []
    numFoodEaten = 0

    # here we put 10 agents every cycle so we can do a test on them
    agents_list_for_test = []

    for cycle in range(0, cycles+1):
        # print("boolean is: ", have_agents_list)
        if(have_agents_list):
            # print("goes here")
            if(len(game.agents) < 10):
                agents_list_for_cycle = list(game.agents.items())
            else:
                agents_list_for_cycle = random.sample(
                    list(game.agents.items()), 10)
            agents_list_for_test.append(agents_list_for_cycle)

        print("cycle number: ", cycle)
        CYCLE_DATA["NoFoodLeft"] = game.isFoodLeft()

        numDead = len(deleted_agents)
        for agent in deleted_agents:
            game.delete_agent(agent)
        deleted_agents = []

        numBirth = len(offspring_dict)
        game.agents.update(offspring_dict)
        offspring_dict = {}
        ###########################################################################################
        if cycle % game.foodYear == 0 and cycle != 0:
            CYCLE_DATA["isFoodYear"] = True
            game.reintroduceFood()
        else:
            CYCLE_DATA["isFoodYear"] = True
        ###########################################################################################
        agents = game.agents
        UPDATE = {"pop": len(agents),
                  "cycle": cycle,
                  "numFood": game.getNumOfFood(),
                  "numFoodEaten": numFoodEaten,
                  "numDead": numDead,
                  "numBirth": numBirth,
                  "centralStorage": game.central_storage,
                  "averageSocialGene": game.getAverageSocialGene(),
                  "averageAge": game.getAverageAge(),
                  "averageEnergy": game.getAverageEnergy()
                  }
        CYCLE_DATA.update(UPDATE)
        numFoodEaten = 0
        if cycle % 1000 == 0:
            AGENTS_DATA = {}
            for agent_name in agents:
                agent = agents[agent_name]
                agent_dict = {"name": agent.name,
                              "energy": agent.energy,
                              "age": agent.age,
                              "numKids": agent.numKids,
                              "impact": agent.impact_strength,
                              "socialGene": agent.social_gene,
                              "othersInPerimenter": game.getOthersInPerimeter(agent)},
                AGENTS_DATA[f"{agent.name}"] = agent_dict
            CYCLE_DATA["agents"] = AGENTS_DATA
        if(len(agents) == 0):
            SIMULATION_DATA["header"]["extinction"] = True
            SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "extinction", agents_list_for_test]
        if(Overpopulation == True):
            SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "Overpopulation", agents_list_for_test]
        SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA

        if(cycle == cycles):
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "normal", agents_list_for_test]
        CYCLE_DATA = {}
        for agent_name in agents:
            
            
            agent = agents[agent_name]
            
            print(agent.social_gene)
            
            ########################################
            # if it is a food test the agents are invinsible
            if(type != "foodTest"):
                agent.energy = agent.energy - game.cost
                agent.age += 1
            ########################################
            if agent.energy <= 0 or agent.age >= Agent.lifeSpan:
                deleted_agents.append(agent)
                continue
            ########################################
            agent_x = agent.x
            agent_y = agent.y
            distance, angle = game.getDistanceAndAngle(agent)
            if(agent.move(agent.neuralNetwork.run_network(np.array([distance, angle])))):
                move = 1
                # print(f"{distance}{angle}")
                fd = agent.facing_direction
                edge = size - 1
                if (fd == 0 and agent_y < edge and not isinstance(game.field.array[agent_x, agent_y + move], Agent)):
                    game.move_agent_out(agent)
                    agent_y = agent_y + move
                elif (fd == 1 and agent_x > 0 and not isinstance(game.field.array[agent_x - move, agent_y], Agent)):
                    game.move_agent_out(agent)
                    agent_x = agent_x - move
                elif (fd == 2 and agent_y > 0 and not isinstance(game.field.array[agent_x, agent_y - move], Agent)):
                    game.move_agent_out(agent)
                    agent_y = agent_y - move
                elif (fd == 3 and agent_x < edge and not isinstance(game.field.array[agent_x + move, agent_y], Agent)):
                    game.move_agent_out(agent)
                    agent_x = agent_x + move
                if isinstance(game.field.array[agent_x, agent_y], Food):
                    # or game.food_energy
                    agent.energy += game.field.array[agent_x, agent_y].energy
                    # print('energy of the food:', game.field.array[agent_x, agent_y].energy)
                    game.delete_food(agent_x, agent_y)
                    numFoodEaten += 1
                agent.x = agent_x
                agent.y = agent_y
                game.field.array[agent.x, agent.y] = agent
            ###############################################
            if(len(agents) + len(offspring_dict) >= game.popLimit):
                Overpopulation = True
                SIMULATION_DATA["header"]["Overpopulation"] = True
            if(game.overrideReproductionSpan):
                # if(not(agent.energy >= 150 and agent.age >= 50 and agent.age - agent.last_age_reproduced >= 50)):
                #     continue
                if(not(agent.age >= Agent.reproductionSpan and agent.age - agent.last_age_reproduced >= Agent.reproductionSpan)):
                    continue
            elif agent.age % Agent.reproductionSpan != 0:
                continue
            agent.last_age_reproduced = agent.age
            agent.numKids += 1
            offspring = agent.reproduce()
            i = 0
            not_placed = True
            while not_placed:
                i += 1
                spiral_updates = spiral_update(i)
                random.shuffle(spiral_updates)
                for update in spiral_updates:
                    off_x = agent_x + update[0]
                    off_y = agent_y + update[1]
                    if(off_x < 100 and off_y < 100):
                        try:
                            if game.field.array[off_x, off_y] is None:
                                offspring.x = off_x
                                offspring.y = off_y
                                not_placed = False
                                break
                        except Exception:
                            pass
            given_name = "agent{0}".format(offspringName)
            offspring.name = given_name
            offspring_dict[given_name] = offspring
            game.field.array[offspring.x, offspring.y] = offspring
            offspringName += 1


def run_simulations(
    give,
    keep,
    folder_name: str = "test",
    file_name: int = None,
    num_of_sims: int = 30,
    num_of_first_gen: int = Game.num_of_first_gen,
    environment_type: str = "Temperate",
    game_type: str = "ISS",
    food_energy: float = Food.energy,
    agent_energy: float = Agent.energy,
    cycles: int = Game.CYCLES,
    tries: int = 1,
    allow_extinction: bool = False,
    have_agents_list: bool = False,
    type: str = "regular"
):
    """run_simulations runs a number of simulations for a number of cycles and outputs the results in a folder in separate files, and also records the name objects in files using pickle

    Args:
        folder_name (str, optional): Folder name to put the files. Defaults to "test".
        file_name (str, optional): File name template to use. Defaults to "default".
        num_of_sims (int, optional): _description_. Defaults to 30.
        num_of_first_gen (int, optional): _description_. Defaults to Game.num_of_first_gen.
        environment_type (str, optional): _description_. Defaults to "Temperate".
        game_type (str, optional): _description_. Defaults to "ISS".
        food_energy (float, optional): _description_. Defaults to Food.energy.
        agent_energy (float, optional): _description_. Defaults to Agent.energy.
        cycles (int, optional): _description_. Defaults to Game.CYCLES.
    """

    print(f"########## :: {num_of_sims} SIMULATIONS INITIATED WITH :: ##########",
          f"########## :: {num_of_first_gen} initial agents,",
          f"########## :: {environment_type} environment type,",
          f"########## :: with {game_type} strategy society,",
          f"########## :: with {food_energy} food energy,",
          f"########## :: and {agent_energy} agent energy,",
          f"########## :: for {cycles} cycles"
          )

    if (folder_name == 'test'):
        folder_name = f"test_{randint(1000,10000) }"

    # if(not(os.path.isdir(f"data/{folder_name}"))):
    #     os.makedirs(f"data/{folder_name}")
    # else:
    #     for f in os.listdir(folder_name):
    #         print(f)
    #         os.remove(f"{folder_name}/{f}")

    i = num_of_sims
    while(i > 0):

        file_name = randint(1000, 10000)

        game = Game(
            agents={},
            environment_type=environment_type,
            game_type=game_type,
            food_energy=food_energy,
            agent_energy=agent_energy,
            num_of_first_gen=num_of_first_gen,
            overrideReproductionSpan=True,
            give=give,
            keep=keep
        )

        game.init_agents()
        game.populate()
        game.put_food(init=True)
        game_init = deepcopy(game)
        if(allow_extinction):
            GAME, SIMULATION_DATA, endstate, agent_list = simulate(game=game, cycles=cycles, have_agents_list=have_agents_list, type=type)
            pickle.dump(game_init, open(
                f"data/{folder_name}/pickledGameINIT_{file_name}.pic", "wb"))
            pickle.dump(GAME, open(
                f"data/{folder_name}/pickledGamePOST_{file_name}.pic", "wb"))
            write_json_to_folder(SIMULATION_DATA, folder_name, file_name)
            visualizePopulation(
                f"data/{folder_name}/output_{file_name}.js", smooth=False)
            if(have_agents_list):
                # print("agent list: ", agent_list)
                with open(f"data/{folder_name}/agent_list_{file_name}.txt", "w+") as f:
                    f.write("\n".join(str(agent) for agent in agent_list))

            i -= 1
        else:
            tryy = 0
            while(tryy < tries):
                # print("here")
                GAME, SIMULATION_DATA, endstate, agent_list = simulate(game=game,
                                                                       cycles=cycles,
                                                                       have_agents_list=have_agents_list,
                                                                       type=type)
                if(endstate != "extinction"):
                    i -= 1
                    pickle.dump(game_init, open(
                        f"data/{folder_name}/pickledGameINIT_{file_name}.pic", "wb"))
                    pickle.dump(GAME, open(
                        f"data/{folder_name}/pickledGamePOST_{file_name}.pic", "wb"))
                    write_json_to_folder(
                        SIMULATION_DATA, folder_name, file_name)
                    visualizePopulation(
                        f"data/{folder_name}/output_{file_name}.js", smooth=False)
                    if(have_agents_list):
                        # print("agent list: ", agent_list)
                        with open(f"data/{folder_name}/agent_list_{file_name}.txt", "w+") as f:
                            f.write("\n".join(str(agent)
                                    for agent in agent_list))
                    break
                tryy += 1


def simulate_SSS(game: Game, cycles=20000, have_agents_list: bool = False, type: str = "regular", voluntary : bool = False):
    """Simulates a given game for the given number of cycles
    Args:
        game (Game): Game passed to the simulation
        cycles (int, optional): Number of cycles for the simulation to run.
        Defaults to 20000.
    """
    Overpopulation = False
    SIMULATION_DATA = {"header":
                       {
                           "gameType": game.game_type,
                           "gameEnvironment": game.environment_type,
                           "totalCycles": cycles,
                           "foodEnergy": game.food_energy,
                           "numFood": int(((Game.environment_types[game.environment_type])/100)*game.field.size*game.field.size),
                           "agentEnergy": game.agent_energy,
                           "numFirstGen": game.num_of_first_gen,
                           "overrideReproductionSpan": game.overrideReproductionSpan,
                           "popLimit": game.popLimit,
                           "Overpopulation": False,
                           "extinction": False,
                           "lastCycle": 0,
                           "centralStorage": game.central_storage
                       }
                       }
    CYCLE_DATA = {}
    size = game.field.size
    offspring_dict = {}
    offspringName = int(game.num_of_first_gen + 1)
    deleted_agents = []
    numFoodEaten = 0

    agents_list_for_test = []
    for cycle in range(0, cycles+1):

        if(have_agents_list):
            if(len(game.agents) < 5):
                agents_list_for_cycle = list(game.agents.items())
            else:
                agents_list_for_cycle = random.sample(
                    list(game.agents.items()), 5)
            agents_list_for_test.append(agents_list_for_cycle)

        print("cycle number: ", cycle)
        CYCLE_DATA["NoFoodLeft"] = game.isFoodLeft()

        numDead = len(deleted_agents)
        for agent in deleted_agents:
            game.delete_agent(agent)
        deleted_agents = []

        numBirth = len(offspring_dict)
        game.agents.update(offspring_dict)
        offspring_dict = {}
        ###########################################################################################
        if cycle % game.foodYear == 0 and cycle != 0:
            CYCLE_DATA["isFoodYear"] = True
            game.reintroduceFood()
        else:
            CYCLE_DATA["isFoodYear"] = True
        ###########################################################################################
        agents = game.agents
        UPDATE = {"pop": len(agents),
                  "cycle": cycle,
                  "numFood": game.getNumOfFood(),
                  "numFoodEaten": numFoodEaten,
                  "numDead": numDead,
                  "numBirth": numBirth,
                  "centralStorage": game.central_storage,
                  "averageSocialGene": game.getAverageSocialGene(),
                  "averageAge": game.getAverageAge(),
                  "averageEnergy": game.getAverageEnergy()
                  }
        CYCLE_DATA.update(UPDATE)
        numFoodEaten = 0
        if cycle % 1000 == 0:
            AGENTS_DATA = {}
            for agent_name in agents:
                agent = agents[agent_name]
                agent_dict = {"name": agent.name,
                              "energy": agent.energy,
                              "age": agent.age,
                              "numKids": agent.numKids,
                              "impact": agent.impact_strength,
                              "socialGene": agent.social_gene,
                              "othersInPerimenter": game.getOthersInPerimeter(agent)},
                AGENTS_DATA[f"{agent.name}"] = agent_dict
            CYCLE_DATA["agents"] = AGENTS_DATA
        if(len(agents) == 0):
            SIMULATION_DATA["header"]["extinction"] = True
            SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "extinction", agents_list_for_test]
        if(Overpopulation == True):
            SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "Overpopulation", agents_list_for_test]
        SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA

        if(cycle == cycles):
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "normal", agents_list_for_test]
        CYCLE_DATA = {}

        # here add the energy from the central storage to randomly selected 10% of the agents
        selected_number = int(len(game.agents)/10)
        agent_list = random.sample(list(game.agents.items()), selected_number)
        agent_names = []
        for agent in agent_list:
            agent_names.append(agent[0])
        # agent_names = random.sample(agent_names, selected_number)
        # print("\n\n1::", game.agents)
        # print("\n\n2::", agents)
        # print("\n\nAGENT_LIST: ", agent_list)
        for agent_name in agent_names:
            if(game.central_storage <= 0):
                break
            game.agents[agent_name].energy += game.give_from_storage
            game.central_storage -= game.give_from_storage
        # reset the central storage
        #game.central_storage = 0

        agents = game.agents

        for agent_name in agents:
            agent = agents[agent_name]
            
            print(agent.social_gene)
            ########################################
            # if it is a food test the agents are invinsible
            if(type != "foodTest"):
                agent.energy = agent.energy - game.cost
                agent.age += 1
            ########################################
            if agent.energy <= 0 or agent.age >= Agent.lifeSpan:
                deleted_agents.append(agent)
                continue
            ########################################
            agent_x = agent.x
            agent_y = agent.y
            distance, angle = game.getDistanceAndAngle(agent)
            if(agent.move(agent.neuralNetwork.run_network(np.array([distance, angle])))):
                move = 1
                # print(f"{distance}{angle}")
                fd = agent.facing_direction
                edge = size - 1
                if (fd == 0 and agent_y < edge and not isinstance(game.field.array[agent_x, agent_y + move], Agent)):
                    game.move_agent_out(agent)
                    agent_y = agent_y + move
                elif (fd == 1 and agent_x > 0 and not isinstance(game.field.array[agent_x - move, agent_y], Agent)):
                    game.move_agent_out(agent)
                    agent_x = agent_x - move
                elif (fd == 2 and agent_y > 0 and not isinstance(game.field.array[agent_x, agent_y - move], Agent)):
                    game.move_agent_out(agent)
                    agent_y = agent_y - move
                elif (fd == 3 and agent_x < edge and not isinstance(game.field.array[agent_x + move, agent_y], Agent)):
                    game.move_agent_out(agent)
                    agent_x = agent_x + move
                if isinstance(game.field.array[agent_x, agent_y], Food):
                    # the energy gained no matter what is this
                    energy_gained = game.field.array[agent_x, agent_y].energy
                    # if the game is voluntary and the social gene is over 0
                    if((not voluntary) or (voluntary and agent.social_gene > 0)):
                        ratio = sigmoid5(agent.social_gene)
                        give = ratio * game.give
                        keep = 1 - give
                        game.central_storage += energy_gained*(give)
                        agent.energy += energy_gained*(keep)
                    agent.energy += energy_gained
                    # print('energy of the food:', game.field.array[agent_x, agent_y].energy)
                    game.delete_food(agent_x, agent_y)
                    numFoodEaten += 1
                agent.x = agent_x
                agent.y = agent_y
                game.field.array[agent.x, agent.y] = agent
            ###############################################
            if(len(agents) + len(offspring_dict) >= game.popLimit):
                Overpopulation = True
                SIMULATION_DATA["header"]["Overpopulation"] = True
            if(game.overrideReproductionSpan):
                # if(not(agent.energy >= 150 and agent.age >= 50 and agent.age - agent.last_age_reproduced >= 50)):
                #     continue
                if(not(agent.age >= Agent.reproductionSpan and agent.age - agent.last_age_reproduced >= Agent.reproductionSpan)):
                    continue
            elif agent.age % Agent.reproductionSpan != 0:
                continue
            agent.last_age_reproduced = agent.age
            agent.numKids += 1
            offspring = agent.reproduce()
            i = 0
            not_placed = True
            while not_placed:
                i += 1
                spiral_updates = spiral_update(i)
                random.shuffle(spiral_updates)
                for update in spiral_updates:
                    off_x = agent_x + update[0]
                    off_y = agent_y + update[1]
                    if(off_x < 100 and off_y < 100):
                        try:
                            if game.field.array[off_x, off_y] is None:
                                offspring.x = off_x
                                offspring.y = off_y
                                not_placed = False
                                break
                        except Exception:
                            pass
            given_name = "agent{0}".format(offspringName)
            offspring.name = given_name
            offspring_dict[given_name] = offspring
            game.field.array[offspring.x, offspring.y] = offspring
            offspringName += 1


def run_test(iss_agents: list, sss_agents: list, duration: int = 200, environment: str = "Test"):

    iss_agents_by_cycles_food_capture = []
    for agent_batches in iss_agents:
        total_capture_for_batch = 0
        for (agent_name, agent) in agent_batches:
            food_num = 0
            game = Game(game_type="ISS", environment_type=environment)
            game.agents[agent_name] = agent
            game.put_one_agent()
            game.put_food(challenge=True)
            _, simulation_data, _, _ = simulate(
                game, duration, type="foodTest")
            food_captured = 0
            for key in simulation_data:
                if key == "header":
                    continue
                food_num = simulation_data[key]['numFoodEaten']
                food_captured += food_num
            total_capture_for_batch += food_captured
        iss_agents_by_cycles_food_capture.append(total_capture_for_batch)

    sss_agents_by_cycles_food_capture = []
    for agent_batches in sss_agents:
        total_capture_for_batch = 0
        for (agent_name, agent) in agent_batches:
            food_num = 0
            game = Game(game_type="ISS", environment_type=environment)
            game.agents[agent_name] = agent
            game.put_one_agent()
            game.put_food(challenge=True)
            _, simulation_data, _, _ = simulate(
                game, duration, type="foodTest")
            food_captured = 0
            for key in simulation_data:
                if key == "header":
                    continue
                food_num = simulation_data[key]['numFoodEaten']
                food_captured += food_num
            total_capture_for_batch += food_captured
        sss_agents_by_cycles_food_capture.append(total_capture_for_batch)

    return [iss_agents_by_cycles_food_capture, sss_agents_by_cycles_food_capture]



def simulate_Competition(game: Game, cycles=20000, have_agents_list: bool = False, type: str = "regular"):
    """Simulates a given game for the given number of cycles
    Args:
        game (Game): Game passed to the simulation
        cycles (int, optional): Number of cycles for the simulation to run.
        Defaults to 20000.
    """
    
    print("correct simulation")
    Overpopulation = False
    SIMULATION_DATA = {"header":
                       {
                           "gameType": game.game_type,
                           "gameEnvironment": game.environment_type,
                           "totalCycles": cycles,
                           "foodEnergy": game.food_energy,
                           "numFood": int(((Game.environment_types[game.environment_type])/100)*game.field.size*game.field.size),
                           "agentEnergy": game.agent_energy,
                           "numFirstGen": game.num_of_first_gen,
                           "overrideReproductionSpan": game.overrideReproductionSpan,
                           "popLimit": game.popLimit,
                           "Overpopulation_iss": False,
                           "Overpopulation_sss": False,
                           "extinction_iss": False,
                           "extinction_sss": False,
                           "lastCycle": 0,
                           "centralStorage": game.central_storage
                       }
                       }
    CYCLE_DATA = {}
    size = game.field.size
    offspring_dict = {}
    offspringName = int(game.num_of_first_gen + 1)
    deleted_agents = []
    numFoodEaten = 0

    agents_list_for_test = []
    for cycle in range(0, cycles+1):

        if(have_agents_list):
            if(len(game.agents) < 10):
                agents_list_for_cycle = list(game.agents.items())
            else:
                agents_list_for_cycle = random.sample(
                    list(game.agents.items()), 10)
            agents_list_for_test.append(agents_list_for_cycle)

        print("cycle number: ", cycle)
        CYCLE_DATA["NoFoodLeft"] = game.isFoodLeft()

        numDead = len(deleted_agents)
        for agent in deleted_agents:
            game.delete_agent(agent)
        deleted_agents = []

        numBirth = len(offspring_dict)
        game.agents.update(offspring_dict)
        offspring_dict = {}
        ###########################################################################################
        if cycle % game.foodYear == 0 and cycle != 0:
            CYCLE_DATA["isFoodYear"] = True
            game.reintroduceFood()
        else:
            CYCLE_DATA["isFoodYear"] = True
        ###########################################################################################
        agents = game.agents
        
        # at cycle 0 we set the agents to be in two different groups, afterwards
        # this will be managed in deaths
        # and or births individually
        if(cycle ==0):
            iss_agents = []
            sss_agents = []
            
            for agent_name in agents:
                if(game.agents[agent_name].isSSS == True):
                    sss_agents.append(game.agents[agent_name])
                else:
                    iss_agents.append(game.agents[agent_name])
                
        UPDATE = {"popISS": len(iss_agents),
                  "popSSS": len(sss_agents),
                  "cycle": cycle,
                  "numFood": game.getNumOfFood(),
                  "numFoodEaten": numFoodEaten,
                  "numDead": numDead,
                  "numBirth": numBirth,
                  "centralStorage": game.central_storage,
                  "averageSocialGene": game.getAverageSocialGene(),
                  "averageAge": game.getAverageAge(),
                  "averageEnergy": game.getAverageEnergy()
                  }
        CYCLE_DATA.update(UPDATE)
        numFoodEaten = 0
        # if cycle % 1000 == 0:
        #     AGENTS_DATA = {}
        #     for agent_name in agents:
        #         agent = agents[agent_name]
        #         agent_dict = {"name": agent.name,
        #                       "energy": agent.energy,
        #                       "age": agent.age,
        #                       "numKids": agent.numKids,
        #                       "impact": agent.impact_strength,
        #                       "socialGene": agent.social_gene,
        #                       "othersInPerimenter": game.getOthersInPerimeter(agent)},
        #         AGENTS_DATA[f"{agent.name}"] = agent_dict
        #     CYCLE_DATA["agents"] = AGENTS_DATA
        if(len(iss_agents) == 0):
            SIMULATION_DATA["header"]["extinction_iss"] = True
            SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA
        if(len(sss_agents) == 0):
            SIMULATION_DATA["header"]["extinction_sss"] = True
            SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA
        if(len(iss_agents) == 0 and  len(sss_agents) == 0):
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "extinction", agents_list_for_test]
        
        # there wont be any overpopulation anyways
        if(Overpopulation == True):
            SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "Overpopulation", agents_list_for_test]
        SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA

        if(cycle == cycles):
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "normal", agents_list_for_test]
        CYCLE_DATA = {}

        # here add the energy from the central storage to randomly selected 10% of the agents
        selected_number = int(len(sss_agents)/10)
        agent_list = random.sample(sss_agents, selected_number)
        
        # agent_names = random.sample(agent_names, selected_number)
        # print("\n\n1::", game.agents)
        # print("\n\n2::", agents)
        # print("\n\nAGENT_LIST: ", agent_list)
        for agent in agent_list:
            if(game.central_storage <= 0):
                break
            agent.energy += game.give_from_storage
            game.central_storage -= game.give_from_storage
        # reset the central storage
        #game.central_storage = 0

        agents = game.agents

        for agent_name in agents:
            agent = agents[agent_name]
            # true if the agent is sss
            sss_agent = agent.isSSS
            ########################################
            # if it is a food test the agents are invinsible
            if(type != "foodTest"):
                agent.energy = agent.energy - game.cost
                agent.age += 1
            ########################################
            if agent.energy <= 0 or agent.age >= Agent.lifeSpan:
                deleted_agents.append(agent)
                if(sss_agent):
                    sss_agents.remove(agent)
                else:
                    iss_agents.remove(agent)
                continue
            ########################################
            agent_x = agent.x
            agent_y = agent.y
            distance, angle = game.getDistanceAndAngle(agent)
            if(agent.move(agent.neuralNetwork.run_network(np.array([distance, angle])))):
                move = 1
                # print(f"{distance}{angle}")
                fd = agent.facing_direction
                edge = size - 1
                if (fd == 0 and agent_y < edge and not isinstance(game.field.array[agent_x, agent_y + move], Agent)):
                    game.move_agent_out(agent)
                    agent_y = agent_y + move
                elif (fd == 1 and agent_x > 0 and not isinstance(game.field.array[agent_x - move, agent_y], Agent)):
                    game.move_agent_out(agent)
                    agent_x = agent_x - move
                elif (fd == 2 and agent_y > 0 and not isinstance(game.field.array[agent_x, agent_y - move], Agent)):
                    game.move_agent_out(agent)
                    agent_y = agent_y - move
                elif (fd == 3 and agent_x < edge and not isinstance(game.field.array[agent_x + move, agent_y], Agent)):
                    game.move_agent_out(agent)
                    agent_x = agent_x + move
                if isinstance(game.field.array[agent_x, agent_y], Food):
                    # or game.food_energy
                    energy_gained = game.field.array[agent_x, agent_y].energy
                    game.central_storage += energy_gained*(game.give)
                    agent.energy += energy_gained*(game.keep)
                    # print('energy of the food:', game.field.array[agent_x, agent_y].energy)
                    game.delete_food(agent_x, agent_y)
                    numFoodEaten += 1
                agent.x = agent_x
                agent.y = agent_y
                game.field.array[agent.x, agent.y] = agent
            ###############################################
            if(len(agents) + len(offspring_dict) >= game.popLimit):
                Overpopulation = True
                SIMULATION_DATA["header"]["Overpopulation"] = True
            if(game.overrideReproductionSpan):
                # if(not(agent.energy >= 150 and agent.age >= 50 and agent.age - agent.last_age_reproduced >= 50)):
                #     continue
                if(not(agent.age >= Agent.reproductionSpan and agent.age - agent.last_age_reproduced >= Agent.reproductionSpan)):
                    continue
            elif agent.age % Agent.reproductionSpan != 0:
                continue
            agent.last_age_reproduced = agent.age
            agent.numKids += 1
            offspring = agent.reproduce()
            i = 0
            not_placed = True
            while not_placed:
                i += 1
                spiral_updates = spiral_update(i)
                random.shuffle(spiral_updates)
                for update in spiral_updates:
                    off_x = agent_x + update[0]
                    off_y = agent_y + update[1]
                    if(off_x < 100 and off_y < 100):
                        try:
                            if game.field.array[off_x, off_y] is None:
                                offspring.x = off_x
                                offspring.y = off_y
                                not_placed = False
                                break
                        except Exception:
                            pass
            given_name = "agent{0}".format(offspringName)
            offspring.name = given_name
            offspring_dict[given_name] = offspring
            if(offspring.isSSS):
                sss_agents.append(offspring)
            else:
                iss_agents.append(offspring)
            game.field.array[offspring.x, offspring.y] = offspring
            offspringName += 1




def simulate_SIT(game: Game, cycles=20000, have_agents_list: bool = False, type: str = "regular", voluntary : bool = True):
    """Simulates a given game for the given number of cycles
    Args:
        game (Game): Game passed to the simulation
        cycles (int, optional): Number of cycles for the simulation to run.
        Defaults to 20000.
    """
    
    # for agent in game.agents:
    #     print("print social genes prior to anything", game.agents[agent].social_gene)
    
    Overpopulation = False
    SIMULATION_DATA = {"header":
                       {
                           "gameType": game.game_type,
                           "gameEnvironment": game.environment_type,
                           "totalCycles": cycles,
                           "foodEnergy": game.food_energy,
                           "numFood": int(((Game.environment_types[game.environment_type])/100)*game.field.size*game.field.size),
                           "agentEnergy": game.agent_energy,
                           "numFirstGen": game.num_of_first_gen,
                           "overrideReproductionSpan": game.overrideReproductionSpan,
                           "popLimit": game.popLimit,
                           "Overpopulation": False,
                           "extinction": False,
                           "lastCycle": 0,
                           "centralStorage": game.central_storage
                       }
                       }
    CYCLE_DATA = {}
    size = game.field.size
    offspring_dict = {}
    offspringName = int(game.num_of_first_gen + 1)
    deleted_agents = []
    numFoodEaten = 0

    agents_list_for_test = []
    for cycle in range(0, cycles+1):

        if(have_agents_list):
            if(len(game.agents) < 5):
                agents_list_for_cycle = list(game.agents.items())
            else:
                agents_list_for_cycle = random.sample(
                    list(game.agents.items()), 5)
            agents_list_for_test.append(agents_list_for_cycle)

        print("cycle number: ", cycle)
        CYCLE_DATA["NoFoodLeft"] = game.isFoodLeft()

        numDead = len(deleted_agents)
        for agent in deleted_agents:
            game.delete_agent(agent)
        deleted_agents = []

        numBirth = len(offspring_dict)
        game.agents.update(offspring_dict)
        offspring_dict = {}
        ###########################################################################################
        if cycle % game.foodYear == 0 and cycle != 0:
            CYCLE_DATA["isFoodYear"] = True
            game.reintroduceFood()
        else:
            CYCLE_DATA["isFoodYear"] = True
        ###########################################################################################
        agents = game.agents
        UPDATE = {"pop": len(agents),
                  "cycle": cycle,
                  "numFood": game.getNumOfFood(),
                  "numFoodEaten": numFoodEaten,
                  "numDead": numDead,
                  "numBirth": numBirth,
                  "centralStorage": game.central_storage,
                  "averageSocialGene": game.getAverageSocialGene(),
                  "averageAge": game.getAverageAge(),
                  "averageEnergy": game.getAverageEnergy()
                  }
        CYCLE_DATA.update(UPDATE)
        numFoodEaten = 0
        if cycle % 500 == 0:
            AGENTS_DATA = {}
            for agent_name in agents:
                agent = agents[agent_name]
                agent_dict = {"name": agent.name,
                              "energy": agent.energy,
                              "age": agent.age,
                              "numKids": agent.numKids,
                              "impact": agent.impact_strength,
                              "socialGene": agent.social_gene,
                              "othersInPerimenter": game.getOthersInPerimeter(agent)},
                AGENTS_DATA[f"{agent.name}"] = agent_dict
            CYCLE_DATA["agents"] = AGENTS_DATA
        if(len(agents) == 0):
            SIMULATION_DATA["header"]["extinction"] = True
            SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "extinction", agents_list_for_test]
        if(Overpopulation == True):
            SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "Overpopulation", agents_list_for_test]
        SIMULATION_DATA[f"{cycle}"] = CYCLE_DATA

        if(cycle == cycles):
            SIMULATION_DATA["header"]['lastCycle'] = cycle
            return [game, SIMULATION_DATA, "normal", agents_list_for_test]
        CYCLE_DATA = {}

        # here add the energy from the central storage to randomly selected 10% of the agents
        selected_number = int(len(game.agents)/10)
        agent_list = random.sample(list(game.agents.items()), selected_number)
        agent_names = []
        for agent in agent_list:
            agent_names.append(agent[0])
        # agent_names = random.sample(agent_names, selected_number)
        # print("\n\n1::", game.agents)
        # print("\n\n2::", agents)
        # print("\n\nAGENT_LIST: ", agent_list)
        for agent_name in agent_names:
            if(game.central_storage <= 0):
                break
            game.agents[agent_name].energy += game.give_from_storage
            game.central_storage -= game.give_from_storage
        # reset the central storage
        #game.central_storage = 0

        agents = game.agents
        
        
        
        for agent_name in agents:
            
            agent = agents[agent_name]
            # print("print social genes prior to anything", agent.social_gene)
            
            
            # first we need to update the social gene of the agent depending on the impact
            impact = 0
            num_iss = 0
            num_sss = 0
            iss_values = []
            sss_values = []
            squares = spiral_impact(Agent.perimeter)
            # print(squares)
            squares.remove((0,0))
            for update in squares:
                search_x = agent.x + update[0]
                search_y = agent.y + update[1]
                if(search_x < 100 and search_y < 100):
                    whatis = game.field.array[search_x, search_y]
                    if(isinstance(whatis, Agent)):
                        # print("what is the social gene? ", whatis.social_gene)
                        # print("what is the energy? ", whatis.energy)
                        if(whatis.social_gene < 0):
                            # print("go here")
                            num_iss += 1
                            strength = mapRange(abs(whatis.age - agent.age), 0, 350, 0, 1) + mapRange(abs(whatis.energy - agent.energy), 0, 100, 0, 1) + mapRange(abs(whatis.numKids - agent.numKids), 0, 7, 0, 1)
                            iss_values.append(strength/game.getDistance(agent, search_x, search_y))
                        else:
                            # print("go here")
                            num_sss += 1
                            strength = mapRange(abs(whatis.age - agent.age), 0, 350, 0, 1) + mapRange(abs(whatis.energy - agent.energy), 0, 100, 0, 1) + mapRange(abs(whatis.numKids - agent.numKids), 0, 7, 0, 1)
                            sss_values.append(strength/game.getDistance(agent, search_x, search_y))
                            
            
            # if there was at all any impact
            if(num_iss > 0 or num_sss > 0): 
                
                # print("iss_values: ", iss_values)
                impact_iss = sum(iss_values) * ((num_iss)**game.bias)
                # print("impact iss: ", impact_iss)
                
                # print("sss_values: ", sss_values)
                impact_sss = sum(sss_values) * ((num_sss)**game.bias)
                # print("impact sss: ", impact_sss)
                
                impact = impact_sss - impact_iss
                # print("impact: ", impact)
                
                sig_imp = sigmoid5(abs(impact))
                # print("sig_imp: ", sig_imp)
                # the impact gets put in the sigmoid function and the resulting value is added or subtracted from the social gene
                if(impact < 0): 
                    agent.social_gene -= sig_imp
                else:
                    agent.social_gene += sig_imp
            
            ########################################
            # if it is a food test the agents are invinsible
            if(type != "foodTest"):
                agent.energy = agent.energy - game.cost
                agent.age += 1
            ########################################
            if agent.energy <= 0 or agent.age >= Agent.lifeSpan:
                deleted_agents.append(agent)
                continue
            ########################################
            agent_x = agent.x
            agent_y = agent.y
            distance, angle = game.getDistanceAndAngle(agent)
            if(agent.move(agent.neuralNetwork.run_network(np.array([distance, angle])))):
                move = 1
                # print(f"{distance}{angle}")
                fd = agent.facing_direction
                edge = size - 1
                if (fd == 0 and agent_y < edge and not isinstance(game.field.array[agent_x, agent_y + move], Agent)):
                    game.move_agent_out(agent)
                    agent_y = agent_y + move
                elif (fd == 1 and agent_x > 0 and not isinstance(game.field.array[agent_x - move, agent_y], Agent)):
                    game.move_agent_out(agent)
                    agent_x = agent_x - move
                elif (fd == 2 and agent_y > 0 and not isinstance(game.field.array[agent_x, agent_y - move], Agent)):
                    game.move_agent_out(agent)
                    agent_y = agent_y - move
                elif (fd == 3 and agent_x < edge and not isinstance(game.field.array[agent_x + move, agent_y], Agent)):
                    game.move_agent_out(agent)
                    agent_x = agent_x + move
                if isinstance(game.field.array[agent_x, agent_y], Food):
                    # the energy gained no matter what is this
                    energy_gained = game.field.array[agent_x, agent_y].energy
                    # if the game is voluntary and the social gene is over 0
                    if((not voluntary) or (voluntary and agent.social_gene > 0)):
                        ratio = sigmoid5(agent.social_gene)
                        give = ratio * game.give
                        keep = 1 - give
                        game.central_storage += energy_gained*(give)
                        agent.energy += energy_gained*(keep)
                    agent.energy += energy_gained
                    # print('energy of the food:', game.field.array[agent_x, agent_y].energy)
                    game.delete_food(agent_x, agent_y)
                    numFoodEaten += 1
                agent.x = agent_x
                agent.y = agent_y
                game.field.array[agent.x, agent.y] = agent
            ###############################################
            if(len(agents) + len(offspring_dict) >= game.popLimit):
                Overpopulation = True
                SIMULATION_DATA["header"]["Overpopulation"] = True
            if(game.overrideReproductionSpan):
                # if(not(agent.energy >= 150 and agent.age >= 50 and agent.age - agent.last_age_reproduced >= 50)):
                #     continue
                if(not(agent.age >= Agent.reproductionSpan and agent.age - agent.last_age_reproduced >= Agent.reproductionSpan)):
                    continue
            elif agent.age % Agent.reproductionSpan != 0:
                continue
            agent.last_age_reproduced = agent.age
            agent.numKids += 1
            offspring = agent.reproduce()
            i = 0
            not_placed = True
            while not_placed:
                i += 1
                spiral_updates = spiral_update(i)
                random.shuffle(spiral_updates)
                for update in spiral_updates:
                    off_x = agent_x + update[0]
                    off_y = agent_y + update[1]
                    if(off_x < 100 and off_y < 100):
                        try:
                            if game.field.array[off_x, off_y] is None:
                                offspring.x = off_x
                                offspring.y = off_y
                                not_placed = False
                                break
                        except Exception:
                            pass
            given_name = "agent{0}".format(offspringName)
            offspring.name = given_name
            offspring_dict[given_name] = offspring
            game.field.array[offspring.x, offspring.y] = offspring
            offspringName += 1



