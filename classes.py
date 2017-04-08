import os
import pygame
from const import *
import random

random.seed()


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
                if 'D' in self.struct[lin][col]:
                    self.pos = [lin, col]
                    break

    def move(self, dir):
        if (dir == DOWN) and (self.pos[0] < self.struct_size-1):
            self.struct[self.pos[0]][self.pos[1]].replace("P","")
            self.pos[0] += 1
            self.struct[self.pos[0]][self.pos[1]] += "P"

        elif (dir == UP) and (self.pos[0] > 0):
            self.struct[self.pos[0]][self.pos[1]].replace("P","")
            self.pos[0] -= 1
            self.struct[self.pos[0]][self.pos[1]] += "P"

        elif (dir == RIGHT) and (self.pos[1] < self.struct_size-1):
            self.struct[self.pos[0]][self.pos[1]].replace("P","")
            self.pos[1] += 1
            self.struct[self.pos[0]][self.pos[1]] += "P"

        elif (dir == LEFT) and (self.pos[1] > 0):
            self.struct[self.pos[0]][self.pos[1]].replace("P","")
            self.pos[1] -= 1
            self.struct[self.pos[0]][self.pos[1]] += "P"

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





