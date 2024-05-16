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
        self.image = game.player1_img        # defines image
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x, self.y = x * TILESIZE, y * TILESIZE        # x & y positioning multiplied by TILESIZE

        self.speed, self.speed_max = 300, 800        # player1 speed
        self.moneybag = 0        # coins collected
        self.coin_multiplier, self.mult_max = 1, 5
        self.hitpoints, self.health_max = 100, 100
        self.ammo = 20
        self.round, self.round_max = 20, 50

        self.ghost, self.cooling = False, False
        self.hypotenuse = ''

        # needed for animated sprite
        self.spritesheet = Spritesheet(path.join(img_folder, Player1_sheet))
        self.load_images()
        self.image = self.material_frames[0]
        self.current_frame = 0
        self.last_update = 0

        self.forward, self.backward = pg.K_w, pg.K_s
        self.right, self.left = pg.K_d, pg.K_a
    
    # get_keys() purpose - moves player1 based on keys
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()        # calls get_pressed() in keys (variable)
        if keys[self.left]:        # if a-key pressed
            self.vx = -self.speed        # x decreases = move left
        if keys[self.right]:        # if d-key pressed
            self.vx = self.speed        # x increases = move right
        if keys[self.forward]:        # if w-key pressed
            self.vy = -self.speed        # y decreases = move up (y starts at row 0 from top)
        if keys[self.backward]:        # if s-key pressed
            self.vy = self.speed        # y increases = move down
        if keys[pg.K_SPACE]:
            if self.ammo > 0:
                self.shoot()
                self.ammo -= 1
    
    def shoot(self):
        shot = Bullet(self.game, self.rect.x, self.rect.y)

    # collide_with_walls() purpose - prevents sprites from moving through walls
    def collide_with_walls(self, dir):        # dir - direction
        if self.ghost == False:
            collide_with_walls(self, dir, self.game.walls)
    
    def collide_with_borders(self, dir):
        collide_with_walls(self, dir, self.game.borders)

    # collide_with_group() purpose - calculates data such as coins/powerups
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        random_power_up = PowerUp.random_effect(self)
        random_power_down = PowerDown.random_effect(self)
        if hits:        # if sprite collides with entity
            if str(hits[0].__class__.__name__) == 'Coin':        # if entity == Coin
                self.moneybag += self.coin_multiplier        # add 1 to moneybag

            elif str(hits[0].__class__.__name__) == 'PowerUp':        # if entity == PowerUp
                if random_power_up == 'speed':
                    self.speed += 100        # increase speed by 200
                
                elif random_power_up == 'ghost':
                    self.ghost = True        # overrides collide_with_walls()

                elif random_power_up == 'coin multiplier':    
                    self.coin_multiplier += 1

                elif random_power_up == 'regen' and self.hitpoints +25 <= self.health_max:
                    self.hitpoints += 25
                
                self.game.cooldown.cd = 5
                self.cooling = True
            
            elif str(hits[0].__class__.__name__) == 'PowerDown':        # if entity == PowerUp
                if random_power_down == 'speed':
                    self.speed = self.speed / 2
                
                elif random_power_down == 'ghost':
                    self.ghost = False

                elif random_power_down == 'inflation':    
                    self.coin_multiplier -= 1

                elif random_power_down == 'degen':
                    self.hitpoints = self.hitpoints - 25
                
                if random_power_down == 'invert keys':
                    self.forward = pg.K_s
                    self.backward = pg.K_w
                    self.right = pg.K_a
                    self.left = pg.K_d
                
                elif random_power_down == 'tax':
                    self.moneybag = self.moneybag // 2
                    
            elif str(hits[0].__class__.__name__) == 'Teleport':       # if entity == Teleport
                local_coordinates = Teleport.random_teleport(self)        # gets the coordinates of the end portal
                # makes player1's coordinates = the end portal coordinates
                self.x, self.y = local_coordinates[0] * TILESIZE, local_coordinates[1] * TILESIZE
                
            elif str(hits[0].__class__.__name__) == 'Mob':
                self.hitpoints = self.hitpoints - 1
            
            elif str(hits[0].__class__.__name__) == 'ShopKeeper':
                self.game.shop_open = True
    
    def load_images(self):
        self.material_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]
        
        self.ghost_frames = [self.spritesheet.get_image(64, 0, 32, 32),
                            self.spritesheet.get_image(96, 0, 32, 32)]
        

    def animate(self):
        now = pg. time.get_ticks()
        if self.ghost == False:
            self.current_imgs = self.material_frames
        else:
            self.current_imgs = self.ghost_frames
        
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.current_imgs)
            bottom = self.rect.bottom
            self.image = self.current_imgs[self.current_frame]
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

        self.collide_with_group(self.game.coins, True)        # checks if player1 has collided with a coin
        self.collide_with_group(self.game.power_ups, True)        # checks if player1 has collided with a powerup
        self.collide_with_group(self.game.power_downs, True)
        self.collide_with_group(self.game.teleports, False)
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.shopkeepers, False)

        if self.game.cooldown.cd < 1:
            self.cooling = False
        
        if self.cooling == False:
            self.collide_with_group(self.game.power_ups, True)
        elif self.cooling == True:
            self.collide_with_group(self.game.power_ups, False)

        if self.hitpoints <= 0:
            self.kill()



