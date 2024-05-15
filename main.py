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
        self.coin_img = pg.image.load(path.join(img_folder, 'Coin.png')).convert_alpha()
        self.powerup_img = pg.image.load(path.join(img_folder, 'PowerUp.png')).convert_alpha()
        self.portal_img = pg.image.load(path.join(img_folder, 'Teleport.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, 'Mob.png')).convert_alpha()
        self.ghost_mario_img = pg.image.load(path.join(img_folder, 'Ghost_Mario.png')).convert_alpha()
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
        self.shop = pg.sprite.Group()

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
            Shop(self).__init__(self)
    
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

        draw_text(self.screen, str(self.player1.moneybag), 64, 'midtop', WHITE, 2 * TILESIZE, 1 * TILESIZE)
        draw_text(self.screen, str(self.cooldown.get_countdown()), 24, 'midtop', BLACK, WIDTH/2 - 32, 2)

        if self.player1.hitpoints > 0:
            draw_health_bar(self.screen, self.player1.rect.x, self.player1.rect.y - 20, self.player1.hitpoints)

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
        draw_text(self.screen, 'Start Menu: Press any key to play', 50, 'midtop', WHITE, WIDTH/2, HEIGHT/2 - 30)
        draw_text(self.screen, '2 Player Game', 20, 'midtop', WHITE, WIDTH/2, 2 * HEIGHT/3)
        pg.display.flip()
        self.wait_for_key()
    
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

    def show_go_screen(self):
        pass



# ------------------------------ Defining Shop (class) ------------------------------
class Shop(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.shop
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.screen = self.game.screen
        self.tilesize = (WIDTH/4, HEIGHT/16)
        self.step_x, self.step_y = WIDTH/5, HEIGHT/16
        self.tile_color = DARKGREY
        self.price, self.time = 1, False

        self.speed_button = pg.Rect(self.step_x, 8 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.speed_txtcolor = GREEN

        self.ghost_button = pg.Rect(3 * self.step_x, 8 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.ghost_txtcolor = GREEN

        self.twox_coin_button = pg.Rect(self.step_x, 12 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.twox_coin_txtcolor = GREEN

        self.regen_button = pg.Rect(3 * self.step_x, 12 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.regen_txtcolor = GREEN

        self.screen.fill(BLACK)
        self.wait_for_shop_key()

    def display(self):
        draw_text(self.screen, 'Shop Menu', 50, 'midtop', GREEN, self.step_x, 2 * HEIGHT/16)

        self.tile1 = pg.Surface(self.tilesize)
        self.tile1.fill(self.tile_color)
        self.screen.blit(self.tile1, (self.step_x, 8 * self.step_y))
        draw_text(self.screen, 'Speed Potion', 35, 'topleft', self.speed_txtcolor, self.step_x, 8 * self.step_y)

        self.tile2 = pg.Surface(self.tilesize)
        self.tile2.fill(self.tile_color)
        self.screen.blit(self.tile2, (3 * self.step_x, 8 * self.step_y))
        draw_text(self.screen, 'Ghost Potion', 35, 'topleft', self.ghost_txtcolor, 3 * self.step_x, 8 * self.step_y)

        self.tile3 = pg.Surface(self.tilesize)
        self.tile3.fill(self.tile_color)
        self.screen.blit(self.tile3, (self.step_x, 12 * self.step_y))
        draw_text(self.screen, '2x Coin', 35, 'topleft', self.twox_coin_txtcolor, self.step_x, 12 * self.step_y)

        self.tile4 = pg.Surface(self.tilesize)
        self.tile4.fill(self.tile_color)
        self.screen.blit(self.tile4, (3 * self.step_x, 12 * self.step_y))
        draw_text(self.screen, 'Regen Potion', 35, 'topleft', self.regen_txtcolor, 3 * self.step_x, 12 * self.step_y)
        
        moneybag_stat = self.game.player1.moneybag
        draw_text(self.screen, 'Balance: ' + str(moneybag_stat), 25, 'midtop', WHITE, WIDTH/6, 4 * HEIGHT/12)

        speed_stat = self.game.player1.speed
        draw_text(self.screen, 'Speed: ' + str(speed_stat), 25, 'midtop', WHITE, 2 * WIDTH/6, 4 * HEIGHT/12)

        ghost_stat = self.game.player1.ghost
        draw_text(self.screen, 'Ghost: ' + str(ghost_stat), 25, 'midtop', WHITE, 3 * WIDTH/6, 4 * HEIGHT/12)

        multiplier_stat = self.game.player1.coin_multiplier
        draw_text(self.screen, 'Coin multiplier: ' + str(multiplier_stat), 25, 'midtop', WHITE, 4 * WIDTH/6, 4 * HEIGHT/12)

        hitpoints_stat = self.game.player1.hitpoints
        draw_text(self.screen, 'Health: ' + str(hitpoints_stat), 25, 'midtop', WHITE, 5 * WIDTH/6, 4 * HEIGHT/12)

        pg.display.flip()
    
    def wait_for_shop_key(self):
        waiting = True
        while waiting:
            key = pg.key.get_pressed()
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.game.quit()
                
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if pg.mouse.get_pressed()[0] and self.game.player1.moneybag >= self.price:
                        self.mouse_pos = pg.mouse.get_pos()
                        if self.speed_button.collidepoint(self.mouse_pos) and self.speed_txtcolor != RED:
                            if self.game.player1.speed + 100 > self.game.player1.speed_max:
                                self.game.player1.speed = self.game.player1.speed_max
                            else:
                                self.game.player1.speed += 100
                            self.game.player1.moneybag += -self.price
                            if self.game.player1.speed == self.game.player1.speed_max:
                                self.speed_txtcolor = RED
                        elif self.ghost_button.collidepoint(self.mouse_pos) and self.ghost_txtcolor != RED:
                            self.game.player1.ghost = True
                            self.game.player1.moneybag += -self.price
                            if self.game.player1.ghost == True:
                                self.ghost_txtcolor = RED
                        elif self.twox_coin_button.collidepoint(self.mouse_pos) and self.twox_coin_txtcolor != RED:
                            if self.game.player1.coin_multiplier + 1 > self.game.player1.mult_max:
                                self.game.player1.coin_multiplier = self.game.player1.mult_max
                            else:
                                self.game.player1.coin_multiplier += 1
                            self.game.player1.moneybag += -self.price
                            if self.game.player1.coin_multiplier == self.game.player1.mult_max:
                                self.twox_coin_txtcolor = RED
                        elif self.regen_button.collidepoint(self.mouse_pos) and self.regen_txtcolor != RED:
                            if self.game.player1.hitpoints + 25 > self.game.player1.health_max:
                                self.game.player1.hitpoints = self.game.player1.health_max
                            else:
                                self.game.player1.hitpoints += 25
                            self.game.player1.moneybag += -self.price
                            if self.game.player1.hitpoints == self.game.player1.health_max:
                                self.regen_txtcolor = RED

            
            if self.game.player1.moneybag < self.price:
                self.speed_txtcolor, self.ghost_txtcolor, self.twox_coin_txtcolor, self.regen_txtcolor = RED, RED, RED, RED
            
            if self.game.player1.speed == self.game.player1.speed_max:
                self.speed_txtcolor = RED

            if self.game.player1.ghost == True:
                self.ghost_txtcolor = RED
            
            if self.game.player1.coin_multiplier >= self.game.player1.mult_max:
                self.twox_coin_txtcolor = RED
            
            if self.game.player1.hitpoints >= self.game.player1.health_max:
                self.regen_txtcolor = RED
                    
            if key[pg.K_ESCAPE]:
                waiting = False
            
            self.update()
                
        self.game.shop_open = False
        self.game.player1.x, self.game.player1.y = SPAWN[0] * TILESIZE, SPAWN[1] * TILESIZE
    
    def update(self):
        self.screen.fill(BLACK)
        self.display()



# ------------------------------ Instantiate Game ------------------------------
# assigns Game to the variable, g
g = Game()

g.show_start_screen()

while True:
    g.new()
    g.run()
    # g.show_go_screen()