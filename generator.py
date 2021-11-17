import random
import math
import statistics

width = 33
step_size = width - 1
distance = int(step_size / 2)
levelMatrix = [[0 for x in range(width)] for y in range(width)] 

rangeOfValue = 16

def generateInitBiome(mt):
    mt[0][0] = random.randint(0,rangeOfValue)
    mt[0][width-1] = random.randint(0,rangeOfValue)
    mt[width-1][0] = random.randint(0,rangeOfValue)
    mt[width-1][width-1] = random.randint(0,rangeOfValue)

def diamondSquare(mt):
    global step_size
    global rangeOfValue
    global distance
    while step_size > 1:
        for i in range(width):
            for j in range(width):
                r = random.randint(0,rangeOfValue)    
                if i % distance == 0 and j % distance == 0 and i > 0 and j > 0 and i < width - 1 and j < width -1:
                    mt[i][j] = round((mt[i-distance][j+distance] + mt[i+distance][j+distance] + mt[i-distance][j-distance] + mt[i+distance][j-distance])/4 + r)
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
                                                except:
                                                    pass
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



        




generateInitBiome(levelMatrix)

diamondSquare(levelMatrix)
print('\n'.join([''.join(['{:5}'.format(item) for item in row]) 
      for row in levelMatrix]))