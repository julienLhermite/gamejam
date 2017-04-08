import pygame
from pygame.locals import *

# elmt de la bibliothèque
# -display
# -mixer
# -draw
# -event
# -image
# -mouse
# -time


# initialise les modules pygame
pygame.init()

# renvoie un objet de classe surface, pour l'instant surface vierge donc noir
# fenetre = pygame.display.set_mode((640, 480))
fenetre = pygame.display.set_mode((640, 480), FULLSCREEN)

fond = pygame.image.load("background.bmp")
# fond = pygame.image.load("background.bmp").convert()

fenetre.blit(fond, (0,0))
# Variable qui continue la boucle si = 1, stoppe si = 0
continuer = 1

# Boucle infinie
while continuer:
    continue


