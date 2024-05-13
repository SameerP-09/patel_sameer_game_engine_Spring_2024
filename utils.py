# This file was created by: Sameer Patel

import pygame as pg

from math import floor
from settings import *



# ------------------------------ Defining Spritesheet (class) ------------------------------
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        # use code below if scaling is necessary
        # image = pg.transform.scale(image, (width // 2, height // 2))
        return image



# ------------------------------ Defining collide_with_walls (func) ------------------------------
def collide_with_walls(self, dir, entity):        # dir - direction
    if dir == 'x':        # if sprite moving horizontally
        hits = pg.sprite.spritecollide(self, entity, False)
        if hits:
            if self.vx > 0:
                self.x = hits[0].rect.left - self.rect.width
            if self.vx < 0:
                self.x = hits[0].rect.right
            self.vx = 0
            self.rect.x = self.x
    if dir == 'y':        # if sprite moving vertically
        hits = pg.sprite.spritecollide(self, entity, False)
        if hits:
            if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
            if self.vy < 0:
                self.y = hits[0].rect.bottom
            self.vy = 0
            self.rect.y = self.y



# ------------------------------ Defining draw_text (func) ------------------------------
# draw_text() purpose - types text on window
def draw_text(surface, text, size, position, color, x, y):
    font_name = pg.font.match_font('times new roman')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    #### text_rect.topleft = (x * TILESIZE, y * TILESIZE)
    if position == 'midtop':
        text_rect.midtop = (x, y)
    elif position == 'topleft':
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)



# ------------------------------ Defining draw_health_bar (func) ------------------------------
# purpose: draw player's health bar
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 32
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)