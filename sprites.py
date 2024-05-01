# This file was created by: Sameer Patel
# Appreciation to Chris Bradfield

# Sprite is a term for a visual image on screen

# ------------------------------ Importing Libraries ------------------------------
import pygame as pg
import random

from math import sqrt
from os import path

from settings import *
from utils import *

vec = pg.math.Vector2

Player1_sheet = 'mario.png'
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')



# ------------------------------ (1) Defining Player1 Class ------------------------------
class Player1(pg.sprite.Sprite):
    # initializes Player1
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #### self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.player1_img        # defines image
        #### self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x, self.y = x * TILESIZE, y * TILESIZE        # x & y positioning multiplied by TILESIZE

        self.speed = 300        # player1 speed
        self.moneybag = 0        # coins collected
        self.coin_multiplier = 1
        self.hitpoints = 100

        self.material, self.cooling = True, False
        self.hypotenuse = ''

        # needed for animated sprite
        self.spritesheet = Spritesheet(path.join(img_folder, Player1_sheet))
        self.load_images()
        self.image = self.standing_frames[0]
        self.current_frame = 0
        self.last_update = 0
    
    # get_keys() purpose - moves player1 based on keys
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()        # calls get_pressed() in keys (variable)
        if keys[pg.K_a]:        # if a-key pressed
            self.vx = -self.speed        # x decreases = move left
        if keys[pg.K_d]:        # if d-key pressed
            self.vx = self.speed        # x increases = move right
        if keys[pg.K_w]:        # if w-key pressed
            self.vy = -self.speed        # y decreases = move up (y starts at row 0 from top)
        if keys[pg.K_s]:        # if s-key pressed
            self.vy = self.speed        # y increases = move down

    # collide_with_walls() purpose - prevents sprites from moving through walls
    def collide_with_walls(self, dir):        # dir - direction
        collide_with_walls(self, dir)
    
    def collide_with_borders(self, dir):
        if dir == 'x':        # if sprite moving horizontally
            hits = pg.sprite.spritecollide(self, self.game.borders, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':        # if sprite moving vertically
            hits = pg.sprite.spritecollide(self, self.game.borders, False)
            if hits:
                if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # collide_with_group() purpose - calculates data such as coins/powerups
    def collide_with_group(self, group, kill, game):
        hits = pg.sprite.spritecollide(self, group, kill)
        random_effect = PowerUp.random_effect(self)
        if hits:        # if sprite collides with entity
            if str(hits[0].__class__.__name__) == 'Coin':        # if entity == Coin
                self.moneybag += self.coin_multiplier        # add 1 to moneybag

            elif str(hits[0].__class__.__name__) == 'PowerUp':        # if entity == PowerUp
                if random_effect == 'speed':
                    self.speed += 100        # increase speed by 200
                    draw_text(self.game.screen, 'PowerUp: Speed', 40, WHITE, self.x, self.y + 20)

                elif random_effect == 'ghost':
                    self.material = False        # overrides collide_with_walls()
                    self.image = game.ghost_mario_img
                    draw_text(self.game.screen, 'PowerUp: Ghost', 15, WHITE, self.x, self.y)

                elif random_effect == '2x coin':
                    # self.moneybag = self.moneybag * 2        # doubles current moneybag
                    self.coin_multiplier *= 2
                    draw_text(self.game.screen, 'PowerUp: 2x Coin', 15, WHITE, self.x, self.y)

                elif random_effect == 'regen':
                    self.hitpoints += 50
                    draw_text(self.game.screen, 'PowerUp: Regen', 15, WHITE, self.x, self.y)
                
                self.game.cooldown.cd = 5
                self.cooling = True
                    
            elif str(hits[0].__class__.__name__) == 'Teleport':       # if entity == Teleport
                local_coordinates = Teleport.random_teleport(self)        # gets the coordinates of the end portal
                # makes player1's coordinates = the end portal coordinates
                self.x, self.y = local_coordinates[0] * TILESIZE, local_coordinates[1] * TILESIZE
                
            elif str(hits[0].__class__.__name__) == 'Mob':
                self.hitpoints = self.hitpoints - 1
    
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]

    def animate(self):
        now = pg. time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    # update() purpose - updates player1's position
    def update(self):
        # needed for animated sprite
        self.animate()

        self.get_keys() # calls get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')        # checks if player1 has collided with a wall horizontally
        self.collide_with_borders('x')        # checks if player1 has collided with a border horizontally
        self.rect.y = self.y
        self.collide_with_walls('y')        # checks if player1 has collided with a wall vertically
        self.collide_with_borders('y')        # checks if player1 has collided with a border vertically
        self.collide_with_group(self.game.coins, True, self.game)        # checks if player1 has collided with a coin
        self.collide_with_group(self.game.power_ups, True, self.game)        # checks if player1 has collided with a powerup
        self.collide_with_group(self.game.teleports, False, self.game)
        self.collide_with_group(self.game.mobs, False, self.game)

        if self.game.cooldown.cd < 1:
            self.cooling = False
        if self.cooling == False:
            self.collide_with_group(self.game.power_ups, True, self.game)
        elif self.cooling == True:
            self.collide_with_group(self.game.power_ups, False, self.game)

        if self.hitpoints <= 0:
            self.kill()
        
        return self.hitpoints

        

