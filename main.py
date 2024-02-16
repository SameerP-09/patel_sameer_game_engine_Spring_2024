# This file was created by: Sameer Patel
# Changes to Mr. Cozort's file appear in One Drive (link in Canvas)

# ------------------------------Importing Libraries------------------------------
# can rename libraries within a file: import (library) as (name)
import pygame as pg

# can import all variables from libraries using: from (library) import *
from settings import *
from sprites import *

# 
import sys

# in course code files --> examples --> game engine --> main.py
from os import path

# from _____ import (function) imports a specific function from a file
from random import randint

# -----------------------------Creating Game (class)-----------------------------
class Game:
    # defines method __init__(); self - default parameter that can be used in all methods
    def __init__(self):
        pg.init()
        # WIDTH and HEIGHT are variables imported from settings
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # makes the string "My First Video Game" the window title
        pg.display.set_caption("My First Video Game")
        # Clock(): class [know this because Clock is capitalized; capitalization is a standard]
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        # purpose: to record data such as high scores or positioning of player
        self.load_data()
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = [] 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        # opens the file in the game folder called map.txt as f
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    
    # TypeError: Player.__init__() takes 3 positional arguments but 4 were given
    # self is a built-in parameter in every method; by having self as a parameter,
    # we call self twice
    def new(self):
        # Group(): class [know this because Clock is capitalized; capitalization is a standard]
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.potions = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # self.all_sprites.add(self.player)
        # for x in range(10, 20):
            # Wall(self, x, 5)
        # enumerate says two things: where a pixel is and what it is
        # need row and column
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 's':
                    print ("a speed potion at", row, col)
                    Speedpotion(self, col, row)

    # Click a line, press alt, and click another line to have two cursors to type with
    def run(self):
        self.playing = True
        while self.playing:
            # divide by 1000 since FPS is measured in milliseconds
            self.dt = self.clock.tick(FPS)/1000
            # mostly input
            self.events()
            # processing
            self.update()
            # output
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def input(self):
        # get_fps(): method [know this because of "clock." before get_fps()]
        # print(self.clock.get_fps())
        pass

    def update(self):
        self.all_sprites.update()
    
    def draw_grid(self):
        # draws horizontal lines
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        # draws vertical lines
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        pass
    
    def events(self):
        # Original Code (that caused the error) - while self.playing:
        # Interface Error: When you try to close the game window by clicking the exit button (top-right),
        #                  the window doesn't close because self.playing is never False
        #                  (self.running is changed to false; not self.playing)
        # listening for events (listening is a term meaning waiting for events to respond to)
        for event in pg.event.get():
            # pg.QUIT executes when you close the game window
            if event.type == pg.QUIT:
                # self.running = False
                self.quit()
                print("The game has ended...")
            # listening for keyboard actions/events
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a: # or event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_d: # or event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_s: # or event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
            #     if event.key == pg.K_w: # or event.key == pg.K_UP:
            #         self.player.move(dy=-1)
    
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass



# -------------------------------Instantiate Game-------------------------------
# assigns Game to the variable, g
g = Game()

# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()