#!/usr/local/bin/python3.5
# -*- coding: <encoding name> -*-

import pygame
import classes
from const import *


def update_graph(hero, score, score_retenue, surfaces, screen):

    # Points
    surfaces= [surface for surface in surfaces if not surface.image_name == "point.png"]
    classes.Background("point_back.png", (SCORE_POS[0] - 20, SCORE_POS[1] - 320), screen, surfaces, global_mode)
    memoir_score = score
    if score < 0:
        new_score = 0
    else:
        new_score = max(score, score_retenue * 100 + 1)
    score_jauge = score % 100

    for point in range(1,score_jauge+1):
        if point % 10:
            classes.Background("1point.png", (SCORE_POS[0], SCORE_POS[1] - 3 * point), screen, surfaces, global_mode)
        else:
            classes.Background("10point.png", (SCORE_POS[0], SCORE_POS[1] - 3 * point), screen, surfaces, global_mode)

    memoir_score_retenue = score_retenue
    new_score_retenue = max([score_retenue, score // 100])
    if new_score_retenue > memoir_score_retenue:
        hero.update_life(+1)

    # Vie
    surfaces = [surface for surface in surfaces if not surface.image_name.startswith("vie")]
    classes.Background("vie_back.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 1:
        classes.Background("vie_1.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 2:
        classes.Background("vie_2.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 3:
        classes.Background("vie_3.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 4:
        classes.Background("vie_4.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 5:
        classes.Background("vie_5.png", LIFE_POS, screen, surfaces, global_mode)

    return surfaces, new_score_retenue, new_score



def init_level(scr, surf, lvl):
    surf = [s for s in surf if (s.image_name != "bordure.png") and (s.image_name != "floor.png")]
    # Initialisation des bordures du niveau
    for i in range(lvl.size + 2):
        if (i == 0) or (i == lvl.size + 1):
            for j in range(lvl.size + 2):
                classes.Background("bordure.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]),
                     scr, surf, global_mode)
        else:
            for j in [0, lvl.size + 1]:
                classes.Background("bordure.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]),
                     scr,
                     surf, global_mode)
            for j in range(1, lvl.size + 1):
                classes.Background("floor.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]),
                     scr,
                     surf, global_mode)
    return surf


def init_personnage(lvl, old_lvl, life):
    # Init Personnage
    ennem = []
    for lin in range(lvl.size):
        for col in range(lvl.size):
            case = lvl.structure[lin][col]
            if DEPART in case:
                h = classes.Hero([lin, col], lvl, "hero-down.png", life, ennem, global_mode)
                h.level = old_lvl
            elif STUPID_GHOST in case:
                classes.StupidGhost([lin, col], lvl, "stupid_ghost.png", 1, ennem, global_mode)
            elif GHOST in case:
                classes.Ghost([lin, col], lvl, "ghost.png", 1, ennem, global_mode)
            elif ORC in case:
                classes.Orc([lin, col], lvl, "orc.png", 1, ennem, global_mode)
            elif TURRET in case:
                Turret([lin, col], lvl, "turret_right.png", 1, ennem, global_mode)

    return h, ennem


def update(liste, niveau, enemies, hero, screen, score):
    for image in liste:
        image.screen.blit(image.surface, image.rect)
    niveau.afficher(screen, hero, enemies, global_mode)
    print(str(niveau))

    myfont = pygame.font.SysFont("monospace", 32)
    label = myfont.render(str(score), 1, (20, 40, 20))
    screen.blit(label, (SCORE_POS[0], SCORE_POS[1]+25))

    pygame.display.flip()


def update_background(back, screen):
    screen.blit(back.surface, back.rect)
    pygame.display.flip()