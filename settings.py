# This file was created by: Sameer Patel

# ------------------------------ Importing Libraries/Modules ------------------------------
import pygame as pg



# ------------------------------ Game Mechanics ------------------------------
WIDTH = 1056
HEIGHT = 768

TILESIZE = 32
FPS = 30



# ------------------------------ Colors ------------------------------
# All colors are tuples; tuple: a collection which is ordered and unchangeable
# (red, green, blue)

BLACK = (0, 0, 0)        # red, green, and blue are min
WHITE = (255, 255, 255)        # red, green, and blue are max
BGCOLOR = (0, 0, 0)

# In RGB, red is 1st, green is 2nd, and blue is 3rd
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# yellow - combination of red and green
YELLOW = (255, 255, 0)

# light grey - combination of white and black
LIGHTGREY = (217, 217, 214)

DARKGREY = (64, 64, 64)
PURPLE = (128, 0, 128)



# ------------------------------ Sprites ------------------------------
PLAYER_SPEED = 300

MOB_HIT_RECT = pg.Rect(0, 0, 96, 96)

# list tracking locations of end portals
EXIT_PORTS = []

# list tracking x and y coordinates of player spawn
SPAWN = []