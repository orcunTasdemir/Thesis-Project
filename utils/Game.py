####################################################################################################################
from typing import Dict, List
from utils.Agent import Agent
from utils.Field import Field
from utils.Food import Food
from utils.tools import *
import random
import numpy as np
####################################################################################################################


class Game:
    """Game class
    Returns:
        str: Returns a string synopsis with information about the game.
    """
####################################################################################################################
    CYCLES = 20000
    foodYear = 40
    default_field_size = 100
    game_types = {"ISS", "SSS"}
    num_of_first_gen = 50
    central_storage = 0.0
    environment_types = {
                         "Temperate": 5.0,
                         "Harsh": 2.5,
                         "Test": 25.0
                         }
    popLimit = 2000
    numFood = environment_types["Temperate"] * 100
    cycles = 20000
    overrideReproductionSpan = True
    cost = 0.5
    give_from_storage : float = 2.0
    sample_size : int = 10
    give : float = 0.25
    keep : float = 0.75
    bias : float = 0.5
####################################################################################################################

    def __init__(self,
                 give = give,
                 keep = keep,
                 agents: dict = {},
                 environment_type: str = "Temperate",
                 game_type: str = "ISS",
                 food_energy: float = Food.energy,
                 agent_energy: float = Agent.energy,
                 num_of_first_gen: int = num_of_first_gen,
                 central_storage: float = 0,
                 overrideReproductionSpan: bool = True,
                 popLimit: int = popLimit,
                 cost: float = cost,
                 foodYear: int = foodYear,
                 numFood : int = numFood,
                 give_from_storage = give_from_storage,
                 sample_size = sample_size):
        """Constructor for the Game object.
           The constructor takes an empty dictionary that holds the agents.
           The environment type either Temperate, Harsh, or Super-Harsh
           Game type which is either ISS or CSS
           Food energy for the energy output of the food
           Agent energy for how much energy the agent starts out with
           Number of agents in the first generation of the game
           The number of energy collected in the Central Storage
        """
        self.give = give
        self.keep = keep
        self.field = Field()
        self.numFood = numFood
        self.central_storage = 0
        self.agents = {}
        self.environment_type = environment_type
        self.game_type = game_type
        self.food_energy = food_energy
        self.agent_energy = agent_energy
        self.num_of_first_gen = num_of_first_gen
        self.overrideReproductionSpan = overrideReproductionSpan
        self.popLimit = popLimit
        self.cost = cost
        self.foodYear = foodYear
        self.give_from_storage = give_from_storage
        self.sample_size = sample_size
####################################################################################################################
    def __str__(self):  # optimized (doesnt matter)
        """
        Print method for the game class objects
        Returns:
            console output: Prints a description of the game
        """
        percent_of_food = self.environment_types[self.environment_type]
        environment_type = self.environment_type
        stringy = "Game:\n"
        stringy += f"Field for the game is {self.field.size} by {self.field.size}.\n"
        stringy += f"The number of first generation was {self.num_of_first_gen}.\n"
        stringy += f"There are currently {len(self.agents)} agents on the field.\n"
        stringy += f"There game type is {self.game_type}.\n"
        if(self.game_type == "SSS"):
            stringy += f"The central storage currently has {self.central_storage} amount of energy in it.\n"
        stringy += f"The environment-type for the game is {environment_type}.\n"
        stringy += f"{percent_of_food}% of the field is covered in food.\n"
        stringy += f"The agent starting energy is {self.agent_energy},\nand the food starting energy is {self.food_energy}.\n"
        return stringy
####################################################################################################################

    def init_agents(self):  # optimal
        """Initializes the agents dictionary
        Args:
            num_of_first_gen (int, optional): Number of first generation. Defaults to num_of_first_gen.
        """
        for i in range(1, self.num_of_first_gen + 1):
            # print("num_of _first_gen: ", self.num_of_first_gen)
            agent_name = "agent{0}".format(i)
            agent = Agent(energy=self.agent_energy)
            agent.name = agent_name
            self.agents[agent_name] = agent
