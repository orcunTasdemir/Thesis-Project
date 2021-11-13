##########################################################

from typing import Dict, List

from agent import Agent
from field import Field
from food import Food
import random

### THEGAME ###
# This is how we create the game, the game is the object we will run the simulation on

class Game:

    ##########################################################
    #environment conditions
    environment_types = { "Temperate_fill" : 80,
                    "Temperate" : 50, #set back to 50
                    "Harsh" : 30,
                    "Super-Harsh" : 10                   
                            };

    #ISS or SSS for individual survival strategy or social survival strategy
    game_types = {"ISS", "SSS"}
    #the default number of agents to be created in the first generation                         
    num_of_first_generation = 1
                            
    ##########################################################
    def __init__(self,
                 #we take a field, the default value is a default field
                 field : Field = Field(),
                 #we also take a food array which is an empty list of food
                 foodArray : list = [],
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
            foodArray (List, optional): Initially empty food list. Defaults to [].
            agents (dict, optional): Initially empty agent dictionary
            with agents's name and the agent object. Defaults to dict().
            environment_type (str, optional): The environment type name from the dictionary of environment-types
        """

        self.field = field
        self.foodArray = foodArray
        self.agents = agents
        self.environment_type = environment_type
    
    ##########################################################
    def __str__(self):
        """
        Print meyhod for the game class objects

        Returns:
            console output: Prints a description of the game
        """

        field_size = self.field.size
        num_of_food = len(self.foodArray)
        percent_of_food = 100 * (num_of_food / (field_size*field_size))
        environment_type = self.environment_type
        stringy = "Game:\n"
        stringy += f"Field for the game is {self.field.size} by {self.field.size}.\n"
        stringy += f"There are {len(self.agents)} agents on the field.\n"
        stringy += f"The number of food available on the field is {len(self.foodArray)}.\nThe {percent_of_food}% of the field is filled with food.\n"
        stringy += f"The environment-type for the game is {environment_type}.\n"

        return stringy

    #########################################################
    def init_field(self, field_size : int):
        """
        Initializes a field

        Args:
            field_size (int): size of the field
        """

        self.field = Field(field_size)
        #print(f"init_field: The new field of size {field_size} is assigned to the game.\n")

    ##########################################################
    def init_agents(self, num_of_agents : int = num_of_first_generation):
        """
        Initializes the agents dictionary

        Args:
            num_of_Agents (int): Number of agents to create
        """

        for i in range(1, num_of_agents + 1):
            self.agents["agent{0}".format(i)] = Agent()

        #print(f"init_agents: A number of {num_of_agents} agents were created and put into the agents dictionary.\n")

    ##########################################################
    def populate(self):
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
                    #put him on the field
                    self.field.array[x,y] = agent
                    break
        #print(f"populate: The field was populated by {len(self.agents)} agents from the agent dictionary at random.\n")
    
    ##########################################################
    def put_food(self):
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
        print("envtype: ", self.environment_type)
        num_of_food = int((self.environment_types[self.environment_type]/100)*size*size)
        
        for i in range(0, num_of_food):
            while True:  
                #random x coordinate for food
                x = random.choice(range(0,size))
                #random y coordinate for food
                y = random.choice(range(0,size))

                if self.field.array[x,y] == None: #if the spot is empty
                    #create food
                    food = Food()
                    #set food's coordinates
                    food.x = x
                    food.y = y
                    #put food
                    self.field.array[food.x,food.y] = food
                    
                    #put food in the food array also so we can 
                    self.foodArray.append(food)
                    break
        #print(f"Environment type is {environment_type}, so {num_of_food} food items were placed in the field at random.")

    ##########################################################
    def delete_agent(self, agent_name : str):
        """
        Once an agent dies in any possible way, we delete him from the game

        Args:
            agent_name (str): Agent to be deleted
        """

        #we need to delete it off the field
        self.field.array[self.agents[agent_name].x, self.agents[agent_name].y] = None
        #we also need to delete him from the dictionary
        self.agents.pop(agent_name, None)

    ##########################################################
    def delete_all_food(self):
        """
        Once a year when we issue new food, the old food from last year is completely wiped
        from the game's field, deletes all the food, method delete_food is for individual deletions
        """
        
        #we need to delete the food from the field.array
        for food in self.foodArray:
            self.field.array[food.x, food.y] = None
        #we also need to delete everything off of the food array
        self.foodArray = []
    
    ##########################################################
    def delete_food(self, food: Food):
        """
        Deletes a single food item once it is eaten by an individual

        Args:
            food (Food): Food to be deleted
        """

        #remove from field
        self.field.array[food.x, food.y] = None
        #remove from the food array
        self.foodArray.remove(food)

    ##########################################################