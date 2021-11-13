import numpy as np
from itertools import permutations

def spiral_update(iteration):
    #for every iteration, I want to widen the perimeter
    #for the base case i = 0, I want only the neighbouring squares to be considered
    num_squares = 8 * iteration
    #squares = np.full([num_square, 2], 0)
    #the only way I could do this is to create a combinations list
    #for all the numbers in the coor list
    coor1 = [x for x in range(-iteration, iteration + 1)]
    #all coordinates for the square
    combinations_object1 = permutations(coor1, 2)
    list1 = list(combinations_object1)
    list1 = list1 + [(x,x) for x in range(-iteration, iteration + 1)]
    #delete (0,0) to be safe because iteration might just be 1
    list1.remove((0,0))
    print("First list: ", list1)
    if iteration > 1:
        #all coordinates for the inner square
        coor2 = [x for x in range(-iteration+1, iteration)]
        combinations_object2 = permutations(coor2, 2)
        list2 = list(combinations_object2)
        list2 = list2 + [(x,x) for x in range(-iteration+1, iteration)]
        print("Second list: ", list2)
        list1 = set(list1) - set(list2)
        print("Resulting list at the end: ", list1)
    return list1

print(spiral_update(2))


#     loop1 = [(0,1), (1,-1), (-1,-0), (-1,-1), (0, -1), (1, -1), (1,0), (1,1)] 

#     -1,-1, 0,-1 , 1,-1, 1,0 ,1,1 , 

#     x = -iteration #for starting x values
#     y = -iteration #for starting y values
#     #for every square in the squares
#     for idx in range(num_square):
#         squares[idx] = [x, y]
#         if x == iteration and y == iteration:

#         if x != iteration: 
#             x += 1
#         else:
#             y += 1 
#     return squares

# print(spiral_update(2))
# x=0
# y=0
# n = np.full([8, 2], 0)
# for index in n:
#         n[1] = x
#         x -= 1
#         y -= 1  