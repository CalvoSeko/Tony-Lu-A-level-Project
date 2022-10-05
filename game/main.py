from cmath import sqrt
from re import X
from typing import final
from warnings import warn
from traceback import print_exception
from numpy import False_
import pygame
import generator
import sys, os
import heapq
from datetime  import datetime
import json
from operator import itemgetter

#start off pygame

pygame.init()
pygame.font.init()
#creating a json dump
#incase that there is no previous json dump
ranking = [["null", 0]]

#these two lines in case which record.json is deleted accidentally
#with open(os.path.join("A-level-Project", "game", 'record.json'),"a") as data:
    #json.dump(ranking, data)

with open(os.path.join("A-level-Project", "game", 'record.json')) as data:  
    ranking = json.load(data)


#constants/variables for the visuals
win_width = 1280
win_height = 720
mat_width = 9
normalFont = pygame.font.Font(os.path.join("A-level-Project", "game", 'normalFont.ttf'), 40)
smallFont = pygame.font.Font(os.path.join("A-level-Project", "game", "normalFont.ttf"), 20)
smallerFont = pygame.font.Font(os.path.join("A-level-Project", "game", "normalFont.ttf"), 16)

#diamond-square use these variables
step_size = mat_width - 1
distance = int(step_size / 2)
rangeOfValue = 20
#variables used for the game loop
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
#defining class for a tile that is draw on screen
class gameTile(pygame.sprite.Sprite): 
# Define the constructor for the game tile
    def __init__(self, color, width, x, y, a, b, cost, selected=False): 
        #a is the horizontal index and b is the vertical index
        super().__init__() 
    # Create a sprite and fill it with colour 
        self.image = pygame.Surface([width,width]) 
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
        self.a = a
        self.b = b
        self.cost = cost
        self.selected = selected

    def updateWhenSelected(self):
        
        if self.selected == False:
            self.selected = True
            self.image.fill((245,105,66))
            return "selected"
        else:
            self.selected = False
            self.image.fill(self.color)
            return "deselected"
class displayTile(pygame.sprite.Sprite): 
# Define the constructor for the game tile
    def __init__(self, color, width, x, y, a, b): 
        super().__init__() 
    # Create a sprite and fill it with colour 
        self.image = pygame.Surface([width,width]) 
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
        self.a = a
        self.b = b
    def changeColor(self):
        self.image.fill((245,105,66))

class playerDisplayTIle(displayTile):
    pass

