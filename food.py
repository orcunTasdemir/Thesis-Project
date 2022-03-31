
#This is how we create food

class Food:

    energy = 50.0
    x = None
    y = None
    
    #init method is the constructor for the food
    def __init__(self, energy  : float = energy, x : int = x, y : int = y):
        """Food

        Args:
            energy (float, optional): _description_. Defaults to energy.
        """
        
        self.energy = energy
        self.x = x
        self.y = y