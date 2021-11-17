import pygame
import generator

#start off pygame
pygame.font.init()
icon = pygame.image.load("icon.png")

#game loop

win_width = 1280
win_height = 720
player_count = 0
FONT = pygame.font.SysFont("comicsans", 20)
running = True
screen = pygame.display.set_mode(win_width, win_height)
pygame.init()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False








