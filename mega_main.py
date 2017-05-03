import os
import pygame

import random
from pygame.locals import *
import time




random.seed()



UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
OUI = "oui"
NON = "non"
SPACE = "space"

MUR = "M"
MUR_CASSE = "m"
DEPART = "D"
HERO = "H"
SORTIE = "S"
GHOST = "G"
ORC = "O"
STUPID_GHOST = "g"
TURRET = "T"
FIREBALL = "*"

MENU_UP = 826
MENU_DOWN = 848
MENU_0 = 58
MENU_1 = 178
MENU_2 = 309
MENU_3 = 413
MENU_4 = 559
MENU_5 = 742
MENU_6 = 782

MOCHE = "images"
MOINS_MOCHE = "images_good"

global_mode = MOCHE

ECTOPLASME = [GHOST, STUPID_GHOST]
TANGIBLE_FOR_GHOST = ECTOPLASME + [HERO, ORC, TURRET]
TANGIBLE = TANGIBLE_FOR_GHOST + [MUR, MUR_CASSE]

CELL_SIZE = (32, 29)
DEP_CASE = (57, 201)
DEP_BORDER_CASE = (DEP_CASE[0]-CELL_SIZE[0], DEP_CASE[1]-CELL_SIZE[1])
GAME_OVER_POS = (DEP_BORDER_CASE[0]+20*CELL_SIZE[0], DEP_BORDER_CASE[1]+CELL_SIZE[1]*2)

FIRST_CELL_X = 120
FIRST_CELL_Y = 80

        # taux, size, coté, sorties, nb_ghost_stupid, nb_ghost, nb_orc , nb_tourelle)
LVL = { 1: [5,    7,   LEFT,    1,        3,              0,       0,      0],
        2: [10,   8,   RIGHT,    1,        2,              3,       0,      0],
        3: [30,    9,   LEFT,    2,        1,              0,       4,      0],
        4: [85,    10,   RIGHT,    1,        4,              2,       2,      0],
        5: [60,    17,   LEFT,    2,        0,              1,       4,      0],
        6: [10,    12,   RIGHT,    1,        2,              1,       3,      1],
        7: [15,    13,   LEFT,    2,        3,              2,       4,      2],
        8: [10,   8,   RIGHT,    1,        2,              2,       4,      3],
        9: [30,    9,   LEFT,    1,        2,              0,       5,      4],
        10: [30,    10,   RIGHT,    2,        4,              5,       6,      5]
      }

LIFE_POS = (DEP_BORDER_CASE[0]+20*CELL_SIZE[0], DEP_BORDER_CASE[1]+CELL_SIZE[1]*10)
SCORE_POS  = (DEP_BORDER_CASE[0]+28*CELL_SIZE[0], DEP_BORDER_CASE[1]+CELL_SIZE[1]*20)



def find_ennemy_at(ennemies, pos):
    ennemy_at = []
    for ennemy in ennemies:
        if ennemy.pos == pos :
            ennemy_at.append(ennemy)
    return ennemy_at


def find_ennemy_at_with_type(ennemies, ennemy_type, pos):
    ennemy_at_with = []
    for ennemy in ennemies:
        if (ennemy.pos == pos) and (ennemy_type == ennemy.type):
            ennemy_at_with.append(ennemy)
    return ennemy_at_with