####################################################################################################################

    def populate(self):  # optimal
        """
        This method populates the given field with
        the given number of agents, placement is random.
        """
        rangee = len(self.agents)+1
        # print("range: ", rangee )
        field_size = self.field.size

        for i in range(1, rangee):
            while True:
                x = random.choice(range(0, field_size))
                y = random.choice(range(0, field_size))

                if self.field.array[x, y] == None:
                    agent = self.agents["agent{0}".format(i)]
                    agent.x = x
                    agent.y = y
                    agent.facing_direction = random.choice(
                        Agent.facing_directions)
                    self.field.array[x, y] = agent
                    break
                
    def populate_for_competition(self):  # optimal
        """
        This method populates the given field with iss and sss agents in random.
        """
        rangee = len(self.agents)+1
        # print("range: ", rangee )
        field_size = self.field.size

        for agent_name in self.agents:
            agent = self.agents[agent_name]
            while True:
                x = random.choice(range(0, field_size))
                y = random.choice(range(0, field_size))

                if self.field.array[x, y] == None:
                    agent.x = x
                    agent.y = y
                    agent.facing_direction = random.choice(
                        Agent.facing_directions)
                    self.field.array[x, y] = agent
                    break
####################################################################################################################      
    def put_one_agent(self):
        for agent_name in self.agents:
            agent = self.agents[agent_name]
            x = random.choice(range(0, self.field.size))
            y = random.choice(range(0, self.field.size))
            if self.field.array[x, y] == None:
                        agent.x = x
                        agent.y = y
                        agent.facing_direction = random.choice(
                            Agent.facing_directions)
                        self.field.array[x, y] = agent
                        break
        
####################################################################################################################

    def put_food(self, init: bool = False, challenge : bool = False):  # optimal
        """Puts food on the field at the start of every year
        Args:
            init (bool, optional): If init is True, we only put food on 50 percent of the field and if false we put food according to the environment_type parameter. Defaults to False.
        """
        size = self.field.size
        
        #If challenge, I want the initial food deployment to be the same
        if(challenge):
            num_of_food = int(((self.environment_types[self.environment_type])/100)*size*size)
            
        #Otherwise I want the first year to have 5/8 food items compared to the regular environment
        elif init:
            num_of_food = int(((self.environment_types[self.environment_type]*5/8)/100)*size*size)
        else:
            num_of_food = int(
                (self.environment_types[self.environment_type]/100)*size*size)

        for i in range(0, num_of_food):
            while True:
                x = random.choice(range(0, size))
                y = random.choice(range(0, size))
                if self.field.array[x, y] is None:
                    food = Food(energy=self.food_energy)
                    food.x = x
                    food.y = y
                    self.field.array[food.x, food.y] = food
                    break
####################################################################################################################

    def delete_agent(self, agent: Agent):  # optimal
        """
        Once an agent dies in any possible way, we delete him from the game
        Args:
            agent_name (str): Name of the agent to be deleted
        """
        self.field.array[self.agents[agent.name].x,
                         self.agents[agent.name].y] = None
        self.agents.pop(agent.name, None)
####################################################################################################################

    def move_agent_out(self, agent: Agent):
        """When the agent moves on another square, we need to remove him from the square he as already on.
        Args:
            x (int): The coordinate the remove from
            y (int): The coordinate to remove from
        """
        self.field.array[self.agents[agent.name].x,
                         self.agents[agent.name].y] = None
####################################################################################################################

    def delete_all_food(self):  # optimized?
        """
        Once a year when we issue new food, the old food from last year is completely wiped
        from the game's field, deletes all the food, method delete_food is for individual deletions
        """
        size = self.field.size
        for i in range(size):
            for j in range(size):
                if isinstance(self.field.array[i][j], Food):
                    self.field.array[i][j] = None
