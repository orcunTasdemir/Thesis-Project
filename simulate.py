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


def spiral_update(iteration):
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


def angle_agent_food(agent : Agent, food : Food):
    agent_x = agent.x
    agent_y = agent.y
    food_x = food.x
    food_y = food.y
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

def simulate(game : Game, cycles = 20000):
    """[summary]

    Args:
        game (Game): Game passed to the simulation
        cycles (int, optional): Number of cycles for the simulation to run.
        Defaults to 20000.
    """
    #offspring dictionary because we cannot change the size of the agent
    #dictionary while we are looping through it 


    #To add the SSS functionality I need to take into account a couple of things,
    #Frist, for every cycle
    #new file writer, starts from
    fr = fileWriter('output', 'output_', '.out', 0)
    fr.open_file()

    #output_file =  open("output.txt", "w")
    agents = game.agents
    offspring_dict = Dict[str, Agent]
    offspring_dict = {}
    output_bin = []
    offspringNames = int(game.num_of_first_generation + 1)

    deleted_agents = []

    for cycle in range(0, cycles):
        print("cycle number: ", cycle)
        agents.update(offspring_dict)
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
        fr.write_line(str(len(agents)))

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
            #print("new set of food is added at the beginning of the year.\n")
        
        for agent_name in agents:

            #print("loop for {}: \n".format(agent_name))

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
                

            ########################################################################################
            #4- check if the agent and a food item are going to be on the same square after one move

            #find the closest food to the agent
            #for each food item in the foodArray calculate the euclidian distance to the agent
            #print("agent is here: ({},{})".format(agent.x, agent.y))
            agent_x = agent.x
            agent_y = agent.y
            agent_facing = agent.facing_direction
            distance_array = []

            #initiated as a random food
            distance = -1
            angle = -1
            food_not_found = True
            i = 1
            #USE scipy.spatial.KDTree TO SPEED THIS UP IF NECESSARY
            while food_not_found == True:
                spiral_updates = spiral_update(i)
                for update in spiral_updates:
                    find_x = agent_x + update[0]
                    find_y = agent_y + update[1]
                    if find_x >= 99:
                        find_x = 99
                    if find_y >= 99:
                        find_y = 99
                    if find_x <= 0:
                        find_x = 0
                    if find_y <= 0:
                        find_y = 0

                    if isinstance(game.field.array[find_x][find_y], Food):
                        food = game.field.array[find_x][find_y]
                        #find euclidian distance from every food
                        euclidian_distance = (((food.x - agent_x) ** 2) + ((food.y - agent_y) ** 2)) ** 0.5
                        angle = angle_agent_food(agent, food)
                        food_not_found = False
                        break
                #for every iteration we didnt find food, I want to update the spiral search value
                i += 1

            # for food in game.foodArray:
            #     #find euclidian distance from every food
            #     euclidian_distance = (((food.x - agent_x) ** 2) + ((food.y - agent_y) ** 2)) ** 0.5
            #     #if the distance is 1 I can break from the loop which gives me some time efficiency
            #     if euclidian_distance == 1:
            #         distance = euclidian_distance
            #         angle = angle_agent_food(agent, food)
            #         break
            #     distance_array.append(euclidian_distance)
            # #if we didnt break from the for loop ever
            # if distance == -1:
            #     distance = min(distance_array)
            #     angle = angle_agent_food(agent, food)


            #print("distance calculated from food: ", distance, "\n")
            #print("angle calculated from food: ", angle, "\n")

            #we have the food neural inputs set now, we make our agent take a move
            move_instructions = agent.neuralNetwork.model.predict([[distance, angle]])
            #print("Move instructions for the agent: ", move_instructions, "\n")
            #now we have everything ready to make our move, dont forget that we cannot
            #move into a square that is already occupied tho
            #now we have our move instructions,
            #we are going to get predictions like this [[0.5472211  0.45277882]]
            #what we need to do is to use this output to inform our movement

            #THERE CANNOT BE MORE THAN ONE AGENT PER SQUARE SO WHAT DO WE DO?
            #if first output is 0 I dont want to move
            turn_left = False
            turn_right = False
            move = 0

            #ASK ABOUT THIS PART, I WANT TO HAVE SOME SORT OF
            #JUSTIFICATION FOR THIS DECISION
            if move_instructions[0][0] < 0.2:
                move = 0
            else:
                #print("MOVE IS ONE!")
                move = 1
                #if the second input rounds to zero we want to turn left
                if move_instructions[0][1] <= 0.4:
                    turn_left = True
                elif move_instructions[0][1] >= 0.6:
                    turn_right = True

            
            #now we can make him move

            #first we need to make him take a turn
            if turn_left:
                agent.facing_direction = Agent.facing_directions[agent.facing_direction - 1]
            elif turn_right:
                #CHECK HERE
                if agent.facing_direction == 3:
                    agent.facing_direction = 0
                else:
                    agent.facing_direction = Agent.facing_directions[agent.facing_direction + 1]

            #update his coordinates according to where he is facing
            agent_x_new = agent_x
            agent_y_new = agent_y
        
            #0 is for facing downwards
            if agent.facing_direction == 0 and agent_y < 99:
                agent_y_new = agent_y + move
            #1 is for facing left
            elif agent.facing_direction == 1 and agent_x > 0:
                agent_x_new = agent_x - move
            #2 is for facing upwards
            elif agent.facing_direction == 2 and agent_y > 0:
                agent_y_new = agent_y - move
            #3 is for facing right
            elif agent.facing_direction == 3 and agent_x < 99:
                agent_x_new = agent_x + move
            
            #empty the last square
            game.field.array[agent_x, agent_y] = None

            #while the square is already occupied by another agent ...
            while isinstance(game.field.array[agent_x_new, agent_y_new], Agent):

                #if the agent is facing up or down and trying to move up or down
                if agent.facing_direction == 0 or agent.facing_direction == 2:
                    #if we are not on the left or right edges of the field
                    if agent_x_new != 0 and agent_x_new != 99:
                        rand_move = random.choice([-1,1])
                        agent_x_new += rand_move
                    #if we are on the left edge
                    elif agent_x_new ==0:
                        agent_x_new += 1
                    #if we are on the right edge
                    else:
                        agent_x_new -= 1
                if not isinstance(game.field.array[agent_x_new, agent_y_new], Agent):
                    break
                #last resort we change the y value too
                #if the agent is facing left or right and trying to move left or right
                if agent.facing_direction == 1 or agent.facing_direction == 3:
                    #if we are not on the top or bottom edges of the field
                    if agent_y_new != 0 and agent_y_new != 99:
                        rand_move = random.choice([-1,1])
                        agent_y_new += rand_move
                    #if we are on the top edge
                    elif agent_y_new ==0:
                        agent_y_new += 1
                    #if we are on the bottom edge
                    else:
                        agent_y_new -= 1
                
            #before putting him in the new coordinates I want to check if there was
            #a food in that same location
            if isinstance(game.field.array[agent_x_new, agent_y_new], Food):
                food = game.field.array[agent_x_new, agent_y_new]
                #if so, I want to add energy to my agent
                agent.energy += food.energy
                #I want to delete the food item
                game.delete_food(food)

            #and finally finalize my movement of the agent
            #update agent's coordinates
            agent.x = agent_x_new
            agent.y = agent_y_new
            #put him on the field
            #print("we move the agent here: ({},{})".format(agent.x, agent.y))
            game.field.array[agent.x, agent.y] = agent
        
            #5- any offsprings created this cycle
            if agent.age%reproductionYear == 0:
                #print("This is the agents reproduction year!")
                #half of agent's energy
                half_energy = agent.energy/2
                agent.energy = half_energy
                #create offspring
                offspring = Agent(half_energy)


                #put him on the field in a random location around a 4x4 box
                #around its parent
                offspring_x =  agent.x + random.choice((-4,5))
                if offspring_x >= 99: offspring_x = 99
                offspring_y =  agent.y + random.choice((-4,5))
                if offspring_y >= 99: offspring_y = 99

                #while coordinates chosen to place the offspring are
                #not occupied with an agent
                count = 0
                while isinstance(game.field.array[offspring_x, offspring_y], Agent):
                    #print("STUCK first")
                    count += 1
                    if count >= 5:
                        break
                    offspring_x =  agent.x + random.choice((-4,5))
                    if offspring_x >= 99: offspring_x = random.choice((-4,5))
                    offspring_y =  agent.y + random.choice((-4,5))
                    if offspring_y >= 99: offspring_y = random.choice((-4,5))

                    if isinstance(game.field.array[offspring_x, offspring_y], Food):
                        food = game.field.array[offspring_x, offspring_y]
                        #if so, I want to add energy to my agent
                        offspring.energy += food.energy
                        #I want to delete the food item
                        game.delete_food(food)


                while isinstance(game.field.array[offspring_x, offspring_y], Agent):
                    #print("STUCK second")
                    offspring_x = random.choice((0,99))
                    offspring_y = random.choice((0,99))

                    if isinstance(game.field.array[offspring_x, offspring_y], Food):
                        food = game.field.array[offspring_x, offspring_y]
                        #if so, I want to add energy to my agent
                        offspring.energy += food.energy
                        #I want to delete the food item
                        game.delete_food(food)

                
                #set the offspring up completely
                # give his coordinates
                offspring.x = offspring_x
                offspring.y = offspring_y
                #give a random facing direction
                offspring.facing_direction = random.choice(Agent.facing_directions)
                #offspring.neuralNetwork.genetic_mutation()

                #put offspring on the field
                game.field.array[offspring.x, offspring.y] = offspring
                #put him in the dictionary
                #but the dictionary cannot change size during the loop
                #so put every offspring in the offspring dictionary and
                #when the cycle changes add them to the agents dictionary
                offspring_dict["agent{0}".format(offspringNames)] = offspring
                #increment the offspring name
                offspringNames += 1
    #one last time after the for loop is over
    agents.update(offspring_dict)
    print("agent_num: ", len(agents))
    offspring_dict = {}
    #delete the agents
    for agent in deleted_agents:
        game.delete_agent(agent)

    deleted_agents = []
    fr.write_line(str(len(agents)))
    fr.close_file()