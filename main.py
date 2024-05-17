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
Final Project: Game Features
 1. Shop Feature
    a. Pauses game
    b. PowerUps Menu
    c. Weapons Menu
    d. Player stats
    e. Accepts Mouse
 2. Player shoots bullets - kills mobs
    a. Ammo variable
    b. Ammo cap
    c. Max upgrade for ammo cap
 3. End Screen
    a. if player dies or player kills all mobs
    b. respawn and quit buttons (accepts mouse)
 4. PowerDowns (includes speed/coin multiplier/health decrease, ghost removal, inverted keys, and tax)
    - random effects from list (same format as PowerUps)
'''

'''
Sources
    - Github Repository (start screen and scrolling map): https://github.com/ccozort/cozort_chris_game_engine_Spring_2024
    - ChatGPT - helped me understand and use screen.blit() and collidepoint() to create shop
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



# ------------------------------ Defining Timer (class) ------------------------------
# copied entirely from Mr. Cozort's code
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
    # purpose: initializes Game
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))        # WIDTH & HEIGHT imported from settings
        pg.display.set_caption('My First Video Game')        # titles the game window
        self.clock = pg.time.Clock()        # Clock(): class because of capitalization (capitalization is a standard)
        pg.key.set_repeat(500, 100)
        self.running = True         # whether the game is running or not
        self.shop_open = False      # whether the shop is open or not
        self.load_data()

        # necessary for end screen
        self.step_x, self.step_y = WIDTH/5, HEIGHT/16
        self.tile_color, self.tilesize = DARKGREY, (WIDTH/4, HEIGHT/16)
        self.respawn_button = pg.Rect(self.step_x, 8 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.quit_button = pg.Rect(3 * self.step_x, 8 * self.step_y, self.tilesize[0], self.tilesize[1])

        self.outcome, self.outcome_txtcolor = '', ''

    # purpose: records game data (scores & positioning)
    def load_data(self):

        # loads images
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')       # image folder
        self.player1_img = pg.image.load(path.join(img_folder, 'Mario.png')).convert_alpha()        # player image
        self.wall_img = pg.image.load(path.join(img_folder, 'Wall.png')).convert_alpha()            # wall image
        self.coin_img = pg.image.load(path.join(img_folder, 'Coin.png')).convert_alpha()            # coin image
        self.powerup_img = pg.image.load(path.join(img_folder, 'PowerUp.png')).convert_alpha()      # powerup image
        self.powerdown_img = pg.image.load(path.join(img_folder, 'PowerDown.png')).convert_alpha()  # powerdown image
        self.portal_img = pg.image.load(path.join(img_folder, 'Teleport.png')).convert_alpha()      # teleport image
        self.mob_img = pg.image.load(path.join(img_folder, 'Mob.png')).convert_alpha()              # mob image
        self.border_img = pg.image.load(path.join(img_folder, 'Border.png')).convert_alpha()        # border image

        # self.map_data = []
        self.map = Map(path.join(game_folder, 'single_player_map.txt'))     # assigns map to self.map

        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''

    '''
    TypeError: Player.__init__() takes 3 positional arguments but 4 were given
     - self is a built-in parameter in every method; by having self as a parameter, we call self twice
    '''

    # purpose: positions & calls sprites
    def new(self):
        self.all_sprites = pg.sprite.Group()        # Group(): class because it is capitalized
        self.walls = pg.sprite.Group()              # New sprite group: walls
        self.coins = pg.sprite.Group()              # New sprite group: coins
        self.power_ups = pg.sprite.Group()          # New sprite group: powerups
        self.power_downs = pg.sprite.Group()        # New sprite group: powerdowns
        self.teleports = pg.sprite.Group()          # New sprite group: teleports
        self.mobs = pg.sprite.Group()               # New sprite group: mobs
        self.borders = pg.sprite.Group()            # New sprite group: borders
        self.shopkeepers = pg.sprite.Group()        # New sprite group: shopkeepers
        self.shop = pg.sprite.Group()               # New sprite group: shop
        self.bullets = pg.sprite.Group()            # New sprite group: bullets

        self.cooldown = Timer(self)         # instantiates timer
        
        for row, tiles in enumerate(self.map.data):        # enumerate says where a pixel is and what it is
            for col, tile in enumerate(tiles):
                if tile == '0':
                    Wall(self, col, row)
                
                elif tile == '1':
                    self.player1 = Player1(self, col, row)
                    SPAWN.append(col)       # records spawn x coordinate
                    SPAWN.append(row)       # records spawn y coordinate
                
                elif tile == 'C':
                    Coin(self, col, row)
                
                elif tile == 'U':
                    PowerUp(self, col, row)
                
                elif tile == 'T':
                    Teleport(self, col, row)
                
                elif tile == 'X':
                    EXIT_PORTS.append([col, row])   # records end portals' x and y coordinates
                
                elif tile == 'M':
                    self.mob = Mob(self, col, row)
                
                elif tile == 'B':
                    Border(self, col, row)
                
                elif tile == 'K':
                    ShopKeeper(self, col, row)
                
                elif tile == 'D':
                    PowerDown(self, col, row)
        
        self.camera = Camera(self.map.width, self.map.height)
    
    # purpose: runs and updates game and graphics
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000        # divide by 1000 since FPS is measured in milliseconds
            self.events()           # mostly input
            self.update()           # processing
            self.draw()             # output
            self.show_go_screen()   # game over screen

    # purpose: ends game and closes window
    def quit(self):
        pg.quit()
        sys.exit()

    # purpose: accepts user input
    def input(self):
        pass

    # purpose: updates sprite graphics based on code
    def update(self):
        if not self.shop_open:                  # if the shop menu is closed, update graphics, camera, and timer
            self.all_sprites.update()
            self.camera.update(self.player1)
            self.cooldown.ticking()
        else:                                   # if the shop menu is open, instantiate Shop
            Shop(self).__init__(self)
    
    # purpose: draws grid/tiles - not currently in use
    def draw_grid(self):
        # draws horizontal lines
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        
        # draws vertical lines
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # purpose: sets background color and draws sprites
    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:         # draws every sprite in the camera
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        draw_text(self.screen, str(self.player1.moneybag), 64, 'midtop', WHITE, 2 * TILESIZE, 1 * TILESIZE)
        draw_text(self.screen, str(self.cooldown.get_countdown()), 24, 'midtop', BLACK, WIDTH/2 - 32, 2)

        if self.player1.hitpoints > 0:          # if player is alive, draw health bar
            draw_health_bar(self.screen, WIDTH - (7 * TILESIZE), 11 * TILESIZE/4, self.player1.hitpoints)

        pg.display.flip()
    
    # purpose: calls quit to close window
    def events(self):

        '''
        Original Code (that caused the error) - while self.playing:
        Interface Error: When you try to close the game window by clicking the exit button (top-right),
                        the window doesn't close because self.playing is never False
                        (self.running is changed to false; not self.playing)
        listening for events (listening is a term meaning waiting for events to respond to)
        '''

        for event in pg.event.get():
            if event.type == pg.QUIT:       # if window is closed
                self.running = False
                self.quit()
    
    # purpose: displays start screen and waits for player input
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        draw_text(self.screen, 'Start Menu: Press any key to play', 50, 'midtop', WHITE, WIDTH/2, HEIGHT/2 - 30)
        draw_text(self.screen, '2 Player Game', 20, 'midtop', WHITE, WIDTH/2, 2 * HEIGHT/3)
        pg.display.flip()
        self.wait_for_key()
    
    # purpose: waits for player to press a key
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:       # if window is closed, end the game
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:      # if any key is pressed, start the game
                    waiting = False

    # purpose: determines whether all the instances of a sprite group are gone
    def all_sprites_gone(self, sprite_group):
        return len(sprite_group) == 0
    
    # purpose: displays end screen (either 'You Win!!!' or 'Your Lose!!!')
    def end_screen(self):
        
        draw_text(self.screen, self.outcome, 50, 'midtop', self.outcome_txtcolor, WIDTH/2, HEIGHT/4)

        # draws respawn and quit buttons
        # ---------- modified from ChatGPT ----------
        self.tile1 = pg.Surface(self.tilesize)
        self.tile1.fill(self.tile_color)
        self.screen.blit(self.tile1, (self.step_x, 8 * self.step_y))
        draw_text(self.screen, 'Respawn', 35, 'topleft', self.outcome_txtcolor, self.step_x, 8 * self.step_y)

        self.tile2 = pg.Surface(self.tilesize)
        self.tile2.fill(self.tile_color)
        self.screen.blit(self.tile2, (3 * self.step_x, 8 * self.step_y))
        draw_text(self.screen, 'Quit Game', 35, 'topleft', self.outcome_txtcolor, 3 * self.step_x, 8 * self.step_y)
        # -------------------------------------------

        pg.display.flip()

    # purpose: checks if player has pressed respawn or quit buttons (with mouse)
    def respawn_or_quit(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:           # if window is closed, end the game
                    waiting = False
                    self.game.quit()

                # ---------- modified from ChatGPT ----------
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:        # if mouse button currently pressed,
                    if pg.mouse.get_pressed()[0]:                                   # if mouse left-clicked,
                        self.mouse_pos = pg.mouse.get_pos()                         # assigns position of mouse to self.mouse_pos
                        if self.respawn_button.collidepoint(self.mouse_pos):        # if mouse in respawn_button during click, end function
                            return
                    
                        elif self.quit_button.collidepoint(self.mouse_pos):         # if mouse in quit_button during click, call self.quit()
                            waiting = False
                            self.quit()
                # -------------------------------------------
            
            self.update_end_screen()

    # purpose: calls end screen functions
    def show_go_screen(self):
        if self.all_sprites_gone(self.mobs):        # if player killed all mobs
            self.playing = False
            self.outcome, self.outcome_txtcolor = 'You Win!!!', GREEN
            self.screen.fill(BGCOLOR)
            pg.display.flip()
            self.respawn_or_quit()
            
        elif self.player1.hitpoints == 0:           # if player died
            self.playing = False
            self.outcome, self.outcome_txtcolor = 'You Died!!!', RED
            self.screen.fill(BGCOLOR)
            pg.display.flip()
            self.respawn_or_quit()
    
    # purpose: updates end screen
    def update_end_screen(self):
        self.screen.fill(BLACK)
        self.end_screen()



# ------------------------------ Defining Shop (class) ------------------------------
class Shop(pg.sprite.Sprite):
    # purpose: initializes Shop
    def __init__(self, game):
        self.groups = game.shop
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.screen = self.game.screen
        self.tilesize = (WIDTH/4, HEIGHT/16)
        self.step_x, self.step_y = WIDTH/5, HEIGHT/16
        self.tile_color = DARKGREY
        self.price, self.time = 3, False

        # -------------------- defines button regions and text color --------------------

        # speed button and text color
        self.speed_button = pg.Rect(self.step_x, 8 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.speed_txtcolor = GREEN

        # ghost button and text color
        self.ghost_button = pg.Rect(3 * self.step_x, 8 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.ghost_txtcolor = GREEN

        # coin multiplier button and text color
        self.twox_coin_button = pg.Rect(self.step_x, 12 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.twox_coin_txtcolor = GREEN

        # regen button and text color
        self.regen_button = pg.Rect(3 * self.step_x, 12 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.regen_txtcolor = GREEN

        # ammo button and text color
        self.ammo_button = pg.Rect(self.step_x, 8 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.ammo_txtcolor = GREEN

        # round button and text color
        self.round_button = pg.Rect(3 * self.step_x, 8 * self.step_y, self.tilesize[0], self.tilesize[1])
        self.round_txtcolor = GREEN
        # ----------------------------------------------------------------------------

        self.screen.fill(BLACK)
        self.can_purchase()

        # begins with PowerUps Menu
        self.current_display = 'powerups'
        self.powerups_display()
        self.wait_for_shop_key()
    
    # purpose: draws PowerUps Menu
    def powerups_display(self):
        draw_text(self.screen, 'PowerUps Menu', 50, 'midtop', GREEN, self.step_x, 2 * HEIGHT/16)

        # ---------- modified from ChatGPT ----------
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
        draw_text(self.screen, str(self.game.player1.coin_multiplier + 1)+'x Coin', 35, 'topleft', self.twox_coin_txtcolor, self.step_x, 12 * self.step_y)

        self.tile4 = pg.Surface(self.tilesize)
        self.tile4.fill(self.tile_color)
        self.screen.blit(self.tile4, (3 * self.step_x, 12 * self.step_y))
        draw_text(self.screen, 'Regen Potion', 35, 'topleft', self.regen_txtcolor, 3 * self.step_x, 12 * self.step_y)
        # -------------------------------------------

        # -------------------- prints player stats --------------------
        # moneybag
        moneybag_stat = self.game.player1.moneybag
        draw_text(self.screen, 'Balance: ' + str(moneybag_stat), 25, 'midtop', WHITE, WIDTH/6, 4 * HEIGHT/12)

        # speed
        speed_stat = self.game.player1.speed
        draw_text(self.screen, 'Speed: ' + str(speed_stat), 25, 'midtop', WHITE, 2 * WIDTH/6, 4 * HEIGHT/12)

        # ghost
        ghost_stat = self.game.player1.ghost
        draw_text(self.screen, 'Ghost: ' + str(ghost_stat), 25, 'midtop', WHITE, 3 * WIDTH/6, 4 * HEIGHT/12)

        # coin multiplier
        multiplier_stat = self.game.player1.coin_multiplier
        draw_text(self.screen, 'Coin multiplier: ' + str(multiplier_stat), 25, 'midtop', WHITE, 4 * WIDTH/6, 4 * HEIGHT/12)

        # health
        hitpoints_stat = self.game.player1.hitpoints
        draw_text(self.screen, 'Health: ' + str(hitpoints_stat), 25, 'midtop', WHITE, 5 * WIDTH/6, 4 * HEIGHT/12)
        # ------------------------------------------------------------
        
        pg.display.flip()

    # purpose: draws Weapons Menu
    def weapons_display(self):
        draw_text(self.screen, 'Weapon Upgrades', 50, 'midtop', GREEN, self.step_x, 2 * HEIGHT/16)

        # ---------- modified from ChatGPT ----------
        self.tile5 = pg.Surface(self.tilesize)
        self.tile5.fill(self.tile_color)
        self.screen.blit(self.tile5, (self.step_x, 8 * self.step_y))
        draw_text(self.screen, 'More Ammo', 35, 'topleft', self.ammo_txtcolor, self.step_x, 8 * self.step_y)

        self.tile6 = pg.Surface(self.tilesize)
        self.tile6.fill(self.tile_color)
        self.screen.blit(self.tile6, (3 * self.step_x, 8 * self.step_y))
        draw_text(self.screen, 'Round Upgrade', 35, 'topleft', self.round_txtcolor, 3 * self.step_x, 8 * self.step_y)
        # -------------------------------------------

        # -------------------- prints player stats --------------------
        # moneybag
        moneybag_stat = self.game.player1.moneybag
        draw_text(self.screen, 'Balance: ' + str(moneybag_stat), 25, 'midtop', WHITE, WIDTH/6, 4 * HEIGHT/12)

        # ammo
        ammo_stat = self.game.player1.ammo
        draw_text(self.screen, 'Ammunition: ' + str(ammo_stat), 25, 'midtop', WHITE, 3 * WIDTH/6, 4 * HEIGHT/12)

        # round
        round_stat = self.game.player1.round
        draw_text(self.screen, 'Round: ' + str(round_stat), 25, 'midtop', WHITE, 5 * WIDTH/6, 4 * HEIGHT/12)

        pg.display.flip()
        # ------------------------------------------------------------

    # purpose: determines whether player can purchase each item
    def can_purchase(self):
        if self.game.player1.moneybag < self.price:                                 # if player has enough money
            self.speed_txtcolor, self.ghost_txtcolor, self.twox_coin_txtcolor, self.regen_txtcolor, self.ammo_txtcolor, self.round_txtcolor = RED, RED, RED, RED, RED, RED
        if self.game.player1.speed == self.game.player1.speed_max:                  # if player speed is maxed
            self.speed_txtcolor = RED
        if self.game.player1.ghost == True:                                         # if player has ghost potion
            self.ghost_txtcolor = RED
        if self.game.player1.coin_multiplier >= self.game.player1.mult_max:         # if coin multiplier is maxed
            self.twox_coin_txtcolor = RED
        if self.game.player1.hitpoints >= self.game.player1.health_max:             # if health is maxed
            self.regen_txtcolor = RED
        if self.game.player1.ammo == self.game.player1.round:                       # if ammo is maxed
            self.ammo_txtcolor = RED
        if self.game.player1.round == self.game.player1.round_max:                  # if round is maxed
            self.round_txtcolor = RED

    # purpose: waits for player to press any key
    def wait_for_shop_key(self):
        waiting = True
        while waiting:
            self.can_purchase()
            key = pg.key.get_pressed()
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:           # if window is closed, end game
                    waiting = False
                    self.game.quit()

                # ---------- modified from ChatGPT ----------
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if pg.mouse.get_pressed()[0] and self.game.player1.moneybag >= self.price:
                        self.mouse_pos = pg.mouse.get_pos()
                        if self.current_display == 'powerups':      # if PowerUps Menu is open
                            # if player presses speed button and player speed not maxed
                            if self.speed_button.collidepoint(self.mouse_pos) and self.game.player1.speed < self.game.player1.speed_max:
                                self.game.player1.speed += 100                  # increase speed by 100
                                self.game.player1.moneybag += -self.price       # subtract price from moneybag
                            
                            # if player presses ghost button and player doesn't have a ghost powerup
                            elif self.ghost_button.collidepoint(self.mouse_pos) and self.game.player1.ghost != True:
                                self.game.player1.ghost = True                  # give player a ghost powerup
                                self.game.player1.moneybag += -self.price       # subtract price from moneybag
                            
                            # if player presses coin multiplier button and coin multiplier not maxed
                            elif self.twox_coin_button.collidepoint(self.mouse_pos) and self.game.player1.coin_multiplier < self.game.player1.mult_max:
                                self.game.player1.coin_multiplier += 1          # increase coin multiplier by 1
                                self.game.player1.moneybag += -self.price       # subtract price from moneybag
                            
                            # if player presses regen button and helth not maxed
                            elif self.regen_button.collidepoint(self.mouse_pos) and self.game.player1.hitpoints < self.game.player1.health_max:
                                if self.game.player1.hitpoints + 25 > self.game.player1.health_max:     # if health + 25 is more than max
                                    self.game.player1.hitpoints = self.game.player1.health_max          # health is the max
                                else:                                                                   # otherwise, add 25 to health
                                    self.game.player1.hitpoints += 25
                                self.game.player1.moneybag += -self.price                               # both cases subtract price from moneybag
                        elif self.current_display == 'weapons':     # if Weapons Menu is open
                            # if player presses ammo button and ammo not maxed
                            if self.ammo_button.collidepoint(self.mouse_pos) and self.game.player1.ammo <= self.game.player1.round:
                                self.game.player1.ammo = self.game.player1.round        # reload ammo
                                self.game.player1.moneybag += -self.price               # subtract price from moneybag
                            
                            # if player presses round button and round not maxed
                            elif self.round_button.collidepoint(self.mouse_pos) and self.game.player1.round < self.game.player1.round_max:
                                self.game.player1.round += 10                           # increase round by 10
                                self.game.player1.moneybag += -self.price               # subtract price from moneybag
                                self.ammo_txtcolor = GREEN                              # ammo text color is green (indicates you can buy)
                
                # -------------------------------------------

                if key[pg.K_ESCAPE]:                    # if esc is pressed, exit shop
                    waiting = False
                if key[pg.K_s]:                         # if s is pressed, go to Weapons Menu
                    self.current_display = 'weapons'
                if key[pg.K_w]:                         # if w is pressed, go to PowerUps Menu
                    self.current_display = 'powerups'

            self.update()
                
        self.game.shop_open = False
        self.game.player1.x, self.game.player1.y = SPAWN[0] * TILESIZE, SPAWN[1] * TILESIZE
    
    # purpose: switches shop menus and redraws menu
    def update(self):
        self.screen.fill(BLACK)
        if self.current_display == 'powerups':      # if PowerUps Menu is opened, call powerup_display()
            self.powerups_display()
        elif self.current_display == 'weapons':     # if Weapons Menu is opened, call weapons_display()
            self.weapons_display()



# ------------------------------ Instantiate Game ------------------------------
# assigns Game to g
g = Game()

g.show_start_screen()

while True:
    g.new()
    g.run()