####################################################################################################################

    def delete_food(self, food_x, food_y):  # optimal
        """Deletes a single food item once it is eaten by an individual
        Args:
            food_x (int): The coordinate the remove from
            food_y (int): The coordinate the remove from
        """
        # remove from field
        self.field.array[food_x, food_y] = None
####################################################################################################################

    def getNumOfFood(self):
        n = 0
        for x in range(self.field.size):
            for y in range(self.field.size):
                if isinstance(self.field.array[x, y], Food):
                    n += 1
        return n

####################################################################################################################
    def isFoodLeft(self):
        for x in range(self.field.size):
            for y in range(self.field.size):
                if isinstance(self.field.array[x, y], Food):
                    return False
####################################################################################################################

    def getAverageSocialGene(self):
        numAgents = len(self.agents)
        total = 0
        for agent_name in self.agents:
            total += self.agents[agent_name].social_gene
        if total == 0:
            return 0
        return total/numAgents
####################################################################################################################

    def getAverageAge(self):
        numAgents = len(self.agents)
        total = 0
        for agent_name in self.agents:
            total += self.agents[agent_name].age
        if total == 0:
            return 0
        return total/numAgents
####################################################################################################################

    def getAverageEnergy(self):
        numAgents = len(self.agents)
        total = 0
        for agent_name in self.agents:
            total += self.agents[agent_name].energy
        if total == 0:
            return 0
        return total/numAgents
####################################################################################################################

    def getOthersInPerimeter(self, agent: Agent):
        perimeter = agent.perimeter
        impact_area = spiral_impact(perimeter)
        total = 0
        for square in impact_area:
            if(isinstance(square, Agent)):
                total += 1
        if total == 0:
            return 0
        return total
####################################################################################################################

    def getDistanceAndAngle(self, agent: Agent):
        agent_x = agent.x
        agent_y = agent.y
        distance = 0.0
        angle = 0.0
        food_not_found = True
        i = 0
        i_max = 10
        arr = self.field.array
        while food_not_found == True:
            if i > i_max:
                distance = mapRange(4.24, 0.0, 14.14, 0.0, 1.0)
                angle = agent.angle_agent_food(agent_x + 3, agent_y + 3)
                break
            i += 1
            spiral_updates = spiral_update(i)
            random.shuffle(spiral_updates)
            for update in spiral_updates:
                find_x = agent_x + update[0]
                find_y = agent_y + update[1]
                if(find_x < 100 and find_y < 100):
                    try:
                        if isinstance(arr[find_x][find_y], Food):
                            food_not_found = False
                            distance = mapRange((
                                (((find_x - agent_x) ** 2) +
                                ((find_y - agent_y) ** 2)) ** 0.5), 0.0, 14.14, 0.0, 1.0)
                            angle = agent.angle_agent_food(find_x, find_y)
                            # print(angle)
                            break
                    except Exception:
                        pass
        return distance, angle
####################################################################################################################    
    def reintroduceFood(self):
        alreadyThere = 0
        size = self.field.size
        for x in range(size):
            for y in range(size):
                if(isinstance(self.field.array[x,y], Food)):
                    alreadyThere += 1
        num_of_food = int((self.environment_types[self.environment_type]/100)*size*size)
        num_of_food = num_of_food - alreadyThere
        for i in range(0, num_of_food):
            while True:
                x = random.choice(range(0, size))
                y = random.choice(range(0, size))
                if self.field.array[x, y] is None:
                    food = Food(energy=self.food_energy)
                    food.x = x
                    food.y = y
                    self.field.array[food.x, food.y] = food
                    break
                
    def getDistance(self, agent: Agent, other_x, other_y):
        agent_x = agent.x
        agent_y = agent.y
        distance = mapRange(((((other_x - agent_x) ** 2) + ((other_y - agent_y) ** 2)) ** 0.5), 0.0, (2*(agent.perimeter**2))**(0.5), 0.0, 1.0)   
        return distance