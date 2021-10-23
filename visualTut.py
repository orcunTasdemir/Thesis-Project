
import random
# import pyplot and colors from matplotlib
from matplotlib import pyplot, colors

#this is how we create an agent, the agent is an abstract datatype
class agent:
    #init method is the constructor for the agent
    def __init__(self, x, y, group):
        self.life = 100 #agents life score
        self.x = x
        self.y = y
        self.group = group

battlefield = [[None for i in range(0,100)] for i in range (0, 100)]

#a function for creating one agent and placing it onto the grid
def agentCreator(size, group, groupList, field, n, m):
    #looping through the entire group
    for j in range (0, size):
        #select random available location
        while True:
            #random x coordinate
            x = random.choice(range(0,n))
            #random y coordinate
            y = random.choice(range(0,m))
            #check if the spot is available, if it isn't we will reiterate
            if field[x][y] == None:
                field[x][y] = agent(x=x,y=y,group=group)
                #append agent object reference to group list
                groupList.append(field[x][y])
                #exit while loop
                break

# list with available x and y locations
locations = battlefield.copy() # using .copy prevents copying by reference
# create empty list for containing agent references in future, type A & B
agents_A = []
agents_B = []
# assigning random spots to agents of group A and B; 
agentCreator(size = 1000,
                group = "A",
                groupList = agents_A,
                field = battlefield,
                n = 100,
                m = 100)
agentCreator(size = 1000,
                group = "B",
                groupList = agents_B,
                field = battlefield,
                n = 100,
                m = 100) 
#.imshow() needs a matrix with float elements;
population = [[0.0 for i in range(0,100)] for i in range(0,100)]
# if agent is of type A, put a 1.0, if of type B, pyt a 2.0
for i in range(1,100):
    for j in range(1,100):
        if battlefield[i][j] == None: # empty
            pass # leave 0.0 in population cell
        elif battlefield[i][j].group == "A": # group A agents
            population[i][j] = 1.0 # 1.0 means "A"
        else: # group B agents
            population[i][j] = 2.0 # 2.0 means "B"

# using colors from matplotlib, define a color map
colormap = colors.ListedColormap(["lightgrey","green","blue"])
# define figure size using pyplot
pyplot.figure(figsize = (12,12))
# using pyplot add a title
pyplot.title("battlefield before simulation run (green = A, blue = B)",
            fontsize = 24)
# using pyplot add x and y labels
pyplot.xlabel("x coordinates", fontsize = 20)
pyplot.ylabel("y coordinates", fontsize = 20)
# adjust x and y axis ticks, using pyplot
pyplot.xticks(fontsize = 16)
pyplot.yticks(fontsize = 16)
# use .imshow() method from pyplot to visualize agent locations
pyplot.imshow(X = population,
             cmap = colormap)
pyplot.show()