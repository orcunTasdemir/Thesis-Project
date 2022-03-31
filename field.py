import numpy as np


class Field:

    
    size : int = 100
    array : np.ndarray = np.full((size, size), None)

    def __init__(self, size = size, array = array):
        self.size = size
        self.array = array
