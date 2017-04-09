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
        2: [10,   9,   RIGHT,    1,        2,              2,       0,      0],
        3: [30,    17,   LEFT,    2,        1,              0,       4,      0],
        4: [85,    10,   RIGHT,    1,        4,              2,       2,      0],
        5: [20,    11,   LEFT,    1,        0,              1,       2,      1],
        6: [10,    14,   RIGHT,    1,        2,              1,       3,      2],
        7: [15,    10,   LEFT,    1,        3,              2,       4,      5],
      }

LIFE_POS = (DEP_BORDER_CASE[0]+20*CELL_SIZE[0], DEP_BORDER_CASE[1]+CELL_SIZE[1]*10)
SCORE_POS  = (DEP_BORDER_CASE[0]+28*CELL_SIZE[0], DEP_BORDER_CASE[1]+CELL_SIZE[1]*20)