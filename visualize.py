from field import Field
from game import *
import numpy as np
from agent import Agent
from food import Food
from matplotlib import colors, pyplot

#library for the visualization purposes
def visualize(game: Game):
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
            if field.array[i,j] == None: # empty
                pass # leave 0.0 in population cell
            elif isinstance(field.array[i,j], Agent): #if agent
                floatMatrix[i][j] = 1.0 # 1.0 means agent
            elif isinstance(field.array[i,j], Food): #if food
                floatMatrix[i][j] = 2.0 # 2.0 means food


    #using colors from matplotlib, define a color map
    colormap = colors.ListedColormap(["lightgrey","blue","green"])
    # define figure size using pyplot
    pyplot.figure(figsize = (12,12))
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
