# This file was created by: Sameer Patel
# Changes to Mr. Cozort's file appear in One Drive (link in Canvas)
# Test: pushing changes to Github

# Click a line, press alt, and click another line to have two cursors to type with
# Shift + Alt + Down Arrow = copy & paste code to next line

# self - default parameter in all methods

'''
goals, rules, feedback, freedom, what, the verb, and will it form a sentence

3 Game Features
 - ghost powerup
 - multiplayer feature
 - teleporter
'''

# ------------------------------ Importing Libraries ------------------------------
# can rename libraries within a file: import (library) as (name)
import pygame as pg

# can import all items from libraries using: from (library) import *
from settings import *
from sprites import *

import sys
from os import path

# from (library) import (function) imports a specific function from a file
from random import randint

# ------------------------------ Creating Game (class) ------------------------------
class Game:
    # initializes Game
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))        # WIDTH & HEIGHT imported from settings
        pg.display.set_caption("My First Video Game")        # titles the game window
        self.clock = pg.time.Clock()        # Clock(): class because it is capitalized (capitalization = standard)
        pg.key.set_repeat(500, 100)
        self.running = True
        self.load_data()

    # load_data() purpose - records game data (e.g. scores & positioning)
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'Mushroom.png')).convert_alpha()
        self.speedpotion_img = pg.image.load(path.join(img_folder, 'Speedpotion.png')).convert_alpha()
        self.map_data = [] 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:        # opens map.txt from game folder as f
            for line in f:        # evaluates each line in f
                # print(line)
                self.map_data.append(line)        # adds the characters in each line as str to list map_data
                # print(self.map_data)
    
    # TypeError: Player.__init__() takes 3 positional arguments but 4 were given
    # self is a built-in parameter in every method; by having self as a parameter,
    # we call self twice
                
    # new() purpose - positions & calls sprites
    def new(self):
        self.all_sprites = pg.sprite.Group()        # Group(): class because it is capitalized
        self.walls = pg.sprite.Group()
        #### self.potions = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()

        #### self.player = Player(self, 10, 10)
        #### self.all_sprites.add(self.player)
        #### for x in range(10, 20):
        ####     Wall(self, x, 5)
        
        for row, tiles in enumerate(self.map_data):        # enumerate says where a pixel is and what it is
            # print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    # print("a wall at", row, col)
                    Wall(self, col, row)
                
                if tile == 'p':
                    self.player = Player(self, col, row)

                #### if tile == 's':
                ####     print ("a speed potion at", row, col)
                ####     Potions(self, col, row)
                
                if tile == 'c':
                    # print("a coin at", row, col)
                    Coin(self, col, row)
                
                if tile == "u":
                    # print("a power up at", row, col)
                    PowerUp(self, col, row)

    # run() purpose - runs and updates game
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000        # divide by 1000 since FPS is measured in milliseconds
            self.events()        # mostly input
            self.update()        # processing
            self.draw()        # output

    # quit() purpose - code to end game & close window
    def quit(self):
        pg.quit()
        sys.exit()

    # input() purpose - accept user input
    def input(self):
        #### print(self.clock.get_fps())        # get_fps(): method [know this because of "clock." before get_fps()]
        pass

    # update() purpose - updates sprite graphics based on code
    def update(self):
        self.all_sprites.update()
    
    # draw_grid() purpose - draws grid/tiles
    def draw_grid(self):
        # draws horizontal lines
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        
        # draws vertical lines
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    # draw_text() purpose - code to write on window
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        surface.blit(text_surface, text_rect)

    # draw() purpose - draws grid and sprites
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
        pg.display.flip()
    
    # events() purpose - calls quit to close window
    def events(self):
        # Original Code (that caused the error) - while self.playing:
        # Interface Error: When you try to close the game window by clicking the exit button (top-right),
        #                  the window doesn't close because self.playing is never False
        #                  (self.running is changed to false; not self.playing)
        # listening for events (listening is a term meaning waiting for events to respond to)
        for event in pg.event.get():
            # pg.QUIT executes when you close the game window
            if event.type == pg.QUIT:
                #### self.running = False

                self.quit()
                print("The game has ended...")
            
            #### listening for keyboard actions/events
            #### if event.type == pg.KEYDOWN:
            ####    if event.key == pg.K_a: # or event.key == pg.K_LEFT:
            ####        self.player.move(dx=-1)
            ####     if event.key == pg.K_d: # or event.key == pg.K_RIGHT:
            ####         self.player.move(dx=1)
            ####     if event.key == pg.K_s: # or event.key == pg.K_DOWN:
            ####         self.player.move(dy=1)
            ####     if event.key == pg.K_w: # or event.key == pg.K_UP:
            ####         self.player.move(dy=-1)
    
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass



# ------------------------------ Instantiate Game ------------------------------
# assigns Game to the variable, g
g = Game()

# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()