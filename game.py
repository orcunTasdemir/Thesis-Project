##########################################################

from typing import Dict, List

from agent import Agent
from field import Field
from food import Food
import random

#game class takes a field, an array of food positions,
# and a dictionary of agents to initialize

class Game:
    def __init__(self):

        self.field = Field
        self.foodArray = []
        self.agents = dict()

    ##########################################################

    #environment conditions
    environment = { "Temperate_fill" : 80,
                    "Temperate" : 50,
                    "Harsh": 20                       
                            };

    #########################################################
    def initField(self, field_size : int):
        """initializes a field

        Args:
            field_size (int): size of the field
        """
        Game.field = Field(field_size)
        print("A field of size {} was created.".format(field_size))

    ##########################################################
    def initAgents(self, num_of_agents : int) -> dict:
        """initializes the agents dictionary
        
        Args:
            num_of_Agents (int): Number of agents to create

        Returns:
            dict: a dictionary of agents named "agentX"
            for the number they are assigned at birth
        """
        for i in range(1,num_of_agents+1):
            Game.agents["agent{0}".format(i)] = Agent()

        print("The first batch of {} agents were created.".format(num_of_agents))


    ##########################################################
    def populate(self):
        """This method populates the given field with
        the given number of agents, placement is random.

        Args:
            field (Field): field to be used
            agent_dict (dict): a dictionary of agents
        """
        #size = field.size

        #putting the agents in
        for i in range(1, len(Game.agent_dict)):   
            while True:  
                #random x coordinate for agent
                x = random.choice(range(0,Game.field.size))
                #random y coordinate for agent
                y = random.choice(range(0,Game.field.size))

                if Game.field.array[x,y] == None: #if the spot is empty
                    Game.field.array[x,y] = Game.agent_dict["agent{0}".format(i)]
                    break
        print("The field was populated by {} agents in random.".format(len(Game.agent_dict)))
    ##########################################################


    def putFood(self, environment_circ : str = "Temperate"):
        """Puts food on the field

        Args:
            field (Field): the field
            environment_circ (str, optional): a dictionary key
            for the environmental circumstance chosen.
            Defaults to "Temperate". Defaults to "Temperate".
        """
    
        #number of food is percentage of food times =
        # the area of the field
        size = Game.field.size

        nu = (Game.environment[environment_circ]/100)*size*size
        num_of_food = int((Game.environment[environment_circ]/100)*size*size)
        print(nu)
        print(num_of_food)
        for i in range(0, num_of_food):
            while True:  
                #random x coordinate for food
                x = random.choice(range(0,size))
                #random y coordinate for food
                y = random.choice(range(0,size))

                if Game.field.array[x,y] == None: #if the spot is empty
                    #create food
                    food = Food()
                    Game.field.array[x,y] = food
                    #put coordinates of the food in the food array
                    Game.foodArray.append([x,y])
                    break
        print("{} food items were placed in the field at random.".format(num_of_food))
        #stroing coordinates for every food created on here