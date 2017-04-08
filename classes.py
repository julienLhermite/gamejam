import os
import pygame
from const import *
import random

random.seed()

class Papa:
    def __init__(self, image_name, coord, screen, surfaces):
        self.surface = pygame.image.load(os.path.join("images", "case", image_name)).convert()
        self.screen = screen
        self.rect = self.sprite.get_rect()
        self.rect = self.rect.move(coord[0], coord[1])
        surfaces.append(self)

class Perso(Papa):

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


    def afficher(self, fenetre):
        """Méthode permettant d'afficher le niveau en fonction 
        de la liste de structure renvoyée par generer()"""
        # Chargement des images (seule celle d'arrivée contient de la transparence)
        mur = pygame.image.load(os.path.join("images", "case", "mur.png")).convert()
        depart = pygame.image.load(os.path.join("images", "case", "depart.png")).convert()
        arrivee = pygame.image.load(os.path.join("images", "case", "arrivee.png")).convert_alpha()

        # On parcourt la liste du niveau
        for i_line, line in enumerate(self.structure):
            # On parcourt les listes de lignes
            for i_cell, cell in enumerate(line):
                x = i_cell * SPRITE_SIZE + FIRST_CELL_X
                y = i_line * SPRITE_SIZE + FIRST_CELL_Y
                if "M" in cell:  # m = Mur
                    fenetre.blit(mur, (x, y))
                if "D" in cell:  # d = Départ
                    fenetre.blit(depart, (x, y))
                if 'P' in cell:  # p = perso
                    fenetre.blit(arrivee, (x, y))





