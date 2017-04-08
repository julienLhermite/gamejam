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


def update(liste):

    for papa in liste:


        papa.screen.blit(papa.surface, papa.rect)

    pygame.display.flip()

pygame.init()



# list of surfaces
surfaces = []

# set window and background
screen = pygame.display.set_mode((1440, 874))
background = Back("bg-excel.png", (0,0), screen, surfaces)



# Init perso
perso = Perso("perso.png", (150, 100), screen, surfaces)

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

update(surfaces)

while not quit:
    quit = pygame.event.get(pygame.QUIT)
    pygame.event.poll()

    # state of the keys
    keys = pygame.key.get_pressed()

    # filter for the keys we're interessted in
    pressed = ((key, _) for (key, _) in moves.items() if keys[key])
    key, dir = next(pressed, (None, None))

    # if a key of the 'moves' dict is pressed:
    if key and (time.time() - last_key_pressed >= 0.7):
        # if we change the direction, we need another animation
        print(dir)
        last_key_pressed = time.time()
        print(perso.rect)
        perso.move(dir)
        print(perso.rect)

    else:
        state = None

    # display first image in cachedeque
    # screen.blit(cachedeque[0], rect)

    update(surfaces)


