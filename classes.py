import os
import pygame
from const import *

class Perso:

    def __init__(self, name, image_name,  coord, vie_max, surfaces):
        self.name = name
        self.vie_max = vie_max
        self.vie = vie_max

        self.sprite = pygame.image.load(os.path.join("images", "case", image_name)).convert()
        surfaces.append(self.sprite)
        self.rect = self.sprite.get_rect()
        self.rect = self.rect.move(coord)

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


    def generer(self):
        """Méthode permettant de générer le niveau en fonction du fichier.
        On crée une liste générale, contenant une liste par ligne à afficher"""
        # On ouvre le fichier
        structure_niveau = [[[]]* size ] * size
        # On parcourt les lignes du fichier
        for ligne in fichier:
            ligne_niveau = []
            # On parcourt les sprites (lettres) contenus dans le fichier
            for sprite in ligne:
                # On ignore les "\n" de fin de ligne
                if sprite != '\n':
                    # On ajoute le sprite à la liste de la ligne
                    ligne_niveau.append(sprite)
            # On ajoute la ligne à la liste du niveau
            structure_niveau.append(ligne_niveau)
        # On sauvegarde cette structure
        self.structure = structure_niveau


    def afficher(self, fenetre):
        """Méthode permettant d'afficher le niveau en fonction 
        de la liste de structure renvoyée par generer()"""
        # Chargement des images (seule celle d'arrivée contient de la transparence)
        mur = pygame.image.load(os.path.join("images", "case", "mur.png")).convert()
        depart = pygame.image.load(os.path.join("images", "case", "depart.png")).convert()
        arrivee = pygame.image.load(os.path.join("images", "case", "arrivee.png")).convert_alpha()

        # On parcourt la liste du niveau
        num_ligne = 0
        for ligne in self.structure:
            # On parcourt les listes de lignes
            num_case = 0
            for sprite in ligne:
                # On calcule la position réelle en pixels
                x = num_case * taille_sprite
                y = num_ligne * taille_sprite
                if sprite == 'm':  # m = Mur
                    fenetre.blit(mur, (x, y))
                elif sprite == 'd':  # d = Départ
                    fenetre.blit(depart, (x, y))
                elif sprite == 'a':  # a = Arrivée
                    fenetre.blit(arrivee, (x, y))
                num_case += 1
            num_ligne += 1




