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

def update(liste, niveau, ennemies):
    for image in liste:
        image.screen.blit(image.surface, image.rect)

    niveau.afficher(screen, hero, ennemies)
    print(str(niveau))
    print(ennemies)
    pygame.display.flip()

def update_background(back, screen):
    screen.blit(back.surface, back.rect)
    pygame.display.flip()

pygame.init()

# list of surfaces
surfaces = []

# set window and background
screen = pygame.display.set_mode((1440, 874))


background = Back("accueil.png", (0,0), screen, surfaces)


level1 = Niveau(30, 7, LEFT, 2, 0, 0, 2)

# Initialisation des bordures du niveau
for i in range(level1.size + 2):
    if (i == 0) or (i == level1.size+1):
        for j in range(level1.size+2):
            Back("bordure.png", (DEP_BORDER_CASE[0]+i*CELL_SIZE[0], DEP_BORDER_CASE[1]+j*CELL_SIZE[1]), screen, surfaces)
    else:
        for j in [0, level1.size+1]:
            Back("bordure.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]), screen,
                 surfaces)

# Init Personnage
ennemies = []
for lin in range(level1.size):
    for col in range(level1.size):
        case = level1.structure[lin][col]
        if DEPART in case:
            hero = Hero([lin, col], level1, "hero.png", 1, ennemies)
        elif STUPID_GHOST in case:
            StupidGhost([lin, col], level1, "stupid_ghost.png", 1, ennemies)
        elif GHOST in case:
            Ghost([lin, col], level1, "ghost.png", 1, ennemies)
        elif ORC in case:
            Orc([lin, col], level1, "orc.png", 1, ennemies)

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

mouse_pressed = False

update_background(background, screen)

playable = False

while not quit:
    quit = pygame.event.get(pygame.QUIT)
    pygame.event.poll()

    # state of the keys
    keys = pygame.key.get_pressed()

    # filter for the keys we're interessted in
    pressed = ((key, _) for (key, _) in moves.items() if keys[key])
    key, dir = next(pressed, (None, None))

    if pygame.mouse.get_pressed() == (1, 0, 0):
        mouse_pressed = True
    if mouse_pressed and (pygame.mouse.get_pressed() == (0, 0, 0)):
        mouse_pressed = False
        print(pygame.mouse.get_pos())
        if (pygame.mouse.get_pos()[1] >= MENU_UP) and (pygame.mouse.get_pos()[1] <= MENU_DOWN):
            # Acceuil
            if (pygame.mouse.get_pos()[0] >= MENU_0) and (pygame.mouse.get_pos()[0] <= MENU_1):
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "accueil.png")).convert_alpha()
                playable = False
            # Credit
            if (pygame.mouse.get_pos()[0] >= MENU_1) and (pygame.mouse.get_pos()[0] <= MENU_2):
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "credits.png")).convert_alpha()
                playable = False
                print("credit")
            # Aide
            if (pygame.mouse.get_pos()[0] >= MENU_2) and (pygame.mouse.get_pos()[0] <= MENU_3):
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "aide.png")).convert_alpha()
                playable = False
            # Moche
            if (pygame.mouse.get_pos()[0] >= MENU_3) and (pygame.mouse.get_pos()[0] <= MENU_4):
                global_mode = MOCHE
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "bg-excel.png")).convert_alpha()
                playable = True
                update(surfaces, level1, ennemies)
            # moins moche
            if (pygame.mouse.get_pos()[0] >= MENU_4) and (pygame.mouse.get_pos()[0] <= MENU_5):
                global_mode = MOINS_MOCHE
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "bg-excel.png")).convert_alpha()
                playable = True
                update(surfaces, level1, ennemies)
            # enjoy =)
            if (pygame.mouse.get_pos()[0] >= MENU_5) and (pygame.mouse.get_pos()[0] <= MENU_6):
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "pas_porno.png")).convert_alpha()
                playable = False
            update_background(background, screen)

    if playable:

        # if a key of the 'moves' dict is pressed et que c'est jouable:
        if  key and (time.time() - last_key_pressed >= 0.2):
            # if we change the direction, we need another animation
            print(dir)
            last_key_pressed = time.time()
            print(hero.pos)
            hero.move(dir)
            for ennemy in ennemies:
                ennemy.move(hero)

            print(hero.pos)
            update(surfaces, level1, ennemies)

            if hero.life == 0:
                print('GAME OVER')
                Back("game-over.jpg", GAME_OVER_POS, screen, surfaces)
                # display first image in cachedeque
                # screen.blit(cachedeque[0], rect)


