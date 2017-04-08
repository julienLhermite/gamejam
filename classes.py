import os
import pygame
from const import *
import random

random.seed()


class Back:
    def __init__(self, image_name, coord, screen, surfaces):
        self.surface = pygame.image.load(os.path.join("images", "background", image_name)).convert()
        self.screen = screen
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(coord[0], coord[1])
        surfaces.append(self)


class Perso():

    def __init__(self, niveau, image_name):
        self.surface = pygame.image.load(os.path.join("images", "case", image_name)).convert()
        self.struct = niveau.structure
        self.struct_size = niveau.size
        self.pos = None
        for lin in range(len(self.struct)):
            if self.pos:
                break
            for col in range(len(self.struct[0])):
                if DEPART in self.struct[lin][col]:
                    self.pos = [lin, col]
                    break

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
            elif MUR_CASSE in self.struct[self.pos[0]+1][self.pos[1]]:
                self.struct[self.pos[0] + 1][self.pos[1]] = self.struct[self.pos[0]+1][self.pos[1]].replace(MUR_CASSE,"")


        elif (dir == UP) and (self.pos[0] > 0):
            if [chose for chose in self.struct[self.pos[0]-1][self.pos[1]] if chose in TANGIBLE] == []:
                self.struct[self.pos[0]][self.pos[1]] =  self.struct[self.pos[0]][self.pos[1]].replace(HERO, "")
                self.pos[0] -= 1
                self.struct[self.pos[0]][self.pos[1]] += HERO
            elif MUR in self.struct[self.pos[0]-1][self.pos[1]]:
                self.struct[self.pos[0] - 1][self.pos[1]] = self.struct[self.pos[0]-1][self.pos[1]].replace(MUR,MUR_CASSE)
            elif MUR_CASSE in self.struct[self.pos[0]-1][self.pos[1]]:
                self.struct[self.pos[0] - 1][self.pos[1]] = self.struct[self.pos[0]-1][self.pos[1]].replace(MUR_CASSE,"")

        elif (dir == RIGHT) and (self.pos[1] < self.struct_size-1):

            if [chose for chose in self.struct[self.pos[0]][self.pos[1]+1] if chose in TANGIBLE] == []:
                self.struct[self.pos[0]][self.pos[1]] =  self.struct[self.pos[0]][self.pos[1]].replace(HERO, "")
                self.pos[1] += 1
                self.struct[self.pos[0]][self.pos[1]] += HERO
            elif MUR in self.struct[self.pos[0]][self.pos[1]+1]:
                self.struct[self.pos[0]][self.pos[1] + 1] = self.struct[self.pos[0]][self.pos[1]+1].replace(MUR,MUR_CASSE)
            elif MUR_CASSE in self.struct[self.pos[0]][self.pos[1]+1]:
                self.struct[self.pos[0]][self.pos[1] + 1] = self.struct[self.pos[0]][self.pos[1]+1].replace(MUR_CASSE,"")

        elif (dir == LEFT) and (self.pos[1] > 0):
            if [chose for chose in self.struct[self.pos[0]][self.pos[1]-1] if chose in TANGIBLE] == []:
                self.struct[self.pos[0]][self.pos[1]] =  self.struct[self.pos[0]][self.pos[1]].replace(HERO,"")
                self.pos[1] -= 1
                self.struct[self.pos[0]][self.pos[1]] += HERO
            elif MUR in self.struct[self.pos[0]][self.pos[1]-1]:
                self.struct[self.pos[0]][self.pos[1] - 1] = self.struct[self.pos[0]][self.pos[1]-1].replace(MUR,MUR_CASSE)
            elif MUR_CASSE in self.struct[self.pos[0]][self.pos[1]-1]:
                self.struct[self.pos[0]][self.pos[1] - 1] = self.struct[self.pos[0]][self.pos[1]-1].replace(MUR_CASSE,"")

class Niveau:
    """Classe permettant de créer un niveau"""

    def __init__(self, ratio_murs, size, direction_in):
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
        print(self.coord_sorties)

    def generer(self):
        structure_niveau = [["" for i in range(self.size)] for j in range(self.size)]

        for i_line in range(self.size):
            for i_cell in range(self.size):
                print(i_line, i_cell)
                if random.randrange(100) <= self.ratio_murs:
                    structure_niveau[i_line][i_cell] = MUR

                if [i_line, i_cell] == self.coord_depart:
                    structure_niveau[i_line][i_cell] = DEPART + HERO

                if [i_line, i_cell] in self.coord_sorties:
                    structure_niveau[i_line][i_cell] = SORTIE

            for line in structure_niveau:
                print(line)
        self.structure = structure_niveau

    def afficher(self, fenetre, perso):
        """Méthode permettant d'afficher le niveau en fonction 
        de la liste de structure renvoyée par generer()"""
        mur = pygame.image.load(os.path.join("images", "case", "mur.png")).convert()
        mur_casse = pygame.image.load(os.path.join("images", "case", "mur_casse.png")).convert()
        depart = pygame.image.load(os.path.join("images", "case", "depart.png")).convert()
        sortie = pygame.image.load(os.path.join("images", "case", "sortie.png")).convert()

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
                    fenetre.blit(perso.surface, (x, y))

    def __str__(self):
        return("\n".join([str(ligne) for ligne in self.structure]))
