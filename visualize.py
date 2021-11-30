from field import Field
from game import *
import numpy as np
from agent import Agent
from food import Food
from matplotlib import colors, pyplot


def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]   

#library for the visualization purposes
def visualizeGame(game: Game):
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
    pyplot.title("First generation (blue = Agents, green = food)",
                fontsize = 24)
    # using pyplot add x and y labels
    pyplot.xlabel("x coordinates", fontsize = 20)
    pyplot.ylabel("y coordinates", fontsize = 20)
    # adjust x and y axis ticks, using pyplot
    pyplot.xticks(fontsize = 16)
    pyplot.yticks(fontsize = 16)
    # use .imshow() method from pyplot to visualize agent locations
    pyplot.imshow(X = floatMatrix,
                cmap = colormap)
    pyplot.show()

    return True

def visualizePopulation(output_file):
    population = read_integers(output_file)
    # define figure size using pyplot
    pyplot.figure(figsize = (8,8))
    # using pyplot add a title
    pyplot.title("Population over cycles",
                fontsize = 24)
    # using pyplot add x and y labels
    pyplot.xlabel("cycles", fontsize = 20)
    pyplot.ylabel("Population", fontsize = 20)
    # adjust x and y axis ticks, using pyplot
    pyplot.xticks(fontsize = 16)
    pyplot.yticks(fontsize = 16)
    # use .imshow() method from pyplot to visualize agent locations
    pyplot.plot(population)
    pyplot.show()