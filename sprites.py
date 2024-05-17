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



# ------------------------------ Defining Player1 Class ------------------------------
class Player1(pg.sprite.Sprite):
    # purpose: initializes Player1
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player1_img
        self.rect = self.image.get_rect()
        
        # velocity x and velocity y
        self.vx, self.vy = 0, 0

        # x & y positioning with units of TILESIZE
        self.x, self.y = x * TILESIZE, y * TILESIZE

        # player statistics
        self.speed, self.speed_max = 300, 800               # (speed) speed & (speed_max) speed cap
        self.moneybag = 0                                   # (moneybag) coins collected
        self.coin_multiplier, self.mult_max = 1, 5          # (coin_multiplier) coin multiplier and (mult_max) multiplier cap
        self.hitpoints, self.health_max = 100, 100          # (hitpoints) health & (health_max) health cap
        self.ammo = 20                                      # (ammo) bullets player starts with
        self.round, self.round_max = 20, 50                 # (round) bullets player can have at one time & (round_max) round cap
        self.ghost, self.cooling = False, False             # (ghost) whether player can go through walls

        self.hypotenuse = ''                                # (hypotenuse) distance from mob in a straight line

        # needed for animated sprite
        self.spritesheet = Spritesheet(path.join(img_folder, Player1_sheet))
        self.load_images()
        self.image = self.material_frames[0]
        self.current_frame = 0
        self.last_update = 0

        # corresponding keys for each direction
        self.forward, self.backward = pg.K_w, pg.K_s
        self.right, self.left = pg.K_d, pg.K_a
    
    # purpose: moves player1 based on keys
    def get_keys(self):
        # player begins with velocity of 0
        self.vx, self.vy = 0, 0

        keys = pg.key.get_pressed()
        if keys[self.left]:                 # if a pressed, x decreases (left)
            self.vx = -self.speed
        if keys[self.right]:                # if d pressed, x increases (right)
            self.vx = self.speed
        if keys[self.forward]:              # if w pressed, y decreases (up)
            self.vy = -self.speed
        if keys[self.backward]:             # if s pressed, y increases (down)
            self.vy = self.speed
        if keys[pg.K_SPACE]:                # if space bar pressed
            if self.ammo > 0:               # if player has bullets, player shoots
                self.shoot()
                self.ammo -= 1
    
    # purpose: creates an instance of a bullet
    def shoot(self):
        shot = Bullet(self.game, self.rect.x, self.rect.y)

    # purpose: prevents sprites from moving through walls (unless player has ghost powerup)
    def collide_with_walls(self, dir):        # dir - direction
        if self.ghost == False:               # if player can't move through walls
            collide_with_walls(self, dir, self.game.walls)      # calls collid_with walls from utils
    
    # purpose: prevents sprites from moving through game borders
    def collide_with_borders(self, dir):
        collide_with_walls(self, dir, self.game.borders)

    # purpose: player can collide with powerups, coins, etc.
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        random_power_up = PowerUp.random_effect(self)
        random_power_down = PowerDown.random_effect(self)
        if hits:                                                    # if sprite collides with entity
            if str(hits[0].__class__.__name__) == 'Coin':           # if player hits a coin, add coin multiplier to moneybag
                self.moneybag += self.coin_multiplier

            elif str(hits[0].__class__.__name__) == 'PowerUp':      # if player hits a powerup
                if random_power_up == 'speed':                      # if speed powerup, increase player speed by 100
                    self.speed += 100
                
                elif random_power_up == 'ghost':                    # if ghost powerup, override collide_with_walls()
                    self.ghost = True

                elif random_power_up == 'coin multiplier':          # if coin multiplier, increase coin multiplier by 1
                    self.coin_multiplier += 1

                elif random_power_up == 'regen':                    # if regen powerup, increase player hitpoints by 25
                    self.hitpoints += 25
                
                # self.game.cooldown.cd = 5
                # self.cooling = True
            
            elif str(hits[0].__class__.__name__) == 'PowerDown':    # if player hits a powerdown
                if random_power_down == 'speed':                    # if speed powerdown, decrease player speed by 100
                    self.speed += -100
                
                elif random_power_down == 'ghost':                  # if ghost powerdown, player collides with walls
                    self.ghost = False

                elif random_power_down == 'inflation':              # if inflation powerdown, decrease coin multiplier by 1
                    self.coin_multiplier -= 1

                elif random_power_down == 'degen':                  # if degen powerdown, decrease player hitpoints by 25
                    self.hitpoints = self.hitpoints - 25
                
                if random_power_down == 'invert keys':              # if invert keys powerdown, swap corresponding keys and directions
                    self.forward = pg.K_s
                    self.backward = pg.K_w
                    self.right = pg.K_a
                    self.left = pg.K_d
                
                elif random_power_down == 'tax':                    # if tax powerdown, divide moneybag by 2
                    self.moneybag = self.moneybag // 2
                    
            elif str(hits[0].__class__.__name__) == 'Teleport':             # if player hits a teleport
                local_coordinates = Teleport.random_teleport(self)          # calls random_teleport to get random end portal
                self.x, self.y = local_coordinates[0] * TILESIZE, local_coordinates[1] * TILESIZE       # player's coordinates = end portal's coordinates
            
            elif str(hits[0].__class__.__name__) == 'Mob':          # if player hits a mob, decrease health by 1
                self.hitpoints = self.hitpoints - 1
            
            elif str(hits[0].__class__.__name__) == 'ShopKeeper':   # if player hits shopkeeper, open shop menu
                self.game.shop_open = True
    
    # purpose: loads player frames
    def load_images(self):
        # frames for player without ghost powerup
        self.material_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]
        
        # frames for player with ghost powerup
        self.ghost_frames = [self.spritesheet.get_image(64, 0, 32, 32),
                            self.spritesheet.get_image(96, 0, 32, 32)]
        
    # purpose: replaces frames every 350 ticks to animate player
    def animate(self):
        now = pg.time.get_ticks()                           # current time in ticks
        if self.ghost == False:                             # if player doesn't have ghost potion
            self.current_imgs = self.material_frames
        else:                                               # if player has ghost potion
            self.current_imgs = self.ghost_frames
        
        if now - self.last_update > 350:                    # every 350 ticks, change frame
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.current_imgs)
            bottom = self.rect.bottom
            self.image = self.current_imgs[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    # purpose: updates player1's position and status
    def update(self):
        # needed for animated sprite
        self.animate()

        self.get_keys() # calls get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.collide_with_walls('x')            # checks if player1 has hit a wall horizontally
        self.collide_with_borders('x')          # checks if player1 has hit a border horizontally

        self.rect.y = self.y
        self.collide_with_walls('y')            # checks if player1 has hit a wall vertically
        self.collide_with_borders('y')          # checks if player1 has hit a border vertically

        self.collide_with_group(self.game.coins, True)              # 'checks if player1 has hit a' coin
        self.collide_with_group(self.game.power_ups, True)          # '' powerup
        self.collide_with_group(self.game.power_downs, True)        # '' powerdown
        self.collide_with_group(self.game.teleports, False)         # '' teleport
        self.collide_with_group(self.game.mobs, False)              # '' mob
        self.collide_with_group(self.game.shopkeepers, False)       # '' shopkeeper

        # if self.game.cooldown.cd < 1:
        #     self.cooling = False
        
        # if self.cooling == False:
        #     self.collide_with_group(self.game.power_ups, True)
        # elif self.cooling == True:
        #     self.collide_with_group(self.game.power_ups, False)

        if self.hitpoints <= 0:         # if player's health is 0, delete instance of player sprite
            self.kill()



# ------------------------------ Defining Wall Class ------------------------------
class Wall(pg.sprite.Sprite):
    # purpose: initializes Wall
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
        # self.speed = 0



# ------------------------------ Defining Border Class ------------------------------
class Border(pg.sprite.Sprite):
    # purpose: initializes Border
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.borders
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.border_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
        # self.speed = 0



# ------------------------------ Defining Bullet Class ------------------------------
class Bullet(pg.sprite.Sprite):
    # purpose: initializes Bullet
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))       # bullet size is smaller than tile like actual bullets
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x, y
        self.speed = 10
    
    # purpose: erases instance of bullet if it collides with a mob, wall, or border
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == 'Mob':
                self.kill()
            elif str(hits[0].__class__.__name__) == 'Wall':
                self.kill()
            elif str(hits[0].__class__.__name__) == 'Border':
                self.kill()

    # purpose: updates movement of bullet instance and checks for collisions
    def update(self):
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.walls, False)
        self.collide_with_group(self.game.borders, False)
        self.rect.x -= self.speed



