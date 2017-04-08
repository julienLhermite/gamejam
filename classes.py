import os
import pygame
from const import *
import random

random.seed()

class Papa:
    def __init__(self, image_name, coord, screen, surfaces):
        self.surface = pygame.image.load(os.path.join("images", "case", image_name)).convert()
        self.screen = screen
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(coord[0], coord[1])
        surfaces.append(self)

class Back:
    def __init__(self, image_name, coord, screen, surfaces):
        self.surface = pygame.image.load(os.path.join("images", "background", image_name)).convert()
        self.screen = screen
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(coord[0], coord[1])
        surfaces.append(self)

class Perso(Papa):

    def __init__(self, image_name, coord, screen, surfaces):
        Papa.__init__(self, image_name, coord, screen, surfaces)

    def move(self, dir):
        if dir == DOWN:
            self.rect = self.rect.move(0, 25)
        elif dir == UP:
            self.rect = self.rect.move(0, -25)
        elif dir == RIGHT:
            self.rect = self.rect.move(25, 0)
        elif dir == LEFT:
            self.rect = self.rect.move(-25, 0)

class Niveau:
    """Classe permettant de créer un niveau"""


    def __init__(self, ratio_murs, size, coord_depart):
        self.size = size
        self.coord_depart = (coord_depart)
        self.ratio_mur = ratio_murs


        structure_niveau = [["" for i in range(size)] for j in range(size)]

        for i_line in range(size):
            for i_cell in range(size):
                print(i_line, i_cell)
                if random.randrange(100) <= ratio_murs:
                    structure_niveau[i_line][i_cell] = "M"

                if [i_line, i_cell] == coord_depart:
                    structure_niveau[i_line][i_cell] = "DP"



            for line in structure_niveau:
                print(line)
        self.structure = structure_niveau

    def afficher(self, fenetre, perso):
        """Méthode permettant d'afficher le niveau en fonction 
        de la liste de structure renvoyée par generer()"""
        mur = pygame.image.load(os.path.join("images", "case", "mur.png")).convert()
        depart = pygame.image.load(os.path.join("images", "case", "depart.png")).convert()

        # On parcourt la liste du niveau
        for i_line, line in enumerate(self.structure):
            # On parcourt les listes de lignes
            for i_cell, cell in enumerate(line):
                x = i_cell * CELL_SIZE[0] + DEPP_CASE[0]
                y = i_line * CELL_SIZE[1] + DEPP_CASE[1]
                if "M" in cell:  # m = Mur
                    print("hey")
                    fenetre.blit(mur, (x, y))
                if "D" in cell:  # d = Départ
                    fenetre.blit(depart, (x, y))
                if 'P' in cell:  # p = perso
                    fenetre.blit(perso.surface, (x, y))





