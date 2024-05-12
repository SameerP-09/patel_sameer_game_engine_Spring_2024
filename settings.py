# This file was created by: Sameer Patel

# ------------------------------ Importing Libraries/Modules ------------------------------
import pygame as pg

# (1) can define 2 variables in 1 line: WIDTH, HEIGHT = 800, 600

# (2) can define 2 variables in 2 lines

# ------------------------------ Game Mechanics ------------------------------
WIDTH = 1056
HEIGHT = 768

# Both ways are valid - but be consistent with the way you use

TILESIZE = 32
FPS = 30



# ------------------------------ Colors ------------------------------
# All colors are tuples; tuple: a collection which is ordered and unchangeable
# (red, green, blue)

BLACK = (0, 0, 0)        # red, green, and blue are min
WHITE = (255, 255, 255)        # red, green, and blue are max
BGCOLOR = (0, 0, 0)

RED = (255, 0, 0)        # In RGB, red is 1st
GREEN = (0, 255, 0)        # In RGB, green is 2nd
BLUE = (0, 0, 255)        # In RGB, blue is 3rd
YELLOW = (255, 255, 0)        # yellow - combination of red and green
LIGHTGREY = (217, 217, 214)        # light grey - combination of white and black
DARKGREY = (64, 64, 64)
PURPLE = (128, 0, 128)



# ------------------------------ Sprites ------------------------------
PLAYER_SPEED = 300
#### P1_HP = 100
#### P2_HP = 100

MOB_HIT_RECT = pg.Rect(0, 0, 96, 96)

EXIT_PORTS = []        # list tracking locations of end portals
SPAWN = []