# ------------------------------ Defining Coin Class ------------------------------
class Coin(pg.sprite.Sprite):
    # purpose: initializes Coin
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE



# ------------------------------ Defining PowerUp Class ------------------------------
class PowerUp(pg.sprite.Sprite):
    # purpose: initializes PowerUp
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.powerup_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    # purpose: generates a random powerup effect
    def random_effect(self):
        effects = ['speed', 'ghost', 'coin multiplier', 'regen']            # list of possible powerup effects
        if self.game.player1.speed == self.game.player1.speed_max:                                  # if player speed is maxed out,
            effects.remove('speed')         # remove 'speed' from effects
        elif self.game.player1.speed < self.game.player1.speed_max and 'speed' not in effects:      # if player speed isn't maxed and 'speed' isn't in effects,
            effects.append('speed')         # add 'speed' to effects

        if self.game.player1.ghost == True:                                     # if player has a ghost powerup,
            effects.remove('ghost')         # remove 'ghost' from effects
        elif self.game.player1.ghost == False and 'ghost' not in effects:       # if player doesn't have a ghost powerup and 'ghost' isn't in effects,
            effects.append('ghost')         # add 'ghost' to powerups
        
        if self.game.player1.coin_multiplier == self.game.player1.mult_max:     # if coin multiplier is maxed out,
            effects.remove('coin multiplier')       # remove coin multiplier from effects
        elif self.game.player1.coin_multiplier < self.game.player1.mult_max and 'coin multiplier' not in effects:   # if coin multiplier isn't maxed out and 'coin multiplier' is not in effects,
            effects.append('coin multiplier')       # add coin multiplier to effects

        if self.game.player1.hitpoints == self.game.player1.health_max:         # if health is maxed out,
            effects.remove('regen')         # remove 'regen' from effects
        elif self.game.player1.hitpoints < self.game.player1.health_max and 'regen' not in effects:        # if health isn't maxed out and 'regen' isn't in effects,
            effects.append('regen')         # add 'regen' to effects

        local_effect = effects[random.randrange(0, len(effects) - 1)]           # random effect assigned to local_effect
        return local_effect



