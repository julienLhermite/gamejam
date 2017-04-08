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

pygame.init()

fenetre = pygame.display.set_mode((1920,1080))
# fenetre = pygame.display.set_mode((1920,1080), FULLSCREEN)

fond = pygame.image.load(os.path.join("images", "background", "background.png")).convert()

hero = Perso("hero", "perso.png", (0,0), 3, fenetre)
hero.sprite.set_colorkey((255,255,255))

def update():
    fenetre.blit(fond, (0,0))
    fenetre.blit(hero.sprite, hero.rect)
    pygame.display.flip()


update()
start_time = time.time()

game_on = True
pygame.key.set_repeat(500, 200)

while game_on:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                print("down")
                hero.move(DOWN)
            if event.key == K_UP:
                print("up")
                hero.move(UP)
            if event.key == K_LEFT:
                print("left")
                hero.move(LEFT)
            if event.key == K_RIGHT:
                print("right")
                hero.move(RIGHT)








        if event.type == QUIT:
            game_on = False
    update()