# ------------------------------ (2) Defining Wall Class ------------------------------
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



# ------------------------------ (3) Defining Coin Class ------------------------------
class Coin(pg.sprite.Sprite):
    # initializes Coin
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE



# ------------------------------ (4) Defining PowerUp Class ------------------------------
class PowerUp(pg.sprite.Sprite):
    # initializes PowerUp
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #### self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.image = game.powerup_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    def random_effect(self):
        effects = ['speed', 'ghost', '2x coin', 'regen']
        local_effect = effects[random.randrange(0, len(effects))]
        #### local_effect = effects[2] - used this line of code to debug
        return local_effect



# ------------------------------ (5) Defining Teleport Class ------------------------------
class Teleport(pg.sprite.Sprite):
    # initializes Teleport
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.teleports
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.portal_img
        self.rect = self.image.get_rect()
        #### self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    def random_teleport(self):
        local_teleport = EXIT_PORTS[random.randrange(0, len(EXIT_PORTS))]
        return local_teleport



# ------------------------------ (6) Defining Player2 class ------------------------------
# class Player2(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         #### self.image = pg.Surface((TILESIZE, TILESIZE))        # creates rect with dimensions TILESIZE by TILESIZE
#         self.image = game.player2_img
#         #### self.image.fill(GREEN)
#         self.rect = self.image.get_rect()
#         self.vx, self.vy = 0, 0
#         self.x, self.y = x * TILESIZE, y * TILESIZE        # x & y positioning based on tiles (x & y increments multiplied by TILESIZE)
#         self.speed = 300        # self.speed records player speed
#         self.moneybag = 0        # moneybag tracks coins
#         self.hitpoints = 100
#         self.material = True
#         self.hypotenuse = ''

#     def get_keys(self):
#         self.vx, self.vy = 0, 0
#         keys = pg.key.get_pressed()        # calls get_pressed() through variable keys
#         if keys[pg.K_LEFT]:        # if a-key pressed
#             self.vx = -self.speed        # x position decreases = move left
#             # print(self.rect.x)
#             # print(self.rect.y)
#         if keys[pg.K_RIGHT]:        # if d-key pressed
#             self.vx = self.speed        # x position increases = move right
#         if keys[pg.K_UP]:        # if w-key pressed
#             self.vy = -self.speed        # y position decreases = move up (pixels in rows - start at row 0 from top)
#         if keys[pg.K_DOWN]:        # if s-key pressed
#             self.vy = self.speed        # y position increases = move down

#     def collide_with_walls(self, dir):
#         Player1.collide_with_walls(self, dir)
    
#     def collide_with_borders(self, dir):
#         Player1.collide_with_borders(self, dir)

#     def collide_with_group(self, group, kill, game):
#         hits = pg.sprite.spritecollide(self, group, kill)
#         random_effect = PowerUp.random_effect(self)
#         if hits:        # if sprite collides with entity
#             if str(hits[0].__class__.__name__) == "Coin":        # if entity == Coin
#                 self.moneybag += 1        # add 1 to moneybag
            
#             elif str(hits[0].__class__.__name__) == "PowerUp":        # if entity == PowerUp
#                 if random_effect == 'speed':
#                     self.speed += 200        # increase speed by 200

#                 elif random_effect == 'ghost':
#                     self.material = False        # overrides collide_with_walls()
#                     self.image = game.ghost_luigi_img

#                 elif random_effect == '2x coin':
#                     self.moneybag = self.moneybag * 2        # doubles current moneybag

#                 elif random_effect == 'regen':
#                     self.hitpoints += 50

