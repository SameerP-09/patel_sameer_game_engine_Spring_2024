# This file was created by: Sameer Patel
# Changes to Mr. Cozort's file appear in One Drive (link in Canvas)
# Test: pushing changes to Github

# Click a line, press alt, and click another line to have two cursors to type with
# Shift + Alt + Down Arrow = copy & paste code to next line

# self - default parameter in all methods

'''
goals, rules, feedback, freedom, what, the verb, and will it form a sentence

Game Features
 1. random powerups - 4 parts
    a. speed potion powerup
    b. ghost powerup
    c. 2x coin powerup
    d. randomizing powerups
 2. teleporter - 2 parts
    a. create teleporter class
    b. randomaize end location
 3. powerup and portal graphics
 4. multiplayer feature
 5. start screen
'''

'''
Sources
    - Github Repository (start screen): https://github.com/ccozort/cozort_chris_game_engine_Spring_2024
'''

# ------------------------------ Importing Libraries/Modules ------------------------------
# can rename libraries within a file: import (library) as (name)
import pygame as pg

# can import all items from libraries using: from (library) import *
from settings import *
from sprites import *

import sys

# from (library) import (function) imports a specific function from a file
from os import path
from math import floor
#### from random import randint

# ------------------------------ Creating Game (class) ------------------------------
class Cooldown():
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)



# ------------------------------ Creating Game (class) ------------------------------
class Game:
    # initializes Game
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))        # WIDTH & HEIGHT imported from settings
        pg.display.set_caption("My First Video Game")        # titles the game window
        self.clock = pg.time.Clock()        # Clock(): class because of capitalization (capitalization is a standard)
        pg.key.set_repeat(500, 100)
        self.running = True        # whether the game is running or not
        self.load_data()

    # load_data() purpose - records game data (scores & positioning)
    def load_data(self):

        # loads images
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'Mario.png')).convert_alpha()
        self.player2_img = pg.image.load(path.join(img_folder, 'Luigi.png')).convert_alpha()
        self.powerup_img = pg.image.load(path.join(img_folder, 'PowerUp.png')).convert_alpha()
        self.portal_img = pg.image.load(path.join(img_folder, 'Teleport.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, 'Ghost.png')).convert_alpha()
        self.map_data = []

        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''

        with open(path.join(game_folder, 'two_player_map.txt'), 'rt') as f:        # opens map.txt from game folder as f
            for line in f:        # evaluates each line in f
                #### print(line)
                self.map_data.append(line)        # adds the characters in each line as str to list map_data
                #### print(self.map_data)
    
    '''
    TypeError: Player.__init__() takes 3 positional arguments but 4 were given
    self is a built-in parameter in every method; by having self as a parameter,
    we call self twice
    '''

    # new() purpose - positions & calls sprites
    def new(self):
        self.timer = Cooldown()
        self.all_sprites = pg.sprite.Group()        # Group(): class because it is capitalized
        self.walls = pg.sprite.Group()
        #### self.potions = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.teleports = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        #### self.player = Player(self, 10, 10)
        #### self.all_sprites.add(self.player)
        #### for x in range(10, 20):
        ####     Wall(self, x, 5)
        
        for row, tiles in enumerate(self.map_data):        # enumerate says where a pixel is and what it is
            # print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '0':
                    # print("a wall at", row, col)
                    Wall(self, col, row)
                
                if tile == '1':
                    self.player = Player(self, col, row)
                
                if tile == '2':
                    self.player2 = Player2(self, col, row)

                #### if tile == 's':
                ####     print ("a speed potion at", row, col)
                ####     Potions(self, col, row)
                
                if tile == 'C':
                    # print("a coin at", row, col)
                    Coin(self, col, row)
                
                if tile == 'U':
                    # print("a power up at", row, col)
                    PowerUp(self, col, row)
                
                if tile == 'T':
                    Teleport(self, col, row)
                
                if tile == 'X':
                    # Teleport(self, col, row)
                    EXIT_PORTS.append([col, row])
                
                if tile == 'M':
                    self.mob = Mob(self, col, row)

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
        #### print(self.clock.get_fps())       # get_fps(): method [know this because of "clock." before get_fps()]
        pass

    # update() purpose - updates sprite graphics based on code
    def update(self):
        self.timer.ticking()
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
        #### text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    # draw() purpose - draws grid and sprites
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1 * TILESIZE, 1 * TILESIZE)
        self.draw_text(self.screen, str(self.player2.moneybag), 64, WHITE, 31 * TILESIZE, 1 * TILESIZE)
        self.draw_text(self.screen, str(self.timer.countdown(45)), 24, WHITE, WIDTH/2 - 32, 2)
        pg.display.flip()
    
    # events() purpose - calls quit to close window
    def events(self):

        '''
        Original Code (that caused the error) - while self.playing:
        Interface Error: When you try to close the game window by clicking the exit button (top-right),
                        the window doesn't close because self.playing is never False
                        (self.running is changed to false; not self.playing)
        listening for events (listening is a term meaning waiting for events to respond to)
        '''

        for event in pg.event.get():
            # pg.QUIT executes when you close the game window
            if event.type == pg.QUIT:
                #### self.running = False

                self.quit()
                print("The game has ended...")
            
            # listening for keyboard actions/events
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
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, 'Start Menu: Press any key to play', 50, WHITE, WIDTH/2, HEIGHT/2 - 30)
        self.draw_text(self.screen, '2 Player Game', 20, WHITE, WIDTH/2, 2 * HEIGHT/3)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        pass
    
    def wait_for_key(self):
        waiting = True
        key = pg.key.get_pressed()
        while waiting:
            self.clock.tick(FPS)
            #### print(1)        # used this to debug
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False



# ------------------------------ Instantiate Game ------------------------------
# assigns Game to the variable, g
g = Game()

g.show_start_screen()

while True:
    g.new()
    g.run()
    # g.show_go_screen()