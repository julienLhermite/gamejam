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


def init_level(scr, surf, lvl):
    surf = [s for s in surf if (s.image_name != "bordure.png") and (s.image_name != "floor.png")]
    # Initialisation des bordures du niveau
    for i in range(lvl.size + 2):
        if (i == 0) or (i == lvl.size + 1):
            for j in range(lvl.size + 2):
                Back("bordure.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]),
                     scr, surf)
        else:
            for j in [0, lvl.size + 1]:
                Back("bordure.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]),
                     scr,
                     surf)
            for j in range(1, lvl.size + 1):
                Back("floor.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]),
                     scr,
                     surf)
    return surf

def init_personnage(lvl, old_lvl):
    # Init Personnage
    ennem = []
    for lin in range(lvl.size):
        for col in range(lvl.size):
            case = lvl.structure[lin][col]
            if DEPART in case:
                h = Hero([lin, col], lvl, "hero.png", 1, ennem)
                h.level = old_lvl
            elif STUPID_GHOST in case:
                StupidGhost([lin, col], lvl, "stupid_ghost.png", 1, ennem)
            elif GHOST in case:
                Ghost([lin, col], lvl, "ghost.png", 1, ennem)
            elif ORC in case:
                Orc([lin, col], lvl, "orc.png", 1, ennem)

    return h, ennem


def update(liste, niveau, enemies):
    for image in liste:
        image.screen.blit(image.surface, image.rect)
    niveau.afficher(screen, hero, enemies, global_mode)
    print(str(niveau))
    pygame.display.flip()


def update_background(back, screen):
    screen.blit(back.surface, back.rect)
    pygame.display.flip()


pygame.init()

# list of surfaces
surfaces = []

# set window and background
screen = pygame.display.set_mode((1440, 874), RESIZABLE)


background = Back("accueil.png", (0,0), screen, surfaces)

level = Niveau(LVL[1][0], LVL[1][1], LVL[1][2], LVL[1][3], LVL[1][4], LVL[1][5], LVL[1][6])

old_level = 1
surfaces = init_level(screen, surfaces, level)
hero, ennemies = init_personnage(level, old_level)


clock = pygame.time.Clock()
last_key_pressed = 0

quit = False

# a simple variable to keep track of time
timer = 0

# a dict of {key: (animation, direction)}
moves = {pygame.K_LEFT:  LEFT,
         pygame.K_RIGHT: RIGHT,
         pygame.K_UP: UP,
         pygame.K_DOWN: DOWN,
         pygame.K_o: OUI,
         pygame.K_n: NON,
         }

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
        if (pygame.mouse.get_pos()[1] >= MENU_UP) and (pygame.mouse.get_pos()[1] <= MENU_DOWN):
            # Acceuil
            if (pygame.mouse.get_pos()[0] >= MENU_0) and (pygame.mouse.get_pos()[0] <= MENU_1):
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "accueil.png")).convert_alpha()
                playable = False
            # Credit
            if (pygame.mouse.get_pos()[0] >= MENU_1) and (pygame.mouse.get_pos()[0] <= MENU_2):
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "credits.png")).convert_alpha()
                playable = False
            # Aide
            if (pygame.mouse.get_pos()[0] >= MENU_2) and (pygame.mouse.get_pos()[0] <= MENU_3):
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "aide.png")).convert_alpha()
                playable = False
            # Moche
            if (pygame.mouse.get_pos()[0] >= MENU_3) and (pygame.mouse.get_pos()[0] <= MENU_4):
                global_mode = MOCHE
                background.image_name = "bg-excel.png"
                background.image_path = os.path.join(global_mode, "background", "bg-excel.png")
                background.surface = pygame.image.load(background.image_path).convert_alpha()
                playable = True
            # moins moche
            if ((pygame.mouse.get_pos()[0] >= MENU_4) and (pygame.mouse.get_pos()[0] <= MENU_5)):
                global_mode = MOINS_MOCHE
                background.image_name = "bg-excel.png"
                background.image_path = os.path.join(global_mode, "background", "bg-excel.png")
                background.surface = pygame.image.load(background.image_path).convert_alpha()
                playable = True
            # enjoy =)
            if (pygame.mouse.get_pos()[0] >= MENU_5) and (pygame.mouse.get_pos()[0] <= MENU_6):
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "pas_porno.png")).convert_alpha()
                playable = False
            update_background(background, screen)
            if playable:
                for surface in surfaces:
                    surface.maj_mode(global_mode)
                for ennemy in ennemies:
                    ennemy.maj_mode(global_mode)
                hero.maj_mode(global_mode)

                update(surfaces, level, ennemies)

    if playable:

        # if a key of the 'moves' dict is pressed et que c'est jouable:
        if key and (time.time() - last_key_pressed >= 0.2):
            # if we change the direction, we need another animation
            print(dir)
            last_key_pressed = time.time()
            print(hero.pos)
            if dir in [RIGHT, LEFT, DOWN, UP]:
                hero.move(dir)
            for ennemy in ennemies:
                ennemy.move(hero)
            print(old_level, hero.level, hero.life)
            print(hero.pos)
            if hero.life == 0:
                print('GAME OVER')
                playable = False
                Back("game-over.jpg", GAME_OVER_POS, screen, surfaces)
                # display first image in cachedeque
                # screen.blit(cachedeque[0], rect)
            update(surfaces, level, ennemies)
            if hero.level > old_level:
                old_level = hero.level
                print('Level Up')
                path = os.path.join("images", "background", "level-up.png")
                screen.blit(pygame.image.load(path).convert_alpha(), (DEP_CASE[0]+CELL_SIZE[0]*(int(level.size/2)-1),
                                                                      DEP_CASE[1] + CELL_SIZE[1] * (int(level.size/2)-1)))
                pygame.display.flip()
                time.sleep(2)
                l = hero.level
                try:
                    level = Niveau(LVL[l][0], LVL[l][1], LVL[l][2], LVL[l][3], LVL[l][4], LVL[l][5], LVL[l][6])
                except KeyError:
                    Back("gagne.jpg", GAME_OVER_POS, screen, surfaces)
                    playable = False
                else:
                    surfaces = init_level(screen, surfaces, level)
                    hero, ennemies = init_personnage(level, old_level)
                update(surfaces, level, ennemies)

    else:
        if key and (dir == OUI):
            old_level = 1
            level = Niveau(LVL[1][0], LVL[1][1], LVL[1][2], LVL[1][3], LVL[1][4], LVL[1][5], LVL[1][6])
            playable = True
            surfaces = [s for s in surfaces if s.image_name != "game-over.jpg" and s.image_name != "gagne.jpg"]
            surfaces = init_level(screen, surfaces, level)
            hero, ennemies =init_personnage(level, old_level)
            update(surfaces, level, ennemies)
        elif key and (dir == NON):
            quit=True




