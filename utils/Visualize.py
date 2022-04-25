from textwrap import wrap
from utils.Field import Field
from utils.Game import *
import numpy as np
from utils.Agent import Agent
from utils.Food import Food
from matplotlib import colors, pyplot
import os
import json
import re

# library for the visualization purposes


def visualizeGame(game: Game, cycles: int, file_num: int):
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

    # visualise, we need a matrix with float elements.
    floatMatrix = np.full((size, size), 0.0)

    # change float values in population according to whether
    # the coordinate is unpopulated, an agent, or a food
    for i in range(0, size):
        for j in range(0, size):
            if field.array[i][j] is None:  # empty
                pass
            elif isinstance(field.array[i][j], Food):  # if food
                floatMatrix[j][i] = 2.0  # 2.0 means food
            else:
                floatMatrix[j][i] = 1.0  # 1.0 means agent

    # using colors from matplotlib, define a color map
    colormap = colors.ListedColormap(["lightgrey", "blue", "green"])
    # define figure size using pyplot
    pyplot.figure(figsize=(8, 8))
    # using pyplot add a title
    pyplot.title("Population of " + game.game_type + " Game with " + game.environment_type + " environment over " + str(cycles) + " cycles.",
                 fontsize=24, wrap=True, pad=10)
    # using pyplot add x and y labels
    pyplot.xlabel("Agents: Blue / Food: Green", fontsize=20)
    # pyplot.ylabel("y coordinates", fontsize = 20)
    # adjust x and y axis ticks, using pyplot
    pyplot.xticks(fontsize=16)
    pyplot.yticks(fontsize=16)
    pyplot.legend(loc='upper left', frameon=False)
    # use .imshow() method from pyplot to visualize agent locations
    pyplot.imshow(X=floatMatrix,
                  cmap=colormap)
    os.chdir('/Users/orcuntasdemir/Desktop/vassar/thesis/code')
    name = "games/gameFig_" + str(file_num) + ".png"
    pyplot.savefig(name)
    # pyplot.show()
    return True


def visualizePopulation(output_file, smooth: bool = True):
    folder = os.path.abspath(os.path.join(output_file, os.pardir))
    file_num = output_file[-7:-3]
    pop_list = []
    cycle_list = []
    f = open(output_file)
    data = json.load(f)
    cycle_num = data["header"]["totalCycles"]
    for key in data:
        if key == "header":
            print("true")
            continue
        if smooth:
            if key == "0" or re.match("^[1-9]+[0-9]*000$", key):
                print(key)
                pop_list.append(data[key]['pop'])
                cycle_list.append(data[key]['cycle'])
        else:
            print(key)
            pop_list.append(data[key]['pop'])
            cycle_list.append(data[key]['cycle'])

    # define figure size using pyplot
    pyplot.figure(figsize=(8, 8))
    # using pyplot add a title
    pyplot.title(f"Population of {data['header']['gameType']} community with {data['header']['gameEnvironment']} environment over {data['header']['totalCycles']} cycles.",
                 fontsize=24, wrap=True, pad=10)
    # using pyplot add x and y labels
    pyplot.xlabel("Honest Replication Attempt capped at 2000", fontsize=16)
    # pyplot.ylabel("Population", fontsize = 20)
    # adjust x and y axis ticks, using pyplot
    pyplot.xticks(fontsize=12)
    pyplot.xticks(np.arange(min(cycle_list), max(cycle_list)+1, 10))
    pyplot.yticks(fontsize=12)
    # use .imshow() method from pyplot to visualize agent locations
    pyplot.plot(cycle_list, pop_list)
    pyplot.ylim([0, 2500])
    strr = f"{folder}/populationFig_{str(file_num)}.png"
    ax=pyplot.axes()

    ax.set_facecolor('white')
    # print(str)
    pyplot.savefig(strr)
    pyplot.close()
    # pyplot.show()