# ------------------------------ (2) Defining Wall Class ------------------------------
class Wall(pg.sprite.Sprite):
    # initializes Wall
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
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
        self.image = game.powerup_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    def random_effect(self):
        effects = ['speed', 'ghost', 'coin multiplier', 'regen']
        if self.game.player1.speed == self.game.player1.speed_max:
            effects.remove('speed')
        elif self.game.player1.speed < self.game.player1.speed_max and 'speed' not in effects:
            effects.append('speed')

        if self.game.player1.ghost == True:
            effects.remove('ghost')
        elif self.game.player1.ghost == False and 'ghost' not in effects:
            effects.append('ghost')
        
        if self.game.player1.coin_multiplier == self.game.player1.mult_max:
            effects.remove('coin multiplier')
        elif self.game.player1.coin_multiplier < self.game.player1.mult_max and 'coin multiplier' not in effects:
            effects.append('coin multiplier')

        if self.game.player1.hitpoints == self.game.player1.health_max:
            effects.remove('regen')
        elif self.game.player1.hitpoints < self.game.player1.health_max:
            effects.append('regen')

        local_effect = effects[random.randrange(0, len(effects) - 1)]
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
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    def random_teleport(self):
        local_teleport = EXIT_PORTS[random.randrange(0, len(EXIT_PORTS))]
        return local_teleport



# ------------------------------ (6) Defining Mob Class ------------------------------
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
        self.speed = 400
        self.chasing = False
    
    def sensor(self):
        self.target = ''
        player1_x_dist = self.rect.x - self.game.player1.rect.x
        player1_y_dist = self.rect.y - self.game.player1.rect.y
        self.game.player1.hypotenuse = sqrt(player1_x_dist**2 + player1_y_dist**2)

        if self.game.player1.hitpoints > 0:
            if self.game.player1.hypotenuse < self.chase_distance:
                self.chasing = True
                self.target = self.game.player1
                return self.target
        else:
            self.chasing = False
            self.target = 'None'
            return self.target
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == 'Bullet':
                self.kill()

    def update(self):
        self.sensor()

        if self.chasing and self.sensor() == self.game.player1:
            self.rot = (self.game.player1.rect.center - self.pos).angle_to(vec(1, 0))
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
        
        self.collide_with_group(self.game.bullets, True)



# ------------------------------ (7) Defining Border Class ------------------------------
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



# ------------------------------ (8) Defining ShopKeeper Class ------------------------------
class ShopKeeper(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.shopkeepers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
        self.speed = 0



# ------------------------------ (9) Defining Bullet Class ------------------------------
class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x, y
        self.speed = 10
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == 'Mob':
                self.kill()
            elif str(hits[0].__class__.__name__) == 'Wall':
                self.kill()
            elif str(hits[0].__class__.__name__) == 'Border':
                self.kill()

    def update(self):
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.walls, False)
        self.collide_with_group(self.game.borders, False)
        self.rect.x -= self.speed



# ------------------------------ (4) Defining PowerUp Class ------------------------------
class PowerDown(pg.sprite.Sprite):
    # initializes PowerUp
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_downs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.powerdown_img
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
    
    def random_effect(self):
        effects = ['speed', 'ghost', 'inflation', 'degen', 'invert keys', 'tax']

        if self.game.player1.speed == 100:
            effects.remove('speed')
        elif self.game.player1.speed > 100 and 'speed' not in effects:
            effects.append('speed')
        
        if self.game.player1.ghost == False:
            effects.remove('ghost')
        elif self.game.player1.ghost == True and 'ghost' not in effects:
            effects.append('ghost')
        
        if self.game.player1.coin_multiplier == 1:
            effects.remove('inflation')
        elif self.game.player1.coin_multiplier > 1 and 'inflation' not in effects:
            effects.append('inflation')

        if self.game.player1.hitpoints <= 25:
            effects.remove('degen')
        elif self.game.player1.hitpoints > 25 and 'degen' not in effects:
            effects.append('degen')

        local_effect = effects[random.randrange(0, len(effects))]
        return local_effect