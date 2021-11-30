##########################################################

from typing import Dict, List

from agent import Agent
from field import Field
from food import Food
import random
import numpy as np

### THEGAME ###
# This is how we create the game, the game is the object we will run the simulation on

class Game:

    ##########################################################
    #environment conditions
    environment_types = { "init" : 50, #set back to 50
                          "Temperate" : 80,    #from paper                
                          "Harsh" : 30,        #from paper
                          "Super-Harsh" : 5    #I made it up    
                            };

    #ISS or SSS for individual survival strategy or social survival strategy
    game_types = {"ISS", "SSS"}
    #the default number of agents to be created in the first generation                         
    num_of_first_generation = 1
                            
    ##########################################################
    def __init__(self,
                 #we take a field, the default value is a default field
                 field : Field = Field(),
                 #we also take an agent dictionary which by default is a 
                 agents : dict = {},
                 #Environment type we are assigning to the game
                 environment_type : str = "Temperate",
                 #game type is set to either ISS or SSS for individual survival strategy or social survival strategy
                 game_type : str = "ISS"):
                 
        """
        Game is a object with a field, agents, and food, this is where out simulation runs

        Args:
            field (Field, optional): Field for the game. Defaults to Field().
            agents (dict, optional): Initially empty agent dictionary
            with agents's name and the agent object. Defaults to dict().
            environment_type (str, optional): The environment type name from the dictionary of environment-types
        """

        self.field = field
        self.agents = agents
        self.environment_type = environment_type
    
    ##########################################################
    def __str__(self): #optimized (doesnt matter)
        """
        Print meyhod for the game class objects

        Returns:
            console output: Prints a description of the game
        """

        field_size = self.field.size
        percent_of_food = self.environment_types[self.environment_type]
        environment_type = self.environment_type
        stringy = "Game:\n"
        stringy += f"Field for the game is {self.field.size} by {self.field.size}.\n"
        stringy += f"There are {len(self.agents)} agents on the field.\n"
        stringy += f"The environment-type for the game is {environment_type}.\n"
        stringy += f"{percent_of_food}% of the field is covered in food..\n"

        return stringy

    #########################################################
    def init_field(self, field_size : int): #optimal
        """
        Initializes a field

        Args:
            field_size (int): size of the field
        """

        self.field = Field(field_size)
        #print(f"init_field: The new field of size {field_size} is assigned to the game.\n")

    ##########################################################
    def init_agents(self, num_of_agents : int = num_of_first_generation): #optimal
        """
        Initializes the agents dictionary

        Args:
            num_of_Agents (int): Number of agents to create
        """

        for i in range(1, num_of_agents + 1):
            agent_name = "agent{0}".format(i)
            agent = Agent()
            agent.name = agent_name
            self.agents[agent_name] = agent

        #print(f"init_agents: A number of {num_of_agents} agents were created and put into the agents dictionary.\n")

    ##########################################################
    def populate(self): #optimal
        """
        This method populates the given field with
        the given number of agents, placement is random.
        """
        #putting the agents in
        for i in range(1, len(self.agents)+1):   
            while True:  
                #random x coordinate for agent
                x = random.choice(range(0,self.field.size))
                #random y coordinate for agent
                y = random.choice(range(0,self.field.size))
                
                #if the spot is empty
                if self.field.array[x,y] == None:
                    agent = self.agents["agent{0}".format(i)]
                    #we give him his corrdinates
                    agent.x = x
                    agent.y = y
                    agent.facing_direction = random.choice(Agent.facing_directions) #we choose a random facing direction
                    #put him on the field inside an array (important)
                    self.field.array[x,y] = []
                    self.field.array[x,y].append(agent)
                    break
        #print(f"populate: The field was populated by {len(self.agents)} agents from the agent dictionary at random.\n")
    
    ##########################################################
    def put_food(self, init : bool = False): #optimal
        """
        Puts food on the field

        Args:
            environment_type (str, optional): a dictionary key
            for the environmental circumstance chosen.
            Defaults to "Temperate". Defaults to "Temperate".
        """
        #number of food is percentage of food times =
        # the area of the field
        size = self.field.size
        ar = self.field.array

        #if first put food then I put 50 percent of the cells
        if init:
            num_of_food = int((self.environment_types["init"]/100)*size*size)
        else:
            #print("envtype: ", self.environment_type)
            num_of_food = int((self.environment_types[self.environment_type]/100)*size*size)
        
        for i in range(0, num_of_food):
            while True:  
                #random x coordinate for food
                x = random.choice(range(0,size))
                #random y coordinate for food
                y = random.choice(range(0,size))
                if ar[x,y] is None: #if the spot is empty
                    #create food
                    food = Food()
                    #set food's coordinates
                    food.x = x
                    food.y = y
                    #put food
                    ar[food.x,food.y] = food
                    break
        #print(f"Environment type is {environment_type}, so {num_of_food} food items were placed in the field at random.")

    ##########################################################
    def delete_agent(self, agent_name : str): #optimal
        """
        Once an agent dies in any possible way, we delete him from the game

        Args:
            agent_name (str): Agent to be deleted
        """

        #we need to delete it off the field by deleteing it from the array for the
        #square in the field
        agent_x = self.agents[agent_name].x
        agent_y = self.agents[agent_name].y
        # print('deleted_agent: ', agent_name)
        # print('agent_x: ', agent_x)
        # print('agent_y: ', agent_y)
        square_array = self.field.array[agent_x, agent_y]
        index = 0
        # print('square_array: ', square_array)
        for agent in square_array:
            if agent.name == agent_name:
                self.field.array[self.agents[agent_name].x, self.agents[agent_name].y] = np.delete(square_array, index)
            index += 1

        #we also need to delete him from the dictionary
        self.agents.pop(agent_name, None)

    
    def move_agent_out(self, agent_name : str):
        agent_x = self.agents[agent_name].x
        agent_y = self.agents[agent_name].y

        square_array = self.field.array[agent_x, agent_y]

        #if it is not the only agent on the square, we only want to get rid of him
        index = 0
        # print('square_array: ', square_array)
        for agent in square_array:
            if agent.name == agent_name:
                self.field.array[self.agents[agent_name].x, self.agents[agent_name].y] = np.delete(square_array, index)
            index += 1

            


    ##########################################################
    def delete_all_food(self): #optimized?
        """
        Once a year when we issue new food, the old food from last year is completely wiped
        from the game's field, deletes all the food, method delete_food is for individual deletions
        """
        size = self.field.size
        ar = self.field.array
        #we need to delete the food from the field.array
        for i in range(size):
            for j in range(size):
                if isinstance(ar[i][j], Food):
                    ar[i][j] = None    
    
    ##########################################################
    def delete_food(self, food_x, food_y): #optimal
        """
        Deletes a single food item once it is eaten by an individual

        Args:
            food (Food): Food to be deleted
        """
        #remove from field
        self.field.array[food_x, food_y] = None

    ##########################################################