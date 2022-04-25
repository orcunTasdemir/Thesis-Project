import numpy as np

class Field:
    """Field Class
    """
    size : int = 100
    array : np.ndarray = None

    def __init__(self, size : int = size):
        """Constructor for the Field class

        Args:
            size (int, optional): Size of the field. Defaults to size.
            array (np.ndarray, optional): Numpy array that holds the objects on the field. Defaults to np.full((size, size), None).
        """
        self.size = size
        self.array = np.full((size, size), None)
