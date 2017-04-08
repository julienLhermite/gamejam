import pygame
import os
import time
from pygame.locals import *

# elmt de la bibliothèque
# -display
# -mixer
# -draw
# -event
# -image
# -mouse
# -time


fenetre = pygame.display.set_mode((1000,500))
# fenetre = pygame.display.set_mode((1920,1080), FULLSCREEN)
test = 2+2

fond = pygame.image.load(os.path.join("images", "background", "background.png")).convert()



perso = pygame.image.load(os.path.join("images", "case", "perso.png")).convert()
perso.set_colorkey((255,255,255))
position_perso = perso.get_rect()
position_perso = position_perso.move(150, 100)


def update():
    fenetre.blit(fond, (0,0))

    fenetre.blit(perso, position_perso)
    pygame.display.flip()


update()
start_time = time.time()

game_on = True

while game_on:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                print("down")
                position_perso = position_perso.move(0, 3)
            if event.key == K_UP:
                print("up")
                position_perso = position_perso.move(0, -3)
            if event.key == K_LEFT:
                print("left")
                position_perso = position_perso.move(-3, 0)
            if event.key == K_RIGHT:
                print("right")
                position_perso = position_perso.move(3, 0)






        if event.type == QUIT:
            game_on = False
    update()
