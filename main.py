import pygame


#start off pygame

icon = pygame.image.load("icon.png")



#game loop
class game():
    global win_width, win_height
    win_width = 1280
    win_height = 720
    def __init__(self):
        pass

        pygame.init()


        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("game")
        pygame.display.set_icon(icon)

        self.clock=pygame.time.Clock()

    def update(self):
        #60fps
        self.clock.tick(60)

        #background
        self.screen.fill((0,0,0))

        #options background
        pygame.draw.rect(self.screen, ((255,255,255)), (0,360,400,340))
        #options slots
        pygame.draw.rect(self.screen, ((0,0,0)),(10,370,380,100))
        pygame.draw.rect(self.screen, ((0,0,0)),(10,480,380,100))
        pygame.draw.rect(self.screen, ((0,0,0)),(10,590,380,100))
        #quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        #update
        pygame.display.flip()


gm = game()
while 1:
    gm.update()





