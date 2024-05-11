# This file was created by: Sameer Patel
# Changes to Mr. Cozort's file appear in One Drive (link in Canvas)
# Test: pushing changes to Github

# Click a line, press alt, and click another line to have two cursors to type with
# Shift + Alt + Down Arrow = copy & paste code to next line

# self - default parameter in all methods

'''
goals, rules, feedback, freedom, what, the verb, and will it form a sentence

Alpha Design: Game Features
 1. random powerups - 4 parts
    a. speed potion powerup
    b. ghost powerup
    c. 2x coin powerup
    d. randomizing powerups
 2. teleporter - 2 parts
    a. create teleporter class
    b. randomize end location
 3. powerup and portal graphics
 4. multiplayer feature
 5. start screen
'''

'''
Feedback
 - Confusion about what PowerUps have been collected
 * PowerUp cooldowns
 - Confine players to arena
 * End screen
'''

'''
Beta goal: PowerUp cooldowns

Beta Design: Game Features
 1. mob detects players with a circle radius
 2. game borders - impenetrable even with ghost potion
 3. scrolling map
'''

'''
Sources
    - Github Repository (start screen and scrolling map): https://github.com/ccozort/cozort_chris_game_engine_Spring_2024
'''

# ------------------------------ Importing Libraries/Modules ------------------------------
# can rename libraries within a file: import (library) as (name)
import pygame as pg

# can import all items from libraries using: from (library) import *
from settings import *
from sprites import *
from utils import *
from tilemap import *

import sys

# from (library) import (function) imports a specific function from a file
from os import path
from math import floor
#### from random import randint



# ------------------------------ Defining Timer (class) ------------------------------
class Timer():
    # sets all properties to zero when instantiated...
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.event_time = 0
        self.cd = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        if self.cd > 0:
            self.countdown()
    # resets event time to zero - cooldown reset
    def get_countdown(self):
        return floor(self.cd)
    def countdown(self):
        if self.cd > 0:
            self.cd = self.cd - self.game.dt
    # def event_reset(self):
    #     self.event_time = floor((self.game.clock.)/1000)
    # sets current time
    def get_current_time(self):
        self.current_time = floor((pg.time.get_ticks())/1000)