#buttons class

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y , width, height, buttonText="button"):
        super().__init__()
        self.image = pygame.Surface([width,height]) 
        self.color = (188, 156, 240)
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
        self.buttonText = buttonText

        self.fillColors = {
            "normal": "#BC9CF0",
            "hover": "#E066FF",
            "pressed": "#483D8B",
        }

        self.buttonSurf = normalFont.render(buttonText, True, (240,255,255))


    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.image.fill(self.fillColors["normal"])
        if self.rect.collidepoint(mousePos):
            self.image.fill(self.fillColors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.image.fill(self.fillColors["pressed"])




#generate the matrices of the three factors on cost
seaLevelMatrix = [[0 for x in range(mat_width)] for y in range(mat_width)] 
generator.generateInitBiome(seaLevelMatrix, mat_width, 16)
generator.diamondSquare(seaLevelMatrix, mat_width, rangeOfValue, distance, step_size)

soilQuality = [[0 for x in range(mat_width)] for y in range(mat_width)] 
generator.generateInitBiome(soilQuality, mat_width, 16)
generator.diamondSquare(soilQuality, mat_width, rangeOfValue, distance, step_size)

drainage = [[0 for x in range(mat_width)] for y in range(mat_width)] 
generator.generateInitBiome(drainage, mat_width, 16)
generator.diamondSquare(drainage, mat_width, rangeOfValue, distance, step_size)
#starting variables of the square drawn on screen
squareX = 360
squareY = 130
tileWidth = 50


#generating the price matrix for the player and the pathfinding algorithm
def calculateCost(SL, SQ, D):
    cost = round((0.1*(SL**2) + 15*SQ + 20*D)/100)-40
    return cost
#calculate the matrix of cost
priceMatrix = [[0 for x in range(mat_width)] for y in range(mat_width)] 
for i in range(mat_width):
    for j in range(mat_width):
        priceMatrix[i][j] = calculateCost(seaLevelMatrix[i][j], soilQuality[i][j], drainage[i][j])

#printing the matrices
print('\n'.join([''.join(['{:5}'.format(item) for item in row]) 
      for row in seaLevelMatrix]))

print("")

print('\n'.join([''.join(['{:5}'.format(item) for item in row]) 
      for row in soilQuality]))

print("")

print('\n'.join([''.join(['{:5}'.format(item) for item in row]) 
      for row in drainage]))

print("")

print('\n'.join([''.join(['{:5}'.format(item) for item in row]) 
      for row in priceMatrix]))

def checkContinuity(myList):
    inCount = 0
    for item in myList:
        if item == (0, 0) or item == (8, 8):
            pass
        else:
            for adjacentVec in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if ((item[0] + adjacentVec[0]), (item[1] + adjacentVec[1])) in myList:
                    inCount += 1
            if inCount != 2:
                return False
            inCount = 0
    return True

#here starts the pathfinding algorithm
class tile():

    def __init__(self, parent=None, position=None):

        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    #allows assigning and comparison between tiles
    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f
    
    def __gt__(self, other):
        return self.f > other.f

def returnPath(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]


def returnMean(costMatrix):
    sum = 0
    for i in range(len(costMatrix)-1):
        for j in range(len(costMatrix[0])-1):
            sum += costMatrix[i][j]
    mean = sum//(len(costMatrix)*len(costMatrix[0]))
    return mean

def aStar(costMatrix, start, end):
    global totalCost
    #define starting tile and the ending tile with their f, g, h and the mean
    startTile = tile(None, tuple(start))
    startTile.g = costMatrix[start[0]][start[1]]

    endTile = tile(None, tuple(end))
    endTile.g = endTile.h = endTile.f = 0

    startTile.h = 0
    startTile.f = startTile.g + startTile.h

    totalCost = 0
    mean = returnMean(costMatrix)
    #end of defining start and end

    openList = []
    closedList = []
    heapq.heapify(openList) 
    heapq.heappush(openList, startTile)
    #a stopping condition
    count = 0
    maxCount = 2048

    #add startTile to the open list
    openList.append(startTile)
    
    adjacent = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    while len(openList) > 0 and count <= maxCount:
        count += 0

        if count > maxCount:
            warn("stop")
            totalCost = currentTile.g
            print(currentTile.g)
            return returnPath(currentTile)
           


        currentTile = heapq.heappop(openList)
        closedList.append(currentTile)
        if currentTile == endTile:
            totalCost = currentTile.g
            print(currentTile.g)
            return returnPath(currentTile)            



        #define children of the current tile
        children = []

        
        for newPosition in adjacent:

            tilePosition = (currentTile.position[0] + newPosition[0], currentTile.position[1] + newPosition[1])

            if tilePosition[0] > (mat_width - 1) or tilePosition[0] < 0 or tilePosition[1] > (mat_width -1) or tilePosition[1] < 0:
                continue
            
            newTile = tile(currentTile, tuple(tilePosition))

            children.append(newTile)


        for child in children:
            if len([closedChild for closedChild in closedList if closedChild == child]) > 0:
                continue

            child.g = currentTile.g + costMatrix[child.position[1]][child.position[0]]
            child.h = sqrt((child.position[0] - endTile.position[0]) ** 2) + ((child.position[1] - endTile.position[1]) ** 2)*mean
            child.f = child.g + child.h.real

            if len([openTile for openTile in openList if child.position == openTile.position and child.g > openTile.g]) > 0:
                continue
            heapq.heappush(openList, child)
    warn("no solution")
    return None
#end of a star algorithm
#add the game tiles into the sprite groups
localA = 0
localB = 0
#declare the sprite groups
tile_group = pygame.sprite.Group()
all_sprite_group = pygame.sprite.Group()
menu_sprite_group = pygame.sprite.Group()
ranking_sprite_group = pygame.sprite.Group()
instruction_sprite_group = pygame.sprite.Group()
final_sprite_group = pygame.sprite.Group()
final_player_sprite_group = pygame.sprite.Group()

for i in range(mat_width):
        for j in range(mat_width):
            myCost = priceMatrix[i][j]
            color = (256-1*drainage[i][j]), (256-0.75*soilQuality[i][j]), (256-(0.005*(seaLevelMatrix[i][j]**2)))
            myTile = gameTile(color, tileWidth, squareX, squareY, localA, localB, myCost)
            squareX += tileWidth
            tile_group.add(myTile)
            all_sprite_group.add(myTile)
            myCost = 0
            localA += 1
        squareY += tileWidth
        localB += 1
        squareX = 360
        localA = 0

squareX1 = 360
squareY1 = 400
localA1 = 0
localB1 = 0
for i in range(mat_width):
        for j in range(mat_width):
            color = (256-1*drainage[i][j]), (256-0.75*soilQuality[i][j]), (256-(0.005*(seaLevelMatrix[i][j]**2)))
            myTile = displayTile(color, 20, squareX1, squareY1, localA1, localB1)
            squareX1 += 20
            final_sprite_group.add(myTile)
            localA1 += 1
        squareY1 += 20
        localB1 += 1
        squareX1 = 360
        localA1 = 0

squareX2 = 720
squareY2 = 400
localA2 = 0
localB2 = 0
for i in range(mat_width):
        for j in range(mat_width):
            color = (256-1*drainage[i][j]), (256-0.75*soilQuality[i][j]), (256-(0.005*(seaLevelMatrix[i][j]**2)))
            myTile = displayTile(color, 20, squareX2, squareY2, localA2, localB2)
            squareX2 += 20
            final_player_sprite_group.add(myTile)
            localA2 += 1
        squareY2 += 20
        localB2 += 1
        squareX2 = 720
        localA2 = 0

start = (0, 0)
end = (8, 8)
#find the computer solution of the matrix
path = aStar(priceMatrix, start, end)
print(path) 
#[0] is the x coordinate and [1] is the y coordinate



#game loop and visuals

adjacent = [(1,0),(0,1),(-1,0),(0,-1)]


running = True
pathList = []
outTimer = 0
outSCost = 0

def calculateScore(seconds, nowCost, desiredCost):
    if nowCost <= desiredCost:
        return round(1000*(desiredCost/nowCost)-seconds)
    else:
        return round(1000*(desiredCost/nowCost)-2*seconds)

acceptedBool = False
buttons = []
submitButton = Button(840, 400, 300, 60, "Submit")
buttons.append(submitButton)
all_sprite_group.add(submitButton)

#buttons for the starting menu
menu_buttons = []
startGameButton = Button(420, 300, 450, 60, "Start")
menu_sprite_group.add(startGameButton)
menu_buttons.append(startGameButton)
startGame = False

checkRankingButton = Button(420, 400, 450, 60, "Ranking")
menu_sprite_group.add(checkRankingButton)
menu_buttons.append(checkRankingButton)
DisplayRankingList = sorted(ranking, key=itemgetter(1))

DisplayRankingOnMenu = False

InstructionOpenButton = Button(420, 500, 450, 60, "Instructions")
menu_sprite_group.add(InstructionOpenButton)
menu_buttons.append(InstructionOpenButton)
openInstructions = False

#display ranking screen menu buttons
return_button = Button(950, 650, 220, 60, "Return")
ranking_sprite_group.add(return_button)

#Instruction screen menu buttons
returnInstructionButton = Button(950, 650, 220, 60, "Return")
instruction_sprite_group.add(returnInstructionButton)

lineInstruction = ["Here are the instructions on the game:", "After click start, the timer will start. Within the least time possible, ", "attempt to find the least cost path from the top left square to the right bottom square.", "The darker the square, the more coins are needed to build a road on the square.", "Do not attempt to build backwards (to the left or up directions), as the path needs to be 17 tiles long.", "Attempt to create a path with lower price or equal to that of the A star algorithm, ", "which rewards more points.", "Click submit to check your score, the path needs to be 17 tiles long, ", "continuous and contains top left and bottom right tiles.", "Close the window after finishing, the score is saved."]


init = 70
InstructionYCoordinates = []
for i in range(len(lineInstruction)):
    InstructionYCoordinates.append(init)
    init += 60


            


def mainloop():
    listOfTimeDisplayedBig = []
    listOfScoreDisplayedBig = []
    listOfRankingYBig = []

    YRankingBig = 120
    for i in range(1, 10):
        if len(DisplayRankingList) <= i:
            break
        listOfRankingYBig.append(YRankingBig)
        listOfTimeDisplayedBig.append(DisplayRankingList[i][0])
        listOfScoreDisplayedBig.append(DisplayRankingList[i][1])
        YRankingBig = YRankingBig + 50
    startGame = False

    while startGame == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousePos = pygame.mouse.get_pos()
            if startGameButton.rect.collidepoint(mousePos):
                startGame = True
            if checkRankingButton.rect.collidepoint(mousePos):
                DisplayRankingOnMenu = True
                while DisplayRankingOnMenu == True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mousePos = pygame.mouse.get_pos()
                        if return_button.rect.collidepoint(mousePos):
                            DisplayRankingOnMenu = False
                    screen.fill((0,0,0))

                    for i in range(len(listOfTimeDisplayedBig)):
                        screen.blit(normalFont.render(listOfTimeDisplayedBig[i], False, (255,160,230)), (120, listOfRankingYBig[i]))
                        screen.blit(normalFont.render(str(listOfScoreDisplayedBig[i]), False, (255, 240, 250)), (800, listOfRankingYBig[i]))
                    ranking_sprite_group.draw(screen)
                    return_button.process()
                    screen.blit(return_button.buttonSurf, ((return_button.rect.x+25), (return_button.rect.y)))
                    pygame.display.flip()
                    clock.tick(60)
            if InstructionOpenButton.rect.collidepoint(mousePos):
                openInstructions = True

                while openInstructions == True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mousePos = pygame.mouse.get_pos()
                        if returnInstructionButton.rect.collidepoint(mousePos):
                            openInstructions = False
                    screen.fill((0,0,0))
                    screen.blit(returnInstructionButton.buttonSurf, ((return_button.rect.x+25), (return_button.rect.y)))
                    for i in range(len(lineInstruction)):
                        screen.blit(smallFont.render(lineInstruction[i], False, (255, 240, 250)), (30, InstructionYCoordinates[i]))
                    
                    instruction_sprite_group.draw(screen)
                    returnInstructionButton.process()
                    screen.blit(returnInstructionButton.buttonSurf, ((returnInstructionButton.rect.x+25), (returnInstructionButton.rect.y)))
                    pygame.display.flip()
                    clock.tick(60)
                

        screen.fill((0,0,0))

        lTitle = "Road Planning Sim"
        title = normalFont.render(lTitle,False, (255,255,255))
        screen.blit(title, (450, 150))

        menu_sprite_group.draw(screen)
        for item in menu_buttons:
            item.process()
        

        screen.blit(startGameButton.buttonSurf, ((startGameButton.rect.x+150), (startGameButton.rect.y)))
        screen.blit(checkRankingButton.buttonSurf, ((checkRankingButton.rect.x+120), (checkRankingButton.rect.y)))
        screen.blit(InstructionOpenButton.buttonSurf, ((InstructionOpenButton.rect.x+80), (InstructionOpenButton.rect.y)))
        all_sprite_group.update()
        pygame.display.flip()
        clock.tick(60)
    
    acceptedBool = False    
    frameCount = 0
    timer = 0
    sCost = 0
    currentScore = 0
    YRanking = 140

    listOfTimeDisplayed = []
    listOfScoreDisplayed = []
    listOfRankingY = []
    for i in range(1, 5):
        if len(DisplayRankingList) <= i:
            break
        listOfRankingY.append(YRanking)
        listOfTimeDisplayed.append(DisplayRankingList[i][0])
        listOfScoreDisplayed.append(DisplayRankingList[i][1])
        YRanking = YRanking + 30

    while acceptedBool == False:
        frameCount += 1
        if frameCount == 60:
            timer += 1
            frameCount = 0

        selectedTileCost = "None"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousePos = pygame.mouse.get_pos()
                for square in tile_group:
                    if square.rect.collidepoint(mousePos):

                        ifSelected = square.updateWhenSelected()
                        if ifSelected == "selected":
                            sCost += square.cost
                            pathList.append((square.a, square.b))
                            print((square.a,square.b))
                            
                        elif ifSelected == "deselected":
                            sCost -= square.cost
                            pathList.remove((square.a, square.b))
                            
                if submitButton.rect.collidepoint(mousePos):
                    if ((0, 0) in pathList) and ((8, 8) in pathList) and len(pathList) == 17 and checkContinuity(pathList) == True:
                        
                        acceptedBool = True

                    else:
                        
                        acceptedBool = False

        for square in tile_group:
            if square.rect.collidepoint(pygame.mouse.get_pos()):
                selectedTileCost = square.cost
                   
        lCreator = "Made by Tony Lu"
        lCost = "A* algorithm gives: " + str(totalCost)
        cCost = "Current cost: " + str(sCost)                       
        selectedTileCostString = "Selected tile costs: " + str(selectedTileCost)
        timerText = "Time: " + str(timer)

        screen.fill((0,0,0))
        all_sprite_group.draw(screen)

        for item in buttons:
            item.process()
        
        #text element variables
        myName = normalFont.render(lCreator, False, (255, 240, 230))
        targetCost = smallFont.render(lCost, False, (255, 240, 230))
        currentCost = smallFont.render(cCost, False, (255, 240, 230))
        selectedTileCostDisplay = smallFont.render(selectedTileCostString, False, (255, 240, 230))
        timerDisplay = normalFont.render(timerText, False, (255, 240, 230))
        #the button
        screen.blit(submitButton.buttonSurf, ((submitButton.rect.x+80), (submitButton.rect.y)))
        #display the texts
        screen.blit(myName,(20,650))
        screen.blit(targetCost,(840, 360))
        screen.blit(currentCost,(840, 330))
        screen.blit(selectedTileCostDisplay,(840, 300))
        screen.blit(timerDisplay, (10, 20))

        #separate section for the ranking display
        screen.blit(normalFont.render("Top 5 scores", False, (255,120,230)), (10, 70))
        for i in range(len(listOfTimeDisplayed)):
            screen.blit(smallerFont.render(listOfTimeDisplayed[i], False, (255,160,230)), (10, listOfRankingY[i]))
            screen.blit(smallerFont.render(str(listOfScoreDisplayed[i]), False, (255, 240, 250)), (240, listOfRankingY[i]))
        #update
        all_sprite_group.update()
        clock.tick(60)
        pygame.display.flip()

    #ending screen for submitting solution
    currentScore = round(calculateScore(timer, sCost, totalCost))
    now = datetime.now()
    currentDateTime = now.strftime("%d/%m/%Y, %H:%M:%S")
    
    global ranking
    ranking.append([currentDateTime, currentScore])
    sorted_ranking = sorted(ranking, key=itemgetter(1)) 

    with open(os.path.join("A-level-Project", "game", 'record.json'), "w") as record:
        json.dump(sorted_ranking, record)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((58,42,64))
        #modify the solution in final screen
        for square in final_sprite_group:
            if (square.a, square.b) in path:
                square.changeColor()
        for square in final_player_sprite_group:
            if (square.a, square.b) in pathList:
                square.changeColor()
        #the contents
        lTimeTaken = "The time taken is " + str(timer) + " seconds"
        lYourCost = "It takes a cost of " + str(sCost) + " coins"
        lTargetCost = "The A* algorithm gives: " + str(totalCost) + " coins"
        lYourScore = "You have achieved: " + str(currentScore) + " points"
        #elements
        notification = normalFont.render("You have submitted your solution", False, (174, 116, 196))
        timeTakenText = smallFont.render(lTimeTaken, False, (182, 137, 199))
        targetCostText = smallFont.render(lTargetCost, False, (190, 145, 210))
        yourCostText = smallFont.render(lYourCost, False, (204, 155, 222))
        yourScoreText = normalFont.render(lYourScore, False, (215, 169, 232))

        computerNot = smallFont.render("A star algorithm", False, (255, 255,255))
        playerNot = smallFont.render("Your soluction", False, (255,255,255))
        #display the texts
        screen.blit(notification, (30, 30))
        screen.blit(timeTakenText, (30, 120))
        screen.blit(yourCostText, (30, 180))
        screen.blit(targetCostText, (30, 240))
        screen.blit(yourScoreText, (30, 300))
        
        screen.blit(computerNot, (360, 620))
        screen.blit(playerNot, (720, 620))

        final_sprite_group.draw(screen)
        final_sprite_group.update()
        final_player_sprite_group.draw(screen)
        final_player_sprite_group.update()
        #updating and fps
        pygame.display.flip()
        clock.tick(60)

mainloop()
