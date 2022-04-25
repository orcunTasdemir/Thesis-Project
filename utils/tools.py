import math
from math import pi
import json
from itertools import product


def write_json_to_folder(results: dict, folder_name, file_name):
    jsonn = json.dumps(results)
    with open(f"data/{folder_name}/output_{file_name}.js", "w+") as f:
        f.write(jsonn)
    return 0


def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]


def spiral_impact(impact_size):
    return [p for p in product([x for x in range(-impact_size, impact_size + 1)], repeat=2)]


def spiral_update(iteration: int = 1):
    """Widens a search perimeter when the agent looks for food, is also used to calculate the array of coordinates for which the agents have a range of impact for others and to be impacted by others.
    Args:
        iteration (int): Nunmber dictates the level of search. Level 1 is squares around the main square and the level 2 would be the squares around the level 1 squares and so on. Defaults to 1.
    Returns:
        list: List of the coordinates of the squares that are the next search range for food.
    """
    return list(set(spiral_impact(iteration)).difference(set(spiral_impact(iteration-1))))

def mapRange(value : float, inMin : float, inMax : float, outMin : float, outMax : float):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))


def sigmoid5(x : float):
    return 1/(1 + math.exp(-(5 * x)))

def sigmoid_impact(x : float):
    return 1/(1 + math.exp(-(5 * x)))