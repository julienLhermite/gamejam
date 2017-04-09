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
ORC = "O"
STUPID_GHOST = "g"

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

TANGIBLE_FOR_GHOST = [GHOST, STUPID_GHOST, HERO, ORC]
TANGIBLE = TANGIBLE_FOR_GHOST + [MUR, MUR_CASSE]

CELL_SIZE = (32, 29)
DEP_CASE = (55, 201)
DEP_BORDER_CASE = (DEP_CASE[0]-CELL_SIZE[0], DEP_CASE[1]-CELL_SIZE[1])
GAME_OVER_POS = (DEP_BORDER_CASE[0]+20*CELL_SIZE[0], DEP_BORDER_CASE[1]+CELL_SIZE[1]*2)

FIRST_CELL_X = 120
FIRST_CELL_Y = 80