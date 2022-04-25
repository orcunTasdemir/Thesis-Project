
class Food:
    """The Food Class
    """

    energy : float = 32.0
    x : int = None
    y : int = None

    def __init__(self, energy: float = energy, x: int = x, y: int = y):
        """Constructor for the Food object
        Args:
            energy (float, optional): The energy the food provides. Defaults to energy.
            x (int, optional): The x coordinate of the food. Defaults to x.
            y (int, optional): The y coordinate of the food. Defaults to y.
        """

        self.energy = energy
        self.x = x
        self.y = y
