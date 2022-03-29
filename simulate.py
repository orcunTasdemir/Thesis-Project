#Changes that can be made:
#doing it now
#one big change is that I am allowing multiple agents to be on the same square

import math
from typing import Dict
import numpy as np
from agent import Agent
from field import Field
from file_writer import fileWriter
from food import Food
import random
from math import pi
from game import Game
import csv
from itertools import permutations

#every 40 cycles 80 percent of the cells are filled with food again
#energy of every individual is decreased by half a point every cycle
#energy increases by 50 after eating food
#an agent creates one offspring every 50 cycles, the offspring is
#placed randomly close by its parent
#parent gives half their energy to their offspring
#350 cycles is the age limit
#simulation lasts 20.000 cycles


def spiral_update(iteration): #is this even necessary, do you like it?
    #for every iteration, I want to widen the perimeter
    #for the base case i = 0, I want only the neighbouring squares to be considered
    num_squares = 8 * iteration
    #squares = np.full([num_square, 2], 0)
    #the only way I could do this is to create a combinations list
    #for all the numbers in the coor list
    coor1 = [x for x in range(-iteration, iteration + 1)]
    #all coordinates for the square
    combinations_object1 = permutations(coor1, 2)
    list1 = list(combinations_object1)
    list1 = list1 + [(x,x) for x in range(-iteration, iteration + 1)]
    #delete (0,0) to be safe because iteration might just be 1
    list1.remove((0,0))
    #print("First list: ", list1)
    if iteration > 1:
        #all coordinates for the inner square
        coor2 = [x for x in range(-iteration+1, iteration)]
        combinations_object2 = permutations(coor2, 2)
        list2 = list(combinations_object2)
        list2 = list2 + [(x,x) for x in range(-iteration+1, iteration)]
        #print("Second list: ", list2)
        list1 = set(list1) - set(list2)
        #("Resulting list at the end: ", list1)
    return list1


def angle_agent_food(agent : Agent, find_x : int, find_y : int): #for thte angle of the food
    agent_x = agent.x
    agent_y = agent.y
    food_x = find_x
    food_y = find_y
    d1 = agent_x - food_x
    d2 = agent_y - food_y
    if d1 == 0:
        if d2 == 0:  # same points?
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
    return deg


foodyear = 40
lifeSpan = 350
reproductionYear = 50

