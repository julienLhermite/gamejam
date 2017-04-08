UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


MUR = "M"
MUR_CASSE = "m"
DEPART = "D"
HERO = "H"
SORTIE = "S"
GHOST = "G"
STUPID_GHOST = "g"



TANGIBLE_FOR_GHOST = [GHOST, STUPID_GHOST, HERO]
TANGIBLE = TANGIBLE_FOR_GHOST + [MUR, MUR_CASSE]

CELL_SIZE = (32, 29)
DEP_CASE = (58, 203)
DEP_BORDER_CASE = (DEP_CASE[0]-CELL_SIZE[0]-3, DEP_CASE[1]-CELL_SIZE[1]-2)

FIRST_CELL_X = 120
FIRST_CELL_Y = 80