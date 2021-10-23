

class Food:
    #init method is the constructor for the food
    def __init__(self, energy  : int = 50):
        """Food constructor

        Args:
            energy (int, optional): Energy the food provides. Defaults to 50.
        """
        self.energy = energy #energy the food provides
        self.x = None #the x coordinate for the agent
        self.y = None #the y coordinate for the agent

