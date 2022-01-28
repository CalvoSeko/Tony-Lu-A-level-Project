import pygame
import generator

#start off pygame
pygame.font.init()

#game loop

win_width = 1280
win_height = 720
mat_width = 17



step_size = mat_width - 1
distance = int(step_size / 2)
rangeOfValue = 20



FONT = pygame.font.SysFont("comicsans", 20)
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((win_width, win_height))


pygame.init()

class Tile(pygame.sprite.Sprite): 
# Define the constructor for snow 
    def __init__(self, color, width, x, y): 
        super().__init__() 
    # Create a sprite and fill it with colour 
        self.image = pygame.Surface([width,width]) 
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y


seaLevelMatrix = [[0 for x in range(mat_width)] for y in range(mat_width)] 
generator.generateInitBiome(seaLevelMatrix, mat_width, 16)
generator.diamondSquare(seaLevelMatrix, mat_width, rangeOfValue, distance, step_size)

soilQuality = [[0 for x in range(mat_width)] for y in range(mat_width)] 
generator.generateInitBiome(soilQuality, mat_width, 16)
generator.diamondSquare(soilQuality, mat_width, rangeOfValue, distance, step_size)

drainage = [[0 for x in range(mat_width)] for y in range(mat_width)] 
generator.generateInitBiome(drainage, mat_width, 16)
generator.diamondSquare(drainage, mat_width, rangeOfValue, distance, step_size)


print('\n'.join([''.join(['{:5}'.format(item) for item in row]) 
      for row in seaLevelMatrix]))

print('\n'.join([''.join(['{:5}'.format(item) for item in row]) 
      for row in soilQuality]))

print('\n'.join([''.join(['{:5}'.format(item) for item in row]) 
      for row in drainage]))

squareX = 300
squareY = 30
tileWidth = 30
tile_group = pygame.sprite.Group()
all_sprite_group = pygame.sprite.Group()

for i in range(mat_width):
        for j in range(mat_width):

            seaColor = (drainage[i][j], soilQuality[i][j], seaLevelMatrix[i][j])
            myTile = Tile(seaColor, tileWidth, squareX, squareY)
            squareX += tileWidth
            tile_group.add(myTile)
            all_sprite_group.add(myTile)
        squareY += tileWidth
        squareX = 300




while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    all_sprite_group.update()
    screen.fill((0,0,0))
    all_sprite_group.draw(screen)
    clock.tick(60)
    
    pygame.display.update()
pygame.quit()
    








