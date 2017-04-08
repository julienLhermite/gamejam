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

while not game_on:
    quit = pygame.event.get(pygame.QUIT)
    pygame.event.poll()

    # state of the keys
    keys = pygame.key.get_pressed()

    # filter for the keys we're interessted in
    pressed = ((key, _) for (key, _) in moves.items() if keys[key])
    key, (cache, dir) = next(pressed, (None, (None, None)))

    # if a key of the 'moves' dict is pressed:
    if key:
        # if we change the direction, we need another animation
        print(key)
        if state != key:
            cachedeque = deque(cache)
            state = key
        # move the square
        rect.move_ip(dir)
    else:
        state = None

    fenetre.fill(pygame.color.Color('green'))

    # display first image in cachedeque
    fenetre.blit(cachedeque[0], rect)


