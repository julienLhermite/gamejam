#!/usr/local/bin/python3.5
# -*- coding: <encoding name> -*-

import os
import pygame
from const import *
# from outils import find_ennemy_at_with_type
import random

random.seed()

def find_ennemy_at(ennemies, pos):
    """
    Retourne l'ennemie qui occupe la position pos
    :param ennemies: liste des ennemies
    :param pos: positon recherché
    :return: liste des ennemies à la position x
    """
    ennemy_at = []
    for ennemy in ennemies:
        if ennemy.pos == pos :
            ennemy_at.append(ennemy)
    return ennemy_at


def find_ennemy_at_with_type(ennemies, ennemy_type, pos):
    """
    Retourne l'ennemie qui occupe la position pos
    :param ennemies: liste des ennemies
    :param pos: positon recherché
    :param ennemy_type: le type de l'ennemie
    :return: liste des ennemies à la position pos avec le type ennemy_time
    """
    ennemy_at_with = []
    for ennemy in ennemies:
        if (ennemy.pos == pos) and (ennemy_type == ennemy.type):
            ennemy_at_with.append(ennemy)
    return ennemy_at_with


class Background():
    """
    Les objets de la classe Background sont des éléments du décors
    """
    def __init__(self, image_name, coord, screen, surfaces, mode):
        """
        :param image_name: le nom de l'image associé
        :param coord: la coordonnée
        :param screen: l'écran sur lequel s'afficher
        :param surfaces: la surface pygame associé
        :param mode: le mode d'affichage graphique ou non
        """
        self.image_name = image_name
        self.image_path = os.path.join(mode, "background", image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()
        self.screen = screen
        self.rect = self.surface.get_rect()
        self.coord = coord
        self.rect = self.rect.move(coord[0], coord[1])
        surfaces.append(self)

    def maj_mode(self, mode):
        """
        Change le mode d'affichage
        :param mode: le mode d'affichage
        """
        self.mode = mode
        self.image_path = os.path.join(mode, "background", self.image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()


class Personnage:
    """
    Classe parente à tous les personnages
    """
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
        """
        Change le mode d'affichage
        :param mode: le mode d'affichage
        """
        self.mode = mode
        self.image_path = os.path.join(mode, "case", self.image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()

    def move(self):
        """
        Méthode à overwrite pour chaque type de personage
        """
        pass

    def update_life(self):
        """
        Méthode à overwrite pour chaque type de personage   "
        """
        pass


class Hero(Personnage):

    def __init__(self, coord, niveau, image_name, life, ennemies, mode):
        super().__init__(coord, niveau, image_name, life, ennemies, mode)
        self.level = 1

    def maj_image(self, dir):
        self.image_name = 'hero-'+ dir + '.png'
        self.image_path = os.path.join(self.mode, 'case', self.image_name)
        self.surface = pygame.image.load(self.image_path).convert_alpha()

    def move(self, dir):
        if dir == UP:
            mv = (-1, 0)
        elif dir == DOWN:
            mv = (1, 0)
        elif dir == LEFT:
            mv = (0, -1)
        elif dir == RIGHT:
            mv = (0, 1)

        next_case_coord = [self.pos[0] + mv[0], self.pos[1] + mv[1]]
        # si la case ou l'on va existe
        if (next_case_coord[0] in range(self.struct_size)) and (next_case_coord[1] in range(self.struct_size)):
            # si rien de tangible sur la case ou on va
            if not [chose for chose in self.struct[next_case_coord[0]][next_case_coord[1]] if chose in TANGIBLE]:
                self.struct[self.pos[0]][self.pos[1]] = self.struct[next_case_coord[0]][next_case_coord[1]]\
                                                                                       .replace(HERO, "")

                self.pos[0] += mv[0]
                self.pos[1] += mv[1]
                self.struct[self.pos[0]][self.pos[1]] += HERO

            else:
                print(self.ennemies)
                ennemies_at = find_ennemy_at(self.ennemies, next_case_coord)
                print("ennemies", ennemies_at)
                # si mur on le casse un peu
                if MUR in self.struct[self.pos[0] + mv[0]][self.pos[1] + mv[1]]:
                    self.struct[next_case_coord[0]][next_case_coord[1]] = self.struct[next_case_coord[0]][next_case_coord[1]] \
                                                                .replace(MUR, MUR_CASSE)
                    # si extoplasme dans le mur
                    if (GHOST or STUPID_GHOST) in [e.type for e in ennemies_at]:
                        for e in ennemies_at:
                            e.update_life(-1)

                # si mur cassé il dipsarait
                elif MUR_CASSE in self.struct[self.pos[0] + mv[0]][self.pos[1] + mv[1]]:
                    self.struct[next_case_coord[0]][next_case_coord[1]] = self.struct[next_case_coord[0]][
                                                                                      next_case_coord[1]] \
                                                                                      .replace(MUR_CASSE, "")
                    # si extoplasme dans le mur
                    if (GHOST or STUPID_GHOST) in [e.type for e in ennemies_at]:
                        for e in ennemies_at:
                            e.update_life(-1)

                else:
                    for e in ennemies_at:
                        print("je tue")
                        if e.type == FIREBALL:
                            self.update_life(-1)
                        e.update_life(-1)

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
