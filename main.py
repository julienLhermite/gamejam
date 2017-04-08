import pygame
from pygame.locals import *
import os

# elmt de la bibliothèque
# -display
# -mixer
# -draw
# -event
# -image
# -mouse
# -time


import pygame
from pygame.locals import *
import time
import os
from classes import *


def update(liste, niveau):
    for image in liste:
        image.screen.blit(image.surface, image.rect)

    niveau.afficher(screen, perso)

    pygame.display.flip()

pygame.init()

# list of surfaces
surfaces = []

# set window and background
screen = pygame.display.set_mode((1440, 874))
background = Back("bg-excel.png", (0,0), screen, surfaces)


level1 = Niveau(10,12,[0,4])
for i in range(level1.size + 2):
    if (i == 0) or (i == level1.size+1):
        for j in range(level1.size+2):
            print(i,j)
            Back("bordure.png", (DEP_BORDER_CASE[0]+i*CELL_SIZE[0], DEP_BORDER_CASE[1]+j*CELL_SIZE[1]), screen, surfaces)
    else:
        for j in [0, level1.size+1]:
            print(i, j)
            Back("bordure.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]), screen,
                 surfaces)

# Init perso
perso = Perso(level1, "perso.png")

print(surfaces)
clock = pygame.time.Clock()
last_key_pressed = 0

quit = False

# a simple variable to keep track of time
timer = 0

# a dict of {key: (animation, direction)}
moves = {pygame.K_LEFT:  LEFT,
         pygame.K_RIGHT: RIGHT,
         pygame.K_UP: UP,
         pygame.K_DOWN: DOWN}


update(surfaces, level1)

while not quit:
    quit = pygame.event.get(pygame.QUIT)
    pygame.event.poll()

    # state of the keys
    keys = pygame.key.get_pressed()

    # filter for the keys we're interessted in
    pressed = ((key, _) for (key, _) in moves.items() if keys[key])
    key, dir = next(pressed, (None, None))

    # if a key of the 'moves' dict is pressed:
    if key and (time.time() - last_key_pressed >= 0.2):
        # if we change the direction, we need another animation
        print(dir)
        last_key_pressed = time.time()
        print(perso.pos)
        perso.move(dir)
        print(perso.pos)
        update(surfaces, level1)

    # display first image in cachedeque
    # screen.blit(cachedeque[0], rect)


