from textwrap import wrap
from Field import Field
from Game import *
import numpy as np
from Agent import Agent
from Food import Food
from matplotlib import colors, pyplot


def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]   

#library for the visualization purposes
def visualizeGame(game: Game, cycles : int, num_agents : int, file_num : int):
    """Takes a field and visualizes
    it with matplotlib

    Args:
        field (Field): field to visualize

    Returns:
        A grid of the entire field with the agents
        and the food color-coded
    """
    field = game.field

    size = field.size

    #visualise, we need a matrix with float elements.
    floatMatrix = np.full((size, size), 0.0)

    #change float values in population according to whether
    #the coordinate is unpopulated, an agent, or a food
    for i in range(0,size):
        for j in range(0,size):
            if field.array[i][j] is None: # empty
                pass
            elif isinstance(field.array[i][j], Food): #if food
                floatMatrix[j][i] = 2.0 # 2.0 means food
            else:               
                floatMatrix[j][i] = 1.0 # 1.0 means agent


    #using colors from matplotlib, define a color map
    colormap = colors.ListedColormap(["lightgrey","blue","green"])
    # define figure size using pyplot
    pyplot.figure(figsize = (8,8))
    # using pyplot add a title
    pyplot.title("Population of " + game.game_type + " Game with " + game.environment_type + " environment over " + str(cycles) + " cycles.", 
                fontsize = 24, wrap = True, pad=10)
    # using pyplot add x and y labels
    pyplot.xlabel("Agents: Blue / Food: Green", fontsize = 20)
    # pyplot.ylabel("y coordinates", fontsize = 20)
    # adjust x and y axis ticks, using pyplot
    pyplot.xticks(fontsize = 16)
    pyplot.yticks(fontsize = 16)
    # use .imshow() method from pyplot to visualize agent locations
    pyplot.imshow(X = floatMatrix,
                cmap = colormap)
    name = "games/gameFig_" + str(file_num) + ".png"
    pyplot.savefig(name)
    #pyplot.show()
    return True

def visualizePopulation(game : Game, cycles : int, num_agents : int, output_file, file_num):
    population = read_integers(output_file)
    # define figure size using pyplot
    pyplot.figure(figsize = (8,8))
    # using pyplot add a title
    pyplot.title("Population of " + game.game_type + " Game with " + game.environment_type + " environment over " + str(cycles) + " cycles.", 
                fontsize = 24, wrap=True, pad=10)
    # using pyplot add x and y labels
    pyplot.xlabel("Agents: Blue / Food: Green", fontsize = 20)
    # pyplot.ylabel("Population", fontsize = 20)
    # adjust x and y axis ticks, using pyplot
    pyplot.xticks(fontsize = 16)
    pyplot.yticks(fontsize = 16)
    # use .imshow() method from pyplot to visualize agent locations
    pyplot.plot(population)
    strr = "games/populationFig_" + str(file_num) + ".png"
    # print(str)
    pyplot.savefig(strr)
    # pyplot.show()
    
# visualizePopulation("output/output_7363.out")