# ------------------------------ Defining Game (class) ------------------------------
class Game:
    # initializes Game
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))        # WIDTH & HEIGHT imported from settings
        pg.display.set_caption('My First Video Game')        # titles the game window
        self.clock = pg.time.Clock()        # Clock(): class because of capitalization (capitalization is a standard)
        pg.key.set_repeat(500, 100)
        self.running = True        # whether the game is running or not
        self.shop_open = False
        self.load_data()

    # load_data() purpose - records game data (scores & positioning)
    def load_data(self):
        # loads images
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player1_img = pg.image.load(path.join(img_folder, 'Mario.png')).convert_alpha()
        # self.player2_img = pg.image.load(path.join(img_folder, 'Luigi.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(img_folder, 'Coin.png')).convert_alpha()
        self.powerup_img = pg.image.load(path.join(img_folder, 'PowerUp.png')).convert_alpha()
        self.portal_img = pg.image.load(path.join(img_folder, 'Teleport.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, 'Mob.png')).convert_alpha()
        self.ghost_mario_img = pg.image.load(path.join(img_folder, 'Ghost_Mario.png')).convert_alpha()
        # self.ghost_luigi_img = pg.image.load(path.join(img_folder, 'Ghost_luigi.png')).convert_alpha()
        self.border_img = pg.image.load(path.join(img_folder, 'Border.png')).convert_alpha()
        
        #self.map_data = []
        self.map = Map(path.join(game_folder, 'single_player_map.txt'))

        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''

        #### with open(path.join(game_folder, 'two_player_map.txt'), 'rt') as f:        # opens map.txt from game folder as f
            #### for line in f:        # evaluates each line in f
                #### self.map_data.append(line)        # adds the characters in each line as str to list map_data
    
    '''aaaa
    TypeError: Player.__init__() takes 3 positional arguments but 4 were given
    self is a built-in parameter in every method; by having self as a parameter,
    we call self twice
    '''

    # new() purpose - positions & calls sprites
    def new(self):
        self.all_sprites = pg.sprite.Group()        # Group(): class because it is capitalized
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.teleports = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.borders = pg.sprite.Group()
        self.shopkeepers = pg.sprite.Group()

        self.cooldown = Timer(self)
        
        for row, tiles in enumerate(self.map.data):        # enumerate says where a pixel is and what it is
            # print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '0':
                    Wall(self, col, row)
                elif tile == '1':
                    self.player1 = Player1(self, col, row)
                    SPAWN.append(col)
                    SPAWN.append(row)
                    # self.player1.spawn = [row, col]
                # elif tile == '2':
                    # self.player2 = Player2(self, col, row)
                elif tile == 'C':
                    Coin(self, col, row)
                elif tile == 'U':
                    PowerUp(self, col, row)
                elif tile == 'T':
                    Teleport(self, col, row)
                elif tile == 'X':
                    EXIT_PORTS.append([col, row])
                elif tile == 'M':
                    self.mob = Mob(self, col, row)
                elif tile == 'B':
                    Border(self, col, row)
                elif tile == 'K':
                    ShopKeeper(self, col, row)
        
        self.camera = Camera(self.map.width, self.map.height)
    
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
        if not self.shop_open:
            self.all_sprites.update()
            self.camera.update(self.player1)
            self.cooldown.ticking()
        else:
            self.show_shop_screen()
    
    # draw_grid() purpose - draws grid/tiles
    def draw_grid(self):
        # draws horizontal lines
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        
        # draws vertical lines
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # draw() purpose - draws grid and sprites
    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # self.draw_grid()
        # self.all_sprites.draw(self.screen)
        draw_text(self.screen, str(self.player1.moneybag), 64, WHITE, 2 * TILESIZE, 1 * TILESIZE)
        # self.draw_text(self.screen, str(self.player2.moneybag), 64, WHITE, 31 * TILESIZE, 1 * TILESIZE)
        draw_text(self.screen, str(self.cooldown.get_countdown()), 24, BLACK, WIDTH/2 - 32, 2)

        if self.player1.hitpoints > 0:
            draw_health_bar(self.screen, self.player1.rect.x, self.player1.rect.y - 20, self.player1.hitpoints)
        # if self.player2.hitpoints > 0:
        #     draw_health_bar(self.screen, self.player2.rect.x, self.player2.rect.y - 20, self.player2.hitpoints)
        
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
                print('The game has ended...')
    
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        draw_text(self.screen, 'Start Menu: Press any key to play', 50, WHITE, WIDTH/2, HEIGHT/2 - 30)
        draw_text(self.screen, '2 Player Game', 20, WHITE, WIDTH/2, 2 * HEIGHT/3)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        pass

    def show_shop_screen(self):
        self.screen.fill(WHITE)
        draw_text(self.screen, 'Shopkeeper', 50, BLACK, WIDTH/2, HEIGHT/2 - 30)
        pg.display.flip()
        self.wait_for_shop_key()

    '''
    Error: shop screen doesn't close because player is still in contact with shopkeeper
    '''
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    
    def wait_for_shop_key(self):
        waiting = True
        while waiting:
            key = pg.key.get_pressed()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
            if key[pg.K_ESCAPE]:
                waiting = False
            if key[pg.K_s]:
                pass
        self.shop_open = False
        self.player1.x, self.player1.y = SPAWN[0] * TILESIZE, SPAWN[1] * TILESIZE



# ------------------------------ Instantiate Game ------------------------------
# assigns Game to the variable, g
g = Game()

g.show_start_screen()

while True:
    g.new()
    g.run()
    # g.show_go_screen()