class Background:
    def __init__(self, image_name, coord, screen, surfaces, mode):
        self.image_name = image_name
        self.image_path = os.path.join(mode, "background", image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()
        self.screen = screen
        self.rect = self.surface.get_rect()
        self.coord = coord
        self.rect = self.rect.move(coord[0], coord[1])
        surfaces.append(self)

    def maj_mode(self, mode):

        self.image_path = os.path.join(mode, "background", self.image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()


class Personnage():
    def __init__(self, coord, niveau, image_name, life, ennemies, mode):
        self.surface = pygame.image.load(os.path.join(mode, "case", image_name)).convert_alpha()
        self.struct = niveau.structure
        self.struct_size = niveau.size
        self.pos = coord
        self.life = life
        self.ennemies = ennemies
        self.image_name = image_name
        self.mode = mode

    def maj_mode(self, mode):
        self.mode = mode
        self.image_path = os.path.join(mode, "case", self.image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()

class Hero(Personnage):

    def __init__(self, coord, niveau, image_name, life, ennemies, mode):
        super().__init__(coord, niveau, image_name, life, ennemies, mode)
        self.level = 1

    def maj_image(self, dir):
        self.image_name = 'hero-'+ dir + '.png'
        self.image_path = os.path.join(self.mode, 'case', self.image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()

    def move(self, dir):
        if (dir == DOWN) and (self.pos[0] < self.struct_size-1):
            # si rien n'est tangible sur la case où on veut aller
            if [chose for chose in self.struct[self.pos[0]+1][self.pos[1]] if chose in TANGIBLE] == []:
                self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(HERO,"")
                self.pos[0] += 1
                self.struct[self.pos[0]][self.pos[1]] += HERO
            # (si y a un mur on le casse un peu)
            elif MUR in self.struct[self.pos[0]+1][self.pos[1]]:
                self.struct[self.pos[0] + 1][self.pos[1]] = self.struct[self.pos[0]+1][self.pos[1]].replace(MUR,MUR_CASSE)
                # si extoplasme dans le mur
                ennemies_at = find_ennemy_at_with_type(self.ennemies, GHOST, [self.pos[0] + 1, self.pos[1]]) +\
                              find_ennemy_at_with_type(self.ennemies, STUPID_GHOST, [self.pos[0]+1,self.pos[1]])
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        ennemy.update_life(-1)
            elif MUR_CASSE in self.struct[self.pos[0]+1][self.pos[1]]:
                self.struct[self.pos[0] + 1][self.pos[1]] = self.struct[self.pos[0]+1][self.pos[1]].replace(MUR_CASSE,"")
                # si extoplasme dans le mur

                ennemies_at = find_ennemy_at_with_type(self.ennemies, GHOST, [self.pos[0] + 1, self.pos[1]]) +\
                              find_ennemy_at_with_type(self.ennemies, STUPID_GHOST, [self.pos[0]+1, self.pos[1]])
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        ennemy.update_life(-1)
            # si il y a un ennemy
            else:
                ennemies_at = [ennemy for ennemy in self.ennemies if ennemy.pos == [self.pos[0] + 1, self.pos[1]]]
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        if ennemy.type == FIREBALL:
                            self.update_life(-1)
                        ennemy.update_life(-1)


        elif (dir == UP) and (self.pos[0] > 0):
            if [chose for chose in self.struct[self.pos[0]-1][self.pos[1]] if chose in TANGIBLE] == []:
                self.struct[self.pos[0]][self.pos[1]] =  self.struct[self.pos[0]][self.pos[1]].replace(HERO, "")
                self.pos[0] -= 1
                self.struct[self.pos[0]][self.pos[1]] += HERO
            elif MUR in self.struct[self.pos[0]-1][self.pos[1]]:
                self.struct[self.pos[0] - 1][self.pos[1]] = self.struct[self.pos[0]-1][self.pos[1]].replace(MUR,MUR_CASSE)
                # si extoplasme dans le mur
                ennemies_at = find_ennemy_at_with_type(self.ennemies, GHOST, [self.pos[0] - 1, self.pos[1]]) +\
                              find_ennemy_at_with_type(self.ennemies, STUPID_GHOST, [self.pos[0]-1,self.pos[1]])
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        ennemy.update_life(-1)
            elif MUR_CASSE in self.struct[self.pos[0]-1][self.pos[1]]:
                self.struct[self.pos[0] - 1][self.pos[1]] = self.struct[self.pos[0]-1][self.pos[1]].replace(MUR_CASSE,"")
                # si extoplasme dans le mur
                ennemies_at = find_ennemy_at_with_type(self.ennemies, GHOST, [self.pos[0] - 1, self.pos[1]]) +\
                              find_ennemy_at_with_type(self.ennemies, STUPID_GHOST, [self.pos[0]-1,self.pos[1]])
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        if ennemy.type == FIREBALL:
                            self.update_life(-1)
                        ennemy.update_life(-1)
            else:
                # si il y a un ennemy
                ennemies_at = [ennemy for ennemy in self.ennemies if ennemy.pos == [self.pos[0] - 1, self.pos[1]]]
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        if ennemy.type == FIREBALL:
                            self.update_life(-1)
                        ennemy.update_life(-1)

        elif (dir == RIGHT) and (self.pos[1] < self.struct_size-1):

            if [chose for chose in self.struct[self.pos[0]][self.pos[1]+1] if chose in TANGIBLE] == []:
                self.struct[self.pos[0]][self.pos[1]] =  self.struct[self.pos[0]][self.pos[1]].replace(HERO, "")
                self.pos[1] += 1
                self.struct[self.pos[0]][self.pos[1]] += HERO
            elif MUR in self.struct[self.pos[0]][self.pos[1]+1]:
                self.struct[self.pos[0]][self.pos[1] + 1] = self.struct[self.pos[0]][self.pos[1]+1].replace(MUR,MUR_CASSE)
                # si extoplasme dans le mur
                ennemies_at = find_ennemy_at_with_type(self.ennemies, GHOST, [self.pos[0], self.pos[1]+1]) +\
                              find_ennemy_at_with_type(self.ennemies, STUPID_GHOST, [self.pos[0], self.pos[1]+1])
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        ennemy.update_life(-1)
            elif MUR_CASSE in self.struct[self.pos[0]][self.pos[1]+1]:
                self.struct[self.pos[0]][self.pos[1] + 1] = self.struct[self.pos[0]][self.pos[1]+1].replace(MUR_CASSE,"")
                # si extoplasme dans le mur
                ennemies_at = find_ennemy_at_with_type(self.ennemies, GHOST, [self.pos[0], self.pos[1]+1]) +\
                              find_ennemy_at_with_type(self.ennemies, STUPID_GHOST, [self.pos[0], self.pos[1]+1])
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        ennemy.update_life(-1)
            else:
                # si il y a un ennemy
                ennemies_at = [ennemy for ennemy in self.ennemies if ennemy.pos == [self.pos[0], self.pos[1]+1]]
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        for ennemy in ennemies_at:
                            if ennemy.type == FIREBALL:
                                self.update_life
                        ennemy.update_life(-1)

        elif (dir == LEFT) and (self.pos[1] > 0):
            if [chose for chose in self.struct[self.pos[0]][self.pos[1]-1] if chose in TANGIBLE] == []:
                self.struct[self.pos[0]][self.pos[1]] =  self.struct[self.pos[0]][self.pos[1]].replace(HERO,"")
                self.pos[1] -= 1
                self.struct[self.pos[0]][self.pos[1]] += HERO
            elif MUR in self.struct[self.pos[0]][self.pos[1]-1]:
                self.struct[self.pos[0]][self.pos[1] - 1] = self.struct[self.pos[0]][self.pos[1]-1].replace(MUR,MUR_CASSE)
                # si extoplasme dans le mur
                ennemies_at = find_ennemy_at_with_type(self.ennemies, GHOST, [self.pos[0], self.pos[1]-1]) +\
                              find_ennemy_at_with_type(self.ennemies, STUPID_GHOST, [self.pos[0], self.pos[1]-1])
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        ennemy.update_life(-1)
            elif MUR_CASSE in self.struct[self.pos[0]][self.pos[1]-1]:
                self.struct[self.pos[0]][self.pos[1] - 1] = self.struct[self.pos[0]][self.pos[1]-1].replace(MUR_CASSE,"")
                # si extoplasme dans le mur
                ennemies_at = find_ennemy_at_with_type(self.ennemies, GHOST, [self.pos[0], self.pos[1] - 1]) + \
                              find_ennemy_at_with_type(self.ennemies, STUPID_GHOST, [self.pos[0], self.pos[1] - 1])
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        ennemy.update_life(-1)
            else:
                # si il y a un ennemy
                ennemies_at = [ennemy for ennemy in self.ennemies if ennemy.pos == [self.pos[0], self.pos[1]-1]]
                if ennemies_at != []:
                    for ennemy in ennemies_at:
                        if ennemy.type == FIREBALL:
                            self.update_life
                        ennemy.update_life(-1)

        self.maj_image(dir)

        if SORTIE in self.struct[self.pos[0]][self.pos[1]]:
            self.level += 1

    def update_life(self, diff):
        self.life += diff
        if self.life > 5:
            self.life = 5
        if self.life < 0:
            self.life = 0


class StupidGhost(Personnage):

    def __init__(self, coord, niveau, image_name, life, ennemies, mode):
        super().__init__(coord, niveau, image_name, life, ennemies, mode)
        self.type = STUPID_GHOST
        self.ennemies.append(self)

    def move(self, hero):
        mvt_possible = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if self.pos[0] == 0:
            mvt_possible.remove((-1, 0))
        elif self.pos[0] == self.struct_size - 1:
            mvt_possible.remove((1, 0))

        if self.pos[1] == 0:
            mvt_possible.remove((0, -1))
        elif self.pos[1] == self.struct_size - 1:
            mvt_possible.remove((0, 1))

        if mvt_possible:
            mvt = mvt_possible[random.randrange(len(mvt_possible))]

            self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(STUPID_GHOST, "")

            if hero.pos == [self.pos[0]+mvt[0], self.pos[1]+mvt[1]]:
                hero.update_life(-1)
            # on maj si y a vraiment rien de tangible en face
            elif [chose for chose in self.struct[self.pos[0] + mvt[0]][self.pos[1] + mvt[1]] if chose in TANGIBLE_FOR_GHOST] == []:
                self.pos[0] += mvt[0]
                self.pos[1] += mvt[1]

            self.struct[self.pos[0]][self.pos[1]] += STUPID_GHOST

    def update_life(self, diff):
        self.life += diff
        if self.life <= 0:
            self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(STUPID_GHOST, "")
            self.ennemies.remove(self)


class Ghost(Personnage):

    def __init__(self, coord, niveau, image_name, life, ennemies, mode):
        super().__init__(coord, niveau, image_name, life, ennemies, mode)
        self.type = GHOST
        self.ennemies.append(self)

    def move(self, hero):
        mvt = [0,0]
        if self.pos[0] < hero.pos[0]:
            mvt = [1, 0]
        elif self.pos[0] > hero.pos[0]:
            mvt = [-1, 0]
        elif self.pos[1] < hero.pos[1]:
            mvt = [0, 1]
        elif self.pos[1] > hero.pos[1]:
            mvt = [0, -1]

        self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(GHOST, "")

        if hero.pos == [self.pos[0]+mvt[0], self.pos[1]+mvt[1]]:
            hero.update_life(-1)
        # on maj si y a vraiment rien de tangible en face
        elif [chose for chose in self.struct[self.pos[0]+mvt[0]][self.pos[1]+mvt[1]] if chose in TANGIBLE_FOR_GHOST] == []:
            self.pos[0] += mvt[0]
            self.pos[1] += mvt[1]
        self.struct[self.pos[0]][self.pos[1]] += GHOST

    def update_life(self, diff):
        self.life += diff
        if self.life <= 0:
            self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(self.type, "")
            self.ennemies.remove(self)


class Orc(Personnage):

    def __init__(self, coord, niveau, image_name, life, ennemies, mode):
        super().__init__(coord, niveau, image_name, life, ennemies, mode)
        self.type = ORC
        self.ennemies.append(self)

    def move(self, hero):
        if (abs(hero.pos[0]-self.pos[0]) <= 1) and (abs(hero.pos[1]-self.pos[1]) <= 1):
            mvt_possible = [(hero.pos[0]-self.pos[0], hero.pos[1]-self.pos[1])]
        else:
            mvt_possible = [(i,j) for i in range(-1,2) for j in range(-1,2)]
            mvt_possible.remove((0,0))

            mvt_possible_copy = [m for m in mvt_possible]
            tangible_possible = [t for t in TANGIBLE if t != HERO]
            for mvt in mvt_possible_copy:
                if (self.pos[0]+mvt[0] > self.struct_size-1) or (self.pos[0]+mvt[0] < 0) or (self.pos[1]+mvt[1] < 0) or \
                   (self.pos[1] + mvt[1] > self.struct_size - 1):
                    mvt_possible.remove(mvt)
                elif [chose for chose in self.struct[self.pos[0]+mvt[0]][self.pos[1]+mvt[1]] if chose in tangible_possible] != []:
                        mvt_possible.remove(mvt)

        # print(mvt_possible)
        if mvt_possible:

            mvt = mvt_possible[random.randrange(len(mvt_possible))]

            self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(ORC, "")

            if hero.pos == [self.pos[0]+mvt[0], self.pos[1]+mvt[1]]:
                hero.update_life(-1)
            # on maj si y a vraiment rien de tangible en face
            elif [chose for chose in self.struct[self.pos[0] + mvt[0]][self.pos[1] + mvt[1]] if chose in TANGIBLE] == []:
                self.pos[0] += mvt[0]
                self.pos[1] += mvt[1]

            self.struct[self.pos[0]][self.pos[1]] += ORC

    def update_life(self, diff):
        self.life += diff
        if self.life <= 0:
            self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(self.type, "")
            self.ennemies.remove(self)

class FireBall(Personnage):
    def __init__(self, coord, niveau, image_name, life, ennemies, mode, hero):
        self.surface = pygame.image.load(os.path.join(mode, "case", image_name)).convert_alpha()
        self.struct = niveau.structure
        self.struct_size = niveau.size
        self.pos = coord
        self.life = life
        self.ennemies = ennemies
        self.image_name = image_name
        self.mode = mode
        self.type = FIREBALL
        self.dir = None
        self.ennemies.append(self)
        self.struct[self.pos[0]][self.pos[1]] += FIREBALL
        if HERO in self.struct[self.pos[0]][self.pos[1]]:
            hero.update_life(-1)
            self.update_life(-1)

    def maj_mode(self, mode):
        self.mode = mode
        self.image_path = os.path.join(mode, "case", self.image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()

    def move(self, hero):
        if self.dir == RIGHT:
            mvt = (0, 1)
        elif self.dir == UP:
            mvt = (-1, 0)
        elif self.dir == LEFT:
            mvt = (0, -1)
        else:
            mvt = (1, 0)

        tangible_possible = [t for t in TANGIBLE if t != HERO]
        if (self.pos[0] + mvt[0] in list(range(self.struct_size))) and (
                (self.pos[1] + mvt[1] in list(range(self.struct_size)))):
            if [chose for chose in self.struct[self.pos[0] + mvt[0]][self.pos[1] + mvt[1]] if chose in tangible_possible] != []:
                self.update_life(-1)
            elif HERO in self.struct[self.pos[0] + mvt[0]][self.pos[1] + mvt[1]]:
                hero.update_life(-1)
                self.update_life(-1)
            else:
                self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(FIREBALL,"")
                self.pos[0] += mvt[0]
                self.pos[1] += mvt[1]
                self.struct[self.pos[0]][self.pos[1]] += FIREBALL
        else:
            self.update_life(-1)

    def update_life(self, diff):
        self.life += diff
        if self.life <= 0:
            self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(self.type, "")
            self.ennemies.remove(self)

class Turret(Personnage):

    def __init__(self, coord, niveau, image_name, life, ennemies, mode):
        super().__init__(coord, niveau, image_name, life, ennemies, mode)
        self.type = TURRET
        self.dir = RIGHT
        self.ennemies.append(self)
        self.firegun_hot = True
        self.niveau = niveau

    def maj_image(self, dir):
        self.image_name = 'turret_'+ dir + '.png'
        self.image_path = os.path.join(self.mode, 'case', self.image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()

    def move(self, hero):
        if self.firegun_hot:
            self.firegun_hot = False
            if self.dir == RIGHT:
                self.dir = UP
                self.maj_image(self.dir)
            elif self.dir == UP:
                self.dir = LEFT
                self.maj_image(self.dir)
            elif self.dir == LEFT:
                self.dir = DOWN
                self.maj_image(self.dir)
            else:
                self.dir = RIGHT
                self.maj_image(self.dir)
        else:
            self.firegun_hot = True
            self.shot_fireball(self.dir, hero)

    def shot_fireball(self, dir, hero):
        if dir == RIGHT:
            fireball_pos = [self.pos[0], self.pos[1] + 1]
        elif dir == LEFT:
            fireball_pos = [self.pos[0], self.pos[1] - 1]
        elif dir == UP:
            fireball_pos = [self.pos[0]-1, self.pos[1]]
        elif dir == DOWN:
            fireball_pos = [self.pos[0]+1, self.pos[1]]

        if (fireball_pos[0] in list(range(self.struct_size))) and ((fireball_pos[1] in list(range(self.struct_size)))):
            tangible_possible = [t for t in TANGIBLE if t != HERO]
            f = FireBall(fireball_pos, self.niveau, "fireball.png", 1, self.ennemies, self.mode, hero)
            f.dir = dir

    def update_life(self, diff):
        self.life += diff
        if self.life <= 0:
            self.struct[self.pos[0]][self.pos[1]] = self.struct[self.pos[0]][self.pos[1]].replace(self.type, "")
            self.ennemies.remove(self)


class Niveau:
    """Classe permettant de créer un niveau"""

    def __init__(self, ratio_murs, size, direction_in, nb_out, nb_stupid_ghost, nb_ghost, nb_orc, nb_turret):
        self.size = size
        self.ratio_murs = ratio_murs
        self.direction_in = direction_in
        self.coord_sorties = []

        # choix de la coord de départ
        random_depart = random.randrange(1,size-1)
        if direction_in == UP:
            self.coord_depart = [0, random_depart]
        elif direction_in == DOWN:
            self.coord_depart = [size-1, random_depart]
        elif direction_in == RIGHT:
            self.coord_depart = [random_depart, size - 1]
        elif direction_in == LEFT:
            self.coord_depart = [random_depart, 0]

        self.position_busy = [self.coord_depart]
        self.set_out(nb_out)
        self.generer()
        self.set_orc(nb_orc)
        self.set_turret(nb_turret)
        self.set_stupid_ghost(nb_stupid_ghost)
        self.set_ghost(nb_ghost)

    def set_turret(self, nb):
        for i in range(nb):
            coord = self.coord_depart
            while coord in self.position_busy or (self.structure[coord[0]][coord[1]] == MUR):
                coord = [random.randrange(self.size), random.randrange(self.size)]
            self.position_busy.append(coord)
            self.structure[coord[0]][coord[1]] += TURRET

    def set_stupid_ghost(self, nb):
        for i in range(nb):
            coord = self.coord_depart
            while coord in self.position_busy:
                coord = [random.randrange(self.size), random.randrange(self.size)]
            self.position_busy.append(coord)
            self.structure[coord[0]][coord[1]] += STUPID_GHOST

    def set_ghost(self, nb):
        for i in range(nb):
            coord = self.coord_depart
            while coord in self.position_busy:
                coord = [random.randrange(self.size), random.randrange(self.size)]
            self.position_busy.append(coord)
            self.structure[coord[0]][coord[1]] += GHOST

    def set_orc(self, nb):
        for i in range(nb):
            coord = self.coord_depart
            while coord in self.position_busy or (self.structure[coord[0]][coord[1]] == MUR):
                coord = [random.randrange(self.size), random.randrange(self.size)]
            self.position_busy.append(coord)
            self.structure[coord[0]][coord[1]] += ORC

    def set_out(self, nb_out):
        """
        ajoute nb_out sorties, (1 ou 2)
        """
        if nb_out > 0:
            random_out1 = random.randrange(1, self.size - 1)
            if self.direction_in == UP:
                self.coord_sorties.append([self.size - 1, random_out1])
            if self.direction_in == DOWN:
                self.coord_sorties.append([0, random_out1])
            if self.direction_in == RIGHT:
                self.coord_sorties.append([random_out1, 0])
            if self.direction_in == LEFT:
                self.coord_sorties.append([random_out1, self.size - 1])

        if nb_out > 1:
            random_out2 = random.randrange(1, self.size - 1)
            if self.direction_in == RIGHT:
                self.coord_sorties.append([self.size - 1, random_out2])
            if self.direction_in == LEFT:
                self.coord_sorties.append([0, random_out2])
            if self.direction_in == DOWN:
                self.coord_sorties.append([random_out2, 0])
            if self.direction_in == UP:
                self.coord_sorties.append([random_out2, self.size - 1])
        # print(self.coord_sorties)

    def generer(self):
        structure_niveau = [["" for i in range(self.size)] for j in range(self.size)]

        for i_line in range(self.size):
            for i_cell in range(self.size):
                if random.randrange(100) <= self.ratio_murs:
                    structure_niveau[i_line][i_cell] = MUR

                if [i_line, i_cell] == self.coord_depart:
                    structure_niveau[i_line][i_cell] = DEPART + HERO

                if [i_line, i_cell] in self.coord_sorties:
                    structure_niveau[i_line][i_cell] = SORTIE

        self.structure = structure_niveau

    def afficher(self, fenetre, hero, ennemies, mode):
        """Méthode permettant d'afficher le niveau en fonction 
        de la liste de structure renvoyée par generer()"""
        mur = pygame.image.load(os.path.join(mode, "case", "mur.png")).convert_alpha()
        mur_casse = pygame.image.load(os.path.join(mode, "case", "mur_casse.png")).convert_alpha()
        depart = pygame.image.load(os.path.join(mode, "case", "depart.png")).convert_alpha()
        sortie = pygame.image.load(os.path.join(mode, "case", "sortie.png")).convert_alpha()


        # On parcourt la liste du niveau
        for i_line, line in enumerate(self.structure):
            # On parcourt les listes de lignes
            for i_cell, cell in enumerate(line):
                x = i_cell * CELL_SIZE[0] + DEP_CASE[0]
                y = i_line * CELL_SIZE[1] + DEP_CASE[1]
                if MUR in cell:  # M = Mur
                        fenetre.blit(mur, (x, y))
                if MUR_CASSE in cell:  # m = Mur cassé
                    fenetre.blit(mur_casse, (x, y))
                if DEPART in cell:  # D = Départ
                    fenetre.blit(depart, (x, y))
                if SORTIE in cell:  # S = Sortie
                    fenetre.blit(sortie, (x, y))
                if HERO in cell:  # p = perso
                    fenetre.blit(hero.surface, (x, y))
                if STUPID_GHOST in cell:
                    for ennemy in find_ennemy_at_with_type(ennemies, STUPID_GHOST, [i_line, i_cell]):
                        fenetre.blit(ennemy.surface, (x, y))
                if GHOST in cell:
                    for ennemy in find_ennemy_at_with_type(ennemies, GHOST, [i_line, i_cell]):
                        fenetre.blit(ennemy.surface, (x, y))
                if ORC in cell:
                    for ennemy in find_ennemy_at_with_type(ennemies, ORC, [i_line, i_cell]):
                        fenetre.blit(ennemy.surface, (x, y))
                if TURRET in cell:
                    for ennemy in find_ennemy_at_with_type(ennemies, TURRET, [i_line, i_cell]):
                        fenetre.blit(ennemy.surface, (x, y))
                if FIREBALL in cell:
                    for ennemy in find_ennemy_at_with_type(ennemies, FIREBALL, [i_line, i_cell]):
                        fenetre.blit(ennemy.surface, (x, y))

    def __str__(self):
        return("\n".join([str(ligne) for ligne in self.structure]))

def update_graph(hero, score, score_retenue, surfaces):

    # Points
    surfaces= [surface for surface in surfaces if not surface.image_name == "point.png"]
    Background("point_back.png", (SCORE_POS[0] - 20, SCORE_POS[1] - 320), screen, surfaces, global_mode)
    memoir_score = score
    if score < 0:
        new_score = 0
    else:
        new_score = max(score, score_retenue * 100 + 1)
    score_jauge = score % 100

    for point in range(1,score_jauge+1):
        if point % 10:
            Background("1point.png", (SCORE_POS[0], SCORE_POS[1] - 3 * point), screen, surfaces, global_mode)
        else:
            Background("10point.png", (SCORE_POS[0], SCORE_POS[1] - 3 * point), screen, surfaces, global_mode)

    memoir_score_retenue = score_retenue
    new_score_retenue = max([score_retenue, score // 100])
    if new_score_retenue > memoir_score_retenue:
        hero.update_life(+1)

    # Vie
    surfaces = [surface for surface in surfaces if not surface.image_name.startswith("vie")]
    Background("vie_back.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 1:
        Background("vie_1.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 2:
        Background("vie_2.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 3:
        Background("vie_3.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 4:
        Background("vie_4.png", LIFE_POS, screen, surfaces, global_mode)
    if hero.life >= 5:
        Background("vie_5.png", LIFE_POS, screen, surfaces, global_mode)

    return surfaces, new_score_retenue, new_score



def init_level(scr, surf, lvl):
    surf = [s for s in surf if (s.image_name != "bordure.png") and (s.image_name != "floor.png")]
    # Initialisation des bordures du niveau
    for i in range(lvl.size + 2):
        if (i == 0) or (i == lvl.size + 1):
            for j in range(lvl.size + 2):
                Background("bordure.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]),
                     scr, surf, global_mode)
        else:
            for j in [0, lvl.size + 1]:
                Background("bordure.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]),
                     scr,
                     surf, global_mode)
            for j in range(1, lvl.size + 1):
                Background("floor.png", (DEP_BORDER_CASE[0] + i * CELL_SIZE[0], DEP_BORDER_CASE[1] + j * CELL_SIZE[1]),
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
                h = Hero([lin, col], lvl, "hero-down.png", life, ennem, global_mode)
                h.level = old_lvl
            elif STUPID_GHOST in case:
                StupidGhost([lin, col], lvl, "stupid_ghost.png", 1, ennem, global_mode)
            elif GHOST in case:
                Ghost([lin, col], lvl, "ghost.png", 1, ennem, global_mode)
            elif ORC in case:
                Orc([lin, col], lvl, "orc.png", 1, ennem, global_mode)
            elif TURRET in case:
                Turret([lin, col], lvl, "turret_right.png", 1, ennem, global_mode)

    return h, ennem


def update(liste, niveau, enemies):
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


pygame.init()

# list of surfaces
surfaces = []

# set window and background
screen = pygame.display.set_mode((1440, 874), RESIZABLE)


background = Background("accueil.png", (0,0), screen, surfaces, global_mode)

level = Niveau(LVL[1][0], LVL[1][1], LVL[1][2], LVL[1][3], LVL[1][4], LVL[1][5], LVL[1][6], LVL[1][7])

old_level = 1
surfaces = init_level(screen, surfaces, level)
hero, ennemies = init_personnage(level, old_level, 5)


score = 25
score_retenue = 0
surfaces, score_retenue, score = update_graph(hero, score, score_retenue, surfaces)

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
         pygame.K_SPACE: SPACE
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
            score -= 1
            last_key_pressed = time.time()

            if dir in [RIGHT, LEFT, DOWN, UP]:
                nb_ennemies = len(ennemies)
                hero.move(dir)

                if len(ennemies) < nb_ennemies:
                    score += 11

                for ennemy in set(ennemies):
                    ennemy.move(hero)

                if hero.life == 0:
                    print('GAME OVER')
                    playable = False
                    hero.image_name = "hero-dead.png"
                    hero.surface = pygame.image.load(os.path.join(global_mode, "case", 'hero-dead.png')).convert_alpha()
                    Background("game-over.jpg", GAME_OVER_POS, screen, surfaces, global_mode)
                    # display first image in cachedeque
                    # screen.blit(cachedeque[0], rect)
                surfaces, score_retenue, score = update_graph(hero, score, score_retenue, surfaces)

                update(surfaces, level, ennemies)
                if hero.level > old_level:
                    score += 26
                    old_level = hero.level
                    print('Level Up')
                    path = os.path.join(global_mode, "background", "level-up.png")
                    screen.blit(pygame.image.load(path).convert_alpha(), (DEP_CASE[0]+CELL_SIZE[0]*(int(level.size/2)-1),
                                                                          DEP_CASE[1] + CELL_SIZE[1] * (int(level.size/2)-1)))
                    myfont = pygame.font.SysFont("monospace", 40)
                    label2 = myfont.render(str(hero.level), 1, (20, 40, 20))
                    screen.blit(label2, (33 + DEP_CASE[0]+CELL_SIZE[0]*(int(level.size/2)-1),
                                        32 + DEP_CASE[1] + CELL_SIZE[1] * (int(level.size/2)-1)))

                    pygame.display.flip()
                    time.sleep(2)
                    l = hero.level
                    try:
                        level = Niveau(LVL[l][0], LVL[l][1], LVL[l][2], LVL[l][3], LVL[l][4], LVL[l][5], LVL[l][6], LVL[l][7])
                    except KeyError:
                        Background("gagne.jpg", GAME_OVER_POS, screen, surfaces, global_mode)
                        playable = False
                    else:
                        surfaces = init_level(screen, surfaces, level)
                        hero, ennemies = init_personnage(level, old_level, hero.life)
                    update(surfaces, level, ennemies)
            elif dir == SPACE:
                background.surface = pygame.image.load(os.path.join(global_mode, "background", "accueil.png")).convert_alpha()
                playable = False
                update_background(background, screen)

    else:
        if key and (dir == OUI) and (time.time() - last_key_pressed >= 0.2):
            last_key_pressed = time.time()
            old_level = 1
            level = Niveau(LVL[1][0], LVL[1][1], LVL[1][2], LVL[1][3], LVL[1][4], LVL[1][5], LVL[1][6], LVL[1][7])
            playable = True
            score = 25
            surfaces = [s for s in surfaces if s.image_name != "game-over.jpg" and s.image_name != "gagne.jpg"]
            surfaces = init_level(screen, surfaces, level)
            hero, ennemies =init_personnage(level, old_level, 5)
            hero.life = 5
            surfaces, score_retenue, score = update_graph(hero, score, score_retenue, surfaces)
            update(surfaces, level, ennemies)
        elif key and (dir == NON) and (time.time() - last_key_pressed >= 0.2):
            last_key_pressed = time.time()
            quit=True
        elif key and (dir == SPACE) and (time.time() - last_key_pressed >= 0.2):
            last_key_pressed = time.time()
            background.image_name = "bg-excel.png"
            background.image_path = os.path.join(global_mode, "background", "bg-excel.png")
            background.surface = pygame.image.load(background.image_path).convert_alpha()
            playable = True
            update_background(background, screen)
            update(surfaces, level, ennemies)






