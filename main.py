import pygame
import sys
import math
import random

#start off pygame
WIN_WIDTH = 640
WIN_HEIGHT = 280


class game():

    def __init__(self):
        pass
        pygame.init()
        size = (WIN_WIDTH,WIN_HEIGHT)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("infection")
        self.clock = pygame.time.Clock()
    
    def update(self):
        self.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.flip
bg = game()
while True:
    bg.update()





