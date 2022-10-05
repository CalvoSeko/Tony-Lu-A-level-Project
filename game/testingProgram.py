import random
from unittest.mock import seal
mat_width = 17
seaLevelMatrix = [[0 for x in range(mat_width)] for y in range(mat_width)] 
def diamondSquare(mt, width, rangeOfValue, distance, step_size):
    
    #mt is the matrix that needs to be modified
    #width is the width of the square matrix
    #rangeOfValue is the intended range of the randomly generated values
    #distance should always be half of step_size
    #step_size helps with checking how many times the procedure has iterated and serves as a stopping point when it equals 1
    
    
    while step_size > 1:
        #this is the diamond step
        for i in range(width):
            for j in range(width):
                r = random.randint(0,rangeOfValue)  
                if i % distance == 0 and j % distance == 0 and i > 0 and j > 0 and i < width - 1 and j < width -1:
                    mt[i][j] = round((mt[i-distance][j+distance] + mt[i+distance][j+distance] + mt[i-distance][j-distance] + mt[i+distance][j-distance])/4 + r)
                #code below lists all possible situations where a value does not have 4 corner values
                else:
                    try:
                        mt[i][j] = round((mt[i+distance][j+distance] + mt[i-distance][j-distance] + mt[i+distance][j-distance])/3 + r)
                    except IndexError:
                        try:
                            mt[i][j] = round((mt[i-distance][j+distance] + mt[i-distance][j-distance] + mt[i+distance][j-distance])/3 + r)
                        except IndexError:
                            try:
                                mt[i][j] = round((mt[i-distance][j+distance] + mt[i+distance][j+distance] + mt[i+distance][j-distance])/3 + r)
                            except IndexError:
                                try:
                                    mt[i][j] = round((mt[i-distance][j+distance] + mt[i+distance][j+distance] + mt[i-distance][j-distance])/3 + r)
                                except IndexError:
                                    try:
                                        mt[i][j] = round((mt[i-distance][j-distance] + mt[i+distance][j-distance])/2 + r)
                                    except IndexError:
                                        try:
                                            mt[i][j] = round((mt[i-distance][j+distance] + mt[i+distance][j+distance])/2 + r)
                                        except IndexError:
                                            try:
                                                mt[i][j] = round((mt[i-distance][j+distance] + mt[i-distance][j-distance])/2 + r)
                                            except IndexError:
                                                try:
                                                    mt[i][j] = round((mt[i+distance][j+distance] + mt[i+distance][j-distance])/2 + r)
                                                except IndexError:
                                                    try:
                                                        mt[i][j] = round((mt[i+distance][j+distance] + r))
                                                    except IndexError:
                                                        try:
                                                            mt[i][j] = round((mt[i+distance][j-distance] + r))
                                                        except IndexError:
                                                            try:
                                                                mt[i][j] = round((mt[i-distance][j+distance] + r))
                                                            except IndexError:
                                                                try:
                                                                    mt[i][j] = round((mt[i-distance][j-distance] + r))
                                                                except IndexError:
                                                                    pass

        #this is the square step
        for i in range(width):
            for j in range(width):
                k = random.randint(0,rangeOfValue)
                try:
                    mt[i][j] = round((mt[i][j+distance]+mt[i][j-distance]+mt[i-distance][j]+mt[i+distance][j])/4 + k)
                except IndexError:
                    try:
                        mt[i][j] = round((mt[i][j-distance]+mt[i-distance][j]+mt[i+distance][j])/3 + k)
                    except IndexError:
                        try:
                            mt[i][j] = round((mt[i][j+distance]+mt[i][j-distance]+mt[i-distance][j]+mt[i+distance][j])/3 + k)
                        except IndexError:
                            try:
                                mt[i][j] = round((mt[i][j+distance]+mt[i][j-distance]+mt[i+distance][j])/3 + k)
                            except IndexError:
                                try:
                                    mt[i][j] = round((mt[i][j+distance]+mt[i][j-distance]+mt[i-distance][j])/3+k)
                                except IndexError:
                                    try:
                                        mt[i][j] = round((mt[i][j+distance]+mt[i+distance][j])/2+k)
                                    except IndexError:
                                        try:
                                            mt[i][j] = round((mt[i][j-distance]+mt[i-distance][j])/2+k)
                                        except IndexError:
                                            try:
                                                mt[i][j] = round((mt[i][j+distance]+mt[i-distance][j])/2+k)
                                            except IndexError:
                                                try:
                                                    mt[i][j] = round((mt[i][j-distance]+mt[i+distance][j])/2+k)
                                                except:
                                                    pass

        step_size = step_size / 2
        distance = int(step_size / 2)

diamondSquare(seaLevelMatrix, 17, 10, 8, 16)
print(seaLevelMatrix)
for x in seaLevelMatrix:  
    for i in x:  
        print(i, end = " ")
    print()  