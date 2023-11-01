from enum import Enum
# COLORS (r, g, b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BGCOLOUR = DARKGREY

# game settings
WIDTH = 1200
HEIGHT = 760
FPS = 60
title = "Sliding Puzzle Game"

class board_setting_1(Enum):
    TILESIZE = 120
    GAME_SIZE = 3

class board_setting_2(Enum):
    TILESIZE = 90
    GAME_SIZE = 4

class board_setting_3(Enum):
    TILESIZE = 72
    GAME_SIZE = 5

