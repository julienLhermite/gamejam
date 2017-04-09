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


import pygame
from collections import deque

pygame.init()
screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()
last_key_pressed = 0

# just some colored squares for our animation
def get_cache(colors):
    tmp=[]
    for c in colors:
        s = pygame.surface.Surface((50,50))
        s.fill(pygame.color.Color(c))
        tmp.append(s)
    return tmp

walk_left, walk_right = get_cache(('red', 'red', 'red')), get_cache(('black', 'white', 'grey'))
walk_down, walk_up = get_cache(('blue', 'blue', 'blue')), get_cache(('black', 'white', 'grey'))


rect = walk_left[0].get_rect(top=100, right=100)
cachedeque = deque(walk_left)
state = None
quit = False

# a simple variable to keep track of time
timer = 0

# a dict of {key: (animation, direction)}
moves = {pygame.K_LEFT:  (walk_left,  (-2, 0)),
         pygame.K_RIGHT: (walk_right, ( 2, 0)),
         pygame.K_UP: (walk_up, (0, -2)),
         pygame.K_DOWN: (walk_down, (0, 2))}

level = Niveau(ratio_murs=65, size=7, coord_depart=[0,4])
print(level.structure)

while not quit:
    quit = pygame.event.get(pygame.QUIT)
    pygame.event.poll()




    level.afficher(screen)




    # state of the keys
    keys = pygame.key.get_pressed()

    # filter for the keys we're interessted in
    pressed = ((key, _) for (key, _) in moves.items() if keys[key])
    key, (cache, dir) = next(pressed, (None, (None, None)))

    # if a key of the 'moves' dict is pressed:
    if key and (time.time() - last_key_pressed >= 0.7) :
        # if we change the direction, we need another animation
        print("ok")
        last_key_pressed = time.time()

        if state != key:
            cachedeque = deque(cache)
            state = key
        # move the square
        rect.move_ip(dir)
    else:
        state = None

    screen.fill(pygame.color.Color('green'))

    # display first image in cachedeque
    screen.blit(cachedeque[0], rect)

    # rotate cachedeque to the left, so the second image becomes the first
    # do this three times a second:
    if state and timer >= 1000./3:
        cachedeque.rotate(-1)
        timer = 0

    # call flip() and tick() only once per frame
    pygame.display.flip()

    # keep track of how long it took to draw this frame
    timer += clock.tick(60)





#
#
# pygame.init()
#
# fenetre = pygame.display.set_mode((1920,1080))
# # fenetre = pygame.display.set_mode((1920,1080), FULLSCREEN)
#
# fond = pygame.image.load(os.path.join(global_mode, "background", "background.png")).convert_alpha()
#
# hero = Perso("hero", "hero.png", (0,0), 3, fenetre)
#
#
# def update():
#     fenetre.blit(fond, (0,0))
#     fenetre.blit(hero.sprite, hero.rect)
#     pygame.display.flip()
#
#
# update()
# start_time = time.time()
#
# game_on = True
# pygame.key.set_repeat(500, 200)
#
# while game_on:
#
#     for event in pygame.event.get():
#         if event.type == KEYDOWN:
#             if event.key == K_DOWN:
#                 print("down")
#                 hero.move(DOWN)
#             if event.key == K_UP:
#                 print("up")
#                 hero.move(UP)
#             if event.key == K_LEFT:
#                 print("left")
#                 hero.move(LEFT)
#             if event.key == K_RIGHT:
#                 print("right")
#                 hero.move(RIGHT)
#
#
#
#
#
#
#
#
#         if event.type == QUIT:
#             game_on = False
#     update()
