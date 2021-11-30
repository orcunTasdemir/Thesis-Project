import numpy as np

#this is how we create a field


class Field():
    #init method is the constructor for the agent
    def __init__(self, size : int = 100):
        self.size = size #the size of the field to be created
        self.array = np.full((size,size), None) #the array that represents each point on the field
        #self.food = None #as we put food to the field we will add
