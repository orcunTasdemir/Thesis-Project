from typing import Dict

from agent import Agent
from field import Field
from food import Food
import random

from game import Game

#every 40 cycles 80 percent of the cells are filled with food again
#energy of every individual is decreased by half a point every cycle
#energy increases by 50 after eating food
#an agent creates one offspring every 50 cycles, the offspring is
#placed randomly close by its parent
#parent gives half their energy to their offspring
#350 cycles is the age limit
#simulation lasts 20.000 cycles

year = 40
lifeSpan = 350
reproductionYear = 50


def simulate(game : Game, cycles = 20000):
    """[summary]

    Args:
        game (Game): Game passed to the simulation
        cycles (int, optional): Number of cycles for the simulation to run.
        Defaults to 20000.
    """

    for cycle in range(0, cycles):
        #every cycle I have many things to take care of
            #1- check every agent to see if they are dead
            #2- decrease everyones energy levels by half
            #3- check if it has been a year, if so add more food
            #4- check if an agent and a food is on the same square, if so add energy and delete food
            #5- Check if anyone is creating offspring this cycle
        #I can do all this if I loop around every agent once, this way is the most time efficient
        agents = game.agents
        
        for agent in game.agents:
            #2- decrease the energy levels first so if he is dead we will know
            agent.energy = agent.energy - 0.5

            #1- he is dead
            if agent.energy == 0:
                #if he is dead, we remove him from the dictionary
                agents.pop(agent, None)

            #3- if it has been a year add food
            if cycle%year == 0:
                #we delete every food from the last year(stale)
                #and introduce more food
                for food in game.f

            
            