# ------------------------------ Defining PowerDown Class ------------------------------
class PowerDown(pg.sprite.Sprite):
    # purpose: initializes PowerUp
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_downs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.powerdown_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    # purpose: generates a random powerdown effect
    def random_effect(self):
        effects = ['speed', 'ghost', 'inflation', 'degen', 'invert keys', 'tax']    # list of possible powerdown effects

        if self.game.player1.speed == 100:                              # if player speed is 100,
            effects.remove('speed')     # remove 'speed' from effects
        elif self.game.player1.speed > 100 and 'speed' not in effects:  # if player speed is greater than 100 and 'speed' isn't in effects,
            effects.append('speed')     # add 'speed' to effects
        
        if self.game.player1.ghost == False:                                # if player doesn't have a ghost powerdown,
            effects.remove('ghost')     # remove 'ghost' from effects
        elif self.game.player1.ghost == True and 'ghost' not in effects:    # if player has a ghost powerdown and 'ghost' isn't in effects
            effects.append('ghost')     # add 'ghost' to effects
        
        if self.game.player1.coin_multiplier == 1:                                  # if coin multiplier is 1,
            effects.remove('inflation')         # remove 'inflation' from effects
        elif self.game.player1.coin_multiplier > 1 and 'inflation' not in effects:  # if coin multiplier is greater than 1 and 'inflation' isn't in effects,
            effects.append('inflation')         # add 'inflation' to effects

        if self.game.player1.hitpoints <= 25:                               # if player health is 25,
            effects.remove('degen')             # remove 'degen' from effects
        elif self.game.player1.hitpoints > 25 and 'degen' not in effects:   # if player health is greater than 25 and 'degen' isn't in effects,
            effects.append('degen')             # add 'degen' to effects

        local_effect = effects[random.randrange(0, len(effects))]       # random effect assigned to local_effect
        return local_effect



# ------------------------------ Defining Teleport Class ------------------------------
class Teleport(pg.sprite.Sprite):
    # purpose: initializes Teleport
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.teleports
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.portal_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    # purpose: finds a random end portal
    def random_teleport(self):
        local_teleport = EXIT_PORTS[random.randrange(0, len(EXIT_PORTS))]
        return local_teleport



# ------------------------------ Defining Mob Class ------------------------------
class Mob(pg.sprite.Sprite):
    # purpose: initializes Mob (copied from Mr. Cozort's code)
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mob_img
        self.rect = self.image.get_rect()

        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel, self.acc = vec(0, 0), vec(0, 0)

        self.rect.center = self.pos
        self.rot, self.chase_distance = 0, 350
        self.speed = 400
        self.chasing = False
    
    def sensor(self):
        self.target = ''        # the player the mob chases
        player1_x_dist = self.rect.x - self.game.player1.rect.x         # horizontal distance betw. player and mob
        player1_y_dist = self.rect.y - self.game.player1.rect.y         # vertical distance betw. player and mob
        self.game.player1.hypotenuse = sqrt(player1_x_dist**2 + player1_y_dist**2)  # Pythagorean Theorem to find straight line distance betw. player and mob

        if self.game.player1.hitpoints > 0:                             # if player is alive,
            if self.game.player1.hypotenuse < self.chase_distance:      # if player is in chase distance, chase player
                self.chasing = True
                self.target = self.game.player1
                return self.target
        else:                                                           # if player died, stop moving
            self.chasing = False
            self.target = 'None'
            return self.target
    
    # purpose: checks if a bullet has hit a mob
    def collide_with_bullet(self, kill):
        hits = pg.sprite.spritecollide(self, self.game.bullets, kill)
        if hits:            # if mob hit a bullet, erase instance of mob sprite
            self.kill()

    # purpose: updates mob's position and status
    def update(self):
        self.sensor()

        if self.chasing and self.sensor() == self.game.player1:         # if mob is chasing player,
            # angle image of mob instance
            self.rot = (self.game.player1.rect.center - self.pos).angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)

            # update movement of mob instance
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)     # acceleration
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt                 # current velocity of mob instance

            # equation of motion
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        
        self.collide_with_bullet(True)      # calls collide_with_bullet; True - kills mob if bullet hits it



# ------------------------------ Defining ShopKeeper Class ------------------------------
class ShopKeeper(pg.sprite.Sprite):
    # purpose: initializes ShopKeeper
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.shopkeepers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
        # self.speed = 0