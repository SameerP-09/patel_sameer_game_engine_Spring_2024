# 

import pygame as pg

clock = pg.time.Clock()

FPS = 30

frames = ['frame1', 'frame2', 'frame3', 'frame4']
x = 0

# while True:
#     x = x%len(frames)
#     print(frames[x])
#     x+=1

previous = 0
current = 0

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 4, height * 4))
        return image

while True:
    clock.tick(FPS)
    current = pg.time.get_ticks()
    if current - previous > 200:
        current = (current + 1) % len(frames)
        print([current])
        previous = current