#             elif str(hits[0].__class__.__name__) == 'Teleport':       # if entity == Teleport
#                 local_coordinates = Teleport.random_teleport(self)        # gets the coordinates of the end portal
#                 self.x, self.y = local_coordinates[0] * TILESIZE, local_coordinates[1] * TILESIZE
                
#             elif str(hits[0].__class__.__name__) == 'Mob':
#                 self.hitpoints = self.hitpoints - 1
    
#     def update(self):
#         self.get_keys() # calls get_keys()
#         self.x += self.vx * self.game.dt
#         self.y += self.vy * self.game.dt
#         self.rect.x = self.x
#         self.collide_with_walls('x')        # checks if player1 has collided with a wall horizontally
#         self.collide_with_borders('x')        # checks if player1 has collided with a border horizontally
#         self.rect.y = self.y
#         self.collide_with_walls('y')        # checks if player1 has collided with a wall vertically
#         self.collide_with_borders('y')        # checks if player1 has collided with a border vertically
#         self.collide_with_group(self.game.coins, True, self.game)        # checks if player1 has collided with a coin
#         self.collide_with_group(self.game.power_ups, True, self.game)        # checks if player1 has collided with a powerup
#         self.collide_with_group(self.game.teleports, False, self.game)
#         self.collide_with_group(self.game.mobs, False, self.game)

#         if self.hitpoints <= 0:
#             self.kill()
        
#         return self.hitpoints


# ------------------------------ (7) Defining Mob Class ------------------------------
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #### self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.mob_img
        self.rect = self.image.get_rect()

        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel, self.acc = vec(0, 0), vec(0, 0)

        self.rect.center = self.pos
        self.rot, self.chase_distance = 0, 350
        self.speed, self.hitpoints = 400, 100
        self.chasing, self.material = False, False
    
    def sensor(self):
        self.target = ''
        player1_x_dist = self.rect.x - self.game.player1.rect.x
        player1_y_dist = self.rect.y - self.game.player1.rect.y
        self.game.player1.hypotenuse = sqrt(player1_x_dist**2 + player1_y_dist**2)

        # player2_x_dist = self.rect.x - self.game.player2.rect.x
        # player2_y_dist = self.rect.y - self.game.player2.rect.y
        # self.game.player2.hypotenuse = sqrt(player2_x_dist**2 + player2_y_dist**2)
                        
        # if self.game.player1.hitpoints > 0 and self.game.player2.hitpoints <= 0:
        #     if self.game.player1.hypotenuse < self.chase_distance:
        #         self.chasing = True
        #         self.target = self.game.player1
        #         return self.target
        #     else:
        #         self.chasing = False
        #         return self.target
        
        # elif self.game.player1.hitpoints <= 0 and self.game.player2.hitpoints > 0:
        #     if self.game.player2.hypotenuse < self.chase_distance:
        #         self.chasing = True
        #         self.target = self.game.player2
        #         return self.target
        #     else:
        #         self.chasing = False
        #         return self.target
        
        # elif self.game.player1.hypotenuse < self.game.player2.hypotenuse:
        #     if self.game.player1.hypotenuse < self.chase_distance:
        #         self.chasing = True
        #         self.target = self.game.player1
        #         return self.target
        #     else:
        #         self.chasing = False
        #         return self.target
        
        # elif self.game.player2.hypotenuse < self.game.player1.hypotenuse:
        #     if self.game.player2.hypotenuse < self.chase_distance:
        #         self.chasing = True
        #         self.target = self.game.player2
        #         return self.target
        #     else:
        #         self.chasing = False
        #         return self.target
        
        # else:
        #     self.chasing = False
        #     self.target = 'None'
        #     return self.target
        
        if self.game.player1.hypotenuse < self.chase_distance:
            self.chasing = True
            self.target = self.game.player1
            return self.target
        else:
            self.chasing = False
            return self.target
    
    def update(self):
        if self.hitpoints <= 0:
            self.kill()
        self.sensor()
        if self.chasing and self.sensor() != 'None':
            if self.sensor() == self.game.player1:
                self.rot = (self.game.player1.rect.center - self.pos).angle_to(vec(1, 0))
            elif self.sensor() == self.game.player2:
                self.rot = (self.game.player2.rect.center - self.pos).angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            # equation of motion
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # hit_rect used to account for adjusting the square collision when image rotates
            #### self.rect.center = self.hit_rect.center



# ------------------------------ (8) Defining Border Class ------------------------------
class Border(pg.sprite.Sprite):
    # initializes Border
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.borders
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.border_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
        self.speed = 0