import numpy as np

class Field:
    #init method is the constructor for the agent
    def __init__(self, size : int = 100):
        self.size = size
        self.array = np.full((size,size), None)
        self.food = None #as we put food to the field we will add

field = Field( )

print(field.food)