def simulate(game : Game, cycles = 20000, file_num : int = 0):
    """[summary]

    Args:
        game (Game): Game passed to the simulation
        cycles (int, optional): Number of cycles for the simulation to run.
        Defaults to 20000.
    """
    
    fds = Agent.facing_directions
    
    #offspring dictionary because we cannot change the size of the agent
    #dictionary while we are looping through it 


    #To add the SSS functionality I need to take into account a couple of things,
    #Frist, for every cycle
    #new file writer, starts from
    fr = fileWriter('output', 'output_', '.out', file_num)
    fr.open_file()

    #size is here
    size = game.field.size

    #output_file =  open("output.txt", "w")
    
    offspring_dict = {}
    offspringName = int(len(game.agents) + 1)
    print("offspringName", offspringName)

    deleted_agents = []
    food_left = False
    
    for cycle in range(0, cycles):
        
        #if there is no food left everything can be different
        for x in range(100):
             for y in range(100):
                if isinstance(game.field.array[x][y], Food):
                    food_left = True
        if not food_left:
            print("There is no food left")
            
        print("cycle number: ", cycle)
        
        game.agents.update(offspring_dict)
        #print("agent_num: ", len(agents))
        offspring_dict = {}
        #delete the agents
        for agent in deleted_agents:
            game.delete_agent(agent)

        deleted_agents = []

        #at the beginning of each cycle I need to put offspring dictionary
        #into the agents dictionary
        #empty the dictionary
        #At each cycle I want to record the number of agents, and the number of food left for now
        fr.write_line(str(len(game.agents)))

        #every cycle I have many things to take care of
            #1- check every agent to see if they are dead
            #2- decrease everyones energy levels by half and age them by 1 year
            #3- check if it has been a year, if so add more food
            #4- check if an agent and a food is on the same square, if so add energy and delete food
            #5- Check if anyone is creating offspring this cycle
        #I can do all this if I loop around every agent once, this way is the most time efficient

        ###########################################################################################
        #3- if it has been a year add food
        if cycle%foodyear == 0:
            #print("A year has passed.\n")
            #we delete every food from the last year(stale?)
            game.delete_all_food()
            #print("All previous food is deleted.\n")
            #and introduce more food
            game.put_food()

        ###########################################################################################
        
        agents = game.agents
        
        for agent_name in agents:

            # print('agent_name: ', agent_name)
            agent = agents[agent_name]
            #######################################################################################
            #2- decrease the energy levels first so if he is dead we will know
            agent.energy = agent.energy - 0.5
            #age him by one year so we know if he is dead
            agent.age += 1

            #######################################################################################
            #1- he is dead
            if agent.energy <= 0 or agent.age >= 350:
                #if he is dead, we delete him
                #print("agent is dead, we remove him.\n")
                #we cannot delete here, save his name and delete him
                #after the loop ends
                deleted_agents.append(agent_name)
                #we skip the agent if he is already dead
                continue
                
            ########################################################################################
            #4- check if the agent and a food item are going to be on the same square after one move
            #find the closest food to the agent
            #for each food item in the foodArray calculate the euclidian distance to the agent
            #print("agent is here: ({},{})".format(agent.x, agent.y))
            agent_x = agent.x
            agent_y = agent.y

            # print('agent_x: ', agent.x)
            # print('agent_y: ', agent.y)
            
            #initiated as a random food
            distance = -1
            angle = -1
            food_not_found = True
            i = 0
            i_max = 3
            arr = game.field.array
            #USE scipy.spatial.KDTree TO SPEED THIS UP IF NECESSARY, should I look into this?
            while food_not_found == True:
                if i > i_max:
                    distance = 4.24
                    angle = angle_agent_food(agent, agent_x+3, agent_y+3)
                    break
                #for every iteration we didnt find food, I want to update the spiral search value
                i += 1
                spiral_updates = spiral_update(i)
                for update in spiral_updates:
                    find_x = agent_x + update[0]
                    find_y = agent_y + update[1]
                
                    try:    #lets see if this try statement works 
                        if isinstance(arr[find_x][find_y], Food):
                            #food found
                            food_not_found = False
                            #food equals to the food in this coordinate
                            #food = game.field.array[find_x][find_y]
                            #find euclidian distance from every food
                            distance = (((find_x - agent_x) ** 2) + ((find_y - agent_y) ** 2)) ** 0.5
                            angle = angle_agent_food(agent, find_x, find_y)
                            break
                    except Exception:
                        pass                

            #we have the food neural inputs set now, we make our agent take a move
            move_instructions = agent.neuralNetwork.run_network(np.array([distance,angle]))
            #print("Move instructions for the agent: ", move_instructions, "\n")
            #now we have everything ready to make our move, dont forget that we cannot
            #move into a square that is already occupied tho
            #now we have our move instructions,
            #we are going to get predictions like this [[0.5472211  0.45277882]]
            #what we need to do is to use this output to inform our movement

            #if first output is 0 I dont want to move
            turn_left = False
            turn_right = False
            move = 0

            #ASK ABOUT THIS PART, I WANT TO HAVE SOME SORT OF
            #JUSTIFICATION FOR THIS DECISION??
            if move_instructions[0][0] > 0.2:
                move = 1
                #if the second input rounds to zero we want to turn left
                if move_instructions[0][1] <= 0.4:
                    turn_left = True
                elif move_instructions[0][1] >= 0.6:
                    turn_right = True

            #now we can make him move
            #first we need to make him take a turn
            if turn_left:
                agent.facing_direction = fds[(agent.facing_direction - 1)%4]
            elif turn_right:
                agent.facing_direction = fds[(agent.facing_direction + 1)%4]

            #we cant empty the last square because there may be other agents
            #on that square, what we can do is that we can utilize our 
            #delete agent function. and write a move_agent_out_function
            # print('is agent here 2: ', game.field.array[agent.x, agent.y])
            # Chnaged cthis NOTSURE
            #             if(len(game.field.array[game.agents[agent_name].x, game.agents[agent_name].y]) == 1):

            if(len(game.field.array[agent.x, agent.y]) == 1):
                game.field.array[agent.x, agent.y] = None
            else:
                game.move_agent_out(agent_name)

            fd = agent.facing_direction
            #0 is for facing downwards
            if fd == 0 and agent_y < (size-1):
                agent_y = agent_y + move
            #1 is for facing left
            elif fd == 1 and agent_x > 0:
                agent_x = agent_x - move
            #2 is for facing upwards
            elif fd == 2 and agent_y > 0:
                agent_y = agent_y - move
            #3 is for facing right
            elif fd == 3 and agent_x < (size-1):
                agent_x = agent_x + move
            
            
            #before putting him in the new coordinates I want to check if there was
            #a food in that same location
            if isinstance(game.field.array[agent_x, agent_y], Food):
                food = game.field.array[agent_x, agent_y]
                #if so, I want to add energy to my agent
                agent.energy += food.energy
                #I want to delete the food item by giving its coordinates
                game.delete_food(agent_x, agent_y)
                #commented below line out as we shouldnt do that: NOTSURE
                #game.field.array[agent_x, agent_y] = [agent]
            
            if game.field.array[agent_x, agent_y] is None:
                game.field.array[agent_x, agent_y] = [agent]
            else:            
                #if there is already an agent
                game.field.array[agent_x, agent_y] = np.append(game.field.array[agent_x, agent_y], agent)

            
            #put him on the field
            #and finally finalize my movement of the agent
            #update agent's coordinates
            agent.x = agent_x
            agent.y = agent_y
            
            #print("we move the agent here: ({},{})".format(agent.x, agent.y))
            #game.field.array[agent.x, agent.y] = agent
        
            #5- any offsprings created this cycle
            if agent.age%reproductionYear == 0:
                #print("This is the agents reproduction year!")
                #half of agent's energy
                half_energy = agent.energy/2
                agent.energy = half_energy
                #create offspring
                offspring = Agent(half_energy)
                offspring.neuralNetwork = agent.neuralNetwork


                #put him on the field in the same square as the parent
                offspring.x =  agent.x
                # if offspring_x >= (size-1): offspring_x = (size-1)
                # if offspring_x <= 0: offspring_x = 0
                offspring.y =  agent.y
                # if offspring_y >= (size-1): offspring_y = (size-1)
                # if offspring_y <= 0: offspring_y = 0

                 
                
                # There wouldnt be food because he is being born to the same square with his parent
                
                # if isinstance(game.field.array[offspring_x, offspring_y], Food):
                #     food = game.field.array[offspring_x, offspring_y]
                #     #if so, I want to add energy to my agent
                #     offspring.energy += food.energy
                #     #I want to delete the food item
                #     game.delete_food(offspring_x, offspring_y)
                #     game.field.array[offspring_x, offspring_y] = [offspring]


                # elif game.field.array[offspring_x, offspring_y] is None:
                #     #it goes in here, the problem isnt this?
                #     game.field.array[offspring_x, offspring_y] = [offspring]
                # else:
                    #if there is already an agent
                game.field.array[offspring.x, offspring.y] = np.append(game.field.array[offspring.x, offspring.y], offspring)
                
               
                #give a random facing direction
                offspring.facing_direction = random.choice(fds)
                offspring.neuralNetwork.genetic_mutation()

                #put offspring on the field
                #game.field.array[offspring.x, offspring.y] = offspring
                #put him in the dictionary
                #but the dictionary cannot change size during the loop
                #so put every offspring in the offspring dictionary and
                #when the cycle changes add them to the agents dictionary
                given_name = "agent{0}".format(offspringName)
                offspring.name = given_name
                offspring_dict[given_name] = offspring
                #increment the offspring name
                offspringName += 1
    #one last time after the for loop is over
    agents.update(offspring_dict)
    #print("agent_num: ", len(agents))
    offspring_dict = {}
    #delete the agents
    for agent in deleted_agents:
        game.delete_agent(agent)

    deleted_agents = []
    fr.write_line(str(len(agents)))
    fr.close_file()