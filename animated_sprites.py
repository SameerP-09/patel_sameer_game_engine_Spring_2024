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

while True:
    clock.tick(FPS)
    current = pg.time.get_ticks()
    if current - previous > 200:
        current = (current + 1) % len(frames)
        print([current])
        previous = current