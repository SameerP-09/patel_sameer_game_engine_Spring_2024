# This file was created by: Sameer Patel
# Appreciation to Chris Bradfield

# Sprite is a term for a visual image on screen

# ------------------------------ Importing Libraries ------------------------------
import pygame as pg
from settings import *

import random

# ------------------------------ (1) Write a player class ------------------------------
class Player(pg.sprite.Sprite):
    # initializes Player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #### self.image = pg.Surface((TILESIZE, TILESIZE))        # creates rect with dimensions TILESIZE by TILESIZE
        self.image = game.player_img
        #### self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x, self.y = x * TILESIZE, y * TILESIZE        # x & y positioning based on tiles (x & y increments multiplied by TILESIZE)
        self.speed = 300        # self.speed records player speed
        self.moneybag = 0        # moneybag tracks coins
        self.material = True
    
    # get_keys() purpose - moves player based on keys
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()        # calls get_pressed() through variable keys
        if keys[pg.K_a]:        # if a-key pressed
            self.vx = -self.speed        # x position decreases = move left
            # print(self.rect.x)
            # print(self.rect.y)
        if keys[pg.K_d]:        # if d-key pressed
            self.vx = self.speed        # x position increases = move right
        if keys[pg.K_w]:        # if w-key pressed
            self.vy = -self.speed        # y position decreases = move up (pixels in rows - start at row 0 from top)
        if keys[pg.K_s]:        # if s-key pressed
            self.vy = self.speed        # y position increases = move down

    # collide_with_walls() purpose - prevents sprites from moving through walls
    def collide_with_walls(self, dir):        # dir - direction
        #### if self.collide_with_group(self.game.power_ups, True):
        ####     if PowerUp.random_effect(self) == 'ghost':
        ####         return
        if self.material == True:
            if dir == 'x':        # if sprite moving horizontally
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                    self.vx = 0
                    self.rect.x = self.x
            if dir == 'y':        # if sprite moving vertically
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vy > 0:
                            self.y = hits[0].rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                    self.vy = 0
                    self.rect.y = self.y

    # collide_with_group() purpose - calculates data such as coins/powerups
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:        # if sprite collides with entity
            if str(hits[0].__class__.__name__) == "Coin":        # if entity == Coin
                self.moneybag += 1        # add 1 to moneybag
            elif str(hits[0].__class__.__name__) == "PowerUp":        # if entity == PowerUp
                if PowerUp.random_effect(self) == 'speed':
                    print('you have collected a speed potion')
                    self.speed += 200        # increase speed by 200
                elif PowerUp.random_effect(self) == 'ghost':
                    print('you have collected a ghost potion')
                    self.material = False
            elif str(hits[0].__class__.__name__) == 'Teleport':       # if entity == Teleport
                local_coordinates = Teleport.random_teleport(self)
                self.x, self.y = local_coordinates[0] * TILESIZE, local_coordinates[1] * TILESIZE
                
            #### if str (hits[0].__class__.__name__) == "Potions":
            ####     self.speed += 200
    
    ## old motion
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy

    # def speed_potion(self):
    #     hits = pg.sprite.spritecollide(self, self.game.speedpotion, False)
    #     if hits:
    #         # increase speed
    #         self.speed = 2

    # update() purpose - updates player position
    def update(self):
        # self.rect.x = self.x
        # self.rect.y = self.y

        self.get_keys() # calls get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')        # checks if player has collided with a wall horizontally
        self.rect.y = self.y
        self.collide_with_walls('y')        # checks if player has collided with a wall vertically
        self.collide_with_group(self.game.coins, True)        # checks if player has collided with a coin
        self.collide_with_group(self.game.power_ups, True)        # checks if player has collided with a powerup
        self.collide_with_group(self.game.teleports, True)
        #### self.collide_with_group(self.game.potions, True)        # checks if player has collided with a potion
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE

        

# ------------------------------ (2) Write a wall class ------------------------------
class Wall(pg.sprite.Sprite):
    # initializes Wall
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
        self.speed = 0
        
    # def update(self):
        # self.rect.x += 1
        # self.rect.x += TILESIZE * self.speed
        # self.rect.y += TILESIZE * self.speed
        # if self.rect.x > WIDTH or self.rect.x < 0:
        #    self.speed *= -1
        # if self.rect.y > HEIGHT or self.rect.y < 0:
        #    self.speed *= -1



#### ------------------------------ (3) Speed Potion class ------------------------------
#### class Potions(pg.sprite.Sprite):
####     def __init__(self, game, x, y):
####         self.groups = game.all_sprites, game.potions
####         pg.sprite.Sprite.__init__(self, self.groups)
####         self.game = game
####         self.imgage = game.speedpotion_img
####         self.image = pg.Surface((TILESIZE, TILESIZE))
####         self.image.fill(RED)
####         self.rect = self.image.get_rect()
####         self.x, self.y = x, y
####         self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE



# ------------------------------ (3) Coin class ------------------------------
class Coin(pg.sprite.Sprite):
    # initializes Coin
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE



# ------------------------------ (4) PowerUp class ------------------------------
class PowerUp(pg.sprite.Sprite):
    # initializes PowerUp
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.image = game.powerup_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    def random_effect(self):
        effects = ['speed', 'ghost']
        local_effect = effects[random.randint(0,len(effects) - 1)]
        return local_effect



# ------------------------------ (4) Teleport class ------------------------------
class Teleport(pg.sprite.Sprite):
    # initializes Teleport
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.portal_img
        self.rect = self.image.get_rect()
        #### self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    def random_teleport(self):
        local_teleport = EXIT_PORTS[random.randint(0, len(EXIT_PORTS) - 1)]
        return local_teleport



# ------------------------------ (5) Player 2 class ------------------------------
class Player2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #### self.image = pg.Surface((TILESIZE, TILESIZE))        # creates rect with dimensions TILESIZE by TILESIZE
        self.image = game.player_img
        #### self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x, self.y = x * TILESIZE, y * TILESIZE        # x & y positioning based on tiles (x & y increments multiplied by TILESIZE)
        self.speed = 300        # self.speed records player speed
        self.moneybag = 0        # moneybag tracks coins
        self.material = True

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()        # calls get_pressed() through variable keys
        if keys[pg.K_LEFT]:        # if a-key pressed
            self.vx = -self.speed        # x position decreases = move left
            # print(self.rect.x)
            # print(self.rect.y)
        if keys[pg.K_RIGHT]:        # if d-key pressed
            self.vx = self.speed        # x position increases = move right
        if keys[pg.K_UP]:        # if w-key pressed
            self.vy = -self.speed        # y position decreases = move up (pixels in rows - start at row 0 from top)
        if keys[pg.K_DOWN]:        # if s-key pressed
            self.vy = self.speed        # y position increases = move down


    def collide_with_walls(self, dir):
        Player.collide_with_walls(self, dir)

    def collide_with_group(self, group, kill):
        Player.collide_with_group(self, group, kill)

    def update(self):
        Player.update(self)